#!/usr/bin/env python3
"""
tracker.json으로 독립 실행형 지원 파이프라인 타임라인(timeline.html)을 만든다.

사용법:  python3 build_timeline.py <user_dir>/CareerLoop
- 주어진 디렉터리에서 tracker.json(전체 단계 이력)을 읽어 지원 건별 간결한
  타임라인 모델을 만들고, 같은 디렉터리에 쓰는 독립 실행형 HTML 파일에 내장한다
  (라이브러리, CDN, 서버 모두 필요 없음).
- 렌더러는 순수 JS + 인라인 SVG라서 즉시 로드되고 오프라인에서도 동작한다.
- pipeline-status 스킬이 호출하며, pipeline-status.html에 iframe으로 내장된다.
"""
import json, os, sys, datetime

BASE = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
TRACKER = os.path.join(BASE, "tracker.json")
OUT = os.path.join(BASE, "timeline.html")
TODAY = datetime.date.today().isoformat()

# ---- stage taxonomy -------------------------------------------------------
APPLY_STAGES = {"applied", "re-applied"}
TERMINAL_REJECT = {"rejected"}
TERMINAL_OUT = {"withdrawn", "declined_by_candidate"}

# 각 단계는 (글리프 키, 주체)로 매핑된다. "mine" = 사용자 본인의 액션으로
# 타임라인 선 위에 그리고, "theirs" = 고용주/리크루터 쪽으로 선 바로 위에 그려서
# 둘이 시각적으로 섞이지 않게 한다.
def glyph_for(stage):
    if stage in APPLY_STAGES: return ("applied", "mine")
    if stage == "considering": return ("discovered", "mine")
    if stage == "recruiter": return ("response", "theirs")
    if stage == "phone_screen": return ("screen", "theirs")
    if stage in ("interview", "onsite", "final", "panel"): return ("screen", "theirs")
    if stage == "offer": return ("offer", "theirs")
    if stage == "rejected": return ("rejected", "theirs")
    if stage == "ghosted": return ("ghosted", "theirs")
    if stage in TERMINAL_OUT: return ("closed", "mine")
    return ("update", "mine")

def d(s):
    return s if (s and isinstance(s, str) and len(s) >= 10) else None

def load_detail(a):
    """tracker_v2_split 스키마: stage_history와 contacts는 tracker.json의 지원
    레코드에 인라인으로 두지 않고 applications/<id>.json(detail_file)과
    contacts/<slug>.json(contacts_file)에 있다."""
    stage_history = a.get("stage_history") or []
    contacts = a.get("contacts") or []
    detail_file = a.get("detail_file")
    if detail_file:
        path = os.path.join(BASE, detail_file)
        if os.path.exists(path):
            try:
                detail = json.load(open(path))
                stage_history = detail.get("stage_history") or stage_history
            except Exception as e:
                print(f"WARN: detail_file을 불러오지 못했습니다 {detail_file}: {e}")
    contacts_file = a.get("contacts_file")
    if contacts_file:
        path = os.path.join(BASE, contacts_file)
        if os.path.exists(path):
            try:
                cdata = json.load(open(path))
                contacts = cdata.get("contacts") or contacts
            except Exception as e:
                print(f"WARN: contacts_file을 불러오지 못했습니다 {contacts_file}: {e}")
    return stage_history, contacts

