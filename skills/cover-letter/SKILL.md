---
name: cover-letter
description: >
  CoverLetterBrief와 writer가 작성하는 최종 문장을 통해, 솔직하고 구체적이며 사용자의 문체에 맞춘 맞춤형
  자기소개서를 작성합니다. 아티팩트 인벤토리에 저장합니다. 이력서 맞춤화 이후 또는 요청 시 실행됩니다.
  /careerloop:cover-letter로도 호출할 수 있습니다. 다음과 같은 요청에 사용합니다: "write a cover letter",
  "cover letter for", "draft a cover letter", "I need a cover letter", "자기소개서 써줘", "이 공고에 맞는 자기소개서 작성해줘".
  (Produces a targeted cover letter via a CoverLetterBrief and writer
  final prose—honest, specific, voice-matched. Saves to the artifact inventory.
  Fires after tailoring or on request. Also /careerloop:cover-letter.)
triggers:
  - "write a cover letter"
  - "cover letter for"
  - "draft a cover letter"
  - "generate a cover letter"
  - "I need a cover letter"
  - "/cover-letter"
  - "cover letter for this role"
  - "cover letter for this job"
  - "자기소개서 써줘"
  - "자기소개서 작성"
  - "자기소개서 초안 만들어줘"
  - "이 직무 자기소개서"
  - "이 공고용 자기소개서가 필요해요"
  - "커버레터 써줘"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

**CoverLetterBrief**를 만든 뒤 최종 자기소개서 문장은 **`writer`**를 호출해 작성합니다. 이 스킬에서 자기소개서 전문을 직접 쓰지 않습니다. 바로 보낼 수 있는 문안은 **`writer`**가 담당합니다.

## 워크플로

### 1. 입력 수집

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분리 레이아웃을 사용합니다. 읽거나 쓰기 전에 반드시 이 문서를 먼저 읽습니다.

**채용공고(JD)** — 필수. 컨텍스트에 아직 없으면 사용자에게 제공해 달라고 요청합니다.

**맞춤화한 이력서** — `{user_dir}/CareerLoop/artifacts-index.json`에서 이 회사와 직무에 대한 이력서 아티팩트가 있는지 확인합니다. 있으면 경험을 프레이밍하는 주된 출처로 사용합니다. 없으면:
> "이 직무에 맞춘 이력서가 아직 보이지 않습니다. 먼저 맞춤 이력서를 만들까요, 아니면 ExperienceLibrary에서 바로 브리프를 만들까요?"

**프로필** — `{user_dir}/CareerLoop/profile.md`를 읽어 차별점, 어조 선호, 상시 지침을 확인합니다.

**연락처 맥락** — 연락처는 더 이상 `applications[]` 안에 있지 않습니다. `tracker.json`에서 이 회사와 직무의 요약 행을 찾아 그 `contacts_file`을 가져오고 `{user_dir}/CareerLoop/` + 해당 경로(`contacts/<company-slug>.json`)를 불러옵니다. `contact_count: 0`이거나 `contacts_file`이 없는 행은 등록된 연락처가 없으므로 읽기를 건너뜁니다. 파일의 `contacts[]`에서 `application`이 행의 `application` 라벨(`"<company> — <role>"`)과 같은 항목만 남기고, 제시하기 전에 `name` 기준으로 중복을 제거합니다. 연락처가 있으면 브리프에 반영할 메모로 남깁니다(사실과 다르면 특정인에 대한 아부성 문구를 쓰지 않습니다).

### 2. 회사 조사

브리프를 만들기 전에, 적합성과 관련된 회사에 대한 **구체적이고 검증 가능한** 사실을 1–2개 찾습니다.
- 최근 제품 출시, 이니셔티브, 전략 방향
- JD에서 읽히는 팀/문화 신호
- 이 회사에 대한 노트 — 요약 행의 `detail_file`(`applications/<application_id>.json` → `notes[]`) 또는 프로필에 있음. 행의 `notes_count`가 `0`이면 상세 파일 읽기를 건너뜁니다.

막연한 칭찬은 쓰지 않습니다. 구체적인 신호가 없으면 브리프에 그렇게 밝힙니다. **`writer`**가 아부성 문구를 생략합니다.

### 2.5 문체 사전 점검 (브리프 작성 전)

`{user_dir}/CareerLoop/voice-profile.md`를 읽습니다.

- **`## User writing samples`** 또는 **`## User writing samples (launch)`** 아래에 사용자가 붙여넣은 블록(실질적인 발췌문)이 **없다면**, CoverLetterBrief를 만들기 **전에 먼저 질문**합니다.

> "자기소개서 초안을 쓰기 전에: **`writer`**가 사용자의 문체를 맞출 수 있도록 **최근 LinkedIn 게시글 2–5개** 또는 다른 짧은 업무 관련 글을 붙여넣어 주세요. **`/careerloop:launch`** 중에 스캔한 이력서/CV/자기소개서에서 얻은 **launch voice harvest** 힌트가 이미 있을 수 있지만, LinkedIn 글이 어조를 더 정확하게 다듬어 줍니다. 수집된 신호만으로 괜찮다면 **skip**(또는 "건너뛰기")이라고 답하세요. 중립적인 어조(**low** 문체 일치도)로 진행합니다."

