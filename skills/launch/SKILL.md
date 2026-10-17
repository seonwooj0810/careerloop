---
name: launch
description: >
  CareerLoop로 구직 활동을 시작합니다. 설정을 위한 단일 진입점입니다. 구직 폴더를 설정하고, 기존 문서에서 사용자 프로필, ExperienceLibrary, 지원 트래커를 구성하며, 실시간 공고 검색을 위한 Indeed MCP 커넥터(브라우저 OAuth), 연봉 데이터용 선택적 Apify, 아웃리치와 미팅 컨텍스트용 선택적 Gmail / Microsoft 365 받은편지함 및 Google Calendar 커넥터(OAuth), 선택적 LinkedIn 게시물 분석, 해당되는 경우 선택적 클라우드 스토리지 커넥터(Google Drive, OneDrive, Dropbox)까지 안내합니다. Customize 버튼이 필요 없으며 이 명령 하나로 모든 설정을 진행합니다. (Launch your job search with CareerLoop — trigger phrases: "launch career", "launch careerloop", "set up careerloop", "configure careerloop", "get started with careerloop".)
triggers:
  - "/careerloop:launch"
  - "/launch"
  - "launch career"
  - "launch careerloop"
  - "begin my job search with careerloop"
  - "set up career"
  - "set up careerloop"
  - "configure careerloop"
  - "get started with careerloop"
  - "커리어 시작"
  - "커리어루프 시작"
  - "커리어루프로 구직 시작"
  - "커리어루프 설정"
  - "커리어루프 처음 설정"
  - "구직 워크스페이스 설정해줘"
---

플러그인을 설치한 뒤 이 스킬을 사용합니다. CareerLoop를 **시작(launch)**하는 방법이며, 구직 폴더 등록, 기존 문서 읽기, 프로필과 ExperienceLibrary 구성, 연동 설정을 진행합니다(이전과 동일한 설정 흐름이며, 구직 시작이라는 관점으로 구성했습니다).

작업 디렉터리(또는 해당 하위 디렉터리)를 사용자의 구직 디렉터리로 설정하며, 이를 `{user_dir}`라고 부릅니다. 이 플러그인이 생성하는 모든 데이터(프로필, ExperienceLibrary, 트래커, 생성된 아티팩트)는 사용자의 원본 문서와 함께 `{user_dir}` 폴더의 하위 디렉터리에 저장됩니다.

**연동(Indeed, Apify, LinkedIn, Gmail, Microsoft 365, Google Calendar):** [CONNECTORS.md](CONNECTORS.md)를 따릅니다. **현재 세션에 아직 연결되지 않은 서비스에 대해서만 안내합니다**(호스트 도구가 없거나 사용자가 문제를 알려 온 경우). 도구가 이미 있으면 **간단히 확인만** 하면 충분하며, 해당 서비스에 대해 설정, OAuth, 브라우저 접근 관련 질문을 **하지 않습니다**.

## 워크플로

### 커넥터 패턴 (3~7단계에 적용)

| 단계 | 할 일 |
| --- | --- |
| **1 — 탐색** | **이 채팅**에서 해당 연동의 도구를 확인합니다. **연결되어 있으면**(도구가 있으면) 간단히 확인하고 해당 연동의 이후 단계는 **건너뜁니다**. |
| **2 — 설정** | **연결되지 않은 경우에만:** 설정할지 **묻고**, [CONNECTORS.md](CONNECTORS.md)를 안내합니다. **사용자가 직접** **Connectors** 설정과 OAuth/토큰 절차를 완료합니다. Chrome/컴퓨터 사용으로 OAuth를 자동화하는 일은 **절대 하지 않습니다**. |
| **3 — 브라우저 접근** | **MCP로 연결되지 않은 경우**이거나 흐름이 **브라우저 전용**인 경우(예: **LinkedIn** 분석)에만 진행합니다. MCP 도구가 이미 작동하는 **Indeed** / **Apify** / 받은편지함 / **캘린더**에 대해서는 묻지 **않습니다**. |

연동마다 **1 → 2 → (필요할 때만 3)** 순서로 적용합니다. 1단계가 이미 성공했다면 2~3단계는 **생략**합니다.

### 1. 구직 디렉터리 확인

**사용자가 디렉터리 경로를 제공한 경우**: 그 경로를 사용합니다. 사용자에게 `{user_dir}` 경로를 알려 줍니다.

**경로가 제공되지 않은 경우**: 다음과 같이 묻습니다.
> "CareerLoop가 구직 활동에 사용할 폴더는 어디인가요? 이력서와 자기소개서가 있는 폴더이며, 제가 생성하는 모든 결과물도 이곳에 저장합니다. 새 채팅을 시작하고 입력창의 "+" 아이콘을 눌러 해당 폴더를 이 채팅에 추가해 주세요."

### 2. 기존 데이터 파일 확인

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분할 레이아웃을 사용합니다. 읽기나 쓰기 전에 반드시 이 문서를 먼저 읽습니다. 이 스킬은 최초 실행 시 트래커를 처음부터 구성하므로 반드시 분할 레이아웃, 즉 요약 행으로 구성된 `tracker.json`과 `applications/`, `contacts/` 디렉터리를 만들어야 하며, 단일 구조(monolithic)의 트래커는 절대 만들지 않습니다.

`{user_dir}`를 확인한 뒤 핵심 데이터 파일이 각각 존재하는지 확인합니다. 각 파일은 독립적으로 처리합니다.

#### 확인할 파일

| 파일 | 경로 |
|---|---|
| 프로필 | `{user_dir}/CareerLoop/profile.md` |
| ExperienceLibrary | `{user_dir}/CareerLoop/ExperienceLibrary.json` |
| 트래커(요약 행) | `{user_dir}/CareerLoop/tracker.json` |
| 지원 상세 | `{user_dir}/CareerLoop/applications/{application_id}.json` |
| 회사별 연락처 | `{user_dir}/CareerLoop/contacts/{company-slug}.json` |
| 아티팩트 인덱스 | `{user_dir}/CareerLoop/artifacts-index.json` |
| 스토리 코퍼스 | `{user_dir}/CareerLoop/StoryCorpus.json` |
| 네트워킹 | `{user_dir}/CareerLoop/networking.json` |

#### 파일별 두 가지 경로

**파일이 존재하는 경우** — 형식과 내용을 검증합니다.

- **`CareerLoop/profile.md`**: 목표 직무, 최저 보상 기준, 지역, 핵심 차별화 요소 섹션이 있어야 합니다. 누락되었거나 비어 있는 섹션이 있으면 다른 가용한 출처(ExperienceLibrary, `{user_dir}`의 이력서 문서)에서 채웁니다. 발견된 공백과 해결 방법을 사용자에게 알립니다.
- **`CareerLoop/profile.md`**: 목표 직무, 최저 보상 기준, 지역, 핵심 차별화 요소 섹션이 있어야 합니다. 누락되었거나 비어 있는 섹션이 있으면 다른 가용한 출처(ExperienceLibrary, `{user_dir}`의 이력서 문서)에서 채웁니다. 또한 다음 보조 섹션이 존재하거나, 비어 있더라도 채울 준비가 된 상태여야 합니다.
  - `## Employment Context`
  - `## Certifications & Credentials`
  누락되었거나 비어 있으면 문서에서 확인해 채운 뒤, 사용자에게 누락된 세부 정보를 확인하거나 추가해 달라고 요청합니다.