def main():
    tracker = json.load(open(TRACKER))
    apps = tracker["applications"]
    rows = []

    for a in apps:
        raw_sh, raw_contacts = load_detail(a)
        sh = [s for s in raw_sh if d(s.get("date"))]
        sh.sort(key=lambda s: s["date"])
        cand_dates = [s["date"] for s in sh]
        for k in ("date_added", "date_applied", "applied_date"):
            if d(a.get(k)): cand_dates.append(a[k])
        if not cand_dates:
            continue  # 시간 축에 놓을 것이 없음

        # ---- 연락처 상호작용(아웃리치 / 응답 / 미팅) --------------------
        touches = []
        for c in (raw_contacts or []):
            who = c.get("name") or "연락처"
            for it in (c.get("interactions") or []):
                if not d(it.get("date")):
                    continue
                t = (it.get("type") or "").lower()
                if any(k in t for k in ("meet", "zoom")) or t == "phone_screen":
                    kind = "meeting"
                elif "inbound" in t or t.endswith("_reply"):
                    kind = "inbound"
                else:
                    kind = "outbound"
                touches.append({"date": it["date"], "dir": kind, "type": t or "contact",
                                "who": who, "note": (it.get("notes") or "")[:400]})
        touches.sort(key=lambda x: x["date"])
        if touches:
            cand_dates += [x["date"] for x in touches]

        start = min(cand_dates)
        applied = d(a.get("date_applied")) or d(a.get("applied_date"))
        status = (a.get("status") or "").lower()
        outcome = (a.get("outcome") or "").lower()

        # 단계 이력으로 이벤트 마커를 만든다
        events = []
        for s in sh:
            st = (s.get("stage") or "").lower()
            g, who = glyph_for(st)
            events.append({"date": s["date"], "stage": st or "update",
                           "g": g, "who": who, "note": (s.get("notes") or "")[:400]})
        # 첫 이벤트가 시작점에 없으면 가장 앞에 발견 링을 둔다
        if not events or events[0]["date"] > start:
            events.insert(0, {"date": start, "stage": "discovered", "g": "discovered", "who": "mine", "note": ""})
        # 지원 다이아몬드가 반드시 있게 한다
        if applied and not any(e["g"] == "applied" for e in events):
            events.append({"date": applied, "stage": "applied", "g": "applied", "who": "mine", "note": ""})
        events.sort(key=lambda e: e["date"])

        last_event = max(e["date"] for e in events)

        ghosted = status == "ghosted"
        ghost_date = None
        if ghosted:
            gd = [e["date"] for e in events if e["g"] == "ghosted"]
            # 명시적 "ghosted" 단계가 있으면 그 날짜를 쓰고, 없으면 무응답이
            # 현재까지 이어지므로 선이 오늘까지 점점 흐려지게 한다.
            ghost_date = gd[0] if gd else (TODAY if TODAY > last_event else last_event)

        active = (not ghosted
                  and status not in TERMINAL_REJECT
                  and status not in TERMINAL_OUT
                  and outcome in ("pending", "", None))

        if ghosted:
            end = ghost_date
        elif active:
            end = TODAY if TODAY > last_event else last_event
        else:
            end = last_event

        rows.append({
            "co": a.get("company") or "—",
            "role": a.get("role") or "",
            "status": status or "unknown",
            "outcome": outcome,
            "priority": (a.get("priority") or "").lower(),
            "start": start,
            "applied": applied,
            "end": end,
            "ghost": ghost_date,        # 무응답이 아니면 null
            "active": active,
            "events": events,
            "touches": touches,
        })

    # 가장 최근 제출 건이 위로(없으면 시작일 기준), 동률이면 회사 이름 순으로 안정 정렬
    rows.sort(key=lambda r: r["co"])
    rows.sort(key=lambda r: (r.get("applied") or r["start"]), reverse=True)

    model = {
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "today": TODAY,
        "rows": rows,
    }

    html = TEMPLATE.replace("__DATA__", json.dumps(model, separators=(",", ":")))
    with open(OUT, "w") as f:
        f.write(html)
    print(f"{OUT} 작성 완료  (지원 {len(rows)}건, 생성일 {TODAY})")