- 사용자가 샘플을 **붙여넣으면**, `voice-profile.md`에 날짜가 붙은 `## User writing samples` 섹션을 추가합니다(다듬은 발췌문 + 한 줄 출처 메모).
- 사용자가 **skip**이라고 하면 그대로 진행하고, **`writer`**용 브리프에 **`voice_match: low`** 의도를 전달합니다.

**`## User writing samples`** 또는 **`## User writing samples (launch)`** 중 하나에 이미 실질적으로 붙여넣은 발췌문이 있으면 이 질문을 건너뜁니다.

### 3. CoverLetterBrief 작성 (여기서 전문은 쓰지 않음)

**`writer`**에게 넘길 구조화된 브리프를 조립합니다.

```markdown
## CoverLetterBrief
- **company**: …
- **role**: …
- **opening_hook_facts**: 불릿 목록 (이 직무+회사를 선택한 이유 — 사실만)
- **core_case_bullets**: EL 성과를 JD 역량에 매핑한 4–8개 불릿 (각 불릿: 사실 + 있으면 지표)
- **close_intent**: 한 줄 (절박함이 아니라 대화를 이어가려는 의도)
- **tone**: 자신감 있고 직접적인 어조; 격려보다 솔직함
- **banned**: 분량 채우기, 검증되지 않은 주장, "혁신적인 리더" 같은 상투적 표현
- **mirrored_jd_terms**: 자연스럽게 포함할 키워드 목록 (ATS)
- **length_target**: 짧은 단락 3–4개, 400단어 미만
- **optional_contact_reference**: 트래커에 있고 사용자가 확인한 경우에 한해 이름/직책만
```

### 4. writer 호출

- 에이전트 이름은 정확히 **`writer`**, 모드는 **`cover-letter`**를 사용합니다. 전체 **CoverLetterBrief**와 **`voice-profile.md`** / **`profile.md`** 경로를 전달합니다. 실패하면 한 번 재시도합니다.

### 5. 제시 및 확인

**`writer`**가 작성한 자기소개서를 보여주기 전에 날짜·경력 연수·도메인 표현을 ExperienceLibrary와 이력서에 대조합니다. 어긋난 문장이 있으면 **먼저 고친 뒤** 제시하고, 고친 내용은 한 줄로 알립니다(오류를 알면서 그대로 보여주지 않습니다). 그런 다음 전문을 그대로 보여주고 묻습니다.
> "괜찮아 보이나요? writer에게 어조 조정, 사례 교체, 분량 축소를 요청할 수 있습니다."

### 6. 아티팩트 저장

확인을 받은 뒤 자기소개서(**`writer`**의 출력)를 저장합니다.

**파일명 (호스트 / MCP 검증 오류 방지):** **ASCII 안전** 문자만 사용합니다. 하이픈 `-`을 쓰고, 엠 대시나 스마트 따옴표는 쓰지 않습니다. 회사명과 직무명은 **정제**합니다. `\ / : * ? " < > |`와 줄바꿈을 제거하고, 공백은 하나로 합치며, 기본 파일명 길이를 제한합니다(약 100자).  
**예시:** `Anthropic-PM-Claude-Code-Cover-Letter-2026-03-24.md`

- **파일명 형식:** `{SanitizedCompany}-{SanitizedRole}-Cover-Letter-{YYYY-MM-DD}.md`
- **경로:** `{user_dir}/` (호스트가 기대하는 경로 형식과 동일하게 — 보통 첨부된 구직 폴더 기준 상대 경로)
- **마크다운 파일은 별도의 도구 호출로 씁니다.** **`artifacts-index.json` 업데이트는 또 다른 호출에서** 유효한 JSON으로 합니다(문자열 안의 `"`는 이스케이프).

**파일 도구가 실패하면** (예: MCP `-32602` / 잘못된 인자): 오류 메시지를 이름으로 하는 파일을 **만들지 않습니다**. **자기소개서 전문**을 마크다운 코드 블록으로 출력하고 사용자에게 직접 저장하도록 안내합니다. `artifacts-index.json`은 파일이 성공적으로 저장된 경우에만 업데이트합니다.
- **`{user_dir}/CareerLoop/artifacts-index.json`에 쓰기**:

```json
{
  "id": "{uuid}",
  "type": "cover_letter",
  "filename": "{filename}",
  "path": "{user_dir}/{filename}",
  "target_company": "{company}",
  "target_role": "{role}",
  "date_created": "{today}",
  "source": "generated",
  "linked_resume": "{filename of tailored resume if used, else null}",
  "notes": "Assembled via CoverLetterBrief + writer"
}
```

`{user_dir}`에 다른 아티팩트 파일(PDF/DOCX)이 있으면, 저장 후 **`artifact-saved`** 워크플로를 한 번 실행합니다.

다음과 같이 확인합니다.
> "**{filename}**으로 저장했습니다."

### 7. 다음 단계 제안

사용자가 이 직무에 대한 지원(건)을 아직 기록하지 않았다면:
> "이 지원(건)을 추적할까요? 'yes'라고 답하거나 `/careerloop:track-application`을 실행하세요."
