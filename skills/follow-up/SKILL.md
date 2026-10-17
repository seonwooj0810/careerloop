---
name: follow-up
description: >
  회사별 응답 기간(response window) 데이터를 활용해 모든 진행 중인 지원 건의 후속 조치 우선순위를 도출합니다.
  각 지원 건을 기간 내(within window), 임박(approaching), 초과(overdue), 심각(critical)으로 분류하고,
  아직 기록되지 않은 회사의 응답 기간 데이터를 조사해 저장합니다.
  FollowUpBrief 항목을 만들고 writer를 호출해 바로 보낼 수 있는 메시지를 작성합니다.
  커넥터가 있고 사용자가 승인하면 이메일/캘린더 데이터로 브리프를 보강합니다.
  (Surfaces follow-up priorities across all active applications using company-specific
  response window data. Trigger examples: "follow up on my applications",
  "what needs a follow-up", "am I being ghosted", "any overdue applications".)
triggers:
  - "follow up on my applications"
  - "what needs a follow-up"
  - "should I follow up"
  - "what should I follow up on"
  - "follow-up queue"
  - "any follow-ups due"
  - "check my follow-ups"
  - "should I follow up on"
  - "how long has it been since I applied"
  - "am I being ghosted"
  - "any overdue applications"
  - "what's taking so long"
  - "지원 후속 조치"
  - "후속 조치가 필요한 게 뭐야"
  - "후속 연락 해야 할까"
  - "후속 조치 대기열"
  - "기한 지난 지원 있어"
  - "지원한 지 얼마나 됐지"
  - "무응답인가"
  - "왜 이렇게 오래 걸려"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

> **경력 연수 인용 규칙:** 경력·도메인 연수를 말할 때는 ExperienceLibrary의 날짜로 직접 계산한 값을 쓴다. 이력서나 프로필의 표기가 계산값과 다르면 계산값을 쓰고 불일치를 한 줄로 알린다(예: 이력서 "5년" ↔ 날짜상 4년 7개월).

회사별 응답 기간 데이터를 사용해 모든 진행 중인 지원 건의 후속 조치 우선순위를 도출합니다.

## 데이터 파일

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분리(split) 레이아웃을 사용합니다. 읽기·쓰기 전에 반드시 해당 문서를 먼저 읽습니다.

| 파일 | 용도 |
|---|---|
| `{user_dir}/CareerLoop/tracker.json` | 모든 지원 건의 요약 행 — 날짜, 상태, 그리고 분리 레이아웃 필드 `application`, `detail_file`, `contacts_file`, `latest_stage`, `latest_stage_date`, `notes_count`, `stage_count`, `contact_count` |
| `{user_dir}/CareerLoop/applications/<application_id>.json` | 지원 건 하나의 `notes[]`와 `stage_history[]` — 실제로 다루는 지원 건에 대해서만 열기 |
| `{user_dir}/CareerLoop/contacts/<company-slug>.json` | 한 회사의 모든 연락처, 각 항목에 소속 `application` 레이블이 태그됨 |
| `{user_dir}/CareerLoop/company-windows.json` | 사용자별 회사 응답 기간 데이터, 필요할 때 조사 |
| `{user_dir}/CareerLoop/profile.md` | 목표 회사, 산업, 직무 맥락 |

---

## 워크플로

### 1. 진행 중인 지원 건 로드

`tracker.json`을 읽습니다(요약 행만). `status`가 `accepted`, `rejected`, `withdrew`, `ghosted`가 아닌 모든 지원 건을 수집합니다. 이들이 후속 조치 추적이 필요한 지원 건입니다.

진행 중인 각 지원 건의 요약 행에서 `id`, `company`, `role`, `application`, `date_applied`, `status`, `latest_stage`, `latest_stage_date`, `follow_up_date`, `notes_count`, `stage_count`, `contact_count`, `detail_file`, `contacts_file`을 추출합니다.

아직 `detail_file`이나 `contacts_file`은 열지 않습니다. 4단계의 분류에 필요한 정보는 요약 행에 모두 있습니다. `latest_stage`와 `latest_stage_date`가 마지막 `stage_history` 항목을 대신하고, `notes_count` / `stage_count`로 상세 파일을 열 가치가 있는지 알 수 있습니다. 상세 정보는 분류를 통과한 지원 건에 대해서만 로드합니다.

### 2. company-windows.json 로드 또는 초기화

`{user_dir}/CareerLoop/company-windows.json`을 읽습니다. 파일이 없으면 다음과 같이 초기화합니다.