TEMPLATE = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>지원 파이프라인 — 타임라인</title>
<style id="tl-style">
html,body{height:100%;margin:0;padding:0}
#tl-root{height:100%;display:flex;flex-direction:column;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#1a1a1a;background:#fff;font-size:13px}
#tl-root *{box-sizing:border-box}
#tl-root h1{flex:none;font-size:16px;font-weight:600;margin:0 0 10px}
#tl-root .tl-sub{font-size:11px;color:#9ca3af;font-weight:400}
#tl-root .tl-legend{flex:none;display:flex;flex-wrap:wrap;gap:14px;align-items:center;font-size:11px;color:#4b5563}
#tl-root .tl-legend .li{display:inline-flex;align-items:center;gap:5px}
#tl-root .tl-legend .tl-legend-head{font-weight:600;color:#374151;margin-left:4px}
#tl-root .tl-legend .tl-legend-head:first-child{margin-left:0}
#tl-root .tl-legend svg{overflow:visible}
#tl-root .tl-legend{margin:10px 0 0;padding-top:10px;border-top:1px solid #f0f0f0}
#tl-root .tl-controls{flex:none;display:flex;align-items:center;gap:8px;margin:0 0 12px;font-size:11px;color:#4b5563}
#tl-root .tl-controls select{font-size:11px;padding:3px 8px;border:0.5px solid #d1d5db;border-radius:6px;background:#fff;color:#1a1a1a;cursor:pointer}
#tl-root .tl-controls .tl-count{color:#9ca3af}
#tl-root .tl-axis-head{flex:none;width:100%;overflow:hidden}
#tl-root .tl-wrap{flex:1 1 auto;min-height:0;position:relative;width:100%;overflow-y:auto;overflow-x:hidden}
#tl-root svg.tl-chart{display:block;width:100%;height:auto;font-family:inherit}
#tl-root .rowhit{cursor:default}
#tl-root .rowhit:hover .rowbg{fill:#f6f7f9}
#tl-root .colab{font-size:11px;fill:#374151}
#tl-root .mlab{font-size:10px;fill:#9ca3af}
#tl-root .axis{stroke:#eceef1;stroke-width:1}
#tl-root .todayln{stroke:#10b981;stroke-width:1;stroke-dasharray:2 3}
#tl-root .tl-tip{position:fixed;pointer-events:none;z-index:9999;background:#111827;color:#f9fafb;padding:8px 10px;border-radius:7px;font-size:11px;line-height:1.45;width:280px;box-shadow:0 6px 20px rgba(0,0,0,.25);opacity:0;transition:opacity .08s;white-space:normal}
#tl-root .tl-tip b{color:#fff}
#tl-root .tl-tip .ev{color:#cbd5e1}
</style>
</head>
<body>
<div id="tl-root">
  <h1>지원 파이프라인 — 타임라인 <span class="tl-sub" id="tl-stamp"></span></h1>
  <div class="tl-controls">
    <label for="tl-filter">표시</label>
    <select id="tl-filter">
      <option value="active" selected>진행 중</option>
      <option value="all">전체</option>
      <option value="rejected">불합격</option>
      <option value="ghosted">무응답</option>
      <option value="closed">철회 / 거절</option>
    </select>
    <span class="tl-count" id="tl-count"></span>
  </div>
  <div class="tl-axis-head" id="tl-axis"></div>
  <div class="tl-wrap" id="tl-wrap"></div>
  <div class="tl-legend" id="tl-legend"></div>
  <div class="tl-tip" id="tl-tip"></div>
</div>

<script id="tl-script">
const TL = __DATA__;

const C = {
  active:'#2563eb', applied:'#2563eb', screen:'#059669', interview:'#059669',
  offer:'#15803d', rejected:'#dc2626', ghosted:'#d97706', closed:'#6b7280', unknown:'#6b7280',
  contact:'#7c3aed'
};
function lineColor(r){
  if(r.ghost) return C.ghosted;
  if(r.status==='rejected') return C.rejected;
  if(r.status==='withdrawn'||r.status==='declined_by_candidate') return C.closed;
  if(r.status==='phone_screen') return C.screen;
  return C.active;
}
const parse = s => new Date(s+'T00:00:00');
const DAY = 86400000;

// ---- 마커 모양(작게, 0,0 중심) ------------------------------------------
function marker(g, color){
  switch(g){
    case 'discovered': return `<circle r="3.4" fill="#fff" stroke="${color}" stroke-width="1.4"/>`;
    case 'applied':    return `<path d="M0,-4.6 L4.6,0 L0,4.6 L-4.6,0 Z" fill="${color}"/>`;
    case 'outreach':   return `<path d="M-3.4,-3.2 L3.6,0 L-3.4,3.2 Z" fill="${color}"/>`;
    case 'closed':     return `<rect x="-3.1" y="-3.1" width="6.2" height="6.2" rx="1" fill="#fff" stroke="${color}" stroke-width="1.4"/>`;
    case 'screen':
    case 'interview':  return `<circle r="3.6" fill="${color}"/>`;
    case 'offer':      return `<path d="M0,-5 L1.4,-1.6 L5,-1.6 L2.1,0.6 L3.2,4.2 L0,2 L-3.2,4.2 L-2.1,0.6 L-5,-1.6 L-1.4,-1.6 Z" fill="${color}"/>`;
    case 'rejected':   return `<path d="M-3.2,-3.2 L3.2,3.2 M3.2,-3.2 L-3.2,3.2" stroke="${color}" stroke-width="1.6" stroke-linecap="round"/>`;
    case 'ghosted':    return `<g fill="${color}"><circle cx="-3" cy="0" r="1"/><circle cx="0" cy="0" r="1"/><circle cx="3" cy="0" r="1"/></g>`;
    case 'response':   return `<circle r="2.7" fill="${color}"/>`;
    case 'meeting':    return `<rect x="-2.6" y="-2.6" width="5.2" height="5.2" rx="1" fill="${color}"/>`;
    default:           return `<circle r="2" fill="${color}"/>`;
  }
}