- **`CareerLoop/ExperienceLibrary.json`**: `meta` 객체와 비어 있지 않은 `units` 배열을 가진 유효한 JSON이어야 합니다. 각 unit에는 `id`, `type`, `company`(또는 `institution`), `title`, `dates`가 있어야 합니다. 필수 필드가 없는 unit은 표시하고 사용자에게 입력을 요청합니다. 배열이 비어 있으면 파일이 없는 것으로 간주하고 다시 구성합니다.

- **`CareerLoop/tracker.json`**: `meta`, `applications` 배열, `pipeline_summary`를 가진 유효한 JSON이어야 합니다. `applications[]`의 모든 항목은 **요약 행**이며 최소한 `id`, `company`, `role`, `status`, `application`(`"{company} — {role}"` 라벨), `detail_file`을 가져야 합니다. `applications[]`에는 제출한 지원만 들어가며, 지원 전 단계의 공고는 `recommendations.json`에 있습니다. `applications` 배열의 실제 내용으로 `pipeline_summary` 집계를 다시 계산하고, 오래된 값이면 갱신합니다.

  그런 다음 분할 레이아웃 자체를 검증합니다.
  - 어떤 행에 인라인 `notes`, `stage_history`, `contacts` 배열이 남아 있으면 분할 이전(v1) 파일입니다. 각 배열을 옮깁니다. `notes[]`와 `stage_history[]`는 `applications/{application_id}.json`으로, `contacts[]`는 `contacts/{company-slug}.json`으로 옮기며 각 연락처에 해당 행의 `application` 라벨을 태그합니다. 그런 다음 행에서 인라인 배열을 삭제합니다. 트래커가 마이그레이션되었음을 사용자에게 알립니다.
  - `id`가 UUID이거나, 단순 순번(`app-001`)이거나, 날짜 접미사가 붙은 형태이면 설명형 slug(`app-{company-slug}-{role-keywords}`, 예: `app-hex-senior-pm`)로 이름을 바꾸고, 상세 파일 이름도 이에 맞게 바꾸며, 이전 id를 해당 행의 `previous_ids`에 추가합니다.
  - 모든 행의 `detail_file`은 디스크에서 실제로 확인되어야 합니다. `notes_count`와 `stage_count`는 상세 배열의 길이와 같아야 하며, `latest_stage`와 `latest_stage_date`는 `stage_history`의 마지막 항목과 일치해야 합니다. 오래된 값은 다시 계산합니다.
  - 연락처가 있는 모든 행은 실제로 확인되는 `contacts_file`을 가져야 하며, `contact_count`는 해당 파일에서 `application`이 행의 `application` 라벨과 같은 항목의 개수와 같아야 합니다. `CareerLoop/contacts/`를 나열해 기존 파일을 재사용하며, 이미 slug가 있는 회사에 두 번째 slug를 만들지 않습니다.

- **`artifacts-index.json`**: `meta` 객체와 `artifacts` 배열을 가진 유효한 JSON이어야 합니다. 나열된 아티팩트 파일명을 `{user_dir}`에 실제로 있는 파일과 대조합니다. 더 이상 존재하지 않는 파일의 항목은 제거합니다. `{user_dir}`에서 발견된 PDF/DOCX 파일 중 아직 인덱싱되지 않은 것은 항목을 추가합니다.

- **`CareerLoop/StoryCorpus.json`**: `meta`, `stories` 배열, `source_index` 배열을 가진 유효한 JSON이어야 합니다. 비어 있거나 오래된 경우 `{user_dir}`에서 찾은 저널/PKM/디브리프/이력서 소스에 대해 `mine-stories` 추출을 실행합니다.

검증 후 사용자에게 다음을 보고합니다.
> - 무엇을 찾았고 검증을 통과했는지
> - 자동으로 수정한 내용
> - 사용자의 입력이 필요한 공백

**파일이 존재하지 않는 경우** — `{user_dir}`의 문서로 생성합니다.

1. `{user_dir}`를 (재귀 없이) 스캔하여 읽을 수 있는 문서(PDF, DOCX, TXT, MD 파일)를 찾습니다.
2. 각 문서를 읽고 관련 내용을 추출합니다.
3. 아래 스키마에 따라 누락된 파일을 구성합니다.
4. 쓰기 전에 누락된 하위 디렉터리를 만듭니다. `CareerLoop/applications/`와 `CareerLoop/contacts/`는 비어 있는 상태로 시작하더라도 반드시 존재해야 합니다.
5. 어떤 문서를 사용했고 무엇을 생성했는지 사용자에게 알립니다.

`{user_dir}`에 원본 문서가 전혀 없으면 최소한의 플레이스홀더 파일을 만들고 사용자에게 이력서를 추가해 달라고 안내합니다.
> "구직 폴더에서 이력서나 문서를 찾지 못했습니다. 이력서(PDF 또는 DOCX)를 추가한 뒤 `/careerloop:launch`를 다시 실행하면 프로필과 ExperienceLibrary를 구성합니다."

#### 새로 생성하는 파일의 스키마

**`CareerLoop/profile.md`**
```markdown
# {Name} — Job Search Profile

## Contact
- Email, Phone, Website (이력서에서 추출)

## Target Roles
(이력서의 목표/요약에서 추출하거나 플레이스홀더로 남김)

## Target Companies
(알 수 없으면 비워 둠)

## Compensation Floor
(비워 둠 — 사용자에게 물어봄)

## Location
(이력서에서 추출하거나 플레이스홀더로 남김)

## Key Differentiators
(이력서 요약/하이라이트에서 추출)

## Employment Context
- Employment status: employed | unemployed | unknown
- 재직 중인 경우: 현재 보상 패키지(알 수 있다면 기본급/보너스/주식/복리후생)와 새로운 직무에 열려 있게 만들 수 있는 이슈(불릿).
- 무직인 경우: 마지막 직장(알고 있다면 직함/회사/종료일), 수입원(실업급여/퇴직금/기타), 새 직장이 필요해지기까지의 여유 기간(주/개월).
- 메모 / 가정 (지어내지 않음).

## Certifications & Credentials
- Degrees:
- Certifications / professional licenses:
- Clearance / security clearance:
- Other credentials:
- Notes (알고 있다면 만료/갱신 등).

## LinkedIn
- LinkedIn slug: (vanity username, 예: `linkedin.com/in/hong-gildong`의 `hong-gildong`)

## Current Search Status
- Actively searching as of {today's date}
```

**`CareerLoop/ExperienceLibrary.json`**
```json
{
  "meta": { "created": "{today}", "version": "1.0", "description": "..." },
  "units": [
    {
      "id": "exp-001",
      "type": "role",          // "role" | "education" | "publications_and_recognition"
      "company": "...",
      "title": "...",
      "dates": "...",
      "summary": "...",
      "achievements": [
        { "id": "exp-001-a1", "theme": "...", "text": "..." }
      ],
      "skills": ["..."]
    }
  ]
}
```

