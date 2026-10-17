---
name: track-application
description: >
  tracker.json에 새 지원을 기록하거나 기존 지원을 업데이트합니다. 단계 이력, 연락처 관리, 면접 기록,
  오퍼 정보 수집, 결과 기록, 후속 조치 일정 관리까지 대화형 추적을 모두 처리합니다. 어떤 지원 이벤트든
  대화로 받아들입니다. /careerloop:track-application으로도 호출할 수 있습니다.
  예: "I just applied to", "I got an interview", "I got rejected", "I got an offer",
  "add to my tracker", "update my application", "지원했어요", "면접 봤어요", "불합격했어요", "오퍼 받았어요".
triggers:
  - "/track-application"
  - "I just applied to"
  - "I applied to"
  - "I submitted an application"
  - "log an application"
  - "track this application"
  - "add to my tracker"
  - "I got a callback"
  - "I got a call from"
  - "they reached out"
  - "I have an interview"
  - "I got an interview"
  - "I scheduled an interview"
  - "I had an interview"
  - "I met with"
  - "I spoke with the recruiter"
  - "I met the hiring manager"
  - "I got rejected"
  - "they rejected me"
  - "they ghosted me"
  - "I withdrew"
  - "I'm withdrawing"
  - "I got an offer"
  - "they made an offer"
  - "I declined the offer"
  - "I accepted the offer"
  - "I accepted"
  - "negotiating an offer"
  - "update my application"
  - "update the status"
  - "add a contact"
  - "log a contact"
  - "I sent the message"
  - "I sent the outreach"
  - "I sent my follow-up"
  - "I reached out to"
  - "I messaged"
  - "I emailed them"
  - "sent it"
  - "outreach sent"
  - "지원했어요"
  - "지원서를 제출했어요"
  - "지원 기록해줘"
  - "트래커에 추가해줘"
  - "면접 일정이 잡혔어요"
  - "면접 봤어요"
  - "불합격했어요"
  - "서류 탈락했어요"
  - "오퍼 받았어요"
  - "오퍼를 수락했어요"
  - "오퍼를 거절했어요"
  - "지원 현황 업데이트해줘"
  - "연락처 추가해줘"
  - "메시지 보냈어요"
  - "후속 메시지 보냈어요"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

지원 기록을 남기거나 업데이트합니다. 사용자에게 무언가를 묻기 전에 먼저 사용자가 말한 내용에서 최대한 많은 정보를 추출합니다.

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분리 레이아웃을 사용합니다. 읽거나 쓰기 전에 반드시 먼저 읽으세요.

## 지원 레코드 스키마

하나의 지원은 세 개의 파일에 걸쳐 저장됩니다. `notes`, `stage_history`, `contacts`는 절대 `tracker.json` 행 안에 넣지 않습니다.

**요약 행** — `tracker.json` → `applications[]`:

```json
{
  "id": "app-<company-slug>-<role-keywords>",
  "application": "<company> — <role>",
  "company": "...",
  "role": "...",
  "job_link": "...",
  "req_id": null,
  "salary_range": "...",
  "location": "...",
  "resume_version": null,
  "date_applied": "YYYY-MM-DD",
  "status": "applied | phone_screen | interview | offer | accepted | rejected | withdrew | ghosted",
  "detail_file": "applications/app-<company-slug>-<role-keywords>.json",
  "contacts_file": "contacts/<company-slug>.json",
  "notes_count": 0,
  "stage_count": 1,
  "contact_count": 0,
  "latest_stage": "applied",
  "latest_stage_date": "YYYY-MM-DD",
  "follow_up_date": "YYYY-MM-DD",
  "next_step": "...",
  "priority": "high | medium | low | null",
  "referral": { "name": "...", "relationship": "colleague | friend | recruiter | other" },
  "offer": {
    "base": "...",
    "bonus": "...",
    "equity": "...",
    "benefits_notes": "...",
    "deadline": "YYYY-MM-DD",
    "decision": null
  },
  "outcome": "pending | hired | rejected | withdrew",
  "outcome_notes": "...",
  "artifacts": []
}
```