```json
{
  "meta": {
    "created": "{today}",
    "version": "1.0",
    "description": "Company-specific hiring response windows for {user's name} — researched from public sources and stored per session"
  },
  "companies": {},
  "size_tier_fallbacks": {
    "startup": {
      "typical_first_response_days": { "min": 3, "max": 14 },
      "follow_up_after_days": 10,
      "notes": "Startups move fast; silence beyond 2 weeks usually means no."
    },
    "mid_market": {
      "typical_first_response_days": { "min": 7, "max": 21 },
      "follow_up_after_days": 14,
      "notes": "Mid-market timelines vary; a single polite follow-up at 2 weeks is standard."
    },
    "enterprise": {
      "typical_first_response_days": { "min": 14, "max": 42 },
      "follow_up_after_days": 21,
      "notes": "Large companies have multi-layer review queues; 3–6 weeks before initial screen is normal."
    }
  }
}
```

### 3. 누락된 회사 조사

진행 중인 각 지원 건의 회사 중 `company-windows.json.companies`에 **아직 없는** 회사는 지금 조사합니다.

**조사 방법:**

웹 검색으로 해당 회사와 직무 레벨에 대해 지원자들이 보고한 채용 일정을 찾습니다. 다음을 검색합니다.
- `"{company name}" hiring process response time site:glassdoor.com`
- `"{company name}" recruiter response time PM OR director site:linkedin.com`
- `"{company name}" interview process how long Blind OR Reddit`

검색 결과에서 다음을 추출합니다.
- 지원부터 첫 리크루터 연락까지의 일반적인 일수(범위)
- 후속 조치를 하기 적절한 시점(불안해 보일 만큼 이르지도, 소용없을 만큼 늦지도 않은 시점)
- 해당 회사에 특화된 ATS 또는 프로세스 메모(예: Greenhouse 사용, 구조화된 패널 면접, 대기업 특유의 느린 채용으로 알려짐)

결과를 `company-windows.json`에 저장합니다.

```json
"Anthropic": {
  "researched_at": "{today}",
  "typical_first_response_days": { "min": 14, "max": 35 },
  "follow_up_after_days": 21,
  "size_tier": "startup",
  "process_notes": "Uses Greenhouse. High application volume for PM/research roles. Recruiter screen typically 3–5 weeks. Structured multi-round process. Following up via Greenhouse portal or LinkedIn is appropriate at 3 weeks.",
  "sources": ["Glassdoor reviews", "LinkedIn recruiter posts", "Blind threads"]
}
```

웹 검색 결과가 특정 회사에 대해 충분하지 않으면, 해당하는 `size_tier_fallbacks` 항목으로 대체하고 그 사실을 기록합니다.

```json
"Acme Corp": {
  "researched_at": "{today}",
  "typical_first_response_days": null,
  "follow_up_after_days": 14,
  "size_tier": "mid_market",
  "process_notes": "No company-specific data found — using mid-market defaults.",
  "sources": ["size_tier_fallback"]
}
```

진행하기 전에 업데이트된 `company-windows.json`을 저장합니다.

### 4. 각 지원 건 분류

진행 중인 각 지원 건에 대해 다음을 계산합니다.
- `days_elapsed` = 오늘 − `date_applied`
- `last_activity` = 요약 행의 `latest_stage_date` (상세 파일 불필요)
- `days_since_activity` = 오늘 − `last_activity`
- `window_max` = 해당 회사의 `company-windows.json` → `typical_first_response_days.max`

분류 기준:

| 상태 | 조건 |
|---|---|
| `within_window` | `days_elapsed` ≤ `window_max` |
| `approaching` | `days_elapsed` > `window_max`의 75%이고 ≤ `window_max` |
| `overdue` | `days_elapsed` > `window_max`이고 ≤ `window_max`의 1.5배 |
| `critical` | `days_elapsed` > `window_max`의 1.5배 |

`phone_screen` 또는 `interview` 단계의 지원 건은 초과 여부를 지원일 기준 `days_elapsed`가 아니라 `days_since_activity`로 판단합니다. 이 단계는 예상 연락 주기가 더 짧습니다(보통 접점 사이 3~7일).

### 5. 면접 관련 후속 조치 확인

먼저 요약 행에서 후보를 추립니다. `latest_stage`에 "interview"가 포함되고 `latest_stage_date`가 최근 7일 이내인 지원 건입니다. 해당 행에 대해서만 `{user_dir}/CareerLoop/` + `detail_file`(`applications/<application_id>.json`)의 상세 파일을 로드하고, `notes[]`에 감사 메시지가 이미 기록되어 있는지 확인합니다(면접일 이후 날짜이고 "thank-you", "thank you", "follow-up" 중 하나를 포함하는 항목). `notes_count`가 `0`이면 찾을 것이 없으므로 로드를 아예 건너뜁니다. 감사 메시지가 기록되어 있지 않다면:

