# 트래커 스키마 v2 — 분리 레이아웃

**지원 데이터를 읽고 쓸 때 기준이 되는 정본 문서입니다.** 지원 기록을 다루는 모든
스킬과 에이전트는 이 파일을 따릅니다.

## 레이아웃

```
{user_dir}/CareerLoop/
├── tracker.json                       요약 행만 보관
├── applications/<application_id>.json 지원 하나의 notes[] + stage_history[]
└── contacts/<company-slug>.json       회사 하나의 모든 연락처
```

`tracker.json`의 `applications[]` 안에는 더 이상 `notes`, `stage_history`, `contacts`가
들어 있지 않습니다. `tracker.json`만 읽어도 상세 파일을 불러오지 않고 전체 파이프라인을
한눈에 볼 수 있습니다. 분리한 이유가 바로 이것입니다. 상세 파일이나 연락처 파일은
실제로 진행 중인 지원에 대해서만 불러옵니다.

## tracker.json

```json
{
  "meta": { "schema": "tracker_v2_split", "last_updated": "YYYY-MM-DD", "layout": { ... } },
  "applications": [ /* 요약 행, 아래 참고 */ ],
  "pipeline_summary": { ... },
  "search_performance": { ... },
  "strategy_signals": { ... }
}
```

### 요약 행(`applications[]`)

기존에 있던 스칼라 필드를 모두 그대로 가지며 — `id`, `company`, `role`, `location`,
`status`, `job_link`, `req_id`, `salary_range`, `date_applied`, `follow_up_date`,
`next_step`, `priority`, `outcome`, `outcome_notes`, `resume_version`, `artifacts` —
여기에 분리 레이아웃용 필드가 추가됩니다.

| 필드 | 타입 | 의미 |
|---|---|---|
| `application` | String | 표시용 레이블. 정확히 `"<company> — <role>"` 형식(em dash, 앞뒤 공백 포함). 연락처 파일에서 조인 값으로 씁니다. |
| `detail_file` | String | `CareerLoop/` 기준 상대 경로. 예: `applications/app-hex-senior-pm.json`. 항상 존재합니다. |
| `contacts_file` | String | `CareerLoop/` 기준 상대 경로. 예: `contacts/hex.json`. 해당 지원에 연락처가 있을 때만 존재합니다. |
| `notes_count` | Int | 상세 파일의 `notes[]` 항목 수. |
| `stage_count` | Int | 상세 파일의 `stage_history[]` 항목 수. |
| `contact_count` | Int | 이 회사의 연락처 중 이 지원에 연결된 연락처 수. |
| `latest_stage` | String | `stage_history`의 마지막 항목의 `stage`. |
| `latest_stage_date` | String | `stage_history`의 마지막 항목의 `date`. |
| `previous_ids` | Array | 이 지원의 이전 id 목록. 이름이 바뀐 경우에만 존재합니다. |

## applications/&lt;application_id&gt;.json

