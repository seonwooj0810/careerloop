---
name: pipeline-status
description: >
  CareerLoop 파이프라인 상태 페이지를 생성합니다. 진행 중인 모든 지원(건),
  집중/추천 직무, 종료된 결과, 패스한 직무를 필터링하고 접을 수 있는 표로 보여주며
  지원 타임라인이 내장되어 있습니다.
  {user_dir}/CareerLoop/pipeline-status.html(및 pipeline-data.js,
  timeline.html)을 작성하고 브라우저에서 엽니다. tracker.json,
  recommendations.json, passed.json을 읽으며 요청할 때마다 항상 최신 스냅샷을
  만들고, /careerloop:setup-schedule로 매일 밤 갱신하도록 예약할 수도 있습니다.
  /careerloop:pipeline-status로도 호출할 수 있습니다.
  트리거 예: "show my pipeline status", "generate pipeline status page",
  "refresh pipeline dashboard", "show me my pipeline", "pipeline status"
  (파이프라인 상태 보여줘, 파이프라인 현황 페이지 생성, 대시보드 새로고침).
triggers:
  - "show my pipeline status"
  - "generate pipeline status page"
  - "refresh pipeline dashboard"
  - "show me my pipeline"
  - "open the pipeline status page"
  - "pipeline status"
  - "regenerate pipeline status"
  - "/careerloop:pipeline-status"
  - "/pipeline-status"
  - "파이프라인 현황 보여줘"
  - "파이프라인 상태 페이지 만들어줘"
  - "파이프라인 대시보드 새로고침"
  - "내 파이프라인 보여줘"
  - "파이프라인 상태 페이지 열어줘"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

파이프라인 상태 페이지(사용자의 전체 구직 파이프라인을 다루는 정적·독립형 HTML 대시보드)를 생성하고 브라우저에서 엽니다.

---

## 1. CareerLoop 설정 확인

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분할 레이아웃을 사용합니다. 읽기·쓰기 전에 반드시 이 문서를 먼저 읽습니다.

`{user_dir}/CareerLoop/tracker.json`, `{user_dir}/CareerLoop/recommendations.json`, `{user_dir}/CareerLoop/passed.json`을 읽습니다. 세 파일 모두 `/careerloop:launch`가 생성하는 핵심 파일입니다.

하나라도 없으면 다음을 출력합니다.
> 파이프라인 상태가 설정되지 않았습니다. 먼저 `/careerloop:launch`를 실행해 CareerLoop를 초기화해 주세요.

그런 다음 중단합니다.

---

## 2. 데이터 읽기 및 정규화

- **`tracker.json`** — 요약 행만 사용합니다. `stage_count` > 0인 각 행은 `applications/` 아래의 `detail_file`을 로드해 `stage_history[]`를 가져옵니다(종료 섹션의 기간 계산에 필요). `stage_count: 0`인 행은 추가로 읽지 않아도 됩니다.
- **`recommendations.json`** — 지원 전 직무이며 `status: "considering"`입니다(`priority`가 `"high"`이면 `"recommended"` — 기존 생성기와 같은 방식으로 정규화합니다. `considering`/`recommended` 레코드의 status가 priority 등급과 맞지 않으면 그 자리에서 수정하고 파일을 다시 씁니다).
- **`passed.json`** — 명시적으로 패스한 직무입니다(`status: "pass"`).

각 레코드를 페이지가 렌더링하는 항목으로만 줄입니다. 전체 단계 이력, 메모, 연락처는 내장하지 않습니다.

- **지원(Applications)**: `company`, `role`, `status`, `job_link`, `priority`, `date_applied`, `follow_up_date`, `location`, `next_step`, 그리고 `[{date}, ...]`로 줄인 `stage_history`(기간 계산용으로 날짜만).
- **추천(Recommendations) / 패스(passed)**: `company`, `role`, `status`, `job_link`, `priority`, `date_added`(`date_discovered` → `added_date` → 첫 메모 날짜 → 첫 stage_history 날짜 순으로 대체하며, 먼저 존재하는 값을 사용), `date_researched`, `location`, `next_step`, 그리고 같은 방식으로 줄인 `stage_history`.