**`CareerLoop/tracker.json`** — 요약 행만 포함합니다. `CareerLoop/applications/`와 `CareerLoop/contacts/`는 비어 있는 상태로 시작하더라도 함께 생성합니다.
```json
{
  "meta": {
    "created": "{today}",
    "version": "2.0",
    "schema": "tracker_v2_split",
    "last_updated": "{today}",
    "layout": {
      "applications": "applications/<application_id>.json — notes[] and stage_history[] for one application",
      "contacts": "contacts/<company-slug>.json — every contact at one company"
    },
    "description": "..."
  },
  "applications": [],
  "pipeline_summary": {
    "as_of": "{today}",
    "applied": 0,
    "declined_or_inactive": 0,
    "overdue_followup": 0
  }
}
```

요약 행 — 사용자가 가져올 제출 완료 지원이 이미 있는 경우에만 작성합니다. `notes`, `stage_history`, `contacts` 배열은 포함하지 않습니다.
```json
{
  "id": "app-hex-senior-pm",
  "application": "Hex — Senior Product Manager",
  "company": "Hex",
  "role": "Senior Product Manager",
  "location": "...",
  "status": "applied",
  "date_applied": "YYYY-MM-DD",
  "follow_up_date": null,
  "next_step": null,
  "priority": "high",
  "outcome": "pending",
  "resume_version": null,
  "artifacts": [],
  "detail_file": "applications/app-hex-senior-pm.json",
  "contacts_file": "contacts/hex.json",
  "notes_count": 1,
  "stage_count": 1,
  "contact_count": 1,
  "latest_stage": "applied",
  "latest_stage_date": "YYYY-MM-DD"
}
```

`id`는 `app-{company-slug}-{role-keywords}` 형식(예: `app-hex-senior-pm`, `app-anthropic-research-pm-labs`)으로 만들며, UUID, 단순 순번(`app-001`), 날짜 접미사가 붙은 id는 절대 사용하지 않습니다. 지원에 연락처가 없으면 `contacts_file`과 `contact_count`는 생략합니다.

**`CareerLoop/applications/{application_id}.json`** — 지원 한 건당 파일 하나이며, 해당 요약 행과 같은 트랜잭션에서 작성합니다.
```json
{
  "schema": "application_detail_v1",
  "application_id": "app-hex-senior-pm",
  "application": "Hex — Senior Product Manager",
  "company": "Hex",
  "role": "Senior Product Manager",
  "stage_history": [
    {
      "stage": "applied",
      "date": "YYYY-MM-DD",
      "notes": "...",
      "interview_type": null,
      "interviewers": [],
      "post_notes": null
    }
  ],
  "notes": [
    { "date": "YYYY-MM-DD", "text": "..." }
  ]
}
```

**`CareerLoop/contacts/{company-slug}.json`** — 회사 한 곳당 파일 하나이며, 해당 회사의 모든 지원을 담당합니다. 각 연락처의 `application` 필드는 요약 행의 `"{company} — {role}"` 라벨입니다.
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
        { "date": "YYYY-MM-DD", "type": "email", "notes": "..." }
      ]
    }
  ],
  "contact_count": 1
}
```

회사 slug: 회사 이름을 소문자로 바꾸고, 악센트를 제거하고, 영숫자가 아닌 문자가 연속된 구간을 모두 하이픈 하나로 바꾸고, 앞뒤 하이픈을 제거합니다(`84.51°` → `84-51`). 먼저 `CareerLoop/contacts/`를 나열하고, 같은 회사에 두 번째 slug를 만들지 말고 이미 있는 파일을 재사용합니다.

작성 후 다음을 검증합니다. 모든 요약 행의 `detail_file`이 실제로 확인되는지, `notes_count` / `stage_count`가 상세 배열과 일치하는지, `latest_stage`가 `stage_history`의 마지막 항목과 일치하는지, 각 `contact_count`가 필터링된 연락처 파일과 일치하는지 확인합니다.

**`CareerLoop/networking.json`**
```json
{
  "meta": { "created": "{today}", "version": "1.0", "description": "Networking data — recruiter relationships and LinkedIn post analytics" },
  "recruiter_relationships": [],
  "networking": []
}
```

**`CareerLoop/recommendations.json`**
```json
{
  "meta": { "created": "{today}", "version": "1.0", "description": "Pre-application role pipeline — roles under consideration before applying" },
  "recommendations": []
}
```

**`CareerLoop/passed.json`**
```json
{
  "meta": { "created": "{today}", "version": "1.0", "description": "Roles considered and explicitly passed on before applying" },
  "passed": []
}
```

**`artifacts-index.json`**
```json
{
  "meta": { "created": "{today}", "version": "1.0", "description": "..." },
  "artifacts": [
    {
      "id": "artifact-001",
      "type": "resume",          // "resume" | "cover_letter" | "linkedin_post"
      "filename": "...",
      "path": "...",
      "target_company": "...",   // 일반/기본 이력서이면 null
      "target_role": "...",      // 일반/기본 이력서이면 null
      "date_created": "...",
      "source": "existing",      // "existing" | "generated"
      "notes": "..."
    }
  ]
}
```

### 2.4 고용 상황 및 자격 정보 수집 (profile.md에 저장)

핵심 파일이 존재하게 된 후(또는 생성/복구된 후), `{user_dir}/CareerLoop/profile.md`에 활용 가능한 컨텍스트가 있는지 확인합니다.

1. `{user_dir}/CareerLoop/profile.md`를 읽고 다음을 확인합니다.
   - `## Employment Context`가 있고 플레이스홀더만 있는 상태가 아닌지,
   - `## Certifications & Credentials`가 있고 플레이스홀더만 있는 상태가 아닌지.

2. `{user_dir}`에서 이미 찾은 문서로 채워 봅니다.
   - CV/이력서/자기소개서 텍스트에서 학위, 자격증, 전문 면허, 보안 인가(clearance) 관련 언급을 추출합니다.
   - 고용 관련 단서(현재 고용주, 이직 공백기 여부, 실업급여/퇴직금 언급 등)를 추출합니다.

3. `Employment Context`가 없거나 불분명하면 목적에 맞는 질문을 한 뒤, 답변을 `profile.md`의 다음 항목 아래에 다시 기록합니다.
   - `## Employment Context`
   - 시나리오 A(재직 중): 현재 보상 패키지와 이직이 매력적으로 느껴질 수 있는 이슈/제약을 묻습니다.
   - 시나리오 B(무직): 실업급여/퇴직금/수입원, 마지막 직장(알고 있다면 직함/회사/종료일),
     새 직장이 필요해지기까지의 여유 기간을 묻습니다.
   - 시나리오 C(알 수 없음): 재직 중인지 무직인지 구분하기 위한 최소한의 질문을 하나만 합니다.

4. `Certifications & Credentials`가 없거나 불분명하면 찾은 내용을
   (짧은 목록으로) 보여 주고 사용자에게 확인과 누락 항목 추가를 요청합니다.

5. `## LinkedIn`에 예약된 분석에 필요한 모든 필드가 있는지 확인합니다.
   - `LinkedIn slug:`
   - `LinkedIn analytics permission: granted | denied`
   - `LinkedIn analytics mode: chrome | computer | either`
   slug가 없거나 비어 있으면 "LinkedIn 사용자 이름(vanity username)이 무엇인가요? (`linkedin.com/in/` 뒤에 오는 부분입니다)"라고 묻고 저장합니다.
   permission/mode가 없으면 한 번만 묻고 저장합니다. 사용자가 분석을 거절하면 `permission: denied`와 `mode: unknown`을 저장합니다.

