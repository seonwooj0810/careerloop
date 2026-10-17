---
name: benchmark
description: >
  사용자의 파이프라인 전환율, 응답 소요 시간, ATS 점수, 보상 포지셔닝을 직무, 레벨, 회사 규모, 지역별로 구분한 업계 기준값과 비교합니다. analyst Operation 4를 호출합니다.
  Benchmarks the user's pipeline conversion rates, response timelines, ATS
  scores, and compensation positioning against industry norms segmented by
  role, level, company size, and geography. Invokes analyst Operation 4.
triggers:
  - "how does my search compare"
  - "benchmark my search"
  - "benchmark my numbers"
  - "am I above average"
  - "am I below average"
  - "how are my response rates"
  - "how do my numbers look"
  - "how does my pipeline compare"
  - "how am I doing compared to other candidates"
  - "what's a normal response rate"
  - "is my conversion rate good"
  - "how long does it usually take to get an offer"
  - "how competitive is my market"
  - "내 구직 활동을 벤치마크해줘"
  - "내 수치 어떤 편이야"
  - "평균보다 높아"
  - "평균보다 낮아"
  - "내 응답률은 어때"
  - "내 전환율은 괜찮아"
  - "오퍼까지 보통 얼마나 걸려"
  - "다른 지원자들에 비해 어떤가"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

사용자의 파이프라인 성과를 직무, 레벨, 회사 규모, 지역에 맞는 업계 기준값과 비교합니다.

## 워크플로

### 1. 데이터 임계값 확인

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분리 레이아웃을 사용합니다. 읽기/쓰기 전에 반드시 이 문서를 읽습니다.

`{user_dir}/CareerLoop/tracker.json`을 읽습니다. 요약 행에서 전체 지원 건 수(모든 상태)를 셉니다. 이 확인에는 상세 파일이 필요 없습니다. 5건 미만이면:

> "의미 있는 벤치마크를 실행하려면 최소 5건의 지원이 필요합니다. 현재 {n}건입니다. `/careerloop:track-application`으로 지원 기록을 계속 쌓은 뒤 이력이 더 늘어나면 다시 실행해 주세요."

임계값 미만이면 여기서 멈춥니다.

5건 이상이지만 확정된 결과가 10건 미만이면, 결과가 예비 수준이라는 점을 덧붙여 진행합니다.

### 2. 전환율 계산에 필요한 단계 이력 로드

아래 모든 파이프라인 전환율과 타임라인 수치는 `stage_history[]`에서 계산되며, **`tracker.json` 단독으로는 단계 이력이 전혀 들어 있지 않습니다.** 단계 이력은 지원 건별 상세 파일로 옮겨졌기 때문입니다. `tracker.json`만으로 지원 → 응답, 스크리닝 → 면접, 면접 → 오퍼, 응답까지 걸린 일수를 계산하면 조용히 0이 나오고, 실제로는 그렇지 않은데도 사용자를 기준값보다 한참 낮다고 보고하게 됩니다.

1. `{user_dir}/CareerLoop/tracker.json`을 읽고 `applications[]`를 가져옵니다.
2. 모든 행을 순회하며 해당 지원 건의 `stage_history[]`를 얻기 위해 행의 `detail_file`(`CareerLoop/` 기준 상대 경로)을 로드합니다. 행의 `stage_count`가 `0`일 때만 건너뜁니다. 그 행은 셀 단계가 실제로 없습니다.
3. 요약 필드가 질문에 바로 답할 때는 그것을 사용합니다. `latest_stage`와 `latest_stage_date`는 현재 퍼널 위치와 마지막 이동 날짜를 알려주고, `stage_count` / `notes_count` / `contact_count`는 읽지 않고도 건수를 알려줍니다.

### 3. analyst 호출 — Operation 4

`analyst` 에이전트에 다음을 넘겨 위임합니다.
- `CareerLoop/tracker.json`(요약 행) **그리고** 로드한 `applications/<application_id>.json` 상세 파일 — 둘 다 전달합니다. 요약 행만으로는 전환율과 타임라인 계산이 불가능합니다
- 전체 `CareerLoop/artifacts-index.json`
- 전체 `CareerLoop/profile.md`
- Operation 4: Market Benchmark를 실행하라는 지시

### 4. 벤치마크 보고서 제시

analyst의 출력을 사용하여 다음과 같이 렌더링합니다.

```
**벤치마크 보고서** — {오늘 날짜}
데이터 신뢰도: {Preliminary / Directional / Moderate / High} (지원 {n}건, 확정된 결과 {n}건)

파이프라인 전환율
  지원 → 응답:          {user%}  (기준값: {low}–{high}%  ·  {상회/하회/기준 수준})
  응답 → 스크리닝:      {user%}  (기준값: {low}–{high}%  ·  {상회/하회/기준 수준})
  스크리닝 → 면접:      {user%}  (기준값: {low}–{high}%  ·  {상회/하회/기준 수준})
  면접 → 오퍼:          {user%}  (기준값: {low}–{high}%  ·  {상회/하회/기준 수준})

타임라인
  평균 응답 소요일:     {n}일  (기준값: {company size mix} 기준 {low}–{high}일)
  무응답(ghosting) 비율: {user%}  (기준값: {low}–{high}%  ·  {상회/하회/기준 수준})

ATS 점수
  아티팩트 평균 점수:   {n}/100  (경쟁력 기준선: 70+  ·  {상회/하회})
  최저 점수 아티팩트:   {score} — {filename}

시장 맥락
  {사용자 목표에 대한 지역 경쟁력과 직무·레벨별 수급을 1–2문장으로}

개선이 필요한 부분
  {기준값을 가장 크게 밑도는 지표 1–3개를 번호 목록으로, 각각 한 줄 해석 포함}

강점
  {기준값을 웃도는 지표 1–2개 — 잘 되고 있는 부분을 짚어줍니다}
```

지표를 계산할 수 없으면(예: 아직 오퍼가 없어 면접 → 오퍼 비율이 정의되지 않음) `—`를 표시하고 이유를 덧붙입니다.

### 5. 다음 단계 제안

가장 성과가 낮은 지표에 따라:

- 지원 → 응답이 기준값 미만: > "이력서가 ATS를 통과하지 못하거나 JD에 충분히 맞춰지지 않았을 수 있습니다. 가장 성과가 낮은 아티팩트에 대해 `/careerloop:resume-score`를 실행해 보세요."
- 응답 → 스크리닝 또는 스크리닝 → 면접이 기준값 미만: > "서류는 통과하고 있으며, 문제는 퍼널 후반부에 있습니다. `/careerloop:pattern-analysis`를 실행하여 정체된 지원 건에 어떤 ExperienceLibrary 유닛이 쓰였는지 확인해 보세요."
- 전반적으로 타임라인이 느림: > "엔터프라이즈 직무는 긴 타임라인이 흔합니다. `/careerloop:track-application`에서 후속 조치가 예약되어 있는지 확인하세요."
- ATS 점수가 70 미만: > "`/careerloop:ats-optimization`을 실행하여 활성 아티팩트에서 효과가 가장 큰 개선점을 찾아보세요."
