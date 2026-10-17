---
name: setup-schedule
description: "CareerLoop 일일 브리프 및/또는 야간 파이프라인 상태 새로 고침을 Cowork 예약 작업으로 생성하거나 업데이트합니다. 일일 브리프는 매일 아침 파이프라인 요약, Gmail 받은편지함 스캔, 후속 조치 알림, 신규 채용 공고 추천을 제공합니다. 선택 사항인 파이프라인 새로 고침은 매일 밤 pipeline-status.html을 다시 생성합니다. /careerloop:setup-schedule로도 호출할 수 있습니다. (Creates or updates the CareerLoop daily brief and/or nightly pipeline status refresh as Cowork scheduled tasks. Trigger examples: \"set up daily brief\", \"schedule my daily brief\", \"automate my morning brief\".)"
triggers:
  - "set up daily brief"
  - "schedule my daily brief"
  - "automate my morning brief"
  - "schedule careerloop"
  - "run my brief every day"
  - "set up the daily schedule"
  - "schedule the daily brief"
  - "create daily brief task"
  - "create scheduled task for daily brief"
  - "/careerloop:setup-schedule"
  - "/setup-schedule"
  - "데일리 브리프 설정"
  - "데일리 브리프 예약"
  - "아침 브리프 자동화"
  - "커리어루프 예약"
  - "매일 브리프 실행해줘"
  - "일일 스케줄 설정"
  - "데일리 브리프 작업 만들어줘"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

CareerLoop 일일 브리프를 Cowork 예약 작업으로 생성하거나 업데이트합니다. 작업이 매일 아침 실행되면 종합 운영 브리프를 전달합니다: 파이프라인 요약, Gmail 받은편지함 스캔(놓친 상태 메일을 잡기 위한 2회 검색 전략), 후속 조치 알림, 그리고 `recommendations.json`에 추가되는 상위 신규 채용 추천.

---

## 1. CareerLoop 설정 확인

`{user_dir}/CareerLoop/profile.md`를 읽습니다.

프로필이 없으면 다음을 출력합니다.
> 일일 스케줄이 설정되지 않았습니다: 먼저 `/careerloop:launch`를 실행해 CareerLoop를 초기화하세요.

그런 다음 중단합니다.

---

## 2. 기존 예약 작업 확인

`mcp__scheduled-tasks__list_scheduled_tasks`를 로드해 호출합니다. 이름이 `careerloop-daily-brief`인 작업과 `careerloop-pipeline-refresh`인 작업(또는 프롬프트가 CareerLoop를 언급하는 작업)을 찾습니다.

**일일 브리프 작업이 발견된 경우:**
- 현재 스케줄과 프롬프트의 한 줄 요약을 표시합니다
- 질문: "이미 일일 브리프가 예약되어 있습니다. 시간을 변경하시겠습니까, 프롬프트를 업데이트하시겠습니까, 아니면 그대로 유지하시겠습니까?"
- 사용자가 업데이트를 원하면: 3~5단계를 따르되, 새로 생성하는 대신 기존 작업의 ID로 `mcp__scheduled-tasks__update_scheduled_task`를 사용합니다
- 사용자가 유지를 원하면: "일일 브리프가 이미 예약되어 있습니다."라고 확인하고, 중단하지 않고 아래의 pipeline-refresh 작업 확인을 계속합니다

**pipeline-refresh 작업이 발견된 경우:** 현재 스케줄을 표시하고 동일한 업데이트/유지 선택지를 제공하며, 사용자가 변경을 원하면 `update_scheduled_task`를 사용합니다.

두 작업이 모두 이미 존재하고 사용자가 둘 다 그대로 유지하기를 원하면, "일일 브리프와 파이프라인 새로 고침이 이미 예약되어 있습니다."라고 확인하고 중단합니다.

---

## 3. 선호 스케줄 확인

질문: "일일 브리프를 몇 시에 받으시겠습니까? 기본값은 **매일 오전 7:00**입니다."

자연어 입력을 받아 cron 표현식으로 변환합니다.

| 입력 | Cron |
|---|---|
| "7am" / "7:00 AM" / 기본값 | `0 7 * * *` |
| "6:30am" | `30 6 * * *` |
| "8am weekdays" | `0 8 * * 1-5` |
| "6am every day" | `0 6 * * *` |

사용자가 기본값을 확인하면 추가 질문 없이 진행합니다.

그런 다음 질문: "파이프라인 상태 대시보드(`pipeline-status.html`)도 매일 밤 자동으로 새로 고치시겠습니까? 기본값은 **매일 오전 2:00**입니다."