6. 저장 규칙:
   - 다른 섹션(Target Roles, Key Differentiators 등)은 덮어쓰지 않습니다.
   - 해당 제목 아래의 내용만 갱신합니다.
   - 사용자가 “잘 모르겠다”고 하면 지어내지 말고 `unknown`을 명시적으로 기록합니다.

### 2.5 보이스 프로필 (launch)

핵심 파일이 존재하게 된 후, `{user_dir}/CareerLoop/voice-profile.md`를 구성하거나 갱신하여 **`writer`**가 실제 어조 신호를 갖도록 합니다. 이력서/CV/편지가 다른 곳에 있는데도 자동 생성된 마크다운 아티팩트 하나만 쓰는 방식은 안 됩니다.

**순서:** 먼저 **2.5b**(목록 확인 + Tier A PDF/DOCX 읽기)를 실행하고, 그다음 **2.5a**(LinkedIn 안내)를 진행한 뒤, 붙여넣은 내용이나 **continue**로 다시 스캔한 결과를 **2.5c**에 반영합니다. **2.5a** 이후 사용자가 새 파일을 추가하면 작성 전에 **2.5b**를 다시 실행합니다.

#### 2.5a LinkedIn / 소셜 글쓰기 요청 (같은 세션)

**2.5b**(그리고 사용자가 새 파일을 추가한 경우의 재스캔) 이후, **2.5c**를 작성하기 전에 한 번 안내합니다.

> **보이스 & 톤:** 이력서뿐 아니라 LinkedIn과 메시지에서의 말투도 반영하기 위해 다음 중 하나를 선택해 주세요.
> 1. 최근 LinkedIn 게시물(또는 다른 짧은 업무 관련 글) 2~5개를 여기에 **붙여넣기**하거나,
> 2. 이 폴더에 파일(예: `linkedin-posts.md`, `.txt`, 또는 PDF 내보내기)로 **추가**한 뒤 저장되었다고 알려 주시거나 **continue**(계속)라고 말씀해 주세요. 폴더를 다시 읽겠습니다.
> 3. **skip**(건너뛰기)이라고 답하시면 이력서/자기소개서만 참고합니다(소셜 게시물과 DM에는 **일치도가 낮아집니다**).

사용자가 **붙여넣은** 경우: 날짜가 포함된 **`## User writing samples (launch)`** 섹션을 추가하여 발췌문(다듬은 것)을 넣고 **source: user paste (launch)**라고 표기합니다.

사용자가 **건너뛴** 경우: **`## Launch — LinkedIn prompt`** 아래에 한 줄을 기록합니다: *User skipped LinkedIn samples at launch; writer may ask again before drafting.*

#### 2.5b 디스크에서 글 수집 (우선순위 순)

**목표:** 흩어진 `.md` 파일만이 아니라 **CV, 이력서, 자기소개서**를 주된 보이스 출처로 사용합니다.

1. **범위:** **`{user_dir}`**를 재귀적으로 순회합니다(또는 최상위 폴더 **및** 숨김이 아닌 모든 하위 폴더 — `Documents/`, `resumes/` 등을 찾을 수 있는 최소 깊이). **제외:** `.git`, `node_modules`, `.Trash`, 그리고 사용자 문서가 아님이 분명한 모든 것.

2. **코퍼스 입력에서 항상 무시:**
   - `{user_dir}/CareerLoop/voice-profile.md` (보이스를 추론하려고 이 파일을 읽지 않습니다).
   - 모든 **`CareerLoop/*.json`** (스키마/데이터이며 보이스가 아님).

3. **모든 후보 파일을 분류합니다** (경로 + 이름 + 존재하는 경우 `artifacts-index.json` 기준):
   - **Tier A — 원본 경력 문서(우선):** 이름/경로가 **resume**, **cv**, **curriculum vitae**, **cover**, **letter**, **bio**, **about** 또는 명백한 사용자 업로드 기본 파일명을 암시하는 `*.pdf`, `*.docx`, `*.txt`, `*.md`. **PDF와 DOCX는 반드시 읽어야 합니다.** `profile.md` / ExperienceLibrary를 구성할 때와 같은 방식으로 읽고, **전문 요약 / 프로필**, **자기소개서 본문**(파일에 있는 경우), **대표 불릿 문장**(전체 경력 이력은 아님)을 추출합니다. 서술 없이 불릿 목록만 있는 파일이면 문체 특성(밀도, 수치, 불릿에서의 어조)을 기록합니다.
   - **Tier B — 기타 산문:** 사용자가 쓴 글로 보이는 나머지 `.md` / `.txt`(변경 로그나 무관한 저장소 readme는 제외).
   - **Tier C — 플러그인이 생성한 아티팩트(주의해서 사용):** `artifacts-index.json`에서 `"source": "generated"`인 항목(및 디스크의 해당 파일). **Tier A** 파일이 하나라도 있으면 Tier C를 서술의 **유일한** 근거로 삼지 **않습니다**. 문단 형태의 글을 Tier C만 제공하는 경우에는 사용하되 **Source: generated artifact**로 표기하고 “자연스러운” 보이스에 대한 **낮은 신뢰도**를 표시합니다.

4. **최소 기준:** **어조가 뚜렷이 다른 여러 출처**(예: 격식 있는 자기소개서 vs 캐주얼한 LinkedIn 붙여넣기)를 찾았다면 하나의 보이스로 뭉뚱그리지 **않고** **2.5c**의 다중 컨텍스트 섹션 및/또는 **Open questions**를 사용합니다.

5. **서술이 전혀 없는 경우:** 불릿과 구조만 있더라도 보이스 메모(간결성, 수치, 키워드 밀도)를 작성하고, 문단 수준의 일치를 위해 **`writer`**에 붙여넣은 글이 필요하다고 표시합니다.

#### 2.5c `voice-profile.md` 작성 (구조)

날짜가 포함된 섹션으로 생성하거나 갱신합니다(이력 보존을 위해 이전 날짜 블록을 아래에 남겨 둘 수 있습니다).

1. **`## Launch voice harvest (YYYY-MM-DD)`** (또는 해당 제목을 선호하면 **`## Setup scan (YYYY-MM-DD)`**를 유지하되, 실행마다 날짜가 있는 harvest를 하나씩 사용):
   - 표 **Source files scanned**: **Path**(`{user_dir}` 기준 상대 경로), **Tier**(A/B/C), **Doc type**(résumé / CV / cover / LinkedIn file / other), **Voice notes**(짧게).
   - 첫 번째 마크다운 파일만이 아니라 찾은 **조건에 맞는 모든 파일을 포함**합니다.

2. **`## Voice by context`**(어조가 갈리거나 사용자가 격식체와 캐주얼한 샘플을 모두 제공한 경우):
   - 하위 섹션 예: **`### Applications (résumé / cover letter)`**, **`### Public (LinkedIn)`**, **`### Other`**. 하위 섹션별로 문체, 문장 길이, 유머, CTA를 기록합니다.
   - 어조가 충돌하고 의도가 불분명하면 **`## Open questions`**(불릿 1~4개)를 추가합니다. 자기소개서 vs DM vs 게시물의 기본 보이스, 청중별로 의도한 **여러 페르소나** 등을 다룹니다.