**상세 파일** — `CareerLoop/applications/<application_id>.json`, 지원당 하나:

```json
{
  "schema": "application_detail_v1",
  "application_id": "app-<company-slug>-<role-keywords>",
  "application": "<company> — <role>",
  "company": "...",
  "role": "...",
  "stage_history": [
    {
      "stage": "...",
      "date": "YYYY-MM-DD",
      "notes": "...",
      "interview_type": "recruiter | hiring_manager | technical | panel | executive | final | null",
      "interviewers": [],
      "post_notes": null
    }
  ],
  "notes": [
    { "date": "YYYY-MM-DD", "text": "..." }
  ]
}
```

**연락처 파일** — `CareerLoop/contacts/<company-slug>.json`, 기업당 하나이며 해당 기업의 모든 지원이 공유합니다.

```json
{
  "company": "...",
  "contacts": [
    {
      "name": "...",
      "application": "<company> — <role>",
      "title": "...",
      "email": null,
      "linkedin": null,
      "relationship": "recruiter | hiring_manager | referral | internal_contact | other",
      "notes": "...",
      "interactions": [
        { "date": "YYYY-MM-DD", "type": "call | email | linkedin | in_person", "notes": "..." }
      ]
    }
  ],
  "contact_count": 0
}
```

`offer`와 `referral`은 관련 데이터가 있을 때만 새 레코드에 포함하고, 없으면 생략합니다. `outcome`은 모든 새 레코드에서 기본값이 `"pending"`입니다. `contacts_file`과 `contact_count`는 지원에 연락처가 생기기 전까지 생략합니다. `previous_ids`는 이름 변경(rename) 후에만 행에 나타납니다.

이 파일들은 모두 JSON을 프로그램으로 로드한 뒤 다시 덤프하는 방식(`json.load` / `json.dump`, `indent=2`, `ensure_ascii=False`)으로 수정하고, 다시 로드해 검증합니다. 원본 JSON을 손으로 편집하다 파일이 손상된 적이 있습니다.

---

## 워크플로

### 1. 이벤트 분류

`tracker.json`을 읽고 이벤트를 `id`로 요약 행과 매칭하며, 일치하는 `id`가 없으면 `previous_ids`로 매칭합니다. 메모나 단계 이력이 관련될 때만 해당 행의 `detail_file`을 불러오고, 연락처가 관련될 때만 `contacts_file`을 불러옵니다. 사용자가 한 말에 따라 어떤 작업이 해당되는지 판단합니다.

| 이벤트 유형 | 연결할 곳 |
|---|---|
| 사용자가 **고려 중**이지만 아직 지원하지 않은 직무 | `tracker.json`이 아니라 `recommendations.json`(`recommendations[]`)에 기록 — 섹션 3a 참조 |
| 새 지원(제출 완료) | 섹션 3 — 레코드 작성 |
| 상태 변경(콜백, 스크리닝, 면접, 불합격) | 섹션 3 — 레코드 작성 |
| 해당 기업의 인물 언급 | 섹션 4 — 연락처 관리 |
| 면접 예정 또는 면접 후 복기 | 섹션 5 — 면접 기록 |
| 오퍼 수령 또는 협상 진행 중 | 섹션 6 — 오퍼 정보 수집 |
| 최종 결과(합격, 불합격, 철회, 무응답) | 섹션 7 — 결과 기록 |
| 아웃리치 또는 후속 메시지 발송 | 섹션 4 — 연락처 관리(상호작용으로 기록) + `follow_up_date`와 `next_step` 업데이트 |

사용자의 메시지 하나가 여러 섹션을 동시에 트리거할 수 있습니다. 예를 들어 "Acme의 Sarah Chen(리크루터)과 면접을 봤어요"는 면접 기록과 연락처 관리를 모두 트리거합니다. 해당하는 것을 모두 처리합니다.