답변을 위와 같은 방식으로 cron 표현식으로 변환합니다. 사용자가 거절하면 4b단계와 5단계의 두 번째 작업을 완전히 건너뜁니다 — 일일 브리프만 설정하는 흐름은 영향을 받지 않습니다.

---

## 4. 자체 완결형 작업 프롬프트 작성

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분리(split) 레이아웃을 사용합니다. 읽기·쓰기 전에 반드시 해당 문서를 먼저 읽습니다. 예약 실행은 매번 새 세션에서 시작하므로, 아래 작업 프롬프트에는 그 지침의 사본이 자체적으로 포함되어 있습니다.

`{user_dir}`를 디스크상의 실제 절대 경로(예: `/Users/jane/career`)로 확정합니다.

다음 프롬프트를 작성하되, `{actual_user_dir}`가 나오는 모든 곳에 실제 경로를 대입합니다.

---

```
CareerLoop 일일 브리프를 실행합니다.

## 구직 폴더
{actual_user_dir}

## 데이터 파일 (모두 {actual_user_dir}/CareerLoop/ 아래)
- tracker.json        — 제출한 지원 건당 요약 행 하나: status, outcome,
                        follow_up_date, next_step, 그리고 application, detail_file,
                        contacts_file, notes_count, stage_count, contact_count,
                        latest_stage, latest_stage_date
- applications/<application_id>.json — 지원 건 하나의 stage_history[]와 notes[]
- contacts/<company-slug>.json       — 한 회사의 모든 연락처, 각 항목에
                        소속 application 레이블이 태그됨
- recommendations.json — 지원 전 파이프라인: status 값 considering / pending_decision / pass
- networking.json     — 리크루터 관계 및 LinkedIn 게시글 분석
- artifacts-index.json — 이력서 및 자기소개서 목록
- profile.md          — 목표 직무, 회사, 최소 보상 기준

지원 데이터는 CareerLoop 플러그인의 references/tracker-schema.md에 정의된
분리 레이아웃을 사용합니다. 읽기·쓰기 전에 반드시 해당 문서를 먼저 읽습니다.
tracker.json의 applications[] 안에는 더 이상 notes, stage_history, contacts가 들어
있지 않습니다. 요약 행만으로 브리프를 계산하고, 상세 파일이나 연락처 파일은
필요한 소수의 지원 건에 대해서만 엽니다.

## 1단계 — 아티팩트 정합

브리프를 계산하기 전에, {actual_user_dir}에서 artifacts-index.json에 아직 없는
PDF 또는 DOCX 파일이 있는지 스캔합니다. 발견되면 아티팩트 개수를 계산하기 전에
인덱스를 정합시킵니다(누락된 항목 추가, 오래된 항목 제거).

## 2단계 — Gmail 받은편지함 스캔 (포괄적 — 예외 없이 매일 실행)

지원 관련 업데이트를 놓치지 않도록 Gmail 검색을 두 번 별도로 실행합니다.

**검색 A — 7일 전체 검색:**
Query: newer_than:7d (recruiter OR "your application" OR "thank you for applying" OR
"interview" OR "next steps" OR "we have reviewed" OR "application status" OR
"not moving forward" OR "decided not to" OR "unfortunately" OR "other candidates" OR
"process completed") in:inbox

**검색 B — 30일 회사별 백필:**
tracker.json을 읽고, status가 종료 상태(rejected, withdrawn, expired,
declined_by_candidate, ghosted)가 아닌 요약 행의 회사명을 수집합니다. 다음 쿼리를 구성해 실행합니다.
Query: newer_than:30d ({company_1} OR {company_2} OR ...) (application OR position OR
role OR interview OR recruiter OR "next steps" OR "not moving forward" OR "other
candidates" OR "process completed") in:inbox

두 검색 중 어느 쪽에서든 발견된 각 이메일에 대해:
- 제출 확인(thank you / application received) → ✅ 확인됨으로 기록하고
  tracker.json과 대조
- 다음 단계 진행(면접 초대, 스크리닝 요청, 평가 링크) → 🔔 조치 필요로 표시하고
  눈에 띄게 보고
- 불합격 또는 "process completed" → references/tracker-schema.md의 다중 파일
  트랜잭션을 즉시 기록하며, 한 파일만 업데이트하고 나머지를 오래된 상태로 두지 않음:
    - applications/<application_id>.json(해당 행의 detail_file)에: 날짜를 오늘이
      아니라 이메일의 날짜로 한 stage_history 항목을 추가하고, 이메일 수신일과
      오늘의 발견일을 모두 기록한 notes[] 항목을 추가
    - tracker.json의 해당 요약 행에서: status를 "rejected"로 설정하고, 새 단계에서
      latest_stage와 latest_stage_date를 설정하고, stage_count와 notes_count를
      새 배열 길이로 올리고, follow_up_date를 비움(null로 설정)
    - pipeline_summary를 재계산
- 그 밖의 리크루터 연락 → 검토 대상으로 표시

중요: stage_history 항목의(따라서 latest_stage_date의) 불합격/이벤트 날짜로는
항상 오늘이 아니라 이메일의 날짜를 사용합니다. 발견까지의 시차를 명시적으로
기록합니다(예: "불합격 이메일 수신
2026-04-24, 발견 2026-05-08").

Gmail을 사용할 수 없으면: "Gmail 확인을 건너뜀 — 수동으로 검토하려면 /careerloop:follow-up을
실행하세요."라고 기록합니다.

## 3단계 — 파이프라인 집계

tracker.json 요약 행에서 status별로 집계:
- 지원(Applied) | 전화 스크리닝(Phone screen) | 면접(Interview) | 오퍼(Offer)

recommendations.json에서 status = "considering"인 레코드를 집계:
- 검토 중(Considering) (지원 퍼널 안에 포함하지 않고 별도로 보고)

추가로 다음을 계산:
- 후속 조치 필요: follow_up_date가 오늘이거나 지난 요약 행
- 오늘 미팅: latest_stage_date = 오늘(로컬)이고 latest_stage가 다음 중 하나와
  (대소문자 구분 없이 부분 문자열로) 일치하는 요약 행: interview, recruiter,
  phone screen, phone_screen, hiring manager, hm, hm interview, technical, panel,
  onsite, executive, final round, final interview. stage_count가 0인 행은 건너뜀.
  latest_stage_date가 오늘보다 나중인 행에 대해서만 detail_file을 읽고
  stage_history[]에서 오늘 날짜의 일치 항목을 스캔 — 미래 날짜로 예약된 단계가
  오늘의 항목을 가리기 때문. 이 집계를 위해 모든 상세 파일을 로드하지 않음.

artifacts-index.json에서 type별로 집계: resume | cover_letter

## 4단계 — 신규 채용 공고 검색

/careerloop:search-jobs를 실행합니다. tracker.json이나 recommendations.json에
아직 없는 상위 2개 직무를 찾습니다.

각 신규 추천 건마다 {actual_user_dir}/CareerLoop/recommendations.json에 추가:
- id: 다음 rec-NNN (기존 최대값에서 증가)
- status: "considering"
- company, role, job_link, comp_estimate, location, fit_signals, gaps (검색 결과에서)
- decision_notes: null
- priority, next_step, outcome: "pending"
- artifacts: []

지원 전 직무를 tracker.json에 추가하지 않습니다.

## 5단계 — 출력 형식

CareerLoop — 일일 브리프  [{today}]

파이프라인
  검토 중          {n}  ← recommendations.json, status = "considering"
  지원             {n}
  전화 스크리닝    {n}
  면접             {n}
  오퍼             {n}

후속 조치 필요     {n}
오늘 미팅          {n 또는 "예정 없음"}

아티팩트
  이력서           {n}
  자기소개서       {n}

받은편지함
  {조치 가능한 이메일: 확인 ✅, 면접 요청 🔔, 확인된 불합격,
  기타 연락. 조치 가능한 것이 없으면: "새로운 리크루터 이메일이 없습니다."}

신규 추천
  {recommendations.json에 추가된 상위 2개 신규 직무, 보상 추정치와 적합 신호 포함.
  없으면: "오늘은 조건에 맞는 새 직무가 없습니다."}

그런 다음 가장 긴급한 순으로 최대 3개의 행동 항목을 덧붙입니다. 근거는 다음과 같습니다.
- tracker.json 요약 행의 실제 follow_up_date 값
- 임박한 응답 기간(company-windows.json이 있으면 확인)
- tracker.json 요약 행의 보류 중인 next_step 값

tracker.json에 strategy_signals 키가 없으면 덧붙임:
> job-scout 순위 산정용 전략 신호를 새로 고치려면 /careerloop:suggest-roles를 실행하세요.

지난 7일 이내의 시장 브리프가 없으면 덧붙임:
> 주간 수요 및 대체(displacement) 업데이트를 보려면 /careerloop:market-brief를 실행하세요.

## 제약 조건
- 날짜, 마감일, 시장 데이터를 지어내지 않음
- 데이터 파일이 없으면 오류를 내지 말고 그 사실을 기록하고 해당 섹션을 건너뜀
- Gmail 검색은 읽기 전용 — 이메일을 보내거나, 초안을 작성하거나, 수정하지 않음
- 30일 회사별 백필 검색은 매일 반드시 실행해야 함 — 놓친 불합격 또는 상태
  이메일을 막는 핵심 안전장치임
- 신규 채용 발굴 결과는 recommendations.json에만 기록 — tracker.json에는 절대 기록하지 않음
- 지원 데이터를 변경하는 모든 쓰기는 다중 파일 트랜잭션임: tracker.json
  요약 행과 상세 파일(연락처가 바뀌면 연락처 파일도)
```