- 면접이 0~2일 전이면: `thank_you_due`로 표시
- 면접이 3~7일 전이면: `thank_you_overdue`로 표시

### 6. 오퍼 마감일 확인

`offer.deadline`이 설정된 모든 지원 건에 대해 남은 일수를 계산합니다. 남은 기간이 3일 이하이면 `offer_deadline_approaching`으로 표시합니다.

### 7. 후속 조치 리포트 출력

순서: critical → 오퍼 마감일 → 감사 메시지 due/overdue → overdue → approaching → within window.

```
**후속 조치 대기열** — {today's date}

심각 {critical count}건  ·  초과 {overdue count}건  ·  임박 {approaching count}건

---

🔴 심각  ({days_elapsed}일 경과 · 응답 기간 {window_max}일)
  {Company} — {Role}
  지원일 {date_applied}. 마지막 활동: {last_activity_description}.
  {지금 취할 만한 행동 1문장 — 후속 조치, 포기, 또는 둘 다}

🟡 초과  ({days_elapsed}일 · 응답 기간 {window_min}–{window_max}일)
  {Company} — {Role}
  {상황 설명 1문장}

📬 감사 메시지 필요
  {Company} — {Role}  (면접 {n}일 전)

🟢 임박  ({days_elapsed}일 · 응답 기간 종료까지 약 {n}일)
  {Company} — {Role}
  {follow_up_after_days}일 후속 조치 시점: {follow_up_date}

✓ 기간 내
  {Company} — {Role}  ({window_max}일 중 {days_elapsed}일째)
```

대기열이 비어 있으면(진행 중인 모든 지원 건이 기간 내이고 미처리 감사 메시지가 없는 경우):
> "진행 중인 모든 지원 건이 예상 응답 기간 내에 있습니다. 아직 후속 조치할 항목이 없습니다."

### 8. writer를 통한 후속 조치 문구 작성

`overdue` 또는 `critical`로 분류된 각 지원 건(및 `thank_you_due` / `thank_you_overdue`)에 대해 **이 스킬에서 바로 보낼 수 있는 문구를 작성하지 않습니다.**

#### 8a. FollowUpBrief 항목 작성

메시지가 필요한 각 행마다 목록에 객체를 추가합니다.

- `company`, `role`, `application`(요약 행의 `"<company> — <role>"` 레이블)
- `stage_kind`: `post_application` | `thank_you_post_interview` | `offer_nudge` | 기타 (`latest_stage`에서 추론하거나, 이미 로드한 경우 상세 파일의 `stage_history[]`에서 추론)
- `channel`: 기본값은 `email`, 사용자나 메모가 나타내면 `linkedin`
- `recipient_name`, `recipient_title` — 아래 **8a-i**에 따라 연락처를 확인하고, 없으면 `null`로 두며 중립적인 인사 지침을 사용
- `applied_or_event_date`, `days_elapsed`(감사 메시지의 경우 면접일)
- `facts_hooks`: 상세 파일의 `notes[]` / `stage_history[].post_notes`에서 가져온 1~3개 항목 — **지어내지 않음**. 메시지가 실제로 필요한 행에 대해서만 `detail_file`을 로드하고, `notes_count`와 `stage_count`로 활용할 내용이 없음을 알 수 있으면 건너뜀
- `tone`: 직접적이되 아첨하지 않는 어조, 이메일 본문은 3~5문장 목표
- `connector_context`: 커넥터를 사용할 수 있고 사용자가 조회를 **승인한** 경우에 한해 짧은 받은편지함/캘린더 맥락, 그렇지 않으면 `null`

**8a-i. 회사 연락처 파일에서 수신자 확인**

1. 요약 행에서 `contacts_file`을 가져옵니다. 행에 `contacts_file`이 없거나 `contact_count`가 `0`이면 연락처가 없는 것이므로 `recipient_name`과 `recipient_title`을 `null`로 설정하고 넘어갑니다.
2. `{user_dir}/CareerLoop/` + `contacts_file`(`contacts/<company-slug>.json`)을 로드합니다. slug를 추측하지 않습니다 — 행의 `contacts_file`이 기준입니다.
3. 해당 파일의 `contacts[]`에서 `application`이 이 요약 행의 `application` 레이블과 같은 항목만 걸러냅니다. 회사 파일 하나가 그 회사의 모든 지원 건을 담고 있으므로, 걸러지지 않은 항목은 다른 직무의 연락처입니다.
4. `stage_kind`에 가장 잘 맞는 연락처를 고릅니다(지원 후 넛지는 리크루터, 감사 메시지는 면접관이나 채용 매니저). 모호하면 걸러진 첫 번째 항목을 사용합니다.
5. 하나를 고르지 않고 사용자에게 연락처를 보여줄 때는 먼저 `name` 기준으로 중복을 제거합니다. 같은 사람이 그 회사의 지원 건마다 한 번씩 나타날 수 있습니다.