3. **`## Voice quality flags (launch)`** — 솔직한 리스크(구직 실용주의 관점이며 인신공격이 아님):
   - 예: 보수적인 고용주에게 부정적으로 읽힐 수 있는 **비꼼 / 냉소**, **과한 노력** 또는 과장, **전형적인 “AI 티”**(공허한 거창함, 군더더기 연결어, 근거 없는 유행어 나열), **사과 / 얼버무림** 반복, 공개 샘플에 담긴 **정치적이거나 논쟁적인 색채**, **과도한 공개**. 각 항목에 **low / medium / high** 우려 수준과 **이유**를 적습니다. 문제가 없으면: *No major flags from available samples.*

4. 끝에 **선택 사항인 `voice_profile_v1` JSON**: 다중 컨텍스트 섹션이 있을 때 `"tones": { "applications": "…", "public": "…" }`를 포함합니다.

5. **`## Usage guidance for writer`:** **자기소개서** vs **LinkedIn** vs **DM**에 어떤 컨텍스트를 쓸지 기록합니다. 모호하면 넘어가기 전에 이 launch 세션에서 **사용자에게 한 번 묻습니다**.

같은 폴더에 Tier A 이력서/CV가 있다면 플러그인이 생성한 자기소개서 하나만으로 충분하다고 간주하지 **않습니다**. 이 섹션을 위해 **해당 파일들을 읽어 들입니다**.

### 2.6 스토리 코퍼스 초기화

핵심 파일과 보이스 프로필 이후:

1. `{user_dir}/CareerLoop/StoryCorpus.json`이 존재하는지 확인합니다.
2. 전처리 단계로 `mine-stories`를 실행합니다.
   - 최초 launch에서는 전체 추출
   - 이후 launch에서는 증분 추출(새로 생기거나 변경된 소스 파일만)
3. 이제 면접 준비가 이 코퍼스를 행동 면접 스토리의 단일 기준 자료로 사용하므로, 모델이 매번 전체 저널을 다시 읽을 필요가 없음을 설명합니다.
4. 소스 파일이 없거나 부족하면 비어 있는(채울 준비가 된) 코퍼스를 유지하고, 사용자에게 저널/메모/PKM 내보내기 파일이 생기면 추가해 달라고 요청합니다.

### 3. Indeed MCP 커넥터 연결 (실시간 공고 검색)

**커넥터 패턴**을 적용합니다. **`search_jobs`** / **`get_job_details`**가 **이 채팅**에서 이미 사용 가능하면 **Indeed**에 대해 묻지 **않습니다**.

CareerLoop의 **`search-jobs`** 스킬은 **Indeed** MCP 도구 **`search_jobs`**와 **`get_job_details`**를 필요로 합니다. **Claude Desktop**에서는 사용자가 **Customize → Connectors**에서 **Indeed**를 연결하고 Indeed와의 **브라우저 기반 OAuth**를 마쳐야 이 도구들이 나타납니다(`.mcp.json`에 붙여넣는 정적 API 키가 **아닙니다**). **도구가 없는 경우에만** **설정(Configure)**을 진행하며, **Connect**와 OAuth는 **사용자가 직접** 완료합니다. **Claude in Chrome**이나 **computer use**로 대신 진행하지 않습니다.

**Claude Desktop에서 예상되는 화면:**

- **Indeed** 커넥터 페이지에는 **“Search for jobs on Indeed”**라는 설명과 개발자 **Indeed**가 표시되고, **Tools** 아래에 **`search_jobs`**와 **`get_job_details`**가 나열됩니다. **Details**에는 커넥터 URL `https://mcp.indeed.com/claude/mcp`가 표시될 수 있습니다(참고용일 뿐이며, JSON을 편집하지 말고 앱을 통해 연결합니다).
- **Connect**를 누르면 연결 흐름이 시작됩니다. Claude가 **“Grant access to Indeed”**를 표시하며 **새 브라우저 탭에서 로그인 절차를 완료**하라는 안내가 나타납니다(필요하면 **“Didn’t work? Relaunch the tab”**도 표시).
- 브라우저에서 **Indeed**가 **`secure.indeed.com`**의 OAuth 페이지(**“Claude would like to access your account”**)를 엽니다. 사용자가 로그인하거나(또는 올바른 Indeed 계정인지 확인하고) 권한(예: 사용자를 대신한 공고 검색, 프로필 접근)을 검토한 뒤 **Continue**를 눌러 승인합니다.

**사용자에게 안내할 절차:**

1. **Customize**(또는 **Settings**) → **Connectors** → 카탈로그에서 **Indeed**를 찾습니다.
2. **Indeed**를 열고 **Tools**에 **`search_jobs`**와 **`get_job_details`**가 포함되어 있는지 확인합니다.
3. **Connect**를 클릭합니다. **Grant access to Indeed**가 나타나면 **새 브라우저 탭**으로 전환해 **Indeed** 로그인 / 동의를 마치고 OAuth 화면에서 **Continue**를 클릭하도록 안내합니다.
4. 성공하면 Claude에 커넥터가 연결된 상태로 표시됩니다(예: **Connect** 대신 **Disconnect**가 보임). 그래도 도구가 나타나지 않으면 **새 채팅**을 시작합니다.

**검증:** 이 세션(또는 새 채팅 이후)에서 **`search_jobs`** / **`get_job_details`**를 사용할 수 있는지 확인합니다. 사용할 수 있다면:

> "Indeed가 연결되었습니다. 언제든 `/careerloop:search-jobs`를 실행하시거나, 목표 직무와 지역에 맞는 공고를 찾아 달라고 말씀해 주세요."

**Indeed**에 대해서는 (브라우저 접근을 포함해) 더 이상 묻지 **않습니다**. 이미 설정이 끝났기 때문입니다.

OAuth 이후에도 도구가 없으면 다음을 확인하도록 안내합니다: Indeed 계정 승인 여부, 커넥터가 계속 활성화되어 있는지, 연결 후 **새 채팅** 시작 여부.

**Claude Cowork / 기타 호스트:** 호스트에 문서화된 방법으로 **Indeed** 공고 검색 MCP를 활성화합니다(가능한 경우 도구 이름은 동일). 자격 증명을 지어내거나 공식 커넥터 없이 Indeed를 스크래핑하지 않습니다.

### 4. 연봉 벤치마킹을 위한 Apify 설정 (선택)

**커넥터 패턴**을 적용합니다. **Apify** 도구가 이미 사용 가능하면 **Apify**에 대해 묻지 **않고** **`/careerloop:salary-research`**를 안내한 뒤 넘어갑니다.

`salary-research` 스킬은 **Apify** MCP 도구를 사용해 실시간 보상 데이터를 가져옵니다. 이 단계는 선택 사항이며, 사용자가 연봉 벤치마킹이 필요 없다면 건너뜁니다.