---

## 4b. 파이프라인 새로 고침 작업 프롬프트 작성 (사용자가 선택한 경우)

사용자가 3단계에서 야간 파이프라인 새로 고침을 선택했다면, 두 번째로 독립적인 자체 완결형 프롬프트를 작성합니다(4단계와 같은 규칙: 일시적 상태 없음, `{actual_user_dir}`를 완전히 확정).

```
{actual_user_dir}에 대해 CareerLoop pipeline-status 스킬을 실행해, 최신
tracker.json, recommendations.json, passed.json으로부터 pipeline-data.js,
pipeline-status.html, timeline.html을 다시 생성합니다.
```

---

## 5. 예약 작업 생성 (또는 업데이트)

`mcp__scheduled-tasks__create_scheduled_task`를 로드합니다.

다음으로 일일 브리프 작업을 생성합니다.
- `taskName`: `careerloop-daily-brief`
- `description`: `CareerLoop daily brief — pipeline digest, Gmail inbox scan, follow-up alerts, and new job recommendations`
- `prompt`: 4단계에서 작성한 작업 프롬프트(경로를 모두 확정, 플레이스홀더 없음)
- `cronExpression`: 3단계의 cron 표현식

사용자가 파이프라인 새로 고침을 선택했다면, **두 번째 독립 작업**으로 생성합니다.
- `taskName`: `careerloop-pipeline-refresh`
- `description`: `CareerLoop pipeline status refresh — regenerates pipeline-status.html nightly`
- `prompt`: 4b단계에서 작성한 작업 프롬프트
- `cronExpression`: 3단계의 파이프라인 새로 고침 cron 표현식

