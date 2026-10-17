---
name: report
description: >
  네 가지 애널리스트 작업(결과 패턴 분석, 전이 가능한 강점, AI 대체 가능성 평가, 시장 벤치마크)을 모두 실행하고,
  통합 인사이트 보고서를 제공한 뒤 브라우저에서 파이프라인 상태 페이지를 엽니다. 사용자의 구직 건강도, 커리어 자산,
  미래 포지셔닝, 그리고 업계 기준 대비 지표를 한눈에 보여주는 통합 뷰입니다. analyst 에이전트와 pipeline-status
  스킬을 호출합니다. 다음과 같은 요청에 사용합니다: "run the analyst", "analyst report", "full analyst report",
  "full career analysis", "show me the full report", "분석 리포트 보여줘", "전체 커리어 분석 돌려줘".
  (Runs all four analyst operations — outcome pattern analysis, transferable
  strengths, AI displacement assessment, and market benchmark — and delivers
  a unified insight report followed by the pipeline status page opened in
  the browser. The integrated view of the user's search health, career
  capital, future positioning, and how their metrics compare to industry
  norms. Invokes the analyst agent and pipeline-status skill.)
triggers:
  - "run the analyst"
  - "analyst report"
  - "full analyst report"
  - "run full analysis"
  - "give me an analyst report"
  - "run all three analyses"
  - "full career analysis"
  - "show me the full report"
  - "분석가 보고서"
  - "전체 분석 보고서"
  - "전체 분석 실행해줘"
  - "분석가 보고서 만들어줘"
  - "세 가지 분석 모두 돌려줘"
  - "전체 커리어 분석"
  - "전체 보고서 보여줘"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

`analyst` 에이전트를 호출해 세 가지 작업을 모두 실행하고 통합 인사이트 보고서를 제공합니다.

## 워크플로

### 1. 데이터 존재 확인

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분리 레이아웃을 사용합니다. 읽거나 쓰기 전에 반드시 이 문서를 먼저 읽습니다.

`{user_dir}/CareerLoop/tracker.json`, `{user_dir}/CareerLoop/ExperienceLibrary.json`, `{user_dir}/CareerLoop/profile.md`, `{user_dir}/CareerLoop/artifacts-index.json`을 읽습니다. ExperienceLibrary가 비어 있으면:

> "ExperienceLibrary가 비어 있습니다. 먼저 `/careerloop:add-source`를 실행해 이력서를 추가하세요."

트래커에 지원(건)이 없으면 그 사실을 본문에 그대로 밝힙니다. 패턴 분석은 제한되지만 나머지 두 작업은 계속 실행할 수 있습니다.

`tracker.json`에는 이제 **요약 행만** 있습니다. 작업 2와 3(전이 가능한 강점, AI 대체 가능성)은 이 행들과 ExperienceLibrary만으로 실행되며 다른 것은 필요 없습니다. 작업 1과 4(결과 패턴, 시장 벤치마크)는 단계 전환과 노트 텍스트를 근거로 추론하는데, 이 정보는 지원(건)별 상세 파일에 있습니다. 따라서 핸드오프 전에 `stage_count`가 `0`보다 크거나 **또는** `outcome` != `"pending"`인 모든 요약 행에 대해 `{user_dir}/CareerLoop/` + `detail_file`을 수집하고, 나머지는 건너뜁니다. contacts 파일은 불러오지 않습니다. 어떤 애널리스트 작업도 사용하지 않습니다.

### 1.5 ATS 점수 존재 확인 (이력서 아티팩트)

`{user_dir}/CareerLoop/artifacts-index.json`을 읽습니다.

`type: "resume"`인 아티팩트 중 `ats_score`가 없거나 `ats_score: null`인 것이 있으면:

- 해당 이력서 아티팩트에 대해 `resume-score`를 호출합니다(스킬이 찾아서 ATS 점검을 실행할 수 있도록 `filename`을 함께 전달).
- JD 맥락이 없어 키워드 커버리지를 계산할 수 없더라도, 서식/서사 ATS 점검은 그대로 진행하고 ATS 점검이 계산할 수 있는 `ats_score`를 기록합니다.
- ATS 점검 후 `{user_dir}/CareerLoop/artifacts-index.json`을 다시 확인합니다. 점수가 여전히 없으면 보고서 하이라이트에 남은 ATS 공백을 기재합니다.