// 글리프별 색상. "mine" 글리프(discovered / applied / closed / update)는
// 행 자체의 상태 색상으로 대체해, 행 전체 상태와 시각적으로 연결되게 한다.
function eventColor(g, rowColor){
  if(g==='rejected') return C.rejected;
  if(g==='ghosted') return C.ghosted;
  if(g==='screen'||g==='interview') return C.screen;
  if(g==='offer') return C.offer;
  if(g==='response'||g==='meeting'||g==='outreach') return C.contact;
  return rowColor;
}

const LEGEND_MINE = [
  ['discovered','파이프라인에 추가'],
  ['applied','지원서 제출'],
  ['outreach','내가 연락함'],
  ['closed','내가 철회 / 거절'],
  ['update','메모 추가'],
];
const LEGEND_THEIRS = [
  ['response','리크루터 / 담당자가 연락함'],
  ['screen','전화 스크리닝 / 면접'],
  ['offer','오퍼'],
  ['rejected','불합격'],
  ['ghosted','응답 없음(무응답)'],
  ['meeting','미팅 진행'],
];

const LABEL_W = 168, PAD_R = 20, ROW_H = 20, AXIS_H = 26, BOT = 14;

let VIEW = [];              // 현재 그려진 행(필터 적용 후), data-i로 인덱싱
let FILTER = 'active';

function matchFilter(r,f){
  if(f==='all') return true;
  if(f==='active') return !!r.active;
  if(f==='ghosted') return !!r.ghost;
  if(f==='rejected') return r.status==='rejected';
  if(f==='closed') return r.status==='withdrawn' || r.status==='declined_by_candidate';
  return true;
}