---

## 3. `pipeline-data.js` 작성

`{user_dir}/CareerLoop/pipeline-data.js`를 오늘 날짜를 사용해 네 개의 전역 할당이 있는 일반 JS 파일(JSON 아님)로 작성합니다.

```js
// CareerLoop 파이프라인 데이터 — 생성일 {YYYY-MM-DD}
var TRACKER_DATA = {"applications": [...slimmed applications...]};
var RECS_DATA = {"recommendations": [...slimmed recommendations...]};
var PASSED_DATA = {"passed": [...slimmed passed...]};
var PIPELINE_GENERATED = "{YYYY-MM-DD}";
```

항상 덮어씁니다. 매번 새로운 스냅샷입니다.

---

## 4. `pipeline-status.html` 작성

아래 템플릿을 사용해 `{user_dir}/CareerLoop/pipeline-status.html`을 작성합니다. `{{USER_NAME}}`은 `profile.md`의 사용자 이름으로 바꿉니다(찾지 못하면 `"나의"`로 대체). 페이지는 `<script src="pipeline-data.js">`로 같은 위치의 `pipeline-data.js`에서 데이터를 불러오고 `timeline.html`을 iframe에 내장하므로, 둘 다 같은 디렉터리에 있어야 합니다.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>구직 — 파이프라인 상태</title>
<script src="pipeline-data.js"></script>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #fff; color: #1a1a1a; padding: 20px 20px 48px; font-size: 13px; }
h1 { font-size: 16px; font-weight: 500; margin-bottom: 3px; }
.meta { font-size: 11px; color: #999; margin-bottom: 14px; }
.page-head { display: flex; align-items: baseline; gap: 10px; margin-bottom: 14px; flex-wrap: wrap; }
.page-head h1 { margin-bottom: 0; }
.page-head .meta { margin-bottom: 0; }
.stamp { color: #10b981; font-weight: 500; }
.summary { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px; margin-top: 5px; }
.chip { font-size: 11px; padding: 3px 10px; border-radius: 20px; font-weight: 500; }
.chip-active { background: #d1fae5; color: #065f46; }
.chip-focus  { background: #ede9fe; color: #5b21b6; }
.chip-closed { background: #f3f4f6; color: #4b5563; }
.chip-passed { background: #f9fafb; color: #9ca3af; }
.controls { display: flex; gap: 10px; margin-bottom: 12px; align-items: center; flex-wrap: wrap; }
.controls label { font-size: 11px; color: #666; }
select { font-size: 11px; padding: 3px 8px; border: 0.5px solid #d1d5db; border-radius: 6px; background: #fff; color: #1a1a1a; cursor: pointer; }
table { width: 100%; border-collapse: collapse; font-size: 12px; }
col.col-co     { width: 15%; }
col.col-role   { width: 34%; }
col.col-stars  { width: 10%; }
col.col-status { width: 12%; }
col.col-date   { width: 10%; }
col.col-loc    { width: 19%; }
thead th { font-size: 10px; font-weight: 600; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.05em; padding: 7px 8px; border-bottom: 1px solid #e5e7eb; background: #fafafa; text-align: left; position: sticky; top: 0; z-index: 2; white-space: nowrap; }
thead th.center { text-align: center; }
tbody tr.section-hdr td { background: #f3f4f6; font-size: 10px; font-weight: 600; color: #6b7280; letter-spacing: 0.06em; text-transform: uppercase; padding: 5px 8px; border-top: 1px solid #e5e7eb; cursor: pointer; user-select: none; }
tbody tr.section-hdr:hover td { background: #eceef1; }
.caret { display: inline-block; width: 10px; margin-right: 3px; color: #9ca3af; font-size: 9px; transition: transform 0.12s ease; }
tbody tr.section-hdr.collapsed .caret { transform: rotate(-90deg); }
tbody tr.data-row.sec-collapsed { display: none; }
tbody tr.data-row { border-bottom: 0.5px solid #f0f0f0; }
tbody tr.data-row:hover { background: #f9fafb; }
tbody tr.hidden { display: none; }
td { padding: 6px 8px; vertical-align: middle; }
td.center { text-align: center; }
a.co { font-weight: 500; color: #1a1a1a; text-decoration: none; border-bottom: 1px solid transparent; }
a.co:hover { border-bottom-color: #6b7280; }
a.role-link { color: #374151; text-decoration: none; border-bottom: 1px dotted #d1d5db; }
a.role-link:hover { color: #1a1a1a; border-bottom-color: #6b7280; }
.role-plain { color: #374151; }
.role-bold { font-weight: 600; color: #374151; }
.badge { display: inline-block; padding: 2px 7px; border-radius: 4px; font-size: 10px; font-weight: 600; white-space: nowrap; }
.b-applied   { background: #dbeafe; color: #1e40af; }
.b-screen    { background: #d1fae5; color: #065f46; }
.b-interview { background: #d1fae5; color: #065f46; }
.b-offer     { background: #dcfce7; color: #15803d; }
.b-ghosted   { background: #fef3c7; color: #92400e; }
.b-rejected  { background: #fee2e2; color: #991b1b; }
.b-withdrawn, .b-declined, .b-expired { background: #f3f4f6; color: #4b5563; }
.b-considering { background: #fef9c3; color: #854d0e; }
.b-rec       { background: #ede9fe; color: #5b21b6; }
.b-pass      { background: #f3f4f6; color: #9ca3af; text-decoration: line-through; }
.b-referred  { background: #e0e7ff; color: #3730a3; }
.b-exec      { background: #bbf7d0; color: #166534; }
.stars { font-size: 11px; white-space: nowrap; }
.loc-text  { font-size: 11px; color: #6b7280; }
.date-val  { font-size: 11px; color: #374151; white-space: nowrap; }
.date-dur  { font-size: 11px; color: #9ca3af; white-space: nowrap; }
.date-disc { font-size: 11px; color: #7c3aed; white-space: nowrap; }
span.dash  { color: #d1d5db; }
.no-data   { padding: 32px 8px; color: #9ca3af; font-size: 12px; }
.badge[data-next] { cursor: help; }
#status-tip { position: fixed; z-index: 50; max-width: 300px; background: #1a1a1a; color: #f9fafb; font-size: 11px; line-height: 1.45; padding: 8px 10px; border-radius: 6px; box-shadow: 0 6px 18px rgba(0,0,0,0.22); pointer-events: none; display: none; }
.tl-embed { width: 100%; border: 0.5px solid #e5e7eb; border-radius: 8px; margin-bottom: 1px; overflow: hidden; }
iframe#tl-frame { display: block; width: 100%; height: 450px; border: 0; }
</style>
</head>
<body>
<div id="status-tip"></div>
<div class="page-head">
  <h1>구직 — 파이프라인 상태</h1>
  <p class="meta">{{USER_NAME}} &nbsp;·&nbsp; <span class="stamp" id="gen-stamp">불러오는 중…</span></p>
</div>
<div class="tl-embed">
  <iframe id="tl-frame" src="timeline.html" title="지원 파이프라인 타임라인" scrolling="no" loading="lazy"></iframe>
</div>
<div class="summary">
  <span class="chip chip-active" id="chip-active">— 진행 중</span>
  <span class="chip chip-focus"  id="chip-focus">— 집중</span>
  <span class="chip chip-closed" id="chip-closed">— 종료</span>
  <span class="chip chip-passed" id="chip-passed">— 패스</span>
</div>
<div class="controls">
  <label>필터:</label>
  <select id="f-status" onchange="applyFilter()">
    <option value="all">전체 행</option>
    <option value="active">진행 중만</option>
    <option value="focus">집중 / 추천</option>
    <option value="action">조치 필요</option>
    <option value="closed">종료</option>
    <option value="passed">패스</option>
  </select>
  <label style="margin-left:6px">최소 평점:</label>
  <select id="f-stars" onchange="applyFilter()">
    <option value="0">전체</option>
    <option value="3">3+</option>
    <option value="4">4+</option>
    <option value="5">5만</option>
  </select>
</div>
<script>
(function(){
  var f=document.getElementById('tl-frame');
  function fit(){try{var d=f.contentDocument||f.contentWindow.document;var h=Math.max(d.body.scrollHeight,d.documentElement.scrollHeight);if(h)f.style.height=(h+8)+'px';}catch(e){}}
  f.addEventListener('load',function(){fit();setTimeout(fit,150);setTimeout(fit,600);});
})();
</script>
<table>
<colgroup>
  <col class="col-co"><col class="col-role"><col class="col-stars">
  <col class="col-status"><col class="col-date"><col class="col-loc">
</colgroup>
<thead><tr>
  <th>회사</th>
  <th>직무</th>
  <th class="center" title="우선순위 평점">평점</th>
  <th>상태</th>
  <th>날짜</th>
  <th>위치</th>
</tr></thead>
<tbody id="tbody"></tbody>
</table>
<script>
var MONTHS=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
function fmtDate(s){if(!s)return null;try{var p=s.split('-');return MONTHS[+p[1]-1]+' '+ +p[2];}catch(e){return s;}}
function daysBetween(a,b){if(!a||!b)return null;try{var d=Math.round((new Date(b+'T00:00:00')-new Date(a+'T00:00:00'))/86400000);return d>=0?d:null;}catch(e){return null;}}
function durationLabel(d){if(d===null)return null;if(d===0)return '<1d';if(d<14)return d+'d';var w=Math.round(d/7);if(w<9)return w+'w';return Math.round(d/30.4)+'mo';}
function parsePriority(p){if(!p&&p!==0)return 0;if(typeof p==='number')return Math.min(5,Math.max(0,Math.round(p)));var s=String(p).toLowerCase();if(s==='critical')return 5;if(s==='high')return 4;if(s==='medium'||s==='normal')return 3;if(s==='low')return 2;return 0;}
function isOverdue(d){if(!d)return false;try{var dt=new Date(d+'T00:00:00'),t=new Date();t.setHours(0,0,0,0);return dt<=t;}catch(e){return false;}}
function getBaseUrl(u){if(!u||u==='#')return null;try{return new URL(u).origin;}catch(e){return null;}}
function stars(n){if(!n)return '<span class="dash">–</span>';var s='';for(var i=1;i<=5;i++)s+='<span style="color:'+(i<=n?'#f59e0b':'#e5e7eb')+'">&#9733;</span>';return '<span class="stars">'+s+'</span>';}
var BL={applied:'지원 완료',referred:'추천받음',phone_screen:'전화 스크리닝',screen:'전화 스크리닝',interview:'면접',executive_round_scheduled:'임원 면접 예정',executive_round_complete:'임원 면접 완료',offer:'오퍼',accepted:'수락',ghosted:'무응답',rejected:'불합격',withdrawn:'철회',declined_by_candidate:'거절',expired:'만료',considering:'검토 중',recommended:'추천',pending_decision:'추천',pass:'패스'};
var BC={applied:'b-applied',referred:'b-referred',phone_screen:'b-screen',screen:'b-screen',interview:'b-interview',executive_round_scheduled:'b-exec',executive_round_complete:'b-exec',offer:'b-offer',accepted:'b-screen',ghosted:'b-ghosted',rejected:'b-rejected',withdrawn:'b-withdrawn',declined_by_candidate:'b-declined',expired:'b-expired',considering:'b-considering',recommended:'b-rec',pending_decision:'b-rec',pass:'b-pass'};
function badge(s,next){var attr=next?' data-next="'+esc(next)+'"':'';return '<span class="badge '+(BC[s]||'b-applied')+'"'+attr+'>'+(BL[s]||s)+'</span>';}
var ACTIVE_S=['applied','referred','phone_screen','screen','interview','executive_round_scheduled','executive_round_complete','offer','accepted'];
var CLOSED_S=['ghosted','rejected','declined_by_candidate'];
var PASSED_S=['withdrawn','expired','pass'];
function getSection(s){if(PASSED_S.indexOf(s)!==-1)return 'passed';if(CLOSED_S.indexOf(s)!==-1)return 'closed';if(ACTIVE_S.indexOf(s)!==-1)return 'active';return 'focus';}
function esc(s){return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
var SL={active:'진행 중인 지원',focus:'집중 — 추천 및 검토 중',closed:'종료',passed:'패스'};
var COLLAPSED={active:false,focus:true,closed:true,passed:true};
var ROWS=[];

function buildRows(){
  var rows=[];
  var apps=(typeof TRACKER_DATA!=='undefined'&&TRACKER_DATA.applications)||[];
  var recs=(typeof RECS_DATA!=='undefined'&&RECS_DATA.recommendations)||[];
  apps.forEach(function(app){
    var status=app.status||'applied',sec=getSection(status);
    var sh=app.stage_history||[];
    var start=app.date_applied||(sh[0]&&sh[0].date)||'';
    var sortDate,dateCell;
    if(sec==='closed'){
      var end=(sh[sh.length-1]&&sh[sh.length-1].date)||start;
      sortDate=end;
      var dur=durationLabel(daysBetween(start,end));
      dateCell=dur?'<span class="date-dur">'+esc(dur)+'</span>':'<span class="dash">–</span>';
    }else{
      sortDate=start;
      var fd=fmtDate(start);
      dateCell=fd?'<span class="date-val">'+esc(fd)+'</span>':'<span class="dash">–</span>';
    }
    rows.push({company:app.company||'—',cUrl:getBaseUrl(app.job_link),role:app.role||'—',jUrl:app.job_link||null,sec:sec,status:status,rating:parsePriority(app.priority),needsAction:isOverdue(app.follow_up_date),location:app.location||'',dateCell:dateCell,sortDate:sortDate,nextStep:app.next_step||null});
  });
  recs.forEach(function(rec){
    var status=rec.status||'considering',sec=getSection(status);
    var sortDate,dateCell;
    if(sec==='closed'){
      sortDate=rec.date_researched||rec.date_added||'';
      var sh=rec.stage_history||[];
      var start=rec.date_added||'';
      var end=(sh[sh.length-1]&&sh[sh.length-1].date)||sortDate;
      var dur=durationLabel(daysBetween(start,end));
      dateCell=dur?'<span class="date-dur">'+esc(dur)+'</span>':'<span class="dash">–</span>';
    }else{
      sortDate=rec.date_added||'';
      var fd=fmtDate(rec.date_added);
      dateCell=fd?'<span class="date-disc">'+esc(fd)+'</span>':'<span class="dash">–</span>';
    }
    rows.push({company:rec.company||'—',cUrl:getBaseUrl(rec.job_link),role:rec.role||'—',jUrl:rec.job_link||null,sec:sec,status:status,rating:parsePriority(rec.priority),needsAction:false,location:rec.location||'',dateCell:dateCell,sortDate:sortDate,nextStep:rec.next_step||null});
  });
  var passed=(typeof PASSED_DATA!=='undefined'&&PASSED_DATA.passed)||[];
  passed.forEach(function(p){
    var sh=p.stage_history||[];
    var start=p.date_added||'';
    var end=(sh[sh.length-1]&&sh[sh.length-1].date)||p.date_researched||start;
    var dur=durationLabel(daysBetween(start,end));
    var dateCell=dur?'<span class="date-dur">'+esc(dur)+'</span>':'<span class="dash">–</span>';
    rows.push({company:p.company||'—',cUrl:getBaseUrl(p.job_link),role:p.role||'—',jUrl:p.job_link||null,sec:'passed',status:'pass',rating:parsePriority(p.priority),needsAction:false,location:p.location||'',dateCell:dateCell,sortDate:end,nextStep:p.next_step||null});
  });
  var so={active:0,focus:1,closed:2,passed:3};
  rows.sort(function(a,b){
    if(so[a.sec]!==so[b.sec])return so[a.sec]-so[b.sec];
    var da=a.sortDate||'',db=b.sortDate||'';
    if(da!==db)return da>db?-1:1;
    return a.company.localeCompare(b.company);
  });
  ROWS=rows;
}

function render(){
  var tbody=document.getElementById('tbody'),html='';
  ['active','focus','closed','passed'].forEach(function(sec){
    var sr=ROWS.filter(function(r){return r.sec===sec;});
    if(!sr.length)return;
    var col=COLLAPSED[sec];
    html+='<tr class="section-hdr'+(col?' collapsed':'')+'" data-sec="'+sec+'"><td colspan="6"><span class="caret">&#9662;</span>'+SL[sec]+' ('+sr.length+')</td></tr>';
    sr.forEach(function(row){
      var co=row.cUrl?'<a class="co" href="'+row.cUrl+'" target="_blank">'+esc(row.company)+'</a>':'<span class="co">'+esc(row.company)+'</span>';
      var roleSpan='<span class="'+(row.needsAction?'role-bold':'role-plain')+'">'+esc(row.role)+'</span>';
      var rInner=row.jUrl?'<a class="role-link" href="'+row.jUrl+'" target="_blank">'+roleSpan+'</a>':roleSpan;
      var locCell=row.location?'<span class="loc-text">'+esc(row.location)+'</span>':'<span class="dash">–</span>';
      html+='<tr class="data-row'+(COLLAPSED[row.sec]?' sec-collapsed':'')+'" data-sec="'+row.sec+'" data-status="'+row.status+'" data-rating="'+row.rating+'" data-action="'+(row.needsAction?'1':'0')+'">'
        +'<td>'+co+'</td><td>'+rInner+'</td>'
        +'<td class="center">'+stars(row.rating)+'</td>'
        +'<td>'+badge(row.status,row.nextStep)+'</td>'
        +'<td>'+row.dateCell+'</td>'
        +'<td>'+locCell+'</td></tr>';
    });
  });
  document.getElementById('tbody').innerHTML=html||'<tr><td colspan="6" class="no-data">데이터 없음 — pipeline-data.js가 같은 폴더에 있는지 확인하세요.</td></tr>';
}

function applyFilter(){
  var sf=document.getElementById('f-status').value;
  var ms=parseInt(document.getElementById('f-stars').value,10);
  var sv={};
  document.querySelectorAll('tbody tr.data-row').forEach(function(r){
    var show=true;
    if(sf==='active')show=r.dataset.sec==='active';
    else if(sf==='focus')show=r.dataset.sec==='focus';
    else if(sf==='action')show=r.dataset.action==='1';
    else if(sf==='closed')show=r.dataset.sec==='closed';
    else if(sf==='passed')show=r.dataset.sec==='passed';
    if(ms>0&&parseInt(r.dataset.rating,10)<ms)show=false;
    r.classList.toggle('hidden',!show);
    if(show)sv[r.dataset.sec]=true;
  });
  document.querySelectorAll('tbody tr.section-hdr').forEach(function(h){h.classList.toggle('hidden',!sv[h.dataset.sec]);});
  updateChips();
}

function updateChips(){
  var vis=Array.from(document.querySelectorAll('tbody tr.data-row:not(.hidden)'));
  document.getElementById('chip-active').textContent=vis.filter(function(r){return r.dataset.sec==='active';}).length+' 진행 중';
  document.getElementById('chip-focus').textContent=vis.filter(function(r){return r.dataset.sec==='focus';}).length+' 집중';
  document.getElementById('chip-closed').textContent=vis.filter(function(r){return r.dataset.sec==='closed';}).length+' 종료';
  document.getElementById('chip-passed').textContent=vis.filter(function(r){return r.dataset.sec==='passed';}).length+' 패스';
}

var stampEl=document.getElementById('gen-stamp');
stampEl.textContent=typeof PIPELINE_GENERATED!=='undefined'?'생성: '+PIPELINE_GENERATED:'데이터 로드됨';
buildRows();render();updateChips();

document.getElementById('tbody').addEventListener('click',function(e){
  var h=e.target.closest('tr.section-hdr');
  if(!h)return;
  var sec=h.dataset.sec;
  var collapsed=h.classList.toggle('collapsed');
  COLLAPSED[sec]=collapsed;
  document.querySelectorAll('tbody tr.data-row[data-sec="'+sec+'"]').forEach(function(r){
    r.classList.toggle('sec-collapsed',collapsed);
  });
});

var tipEl=document.getElementById('status-tip');
function positionTip(e){
  var x=e.clientX+14,y=e.clientY+14;
  var maxX=window.innerWidth-310,maxY=window.innerHeight-90;
  if(x>maxX)x=e.clientX-314;
  if(y>maxY)y=e.clientY-40;
  tipEl.style.left=x+'px';
  tipEl.style.top=y+'px';
}
document.getElementById('tbody').addEventListener('mouseover',function(e){
  var t=e.target.closest('.badge[data-next]');
  if(!t)return;
  tipEl.textContent=t.getAttribute('data-next');
  tipEl.style.display='block';
  positionTip(e);
});
document.getElementById('tbody').addEventListener('mousemove',function(e){
  if(tipEl.style.display==='block'&&e.target.closest('.badge[data-next]'))positionTip(e);
});
document.getElementById('tbody').addEventListener('mouseout',function(e){
  var t=e.target.closest('.badge[data-next]');
  if(!t)return;
  tipEl.style.display='none';
});
</script>
</body>
</html>
```

---

## 5. 내장 타임라인 생성

사용자의 데이터 디렉터리를 대상으로 플러그인의 타임라인 생성기를 실행합니다.

```bash
python3 {plugin_dir}/scripts/build_timeline.py {user_dir}/CareerLoop
```

이 스크립트는 `tracker.json`(분할된 `detail_file`/`contacts_file` 스키마를 준수)을 읽고 `{user_dir}/CareerLoop/timeline.html`을 작성하며, `pipeline-status.html`이 이를 iframe으로 내장합니다.

---

## 6. 브라우저에서 열기

```bash
python3 -c "import webbrowser, os; webbrowser.open('file://' + os.path.abspath('{user_dir}/CareerLoop/pipeline-status.html'))"
```

## 7. 확인

```
파이프라인 상태 페이지 생성 완료 → {user_dir}/CareerLoop/pipeline-status.html
브라우저에서 여는 중입니다.
```

파일이 이미 있으면 덮어씁니다. 항상 새로운 스냅샷입니다.

---

## 가드레일

- 데이터를 절대 지어내지 않습니다. `tracker.json`, `recommendations.json`, `passed.json` 중 하나라도 없으면 사용자에게 `/careerloop:launch`를 안내하고 중단합니다.
- `pipeline-data.js`는 JSON이 아닌 일반 JS 전역 변수 파일입니다. `export`나 ES 모듈 구문으로 감싸지 않습니다. `pipeline-status.html`은 일반 `<script src>` 태그로 이를 불러옵니다.
- `pipeline-data.js`, `pipeline-status.html`, `timeline.html`을 `{user_dir}/CareerLoop/`에 함께 둡니다. 페이지의 iframe과 script-src 참조는 상대 경로입니다.
- 이 스킬은 요청 시 실행하거나 `/careerloop:setup-schedule`(대시보드 새로고침 옵션)로 매일 밤 예약할 수 있으며, 어느 경로든 정확히 같은 단계를 수행합니다.