사용자에게 Apify 토큰을 채팅에 붙여넣거나, `claude_desktop_config.json`을 편집하거나, MCP 시작을 위해 로컬 환경 변수나 dotfile에 의존하라고 요청하지 **않습니다**. Claude Desktop은 MCP `args` 안에서 셸 방식의 변수 확장을 수행하지 않기 때문입니다. **사용자가 직접** 앱의 **Apify** 커넥터 양식에 토큰을 붙여넣습니다. 브라우저 자동화로 설정하지 않으며, 플러그인 자체는 이 토큰을 읽거나 저장하거나 전송하지 않습니다.

먼저 Apify MCP가 이미 연결되어 있는지 확인합니다. 지연(deferred) 상태일 수 있으므로 다시 확인하고, 필요하면 활성화합니다. 활성 상태라면 프로필의 직무와 지역으로 `/careerloop:salary-research`를 실행해 보라고 안내합니다. 그렇지 않으면 사용자에게 묻습니다.
> "연봉 벤치마킹을 설정하시겠어요? Apify의 무료 티어(월 $5 크레딧 — 개인 구직 용도로는 충분합니다)를 사용해 직무와 지역별 실시간 연봉 데이터를 가져옵니다."

**예인 경우 — Claude Desktop 커넥터 흐름:**

1. **https://apify.com**에서 가입하도록 안내합니다(무료 계정).

2. **Console → Settings → Integrations**에서 **Personal API token**을 복사합니다(비공개로 보관하며, 이 대화에 붙여넣으라고 요청하지 **않습니다**).

3. 호스트 UI에서 다음 순서로 안내합니다.
   - **Customize**(또는 **Settings**) → **Connectors**를 엽니다
   - **Desktop** 아래에서 **Apify**를 선택합니다(**apify-mcp-server**로 표시될 수 있음)
   - **Configure**를 엽니다
   - **Apify token (Required)**에 토큰을 붙여넣습니다
   - **Enabled tools**를 다음 문자열 그대로 설정합니다(쉼표로 구분, 공백 없음).

     `call-actor,get-actor-run,get-dataset-items,cheapget/best-job-search`

   - **Save**를 누르고, 커넥터를 **켠** 뒤, MCP 도구가 로드되도록 **새 채팅**을 시작합니다

4. 검증: Apify 도구(예: **Call Actor**, **Get Actor run**, **Get dataset items**)를 사용할 수 있는지 확인합니다. 도구를 지연 상태에서 활성화해야 하면 그렇게 합니다. 도구가 없으면 다시 확인할 항목(토큰, enabled tools 문자열, 커넥터 활성화 여부, 새 세션)을 정리해 알려 줍니다. Apify가 **이미 연결되어 있으면** 그에 대해 더 이상 질문하지 **않습니다**.

**Cowork / 기타 호스트:** 사용자가 Claude Desktop을 쓰지 않는다면 호스트에 문서화된 방식으로 Apify MCP를 추가하도록 안내합니다(**Enabled tools** 문자열은 동일하며, UI에 제공되면 보안 토큰 필드를 사용). 토큰을 포함하는 JSON 설정을 지어내지 않습니다.

**아니요이거나 건너뛴 경우:**

> "알겠습니다. 연봉 벤치마킹은 지금은 꺼 둡니다. 언제든 `/careerloop:launch`를 다시 실행해 설정할 수 있습니다."

### 5. LinkedIn 게시물 분석 제안 (선택)

**커넥터 패턴**을 적용합니다(이 흐름에서 LinkedIn은 보통 호스트 MCP가 **없으므로** **브라우저 접근**이 핵심 수단입니다).

**Indeed**와 **Apify** 이후(또는 사용자가 Apify를 건너뛴 경우), **사용자 본인**의 LinkedIn 게시물 지표를 **`{user_dir}/CareerLoop/networking.json`**(`networking[]`, **`linkedin-post-analytics`** 기준)에 **읽기 전용**으로 스냅샷하는 기능을 제안합니다. 선택 사항이며, 명확한 **예**가 없으면 실행하지 않습니다.

**1 — 탐색:** 이 플러그인 경로에는 보통 LinkedIn MCP 도구가 **없습니다**. 분석은 **브라우저** 접근(3단계)을 사용한다고 안내합니다.

**2 — 설정:** 호스트가 사용할 수 있는 브라우저 프로필에서 **LinkedIn에 로그인되어 있는지** **묻습니다**. 로그인은 **사용자가 직접** 합니다. LinkedIn 로그인을 자동화하지 않습니다.

**3 — 브라우저 접근:** **읽기 전용** LinkedIn 분석에 **Claude in Chrome** 및/또는 **computer use**를 사용할지 **묻습니다**(**둘 다 안 함** / Chrome / computer use / 둘 다). **둘 다 안 함**이면 브라우저에서 분석을 실행하지 **않고** **나중에 예약**하거나 건너뛰도록 제안합니다.

지금 실행하거나 나중에 예약하기 전에 선택 사항을 `{user_dir}/CareerLoop/profile.md`의 `## LinkedIn` 아래에 저장합니다.
- `LinkedIn analytics permission: granted | denied`
- `LinkedIn analytics mode: chrome | computer | either`
**둘 다**를 선택하면 `mode: either`로 저장합니다.

**다음과 같이 말합니다:**

> **LinkedIn 가시성(선택):** **내** 게시물 분석을 커리어 트래커에 (읽기 전용으로) 스냅샷할 수 있습니다. 어떤 브라우저 접근을 사용할까요 — **Claude in Chrome**, **computer use**, **둘 다**, 또는 **둘 다 안 함**(지금은 브라우저 실행 건너뛰기)?  
> **지금** 실행하거나 **`/schedule`**로 **나중에** 실행하고 싶다면 알려 주세요.

**지금 실행을 선택**했고 **Chrome** 및/또는 **computer use**를 승인한 경우:

1. 선택한 도구를 호스트에서 사용할 수 있는지 확인합니다. **둘 다** 승인하지 않았거나 도구가 없으면 스크래핑하지 **않고**, 도구를 활성화하고 LinkedIn에 로그인한 뒤 **`linkedin-post-analytics`** 또는 **`/careerloop:linkedin-post-analytics`**를 실행하면 된다고 설명합니다(또는 새 채팅에서 **continue**).
2. 승인된 경우: **`skills/linkedin-post-analytics/SKILL.md`**를 처음부터 끝까지 따릅니다(LinkedIn vanity slug를 모르면 묻고, `networking.json`에 스냅샷을 추가하고, 요약).

**나중에 예약을 선택**한 경우: 예약 없이 실행되는 `/schedule`이 다시 묻지 않고 실행될 수 있도록 지금 slug/permission/mode를 `profile.md`에 저장합니다.

**건너뛰거나 미룬 경우:**

> "알겠습니다. 언제든 **`linkedin-post-analytics`** 또는 **`/careerloop:linkedin-post-analytics`**를 실행하시거나, 준비되면 **`/schedule`** 작업을 추가하세요. 가시성 관련 작업을 하실 때는 **`networking-strategist`**가 알려 드릴 수 있습니다."

### 6. 이메일 및 미팅 컨텍스트를 위한 Gmail / Microsoft 365 / Google Calendar 연결 (선택)

**커넥터 패턴**을 적용합니다. 해당 서비스의 도구가 **이 채팅**에 **이미** 있으면 **Gmail**, **Microsoft 365**, **Google Calendar**에 대해 안내하지 **않습니다**(간단한 확인만).