### 2. analyst 호출 — 네 가지 작업 모두

`analyst` 에이전트에게 다음을 넘깁니다.
- 전체 `CareerLoop/tracker.json` (요약 행 — `status`, `outcome`, `date_applied`, `follow_up_date`, `latest_stage`, `latest_stage_date`, `notes_count`, `stage_count`, `contact_count`, `pipeline_summary`, `search_performance`)
- 1단계에서 선택한 `CareerLoop/applications/<application_id>.json` 상세 파일들(`application_id`로 키 지정). 이 파일들에 작업 1과 4에 필요한 `stage_history[]`와 `notes[]`가 있습니다. 단계 이력은 `tracker.json`에 **없다**는 점을 분명히 밝힙니다. 요약 행만으로 전환율 계산을 하면 오류 없이 전환이 0건으로 나옵니다
- 전체 `CareerLoop/ExperienceLibrary.json`
- 전체 `artifacts-index.json`
- 전체 `CareerLoop/profile.md`
- AI 대체 가능성 평가 전에 Anthropic, “Labor market impacts of AI: A new measure and early evidence” (Massenkoff·McCrory, 2026-03-05, https://www.anthropic.com/research/labor-market-impacts)를 확인하라는 지시(웹 도구로 원문 확인 → 작업 폴더의 PDF → 둘 다 불가하면 수치를 인용하지 말고 “보고서 미확인”을 명시)
- 네 가지 작업을 모두 실행하라는 지시: 결과 패턴(Op 1), 전이 가능한 강점(Op 2), AI 대체 가능성(Op 3), 시장 벤치마크(Op 4)
- 지시: 서술 보고서와 함께, `{user_dir}/CareerLoop/analyst-graph-data.json`에 쓸 수 있는 그래프용 데이터를 다음 스키마로 반환할 것
  - `ai_displacement_outlook`: `{overall_risk, exposure_min_pct, exposure_max_pct, durable_min_pct, durable_max_pct, durable_differentiators[], narrative_reframe}`
  - `transferable_strengths`: `{name, rating, score_0_100, evidence, destinations[]}`의 배열

### 3. 통합 보고서 제시

텍스트 보고서에는 `HIGHLIGHTS`, `PART 1: WHAT'S WORKING IN YOUR SEARCH`, `RECOMMENDED NEXT ACTIONS`만 포함합니다. `PART 2`/`PART 3`/`PART 4` 섹션은 출력하지 않고, 대신 AI 대체 가능성 + 전이 가능한 강점 그래프와 파이프라인/벤치마크 상세는 파이프라인 대시보드를 보도록 안내합니다.

```
**Analyst Report** — {오늘 날짜}

HIGHLIGHTS
- 검색:        {무엇이 효과가 있고 없는지에 대한 한 문장 평가}
- 강점:        {가장 전이 가능한 역량에 대한 한 문장}
- AI 전망:     {전반적인 대체 가능성 리스크 수준에 대한 한 문장}
- 시장 대비:   {이 레벨과 시장의 기준과 비교한 파이프라인 지표에 대한 한 문장}
- ATS 현황:    {이력서 아티팩트의 `ats_score` 존재 여부(및 남은 공백)에 대한 한 줄}

---

PART 1: WHAT'S WORKING IN YOUR SEARCH
{가장 실행 가능성이 높은 결과 패턴 발견 사항 하나에 대한 1–2문장 하이라이트}
{다음을 담은 짧은 상세 설명(3–6개 불릿): 데이터가 보여주는 것, 아직 보여주지 못하는 것, 가장 큰 파이프라인 병목 1–2개}

ExperienceLibrary 가중치 업데이트: {n}건 변경 (상향 {n}, 하향 {n})
데이터 신뢰도: {Preliminary / Directional / Moderate / High}

참고: AI 대체 가능성 + 전이 가능한 강점 그래프(그리고 파이프라인 퍼널/벤치마크 + ExperienceLibrary 가중치)는 파이프라인 대시보드에서 인터랙티브하게 볼 수 있으므로, 텍스트 보고서에는 같은 차트/표를 중복해서 싣지 않습니다.

---

---

PART 3: AI DISPLACEMENT OUTLOOK
{상세 설명 전에 오는 1–2문장의 섹션 하이라이트}
{현재 및 목표 직무의 리스크 프로필, 지속 가능한 차별점, 서사 재구성}

---

PART 4: BENCHMARK vs. INDUSTRY NORMS
{1–2문장의 섹션 하이라이트 — 이 레벨과 시장 기준에서 지표가 기준보다 높은가, 낮은가?}

  파이프라인 ({level} · {주요 회사 규모} · {지역})
    지원 → 응답:        {user%}  기준 {low–high%}  {▲ 상회 / ▼ 하회 / — 기준 수준}
    응답 → 스크린:      {user%}  기준 {low–high%}  {▲/▼/—}
    스크린 → 면접:      {user%}  기준 {low–high%}  {▲/▼/—}
    면접 → 오퍼:        {user%}  기준 {low–high%}  {▲/▼/—}
    평균 응답 소요일:   {n}일    기준 {low–high}일  {▲/▼/—}
    무응답(ghosting) 비율: {user%}  기준 {low–high%}  {▲/▼/—}

  ATS 점수
    평균: {n}/100  ·  기준선: 70+  ·  {상회/하회}
    최저: {score} — {filename}

  {레벨 및 회사 규모 기준 대비 보상 포지셔닝에 대한 1–2문장, 데이터가 없으면 salary-research를 실행하라는 안내}

---

RECOMMENDED NEXT ACTIONS
1. {네 가지 분석을 모두 반영한 가장 영향력 큰 액션}
2. ...
```

### 4. 대시보드 그래프 데이터 쓰기 (AI 대체 가능성 + 전이 가능한 강점)

2단계에서 analyst 에이전트가 반환한 그래프용 데이터를 사용해 `{user_dir}/CareerLoop/analyst-graph-data.json`을 씁니다(필요하면 `{user_dir}/CareerLoop/`를 생성).

필수 JSON 키:
- `ai_displacement_outlook`
- `transferable_strengths`

데이터가 부족해 필드가 빠지면, 대시보드가 실패하지 않고 자리 표시자를 보여주도록 `null`(또는 `[]`)로 설정합니다.

대시보드 하위 키 (가능한 경우):
- `ai_displacement_outlook`: `overall_risk`, `exposure_min_pct`, `exposure_max_pct`, `durable_min_pct`, `durable_max_pct`
- `transferable_strengths[]`: `name`, `rating`, `score_0_100` (선택적으로 `evidence`, `destinations[]`)

### 5. 파이프라인 상태 페이지 생성

텍스트 보고서를 제시한 뒤 `pipeline-status` 스킬을 호출합니다. 이 스킬이 트래커/추천/패스(passed) 데이터를 읽고, `{user_dir}/CareerLoop/pipeline-status.html`(및 `pipeline-data.js`, `timeline.html`)을 쓴 다음 브라우저에서 자동으로 엽니다.

사용자가 요청하길 기다리지 말고, 보고서를 실행할 때마다 생성합니다.

### 6. 다음 단계 제안

네 가지 분석 전반에서 가장 두드러진 발견에 따라 다음과 같이 안내합니다.
- ATS 점수가 낮은 것이 있으면: > "개선 여지가 있는 이력서에 대해 `/careerloop:ats-optimization`을 실행하세요."
- 검색 패턴이 약하면: > "업데이트된 ExperienceLibrary 가중치로 `/careerloop:tailor-resume`를 실행하세요."
- 전이 가능한 강점이 피벗을 시사하면: > "{role type}을 대상으로 `/careerloop:search-jobs`를 실행하세요."
- 현재 포지셔닝에서 AI 리스크가 높으면: > "재구성한 서사를 시도해 보려면 `/careerloop:cover-letter`를 실행하세요."
- 파이프라인 지표가 기준보다 낮으면: > "맞춤 개선안이 포함된 전체 분석은 `/careerloop:benchmark`를 실행하세요."