```json
{
  "schema": "application_detail_v1",
  "application_id": "app-hex-senior-pm",
  "application": "Hex — Senior Product Manager",
  "company": "Hex",
  "role": "Senior Product Manager",
  "stage_history": [
    {
      "stage": "recruiter",
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

## contacts/&lt;company-slug&gt;.json

```json
{
  "company": "Hex",
  "contacts": [
    {
      "name": "Carlos Aguilar",
      "application": "Hex — Senior Product Manager",
      "title": "Head of Product",
      "relationship": "hiring_manager",
      "notes": "...",
      "interactions": [
        { "date": "YYYY-MM-DD", "type": "call | email | linkedin | in_person", "notes": "..." }
      ]
    }
  ],
  "contact_count": 4
}
```

회사 파일 하나가 그 회사의 모든 지원을 담당합니다. 각 연락처의 `application` 필드는
특정 지원의 `application` 레이블을 가리킵니다. 같은 회사의 두 지원에 같은 사람이
나오면 지원마다 항목을 하나씩 둡니다. 사용자에게 보여 줄 때는 `name` 기준으로
중복을 제거하세요.

**회사 슬러그:** 회사 이름을 소문자로 바꾸고, 악센트를 제거하고, 영숫자가 아닌 문자가
연속된 구간마다 하이픈 하나로 치환한 뒤, 앞뒤 하이픈을 잘라 냅니다.
`84.51°` → `84-51`, `StrainBrain / Powr Plant` → `strainbrain-powr-plant`,
`Northwestern University — Office for Research` → `northwestern-university-office-for-research`.
이미 있는 회사에 새 슬러그를 만들어 내지 마세요. `CareerLoop/contacts/`를 나열해
이미 있는 파일을 재사용합니다.

## 지원 건 찾기

1. `tracker.json`을 읽고 `id`로 매칭합니다.
2. 매칭되지 않으면 각 행의 `previous_ids`를 확인합니다. `briefs/` 아래의 과거 파일은
   이름이 바뀐 id를 참조하며, 여전히 유효한 조회 대상입니다.
3. 메모나 단계 이력이 실제로 필요할 때만 `detail_file`을 불러옵니다.
4. 연락처가 실제로 필요할 때만 `contacts_file`을 불러온 뒤, `contacts[]`에서
   `application`이 해당 행의 `application`과 같은 항목만 걸러 냅니다.

## 지원 id

형식: `app-<company-slug>-<role-keywords>`. 예: `app-hex-senior-pm`,
`app-anthropic-research-pm-labs`, `app-ocrolus-dir-product-platform`.

UUID, 단순 일련번호(`app-001`), 날짜가 붙은 id는 만들지 않습니다. 같은 회사에서 같은
직무의 기존 지원과 id가 충돌할 때**만** 구분용 접미사를 붙이고, 숫자나 날짜보다
직무에서 따온 구별되는 단어를 우선합니다.

## 쓰기 규칙

지원 데이터를 바꾸는 모든 쓰기는 **다중 파일 트랜잭션**입니다. 한 파일만 쓰고
나머지를 건너뛰어서는 안 됩니다.

**메모 추가**

1. 상세 파일의 `notes[]`에 `{ "date", "text" }`를 추가합니다. 기존 항목을 덮어쓰거나
   순서를 바꾸지 않습니다.
2. 요약 행의 `notes_count`를 새 배열 길이로 설정합니다.

**단계 추가**

1. 상세 파일의 `stage_history[]`에 단계 객체를 추가합니다.
2. 요약 행의 `stage_count`, `latest_stage`, `latest_stage_date`를 설정합니다.
3. 그 단계가 상태 변경을 뜻하면 요약 행의 `status`를 갱신합니다.

**연락처 추가 또는 갱신**

1. 요약 행에서 `contacts_file`을 확인합니다. 행에 없으면 위 규칙대로 슬러그를 만들고,
   파일이 없을 경우 `company`, `contacts: []`, `contact_count: 0`을 담은
   `contacts/<slug>.json`을 만든 뒤 행에 `contacts_file`을 설정합니다.
2. `name`과 `application`이 모두 같은 기존 항목을 찾습니다. 없으면 추가하고,
   있으면 제자리에서 갱신한 뒤 `interactions[]`에 추가합니다.
3. 파일의 `contact_count`와, 해당 지원의 요약 행 `contact_count`를 다시 계산합니다.

**새 지원 만들기**

1. 위 규칙대로 id를 만들고 레이블 `"<company> — <role>"`을 구성합니다.
2. `schema`, `application_id`, `application`, `company`, `role`,
   `stage_history`(현재 단계 항목 하나), `notes`를 담아 `applications/<id>.json`을 씁니다.
3. 스칼라 필드, `application`, `detail_file`, `notes_count`, `stage_count`,
   `latest_stage`, `latest_stage_date`, 그리고 연락처가 있으면
   `contacts_file`/`contact_count`를 담은 요약 행을 `tracker.json` → `applications[]`에
   추가합니다.
4. `pipeline_summary`를 다시 계산합니다.

**지원 이름 변경 또는 삭제**

id와 함께 상세 파일 이름도 바꾸고, 이전 id를 `previous_ids`에 추가하고, 회사
연락처 파일의 `application` 레이블을 모두 갱신합니다.

## 편집 안전 수칙

이 파일들은 JSON을 프로그램으로 불러와 다시 덤프하는 방식으로 편집하고(Python
`json.load` / `json.dump`, `indent=2`, `ensure_ascii=False`), 다시 불러와 재검증합니다.
원본 JSON을 손으로 편집하다가 이 워크스페이스의 파일이 조용히 깨진 적이 있습니다.

다중 파일 쓰기가 끝나면 다음을 확인합니다. 모든 요약 행의 `detail_file`이 실제 파일로
연결되는지, `notes_count` / `stage_count`가 상세 파일의 배열과 일치하는지,
`latest_stage`가 `stage_history`의 마지막 항목과 일치하는지.

## 비상 탈출구

`CareerLoop/_migration/rehydrate.py`는 분리 이전 v1 형태가 필요한 도구를 위해
단일 평면 트래커를 `tracker-rehydrated.json`으로 다시 만듭니다. 읽기 전용 편의 기능이며,
그 출력을 정본으로 취급하거나 거기에 다시 쓰지 마세요.