**Indeed**, **Apify**, **LinkedIn 게시물 분석** 제안(또는 건너뜀) 이후, **Gmail** 및/또는 **Microsoft 365**(받은편지함) 및/또는 **Google Calendar**를 제안합니다. 그러면 **`draft-outreach`**, **`follow-up`**, **`contact-context`**가 **사용자가 각 조회를 명시적으로 승인한 경우에 한해** **읽기 전용**으로 메일을 검색하고 연락처와의 **최근 미팅**을 요약할 수 있습니다.

**2단계에 한정:** **Connectors**를 Chrome/computer-use 도구로 자동화하지 않습니다. Gmail/M365/Calendar를 설정하거나 다시 활성화할지 **묻고**, **예**라면 사용자가 **직접** **Connectors** 설정과 OAuth를 완료하고 사용자는 안내만 제공합니다.

#### 6a. Gmail — 먼저 연결 상태 확인

1. **이 세션 확인:** **이 채팅**에서 사용 가능한 도구를 확인합니다. **Gmail** / Google 메일에 해당함이 분명한 도구가 있으면(이름에 `gmail`, `google` 등이 포함되는 경우가 많으며 정확한 문자열은 호스트마다 다름) 이 세션에서 **Gmail이 연결되어 활성화된 것**으로 처리합니다. 이를 간단히 말하고(예: “여기서는 Gmail이 연결된 것으로 보입니다. 검색을 승인하시면 받은편지함 컨텍스트에 활용할 수 있습니다”) Gmail을 다시 설치하라고 요청하지 **않습니다**. 필요하다면 아래에서 **Microsoft 365**는 계속 제안합니다.

2. **Gmail 도구가 보이지 않는 경우:** 채팅에서는 **Connectors** 화면을 **볼 수 없습니다**. **Customize** / **Settings** → **Connectors**를 열어 **Gmail**을 확인해 달라고 요청합니다.
   - **Gmail이 목록에 없음:** **6d** 단계의 일반적인 “추가 + 연결” 경로(최초 설치)를 사용합니다.
   - **Gmail이 목록에 있지만 꺼져 있음**(토글 비활성화, 커넥터 비활성 또는 이에 준하는 상태): 정중하게 묻습니다. 예:  
     > “Claude에 **Gmail** 커넥터가 이미 있지만 현재 활성화되어 있지 않습니다. **읽기 전용** 접근으로 **켜시겠어요**? CareerLoop는 **사용자가 승인한** 조회에 대해서만 검색하며, Anthropic의 Gmail 연동은 사용자를 대신해 메일을 보내지 않습니다.”  
     **예**라면 **Connectors**에서 사용자가 **직접** 토글(또는 이에 준하는 항목)을 **활성화**하고, UI가 요청하면 **Connect** / 재인증을 진행한 뒤, 그래도 도구가 로드되지 않으면 **새 채팅**을 시작하도록 안내합니다. 토글을 바꾸거나 OAuth를 완료하기 위해 **Claude in Chrome**이나 **computer use**를 사용하지 **않습니다**.
   - **Gmail이 목록에 있지만 로그인되어 있지 않음**(**Connect**, **Reconnect** 또는 연결 해제 상태로 표시): 정중하게 묻습니다. 예:  
     > “Gmail이 추가되어 있지만 Google 계정에 연결되어 있지 않습니다. **설정하시겠어요**? **Connect**를 클릭하고 Claude가 여는 브라우저 탭에서 Google 로그인을 마치시면 됩니다. 같은 **읽기 전용** 방식이며, 매번 사용자가 예라고 할 때만 검색합니다.”  
     **예**라면 아래 절차를 안내합니다. **사용자가** 앱에서 **Connect**를 클릭하고 **OAuth**를 완료합니다(채팅에 비밀번호를 입력하지 않음).

3. **활성화/연결을 거절하는 경우:** 그 의사를 존중하고, 나중에 **Connectors**에서 켤 수 있다고 알려 줍니다.

#### 6b. Microsoft 365 (기존과 동일한 패턴)

관련이 있을 때 **Microsoft 365**를 제안합니다(**6d** 참조). 선택 사항: **Microsoft 365** 도구가 이 세션에 이미 있는 경우(프로젝트 **`.mcp.json`**의 **`ms365`** → `https://microsoft365.mcp.claude.com/mcp`를 통한 경우 포함 — Gmail/Google Calendar의 **대안**으로서의 Outlook/M365), 이를 확인하고 중복되는 설치 안내는 건너뜁니다.

#### 6c. Google Calendar — 먼저 연결 상태 확인

1. **이 세션 확인:** **이 채팅**에서 사용 가능한 도구를 확인합니다. **Google Calendar**에 해당함이 분명한 도구가 있으면(이름에 `calendar`, `google_calendar`, `gcal` 등이 포함되는 경우가 많으며 정확한 문자열은 호스트마다 다름) 이 세션에서 **Google Calendar가 연결되어 활성화된 것**으로 처리합니다. 이를 간단히 말하고(예: “Google Calendar가 연결된 것으로 보입니다. 조회를 승인하시면 미팅 컨텍스트에 활용할 수 있습니다”) Google Calendar를 다시 설치하라고 요청하지 **않습니다**.

2. **Google Calendar 도구가 보이지 않는 경우:** 채팅에서는 **Connectors** 화면을 **볼 수 없습니다**. **Customize** / **Settings** → **Connectors**를 열어 **Google Calendar**를 확인해 달라고 요청합니다.
   - **Google Calendar가 목록에 없음:** **6d** 단계의 일반적인 “추가 + 연결” 경로(최초 설치)를 사용합니다.
   - **Google Calendar가 목록에 있지만 꺼져 있거나** **Connect** / **Reconnect**로 표시됨: 정중하게 묻습니다. 예:  
     > “Claude에 **Google Calendar** 커넥터가 이미 있지만 현재 활성화되어 있지 않습니다. **켜시겠어요**? CareerLoop는 **사용자가 승인한** 조회에 한해서만 일정을 읽습니다. 예를 들어 아웃리치를 작성하기 전에 채용 관리자와의 이전 통화를 확인하는 경우입니다.”  
     **예**라면 사용자가 **Connectors**에서 **직접** **활성화** / **Connect**를 하고, 요청되면 **OAuth**를 완료한 뒤, 그래도 도구가 로드되지 않으면 **새 채팅**을 시작하도록 안내합니다. 토글을 바꾸거나 OAuth를 완료하기 위해 **Claude in Chrome**이나 **computer use**를 사용하지 **않습니다**.
   - **활성화/연결을 거절하는 경우:** 그 의사를 존중하고, 나중에 **Connectors**에서 켤 수 있다고 알려 줍니다.

#### 6d. 일반 이메일 및 캘린더 제안 (커넥터 상태를 모르거나 사용자가 여러 개를 원하는 경우)

**6a**에서 **Gmail** 도구가 세션에 있음을 이미 확인했다면 중복되는 부분에서는 이 제안에서 **Gmail을 생략**합니다. **6c**에서 **Google Calendar** 도구가 세션에 있음을 이미 확인했다면 중복되는 설치 안내에서 **Google Calendar를 생략**하되, **Microsoft 365**가 없다면 계속 제안합니다.