**새 지원의 중복 확인** — 사용자가 새 지원을 기록하려는데 같은 기업의 항목이 이미 있으면, 또 하나를 만들기 전에 확인합니다.
> "{Company}의 {Role} 직무에 이미 지원 기록이 있습니다. 새로운 직무인가요, 아니면 그 지원에 대한 업데이트인가요?"

---

### 2. 대화 입력에서 필드 추출

| 필드 | 찾을 내용 |
|---|---|
| `company` | 기업명 |
| `role` | 직무명 |
| `job_link` | 제공된 경우 URL |
| `salary_range` | 보상 관련 언급 |
| `location` | 도시, 주, 원격/하이브리드 |
| `date_applied` | "오늘", "어제", 특정 날짜 — YYYY-MM-DD로 변환 |
| `status` | 단계 키워드 |
| `follow_up_date` | "~까지 후속 연락", "다시 확인", "마감" — YYYY-MM-DD로 변환 |
| `referral` | "추천받음", "지인을 통해" — 이름과 관계를 기록 |
| `notes` | 인상, 맥락, 직무를 알게 된 경로, 리크루터 정보 |
| `next_step` | 언급된 다음 행동 |
| `priority` | 명시적인 긴급도나 관심 수준 |

새 레코드의 필수 항목: `company`, `role`, `status`. 누락된 경우 `company`와 `role`만 묻습니다. 선택 필드는 묻지 않습니다.

---

### 3a. 지원 전 직무(고려 중)

사용자가 관심 있는 직무를 언급했지만 **아직 지원하지 않았다면**, `tracker.json` 대신 `{user_dir}/CareerLoop/recommendations.json`에 기록합니다.

- `recommendations[]`에 새 항목을 추가합니다: `id`(다음 `rec-NNN`), `company`, `role`, `job_link`, `comp_estimate`, `location`, `status: "considering"`, `priority`, `next_step`, `notes`, `fit_signals`(가능하면 사용자 맥락에서), `gaps`(언급된 경우), `decision_notes: null`, `outcome: "pending"`, `artifacts: []`.
- `applications[]`에 추가하거나 `pipeline_summary`를 업데이트하지 **않습니다**. 지원 전 직무는 별도로 추적합니다.
- 사용자가 나중에 지원했다고 말하면 레코드를 이동합니다. `recommendations[]`에서 제거하고, 섹션 3의 전체 새 지원 쓰기 절차(`app-<company-slug>-<role-keywords>` id 생성, 상세 파일 작성, 요약 행 추가)를 `status: "applied"`로 실행한 뒤 `pipeline_summary`를 업데이트합니다.
- 사용자가 `recommendations.json` 항목을 보류/거절한다고 말하면(지원하지 않고 더 이상 진행하지 않음), 레코드를 이동합니다. `recommendations[]`에서 제거하고 `{user_dir}/CareerLoop/passed.json` → `passed[]`에 추가하며, `status: "pass"`, `date_passed`(사용자가 다른 날짜를 주지 않으면 오늘), 이유가 주어졌다면 `decision_notes`에 그 이유를 설정합니다(없으면 `null`로 둡니다). 보류한 직무는 `tracker.json`이나 `pipeline_summary`에 추가하지 않습니다.

---

### 3. 레코드 작성

**새 지원** — 여러 파일에 걸친 트랜잭션입니다. 모든 부분을 수행하거나 아무것도 하지 않습니다.