`{user_dir}/CareerLoop/profile.md`와 **`voice-profile.md`**를 읽어 서명 이름과 문체를 확인합니다.

**문체 사전 점검(8b 전에 세션당 한 번):** **`writer`**를 호출할 예정인데 `voice-profile.md`의 **`## User writing samples`** 또는 **`## User writing samples (launch)`** 아래에 붙여넣은 실질적인 글이 없다면, 사용자에게 **LinkedIn 게시글 2~5개** 또는 짧은 글을 요청합니다(또는 중립적인 어조로 **건너뛰기**). 붙여넣은 내용은 `voice-profile.md`에 추가합니다. 샘플이 이미 있거나 사용자가 건너뛰면 그대로 진행합니다.

#### 8b. writer 호출

- 에이전트 이름은 정확히 **`writer`**를 사용하고 모드는 **`follow-up`**으로 지정합니다. 가능하면 모든 **FollowUpBrief** 객체를 한 번의 호출로 전달합니다. 실패하면 한 번 재시도합니다.

#### 8c. 결과 제시

각 지원 건 항목 아래에 **`writer`**의 출력(이메일이면 제목 줄, 본문, 요청 시 LinkedIn 버전)을 보여줍니다.

이메일/캘린더 커넥터가 있으면 **`writer`**를 호출하기 전에 승인된 이전 스레드 맥락으로 브리프를 보강합니다.

#### 8d. 발송 확인 + 자동 추적

모든 메시지를 보여준 뒤 다음과 같이 안내합니다.
> "보내신 메시지마다 'sent [회사명]'이라고 답해 주시면 트래커에 기록해 드리겠습니다."

사용자가 특정 회사에 대한 발송을 확인하면, [references/tracker-schema.md](../../references/tracker-schema.md)에 설명된 다중 파일 트랜잭션을 기록합니다 — 한 파일만 업데이트하고 나머지를 건너뛰는 일은 절대 없어야 합니다.

- `tracker.json`에서 일치하는 요약 행을 찾습니다(`id`로 매칭하고, 이전 브리프에서 온 id라면 `previous_ids`도 확인)
- `{user_dir}/CareerLoop/` + `contacts_file`에서, 메시지를 보낸 연락처(`name`이 일치하고 `application`이 요약 행의 `application` 레이블과 같은 항목)의 `interactions[]`에 추가합니다.
  ```json
  { "date": "YYYY-MM-DD", "type": "email | linkedin", "notes": "Follow-up sent — {stage_kind}" }
  ```
  지정된 연락처가 없으면 연락처를 지어내지 말고 이 단계를 건너뜁니다.
- `{user_dir}/CareerLoop/` + `detail_file`의 `notes[]`에 `{ "date": "YYYY-MM-DD", "text": "Follow-up sent via {channel}: {stage_kind}" }`를 추가한 뒤, 요약 행의 `notes_count`를 새 배열 길이로 설정합니다
- 요약 행의 `follow_up_date`를 오늘 + 해당 회사의 `follow_up_after_days` 기간으로 업데이트합니다(찾을 수 없으면 규모별 대체값 사용)
- 요약 행의 `next_step`을 "Await response to follow-up"으로 업데이트합니다
- 확인 메시지: `기록 완료: {Company}에 후속 조치 발송 — 다음 후속 조치 시점: {new follow_up_date}`

---

## 절대 하지 않는 일

- 조사로 뒷받침된 응답 기간이 지나기 전에 지원 건을 overdue로 표시하지 않습니다 — 일률적인 7일 규칙을 사용하지 않습니다
- 이 스킬에서 **바로 보낼 수 있는** 후속 조치 문장을 작성하지 않습니다 — **FollowUpBrief** 객체만 만들고, 메시지는 **`writer`**가 작성합니다
- 아직 응답 기간 내에 있는 지원 건에 대해서는 후속 조치 문구를 작성하지 않습니다
- 연락처 이름을 지어내지 않습니다 — 등록된 연락처가 없으면 "there"를 사용합니다
- 회사 응답 기간 데이터를 `{user_dir}/CareerLoop/company-windows.json` 외의 위치에 저장하지 않습니다
- 항목이 90일 넘게 오래된 경우가 아니라면, `company-windows.json`에 이미 있는 회사를 다시 조사하지 않습니다