**다음과 같이 말합니다:**

> **이메일 및 캘린더 컨텍스트(선택):** 채용 담당자나 채용 관리자에게 이미 어떤 이야기를 했는지, 그리고 그들과의 **최근 미팅**(통화, 면접)을 기억하는 데 도움을 받고 싶다면 Claude의 **Connectors**를 통해 **Gmail** 및/또는 **Microsoft 365(Outlook)** 및/또는 **Google Calendar**를 연결할 수 있습니다. 인증은 브라우저에서의 **OAuth**이며 채팅에 비밀번호를 입력하지 않습니다. CareerLoop는 특정 조회에 대해 **사용자가 예라고 할 때만** 메일을 검색하거나 캘린더를 읽습니다.  
> **Gmail**, **Microsoft 365**, **Google Calendar**, **여러 개 조합**을 **설정**하시겠어요, 아니면 지금은 **건너뛰시겠어요**?

**설정하려는 경우(클릭은 사용자가 직접 하며, 연결에 Chrome/computer-use 도구를 사용하지 않음):**

1. **Customize** / **Settings** → **Connectors**.
2. **Gmail:** **Gmail**을 열고 → **Connect** → **Google** 로그인과 동의를 마칩니다. 공식 문서: [Gmail integration](https://claude.com/docs/connectors/google/gmail) · [Google Workspace connectors](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors).
3. **Google Calendar:** **Google Calendar**를 열고 → **Connect** → **Google** 로그인과 동의를 마칩니다(Gmail과는 별도의 커넥터). 공식 문서: [Google Calendar integration](https://claude.com/docs/connectors/google/calendar) · [Google Workspace connectors](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors).
4. **Microsoft 365(Outlook 포함, 캘린더/Teams 화면은 호스트에 따름):** **Microsoft 365**를 열고 → **Connect** → **Microsoft** 로그인을 마칩니다. **Team/Enterprise** 플랜과 경우에 따라 **관리자 설정**이 필요할 수 있습니다. [Microsoft 365 connector](https://claude.com/docs/connectors/microsoft/365)와 [Enabling and using the Microsoft 365 connector](https://support.claude.com/en/articles/12542951-enabling-and-using-the-microsoft-365-connector)를 참조하세요. 보안 개요: [Microsoft 365 connector: Security Guide](https://support.claude.com/en/articles/12684923-microsoft-365-connector-security-guide).
5. 연결할 때마다 메일 또는 캘린더 관련 도구가 나타나지 않으면 **새 채팅**을 제안합니다.

**검증:** 호스트가 Gmail, Microsoft 365, Google Calendar 도구를 노출하면 목록에 있고 활성화되어 있는지 확인합니다. 사용자의 **플랜이나 조직**에 커넥터가 포함되어 있지 않으면 그 사실을 분명히 말하고 앱의 **Connectors** 카탈로그와 [CONNECTORS.md](CONNECTORS.md)를 안내합니다. 해당 도구가 **이미** 작동 중이면 메일이나 캘린더에 대한 브라우저 접근은 묻지 **않습니다**. 채팅의 MCP로 충분합니다.

**건너뛴 경우:**

> "알겠습니다. 아웃리치와 후속 조치는 받은편지함이나 캘린더 검색 없이도 작동합니다. 나중에 **Settings → Connectors**에서 연결하시거나 **`/careerloop:launch`**를 다시 실행하시면 됩니다. 자세한 내용: **CONNECTORS.md**."

### 7. 클라우드 스토리지 커넥터 설정 (선택)

**커넥터 패턴**을 적용합니다. 선택한 제공업체의 도구가 이 채팅에 이미 있으면 스토리지 설정을 안내하지 **않습니다**.

이메일/캘린더 설정 이후(또는 건너뛴 이후), 아티팩트 이동성을 위한 클라우드 스토리지를 제안합니다.

> **클라우드 스토리지(선택):** 구직 관련 파일/아티팩트를 노트북 한 대 밖에도 백업해 두고 싶으신가요? **로컬 전용** 저장소로 유지하셔도 됩니다.  
> - **Google Drive:** Claude의 기본 Drive 커넥터는 일반적인 구직 파일(PDF/DOCX 등)에 대해 안정적이지 않으므로 **Google Drive 앱 동기화**(또는 수동 백업/복원)를 권장합니다.  
> - **OneDrive:** Claude의 Microsoft 365/OneDrive 파일 접근 커넥터는 기본 형식(Word/PowerPoint/PDF)에 최적화되어 있어 플러그인의 JSON 아티팩트에는 안정적으로 사용할 수 없으므로 **OneDrive 애플리케이션 동기화**(또는 수동 백업/복원)를 권장합니다.  
> - **Dropbox:** 같은 내구성 이유로 **Dropbox 애플리케이션 동기화**(또는 수동 백업/복원)를 권장합니다.  
> 어떤 방법을 원하시나요?

제공업체를 선택한 경우:

1. 어떤 제공업체를 원하는지, 그리고 **앱 동기화**와 **수동 백업/복원** 중 무엇을 선호하는지 확인합니다.
2. **클라우드 스토리지를 선택한 경우:** 구직 파일을 위해 커넥터를 연결하라고 요청하지 **않습니다**. 대신 다음을 묻습니다.
   - **동기화 애플리케이션**을 사용하시겠어요, 아니면 **수동 백업/복원**을 하시겠어요?
   - **앱 동기화**의 경우: Google, Microsoft 또는 Dropbox 데스크톱 앱으로 로컬 `{user_dir}` 폴더를 동기화하도록 안내합니다(모든 기기에서 폴더 내용을 로컬로 사용할 수 있도록).
   - **수동 백업/복원**의 경우: 기기를 바꾸기 전에 구직 폴더를 클라우드 스토리지 제공업체에 복사하고, 새 기기에서 launch를 실행하기 전에 로컬 폴더로 복원하도록 안내합니다.
   - 어느 경우든 폴더를 로컬에서 사용할 수 있게 된 후 **새 채팅**을 시작하도록 안내합니다.

**먼저 탐색하는 동작:**
- 선택한 제공업체가 이미 로컬로 동기화 중이거나(또는 복원된 폴더가 이미 있으면) 이를 확인하고 설정 안내는 건너뜁니다.
- 로컬 폴더 내용이 아직 없으면 먼저 동기화/복원을 완료한 뒤 채팅을 다시 시작하도록 안내합니다.

**가드레일:**
- 스토리지 설정에 브라우저 자동화를 사용하지 않습니다. 동기화/백업 단계는 사용자가 수행합니다.
- 건너뛰면 `{user_dir}`의 로컬 파일 시스템 저장소를 유지하고 launch를 정상적으로 계속합니다.

### 8. 면접 전사 (선택)

`prep-interview`와 `mock-interview`는 텍스트 전용입니다. 별도로, 사용자가 녹음된 면접을 자동으로 전사하길 원하면(`/careerloop:interview-capture`용) 한 번 제안합니다.

> "녹음된 면접을 자동으로 전사하고 싶으시다면 언제든 `/careerloop:setup-transcribe`를 실행하세요. 작은 로컬 서버를 설치하며, 터미널 없이도 안내해 드립니다."

어느 쪽이든 이 단계 때문에 launch를 중단하지 않습니다.