function render(){
  const wrap = document.getElementById('tl-wrap');
  const head = document.getElementById('tl-axis');
  const W = Math.max(640, wrap.clientWidth || 900);
  const plotX0 = LABEL_W, plotX1 = W - PAD_R, plotW = plotX1 - plotX0;
  const rows = TL.rows.filter(r=>matchFilter(r,FILTER));
  VIEW = rows;
  const cnt = document.getElementById('tl-count');
  if(cnt) cnt.textContent = `지원 ${TL.rows.length}건 중 ${rows.length}건`;
  if(!rows.length){
    head.innerHTML = '';
    wrap.innerHTML = '<svg class="tl-chart" viewBox="0 0 640 40"><text x="12" y="24" class="mlab">이 필터에 맞는 지원이 없습니다.</text></svg>';
    return;
  }

  // 시간 범위(단계 이벤트, 구간 끝점, 연락처 접점 포함)
  let lo = Infinity, hi = -Infinity;
  rows.forEach(r=>{ r.events.forEach(e=>{const t=parse(e.date).getTime(); if(t<lo)lo=t; if(t>hi)hi=t;});
                    (r.touches||[]).forEach(e=>{const t=parse(e.date).getTime(); if(t<lo)lo=t; if(t>hi)hi=t;});
                    const s=parse(r.start).getTime(), en=parse(r.end).getTime();
                    if(s<lo)lo=s; if(en>hi)hi=en; });
  const todayT = parse(TL.today).getTime(); if(todayT>hi)hi=todayT;
  lo -= 5*DAY; hi += 6*DAY;
  const x = t => plotX0 + (t-lo)/(hi-lo)*plotW;

  // 월 눈금
  let ticks=[]; const dLo=new Date(lo);
  let m=new Date(dLo.getFullYear(), dLo.getMonth(), 1);
  if(m.getTime()<lo) m=new Date(m.getFullYear(), m.getMonth()+1, 1);
  const MON=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  while(m.getTime()<=hi){ ticks.push(new Date(m)); m=new Date(m.getFullYear(), m.getMonth()+1, 1); }
  const xt = x(todayT);
  const bodyH = rows.length*ROW_H + 6;

  // ---- 고정 축 헤더(스크롤되지 않음) --------------------------------------
  let hs = `<svg class="tl-chart" viewBox="0 0 ${W} ${AXIS_H}" style="width:${W}px;height:${AXIS_H}px" preserveAspectRatio="xMinYMin meet">`;
  ticks.forEach(t=>{ const xp=x(t.getTime());
    hs += `<text class="mlab" x="${xp.toFixed(1)}" y="${AXIS_H-9}" text-anchor="middle">${MON[t.getMonth()]}${t.getMonth()===0?" '"+String(t.getFullYear()).slice(2):''}</text>`;
  });
  hs += `<text class="mlab" x="${xt.toFixed(1)}" y="10" text-anchor="middle" fill="#10b981">오늘</text>`;
  hs += `<line class="axis" x1="0" y1="${AXIS_H-1}" x2="${W}" y2="${AXIS_H-1}"/></svg>`;
  head.innerHTML = hs;

  // ---- 스크롤되는 본문 ----------------------------------------------------
  let s = `<svg class="tl-chart" viewBox="0 0 ${W} ${bodyH}" style="width:${W}px;height:${bodyH}px" preserveAspectRatio="xMinYMin meet" role="img">`;
  let defs = '<defs>';
  ticks.forEach(t=>{ const xp=x(t.getTime());
    s += `<line class="axis" x1="${xp.toFixed(1)}" y1="0" x2="${xp.toFixed(1)}" y2="${bodyH}"/>`;
  });
  s += `<line class="todayln" x1="${xt.toFixed(1)}" y1="0" x2="${xt.toFixed(1)}" y2="${bodyH}"/>`;

  rows.forEach((r,i)=>{
    const yc = i*ROW_H + ROW_H/2;
    const col = lineColor(r);
    const xs = x(parse(r.start).getTime());
    const xe = x(parse(r.end).getTime());

    // 행 히트 영역 + 호버 배경
    s += `<g class="rowhit" data-i="${i}">`;
    s += `<rect class="rowbg" x="0" y="${i*ROW_H}" width="${W}" height="${ROW_H}" fill="transparent"/>`;

    // 레이블(회사) — 길면 잘라서 표시
    const co = r.co.length>24 ? r.co.slice(0,23)+'…' : r.co;
    s += `<text class="colab" x="10" y="${yc+3}">${esc(co)}</text>`;

    // 선
    if(r.ghost){
      const xa = x(parse(r.applied||r.start).getTime());
      const gid = 'g'+i;
      const af = Math.max(0, Math.min(1, (xa-xs)/Math.max(1,(xe-xs))));
      defs += `<linearGradient id="${gid}" gradientUnits="userSpaceOnUse" x1="${xs}" y1="0" x2="${xe}" y2="0">`
            + `<stop offset="0" stop-color="${col}" stop-opacity="0.9"/>`
            + `<stop offset="${af.toFixed(3)}" stop-color="${col}" stop-opacity="0.9"/>`
            + `<stop offset="1" stop-color="${col}" stop-opacity="0"/></linearGradient>`;
      s += `<line x1="${xs.toFixed(1)}" y1="${yc}" x2="${xe.toFixed(1)}" y2="${yc}" stroke="url(#${gid})" stroke-width="2.4" stroke-linecap="round"/>`;
    } else {
      const dash = r.active ? '' : '';
      s += `<line x1="${xs.toFixed(1)}" y1="${yc}" x2="${xe.toFixed(1)}" y2="${yc}" stroke="${col}" stroke-width="2.4" stroke-opacity="0.9" stroke-linecap="round"${dash}/>`;
      if(r.active) s += `<circle cx="${xe.toFixed(1)}" cy="${yc}" r="3.2" fill="#fff" stroke="${col}" stroke-width="1.5"/>`;
    }

    // 마커 — 내가 한 일은 선 위에 놓고, 상대가 한 일(리크루터 연락, 스크리닝,
    // 오퍼, 불합격, 무응답)은 선 바로 위에 띄우고 짧은 눈금으로 선에 연결한다.
    r.events.forEach(e=>{
      const mc = eventColor(e.g, col);
      const ex = x(parse(e.date).getTime());
      const theirs = e.who === 'theirs';
      const ey = theirs ? (yc-7) : yc;
      if(theirs) s += `<line x1="${ex.toFixed(1)}" y1="${yc}" x2="${ex.toFixed(1)}" y2="${ey.toFixed(1)}" stroke="${mc}" stroke-width="0.75" stroke-opacity="0.4"/>`;
      s += `<g transform="translate(${ex.toFixed(1)},${ey.toFixed(1)})">${marker(e.g,mc)}</g>`;
    });

    // 연락처 상호작용: 내 아웃리치는 내가 한 다른 일처럼 선 위에 놓고,
    // 상대의 답장과 미팅은 선 위에 띄운다.
    (r.touches||[]).forEach(e=>{
      const tx = x(parse(e.date).getTime());
      const gl = e.dir==='outbound' ? 'outreach' : (e.dir==='meeting' ? 'meeting' : 'response');
      const theirs = e.dir !== 'outbound';
      const ty = theirs ? (yc-7) : yc;
      if(theirs) s += `<line x1="${tx.toFixed(1)}" y1="${yc}" x2="${tx.toFixed(1)}" y2="${ty.toFixed(1)}" stroke="${C.contact}" stroke-width="0.75" stroke-opacity="0.4"/>`;
      s += `<g transform="translate(${tx.toFixed(1)},${ty.toFixed(1)})">${marker(gl,C.contact)}</g>`;
    });

    s += `</g>`;
  });

  s += defs + '</defs></svg>';
  wrap.innerHTML = s;
  attachTips(wrap);
}