1. **`id` 생성**: `app-<company-slug>-<role-keywords>` 형식으로 만듭니다. 예: `app-hex-senior-pm`, `app-ocrolus-dir-product-platform`. 기업명 슬러그는 소문자로 바꾸고, 악센트를 제거하고, 영숫자가 아닌 문자의 연속을 하이픈 하나로 치환하고, 앞뒤 하이픈을 제거해 만듭니다. 직무명에서 키워드 2~4개를 고릅니다. **UUID, `app-NNN`, 날짜 접미사는 절대 만들지 않습니다.** 같은 기업의 같은 직무로 기존 지원과 id가 충돌할 때만 직무에서 구분되는 단어를 추가합니다. 숫자나 날짜가 아니라 구분되는 단어여야 합니다.
2. **`application` 라벨 생성**: 정확히 `"<company> — <role>"`로 만듭니다(em dash, 앞뒤 공백 포함). 연락처가 다시 가리키는 조인 값입니다.
3. **`CareerLoop/applications/<id>.json` 작성**: `schema: "application_detail_v1"`, `application_id`, `application`, `company`, `role`, 현재 단계 항목 하나가 담긴 `stage_history`, 그리고 `notes`를 포함합니다. `notes`는 사용자가 맥락을 제공했다면 항목 하나가 든 배열, 아니면 빈 배열입니다.
4. **요약 행 추가**: `tracker.json` → `applications[]`에 스칼라 값과 함께 `application`, `detail_file: "applications/<id>.json"`, `notes_count`, `stage_count`, `latest_stage`, `latest_stage_date`(상세 파일과 일치)를 추가합니다. 연락처를 기록한 경우에만 `contacts_file`과 `contact_count`를 추가합니다(섹션 4).
5. `outcome`을 `"pending"`으로 설정합니다.
6. 기업 회신 기간 정보(아래 참조)를 사용해 `follow_up_date`를 설정합니다. 사용자가 명시적으로 날짜를 말한 경우에만 사용자가 준 날짜를 사용합니다.

**새 지원의 follow_up_date 설정:**

`{user_dir}/CareerLoop/company-windows.json`을 읽고 기업을 찾습니다.
- 찾은 경우: `follow_up_date` = `date_applied` + `follow_up_after_days`
- 찾지 못한 경우: 웹 검색으로 기업을 조사하고(`follow-up` 스킬과 같은 방법 — Glassdoor, LinkedIn, Blind) 날짜를 설정하기 전에 결과를 `company-windows.json`에 저장합니다. 조사에서 쓸 만한 데이터가 나오지 않으면 규모 등급별 기본값(스타트업: +10일, 중견: +14일, 대기업: +21일)으로 대체합니다.

날짜를 설정한 뒤에는 확인 출력에 그 내용을 알립니다.

**상태 업데이트** — 일치하는 요약 행을 찾아 `detail_file`을 불러온 뒤:
- 상세 파일의 `stage_history[]`에 새 항목을 추가합니다. 기존 항목을 덮어쓰거나 순서를 바꾸지 않습니다.
- 사용자가 새로운 정보를 제공했다면 상세 파일의 `notes[]`에 새 항목을 추가합니다. 기존 메모 항목을 덮어쓰지 않습니다.
- 요약 행에서: `status`를 업데이트하고, `stage_count`를 새 `stage_history` 길이로 설정하고, 방금 추가한 항목으로 `latest_stage`와 `latest_stage_date`를 설정하고, 메모를 추가했다면 `notes_count`를 새 `notes` 길이로 설정합니다.
- 언급된 경우 행의 `follow_up_date`와 `next_step`을 업데이트합니다.

**쓰기를 한 뒤에는 항상** `tracker.json`의 `pipeline_summary` 집계를 다시 계산해 업데이트합니다. `pipeline_summary`는 제출된 지원(`applications[]`)만 반영하며, `recommendations.json`의 지원 전 직무는 여기서 집계하지 않습니다.

**턴을 끝내기 전에 확인:** 모든 요약 행의 `detail_file`이 실제로 존재하는지, `notes_count`와 `stage_count`가 상세 파일의 배열과 일치하는지, `latest_stage` / `latest_stage_date`가 마지막 `stage_history` 항목과 일치하는지 확인합니다.

**쓰기 직후** 턴을 끝내기 전에 **`application-update`** 스킬 워크플로(job-scout / pattern-analysis 알림을 위한 안내 갱신)를 실행합니다.

