---
name: market-brief
description: >
  사용자의 목표 직무에 대한 시장 인텔리전스 브리프를 생성합니다. 직무 수요 동향, AI/자동화 대체 신호, 지역별 경쟁 상황 맥락을 포함하며 market-researcher 에이전트를 호출합니다.
  Generates a market intelligence brief for the user's target roles, including
  role demand trends, AI/automation displacement signals, and geographic
  competitiveness context. Invokes the market-researcher agent.
triggers:
  - "market brief"
  - "job market trends"
  - "what does the market look like"
  - "market demand for my role"
  - "is this role in demand"
  - "ai displacement outlook"
  - "how competitive is my market right now"
  - "/careerloop:market-brief"
  - "시장 브리프"
  - "채용 시장 동향"
  - "시장이 어때 보여"
  - "내 직무 시장 수요"
  - "이 직무 수요 있어"
  - "AI 대체 전망"
  - "지금 내 시장 경쟁이 치열해"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

### 스케줄링 (Claude Cowork)

**권장:** Cowork **`/schedule`**로 **주간** 실행(예: 매주 같은 요일)하면 매일 쏟아지는 잡음 없이 시장 신호를 최신으로 유지할 수 있습니다. 예약 실행 페이로드 예시:

> Run `/careerloop:market-brief` (CareerLoop `market-brief` skill) for my configured `{user_dir}`.

`market-researcher` 에이전트를 호출하여 사용자의 목표 직무와 지역 선호에 기반한 최신 시장 인텔리전스 브리프를 생성합니다.

중요한 호출/데이터 소스 규칙:
- 에이전트 이름은 정확히 `market-researcher`를 사용합니다(별칭 금지).
- 외부 웹 커넥터를 사용할 수 없다는 이유로 스킬을 실패시키지 않습니다.
- 사용자가 실시간 웹 소스를 명시적으로 요청하지 않는 한 로컬 근거(`profile.md`, `tracker.json`, `ExperienceLibrary.json`, analyst 기준값 표, AI 보고서)를 기본으로 사용합니다.
- 외부 소스를 요청받았으나 사용할 수 없으면 로컬 근거로 계속 진행하고 신뢰도의 한계를 표시합니다.

## 워크플로

### 1. 필수 컨텍스트 확인

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분리 레이아웃을 사용합니다. 읽기/쓰기 전에 반드시 이 문서를 읽습니다.

`{user_dir}/CareerLoop/profile.md`를 읽습니다.

목표 직무가 없으면:
> "시장 브리프를 생성하려면 목표 직무가 필요합니다. 먼저 `/careerloop:launch`를 실행하거나 `CareerLoop/profile.md`에 목표 직무를 입력해 주세요."

지역 선호가 없으면 계속 진행하되 지역 신뢰도를 제한적으로 표시합니다.

선택적으로 읽을 파일:
- 사용자별 전환율/타임라인 신호를 위한 `{user_dir}/CareerLoop/tracker.json` — 요약 행(`status`, `outcome`, `date_applied`, `latest_stage`, `latest_stage_date`)에 이 신호가 담겨 있습니다. 이 스킬은 지원 건별 단계 이력이 필요하지 않으므로 `detail_file`은 열지 않습니다
- 역량 적합성 맥락을 위한 `{user_dir}/CareerLoop/ExperienceLibrary.json`

### 2. market-researcher 호출

`market-researcher`에 다음을 넘겨 위임합니다.
- 전체 `CareerLoop/profile.md`
- 전체 `CareerLoop/tracker.json`(있는 경우) — 요약 행만 사용합니다. 단계 이력은 `applications/<application_id>.json`에 있으며 이 브리프에는 필요하지 않다고 에이전트에 알립니다
- 전체 `CareerLoop/ExperienceLibrary.json`(있는 경우)
- 필수 세 섹션을 모두 포함하라는 지시:
  1. Role demand trends (직무 수요 동향)
  2. AI/automation displacement outlook (AI/자동화 대체 전망)
  3. Geographic competitiveness signals (지역 경쟁력 신호)

사용자가 특정 직무/지역에 대해 물으면 브리프에서 이를 우선하고 프로필의 다른 목표는 부차적으로 다룹니다.

에이전트 이름/도구 문제로 호출이 실패하면:
- 정확한 `market-researcher` 이름으로 한 번 재시도합니다.
- 그래도 실패하면 로컬 파일을 바탕으로 구조화된 부분 결과를 반환하고 에이전트 호출이 실패했음을 명확히 밝힙니다.

### 3. 브리프 제시

반환된 출력을 다음 구조로 렌더링합니다.

```
**Market Brief** — {오늘 날짜}
대상 직무: {목록}
지역: {범위}
신뢰도: {Preliminary / Directional / Moderate / High}

HIGHLIGHTS
- 수요: {1줄}
- AI 전망: {1줄}
- 지역: {1줄}

ROLE DEMAND TRENDS
{직무별 수요 상황과 시사점}

AI/AUTOMATION DISPLACEMENT OUTLOOK
{고위험 vs 지속 가능한 업무 군집 + 포지셔닝 전환}

GEOGRAPHIC SIGNALS
{시장별 경쟁 상황과 타임라인 시사점}

PRIORITIZED NEXT MOVES (30-60 days)
1. ...
2. ...
3. ...
```

브리프는 실용적으로 유지합니다. 간결하고 근거 기반이며 탐색 의사결정과 직접 연결되어야 합니다.

### 4. 브리프를 디스크에 저장

렌더링한 브리프를 별도의 파일 쓰기 호출로 `{user_dir}/Market-Brief-{YYYY-MM-DD}.md`에 씁니다.

**파일 도구가 실패하면:** 전체 브리프를 펜스 마크다운 블록으로 출력하고 사용자에게 직접 저장하라고 안내합니다. 파일이 저장되지 않았다면 인덱스 갱신은 건너뜁니다.

성공하면 별도의 호출로 `{user_dir}/CareerLoop/artifacts-index.json`을 갱신합니다. 다음을 추가합니다.

```json
{
  "id": "{uuid}",
  "type": "market_brief",
  "filename": "Market-Brief-{YYYY-MM-DD}.md",
  "path": "{user_dir}/Market-Brief-{YYYY-MM-DD}.md",
  "target_company": null,
  "target_role": null,
  "date_created": "{today}",
  "source": "generated",
  "notes": "Market intelligence brief — {comma-separated target roles}"
}
```

### 5. PDF 생성을 위해 writer에 위임

`writer` 에이전트를 `market-brief-pdf` 모드로 호출하며 다음을 전달합니다.
- 4단계에서 저장한 마크다운 파일 경로
- 오늘 날짜

writer는 마크다운을 PDF로 변환하여 `{user_dir}/`에 마크다운과 나란히 저장하고, 확인된 PDF 경로를 이 작업의 최종 산출물로 사용자에게 제시합니다.

### 6. 다음 단계 제안

최우선 권고에 따라:
- 타기팅 전환이 필요하면: 직무/지역 필터를 다듬어 `/careerloop:search-jobs`를 제안합니다.
- 내러티브 전환이 필요하면: `/careerloop:assessment` 후 `/careerloop:tailor-resume`를 제안합니다.
- 실행 주기가 문제라면: `/careerloop:follow-up`과 `/careerloop:track-application`을 제안합니다.