function esc(t){return (t||'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}

const STLAB = {applied:'지원 완료',considering:'검토 중',recruiter:'리크루터 연락',
  phone_screen:'전화 스크리닝',rejected:'불합격',ghosted:'무응답',withdrawn:'철회',
  declined_by_candidate:'거절',discovered:'발견','re-applied':'재지원',update:'업데이트'};

const DIRLAB = {outbound:'내가 연락함', inbound:'상대가 회신함', meeting:'미팅'};

function attachTips(wrap){
  const tip = document.getElementById('tl-tip');
  wrap.querySelectorAll('.rowhit').forEach(g=>{
    g.addEventListener('mousemove',ev=>{
      const r = VIEW[+g.dataset.i];
      if(!r) return;
      const items = [];
      r.events.forEach(e=>items.push([e.date, `${STLAB[e.stage]||e.stage}`, false]));
      (r.touches||[]).forEach(e=>items.push([e.date,
        `✉ ${esc(e.who)} — ${DIRLAB[e.dir]||e.dir}`, true]));
      items.sort((a,b)=>a[0]<b[0]?-1:a[0]>b[0]?1:0);
      const evs = items.map(([dt,lab,isc])=>
        `<span class="ev"${isc?' style="color:#c4b5fd"':''}>${dt} · ${lab}</span>`).join('<br>');
      let statusLine = r.ghost ? `무응답 (확인일 ${r.ghost})`
                     : r.active ? `진행 중 · ${r.status}` : r.status;
      tip.innerHTML = `<b>${esc(r.co)}</b><br>${esc(r.role)}<br>`
        + `<span class="ev">${statusLine}</span><br><br>${evs}`;
      // 커서에 모서리를 맞추고, 공간이 있는 쪽으로 펼친다
      const GAP = 14, M = 8;
      const tw = tip.offsetWidth, th = tip.offsetHeight;
      const vw = window.innerWidth, vh = window.innerHeight;
      let left = ev.clientX + GAP;
      if(left + tw + M > vw) left = ev.clientX - GAP - tw;   // 왼쪽으로 뒤집기
      if(left < M) left = M;
      let top = ev.clientY + GAP;
      if(top + th + M > vh) top = ev.clientY - GAP - th;     // 위쪽으로 뒤집기
      if(top < M) top = M;
      tip.style.left = left+'px'; tip.style.top = top+'px'; tip.style.opacity = 1;
    });
    g.addEventListener('mouseleave',()=>{tip.style.opacity=0;});
  });
}

function legend(){
  const el = document.getElementById('tl-legend');
  const item = ([g,label])=>{
    const c = eventColor(g, C.active);
    return `<span class="li"><svg width="14" height="14" viewBox="-7 -7 14 14">${marker(g,c)}</svg>${label}</span>`;
  };
  el.innerHTML =
    `<span class="li tl-legend-head">선 위 — 나:</span>` + LEGEND_MINE.map(item).join('') +
    `<span class="li tl-legend-head">선 위쪽 — 상대:</span>` + LEGEND_THEIRS.map(item).join('');
}

function boot(){
  document.getElementById('tl-stamp').textContent =
    `(지원 ${TL.rows.length}건 · 생성 ${TL.generated.replace('T',' ')})`;
  legend();
  render();
}
const sel = document.getElementById('tl-filter');
if(sel){ FILTER = sel.value; sel.addEventListener('change',()=>{FILTER = sel.value; boot();}); }
let rt; window.addEventListener('resize',()=>{clearTimeout(rt);rt=setTimeout(boot,150);});
boot();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