이 둘은 별개의 예약 작업입니다 — 한쪽의 실패가 다른 쪽을 막아서는 안 되며, 사용자는 각각 독립적으로 거절하거나 나중에 제거할 수 있습니다.

---

## 6. 사용자에게 확인

```
✅ 일일 브리프가 예약되었습니다 — 매일 {time}에 실행됩니다.

  스킬:   careerloop:daily-schedule
  폴더:   {user_dir}
  작업:   careerloop-daily-brief
```

파이프라인 새로 고침도 함께 예약했다면 다음을 덧붙입니다.

```
✅ 파이프라인 상태 새로 고침이 예약되었습니다 — 매일 {time}에 실행됩니다.

  스킬:   careerloop:pipeline-status
  폴더:   {user_dir}
  작업:   careerloop-pipeline-refresh
```

그런 다음:

```
스케줄이나 프롬프트를 조정하려면 "reschedule my daily brief" /
"reschedule my pipeline refresh"라고 말하거나(한국어로 "일일 브리프 다시 예약해 줘" /
"파이프라인 새로 고침 다시 예약해 줘"도 가능), /careerloop:setup-schedule을 다시 실행하세요.
```

---

## 가드레일

- 일치하는 작업이 이미 있으면 항상 `create`가 아니라 `update_scheduled_task`를 사용합니다 — 중복을 방지합니다
- 각 프롬프트는 완전히 자체 완결형이어야 합니다: "현재 세션", "위의 맥락", 일시적 상태를 참조하지 않습니다
- 각 프롬프트의 경로는 절대 경로로 완전히 확정되어야 합니다 — 저장하기 전에 `{user_dir}`를 반드시 치환해야 합니다
- Gmail 검색은 읽기 전용입니다. 일일 브리프 작업 프롬프트에 전송/초안/삭제 지침을 절대 포함하지 않습니다
- 일일 브리프와 파이프라인 새로 고침은 독립적인 예약 작업입니다 — 2단계에서 항상 각각 따로 확인하고 관리합니다