---

### 4. 연락처 관리

연락처는 `CareerLoop/contacts/<company-slug>.json`에 저장하며, 기업당 파일 하나를 해당 기업의 모든 지원이 공유합니다. 사용자가 해당 기업의 인물을 언급하면:

**먼저 파일을 확정합니다** — 요약 행에서 `contacts_file`을 가져옵니다. 행에 없으면 `CareerLoop/contacts/`를 나열해 이 기업에 이미 있는 파일을 재사용합니다. 이미 슬러그가 있는 기업에 두 번째 슬러그를 만들지 않습니다. 파일이 없으면 슬러그를 만들고(소문자, 악센트 제거, 영숫자가 아닌 문자의 연속을 하이픈 하나로 합침, 앞뒤 하이픈 제거) `contacts/<slug>.json`을 `{ "company": "...", "contacts": [], "contact_count": 0 }`로 생성합니다. 그런 다음 요약 행에 `contacts_file`을 설정합니다.

**새 연락처 추가** — 해당 파일의 `contacts[]`에서 같은 `name` **그리고** 같은 `application` 라벨을 가진 항목을 찾습니다. 없으면 추가합니다.

```json
{
  "name": "...",
  "application": "<company> — <role>",
  "title": "...",
  "email": null,
  "linkedin": null,
  "relationship": "recruiter | hiring_manager | referral | internal_contact | other",
  "notes": "...",
  "interactions": []
}
```

`application`은 요약 행의 `application` 라벨과 정확히 같아야 합니다. 한 기업의 두 지원에 관여하는 같은 사람은 지원마다 항목 하나씩 갖습니다.

**상호작용 기록** — 사용자가 알려진 연락처와의 대화, 통화, 이메일, 미팅을 언급하면 해당 항목을 그 자리에서 업데이트하고 `interactions[]`에 추가합니다.

```json
{ "date": "YYYY-MM-DD", "type": "call | email | linkedin | in_person", "notes": "..." }
```

**연락처를 쓴 뒤에는 항상** 연락처 파일의 `contact_count`(파일 내 전체 항목 수)와 요약 행의 `contact_count`(`application`이 해당 행과 일치하는 항목 수)를 다시 계산합니다.

**추천(Referral)** — 사용자가 추천을 받아 지원했다면 `tracker.json`의 요약 행에 추가합니다.

```json
"referral": { "name": "...", "relationship": "colleague | friend | recruiter | other" }
```

사용자가 제공하지 않는 한 이메일이나 LinkedIn을 묻지 않습니다.

---

### 5. 면접 기록

**예정된 면접 등록** — 상세 파일의 `stage_history[]`에 추가합니다.

```json
{
  "stage": "interview",
  "date": "YYYY-MM-DD",
  "notes": "...",
  "interview_type": "recruiter | hiring_manager | technical | panel | executive | final",
  "interviewers": ["Name — Title", "..."],
  "post_notes": null
}
```

그런 다음 요약 행에서: `stage_count`를 새 배열 길이로 설정하고, 이 항목으로 `latest_stage`와 `latest_stage_date`를 설정하며, 해당 단계로 상태가 바뀌면 `status`를 업데이트합니다. 면접이 예정되어 있다면 `follow_up_date`를 면접 날짜로 설정합니다.

**면접 후 복기** — 사용자가 면접이 어땠는지 알려주면 상세 파일을 열어 일치하는 `stage_history` 항목을 찾아 `post_notes`를 채웁니다. 같은 파일의 `notes[]`에 추가합니다.

```json
{ "date": "YYYY-MM-DD", "text": "Post-interview: {what the user shared}" }
```

그런 다음 요약 행의 `notes_count`를 새 `notes` 길이로 설정합니다.

사용자가 해당 기업의 연락처 파일에 없는 면접관 이름이나 직함을 언급하면, 섹션 4를 통해 추가합니다. `application` 라벨과 `contact_count` 관리도 포함합니다.

면접이 끝난 뒤 후속 메시지를 아직 보내지 않았다면, 요약 행의 `follow_up_date`를 2일 뒤로, `next_step`을 "Send thank-you note"로 설정합니다.

---

### 6. 오퍼 정보 수집

사용자가 오퍼를 받았다고 알리면:

1. 상세 파일의 `stage_history[]`에 오퍼 단계를 추가하고, 요약 행에서 `status`를 `"offer"`로 설정하고 `stage_count`, `latest_stage`, `latest_stage_date`를 갱신합니다.
2. 사용자가 말한 내용에서 오퍼 세부 정보를 추출해 요약 행에 `offer` 객체를 기록합니다.

```json
"offer": {
  "base": "...",
  "bonus": "...",
  "equity": "...",
  "benefits_notes": "...",
  "deadline": "YYYY-MM-DD",
  "decision": null
}
```

3. 오퍼 마감일이 언급되었다면 `follow_up_date`를 그 마감일로 설정합니다.
4. 사용자가 공유한 내용만 기록합니다. 모든 필드를 캐묻지 않습니다.

기록 후 다음과 같이 묻습니다.
> "이 직무와 지역의 시장 연봉 데이터를 가져와서 오퍼와 비교해 드릴까요?"

---

### 7. 결과 기록

사용자가 최종 결과를 알리면:

| 사용자가 한 말 | `status` | `outcome` |
|---|---|---|
| 수락함, 취업함 | `accepted` | `hired` |
| 불합격 | `rejected` | `rejected` |
| 철회함, 중도 포기 | `withdrew` | `withdrew` |
| 무응답(ghosted), 회신 없음 | `ghosted` | `rejected` |

레코드를 업데이트합니다. 상세 파일을 먼저, 그다음 요약 행입니다.
- 상세 파일의 `stage_history[]`에 최종 항목을 추가합니다.
- 사용자가 남길 가치가 있는 맥락을 줬다면 상세 파일에 `notes[]` 항목을 추가합니다.
- 요약 행에서: `status`와 `outcome`을 설정하고, `outcome_notes`에 사용자가 준 이유나 맥락을 설정하고, `stage_count`, `latest_stage`, `latest_stage_date`, `notes_count`를 갱신합니다.
- `pipeline_summary`를 업데이트합니다. 진행 중 집계에서 제외합니다.

결과가 `"hired"`이면:
> "축하드립니다. 이 지원을 수락(accepted)으로 표시하고 진행 중인 다른 지원들을 정리할까요?"

결과가 `"rejected"`이고 이유가 주어졌다면:
> "기록했습니다. 다음에 패턴 분석을 실행할 때 analyst가 이 내용을 반영합니다."

**패턴 분석 알림** — 종료 결과를 기록한 뒤, `tracker.json`에서 `outcome`이 `"pending"`이 아닌 지원의 총 수를 셉니다. 그 수가 정확히 5, 10, 15이거나 그 이후 10의 배수이면 다음을 덧붙입니다.
> "이제 확정된 결과가 {count}건이라 패턴 분석을 실행하기에 충분합니다. `/pattern-analysis`를 실행하면 지금까지 효과가 있었던 것을 기준으로 ExperienceLibrary 가중치와 job-scout 점수를 업데이트합니다."

---

### 8. 아티팩트 연결

사용자가 이 지원에 사용한 이력서나 자기소개서를 언급하면, `artifacts-index.json`에서 파일명으로 일치하는 항목을 찾아 `tracker.json`의 요약 행 `artifacts[]`에 연결합니다.

---

### 9. 확인

```
기록 완료: {Company} — {Role}
상태: {status}
{follow_up_date가 설정된 경우: "후속 조치: {date}"}
{연락처 추가 또는 상호작용 기록, 해당되면 한 줄}
```

확인 메시지는 3~4줄로 유지합니다. 모든 필드를 다시 나열하지 않습니다.
