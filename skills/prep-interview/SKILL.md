---
name: prep-interview
description: >
  특정 지원 건 또는 직무에 대한 전체 면접 준비: 회사 및 뉴스 맥락, 단계별 질문(recruiter, hiring manager, technical, panel, executive, final), StoryCorpus에서 가져온 스토리 근거(ExperienceLibrary 폴백 포함). 텍스트 전용이며, 사용자가 타이핑 대신 음성으로 말하면 호스트 STT 전사본 붙여넣기를 받습니다. 브리프를 CareerLoop/interview-prep/ 아래에 저장하고 tracker.json에 [prep] 노트를 기록합니다. /careerloop:prep-interview로도 호출할 수 있습니다.
  Full interview preparation for a specific application or role: company and
  news context, stage-specific questions (recruiter, hiring manager, technical,
  panel, executive, final), and story evidence retrieved from StoryCorpus
  (with ExperienceLibrary fallback). Text-only; accepts a pasted host-STT
  transcript if the user dictates instead of typing.
  Saves a brief under CareerLoop/interview-prep/ and logs a [prep] note in
  tracker.json. Also invocable via /careerloop:prep-interview.
triggers:
  - "/prep-interview"
  - "/careerloop:prep-interview"
  - "prep me for my interview"
  - "prep for my interview"
  - "interview prep for"
  - "prepare for my interview"
  - "recruiter call tomorrow"
  - "recruiter screen with"
  - "phone screen with"
  - "hiring manager interview"
  - "HM interview"
  - "mock prep for"
  - "면접 준비시켜줘"
  - "면접 준비"
  - "내일 면접 준비해줘"
  - "리크루터 통화 내일이야"
  - "리크루터 스크리닝 준비"
  - "전화 면접 준비"
  - "채용 담당자 면접 준비"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

> **경력 연수 인용 규칙:** 경력·도메인 연수를 말할 때는 ExperienceLibrary의 날짜로 직접 계산한 값을 쓴다. 이력서나 프로필의 표기가 계산값과 다르면 계산값을 쓰고 불일치를 한 줄로 알린다(예: 이력서 "5년" ↔ 날짜상 4년 7개월).

## 워크플로

### 1. `{user_dir}` 확인 및 게이트

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분리 레이아웃을 사용합니다. 읽기/쓰기 전에 반드시 이 문서를 읽습니다.

`CareerLoop/profile.md`, `ExperienceLibrary.json`, `tracker.json`이 필요합니다. 없으면:

> 먼저 `/careerloop:launch`를 실행하여 CareerLoop를 초기화해 주세요.

스토리 코퍼스 게이트:
- 우선 소스: `CareerLoop/StoryCorpus.json`.
- 없으면 `mine-stories`를 먼저 실행하거나 제안합니다.
- 사용자가 바로 계속하길 원하면 `ExperienceLibrary.json` 폴백으로 진행하고, 스토리별 신뢰도가 더 낮다는 점을 명확히 표시합니다.

### 2. 대상 식별

사용자 메시지 또는 트래커에서:

- **`application_id`**가 주어지면 우선 사용하고, 아니면 **회사** + **직무**를 `tracker.json`의 `applications[]`와 대조합니다. `application_id`가 어떤 행의 `id`와도 일치하지 않으면, 일치 없음으로 판단하기 전에 각 행의 `previous_ids`를 확인합니다. 이전 id로 저장된 준비 브리프도 계속 찾을 수 있습니다.
- 일치한 행의 `detail_file`, `contacts_file`, `application` 라벨을 보관합니다. 6단계의 쓰기에 필요합니다.
- 이전 단계 이력과 노트는 행의 `detail_file`(`CareerLoop/applications/<application_id>.json`)에서 가져옵니다. `tracker.json`에는 `latest_stage`와 `latest_stage_date`만 있습니다. `contacts_file`은 면접관 배경이 필요할 때만 로드하며, `contacts[]`를 `application`이 행의 `application`과 같은 항목으로 필터링합니다.
- 모호하면 짧은 구분 질문을 하나 합니다.

없으면 수집합니다.

- **`interview_stage`:** `recruiter` | `hiring_manager` | `technical` | `panel` | `executive` | `final` (기본값: 표현에서 추론. recruiter call / phone screen → `recruiter`).
- 선택: **면접관** 이름/직함, **면접 날짜**, JD 텍스트 또는 붙여넣기.

### 3. 선택적 음성 입력

텍스트 전용입니다. 사용자가 타이핑하는 대신 호스트 수준 음성 인식(STT)의 **전사본**을 붙여넣으면, **`interview-coach`**로의 핸드오프에 `user_audio_transcript`로 전달합니다.

### 4. 맞춤 스토리 검색

interview-coach를 호출하기 전에 다음 입력으로 `story-retrieval`을 실행합니다.

- `application_id` 또는 `company` + `role`
- `interview_stage`
- 선택: JD 및 면접관 컨텍스트

반환된 8–12개의 선별 스토리를 주요 면접 근거 페이로드로 사용합니다.

### 5. **interview-coach** 호출

다음 입력으로 **`agents/interview-coach/AGENT.md`**를 읽고 따릅니다.

- `mode`: **`prep`**
- `interview_stage` (필수)
- `application_id` 또는 `company` + `role`
- 선택: `interviewer`, JD, `interview_date`, `user_audio_transcript`
- `story-retrieval`에서 받은 `selected_stories` 페이로드

에이전트 이름은 정확히 **`interview-coach`**를 사용합니다.

### 6. 결과 저장

코치 콘텐츠가 생성된 뒤:

1. **디렉터리:** `{user_dir}/CareerLoop/interview-prep/`가 존재하는지 확인합니다.
2. **파일:** 에이전트의 경로 규칙(회사 슬러그, 단계, 날짜 = 사용자가 파일명 접미사용 면접 날짜를 지정하지 않는 한 현지 기준 오늘)에 따라 전체 준비 브리프를 마크다운으로 저장합니다.
3. **상세 파일:** 일치한 행의 `detail_file`인 `{user_dir}/CareerLoop/applications/<application_id>.json`의 `notes[]`에 다음 객체를 추가합니다.

```json
{
  "date": "YYYY-MM-DD",
  "text": "[prep] Interview prep brief saved: CareerLoop/interview-prep/{filename}.md (stage: {stage})."
}
```

기존 노트 항목을 덮어쓰거나 순서를 바꾸지 않습니다.

4. **요약 행:** 일치하는 `tracker.json` → `applications[]` 행의 `notes_count`를 상세 파일의 새 `notes[]` 길이로 설정합니다. 이 노트는 단계를 추가하지 않으므로 `stage_count`, `latest_stage`, `latest_stage_date`, `status`는 건드리지 않습니다.

두 JSON 파일을 프로그램적으로 로드하고 다시 덤프(`json.load` / `json.dump`, `indent=2`, `ensure_ascii=False`)한 뒤, 다시 로드하여 `notes_count`가 상세 배열과 일치하는지 검증합니다. 일치하는 지원 건이 없으면 두 쓰기를 모두 건너뛰되, 분명한 파일명으로 `interview-prep/` 아래에 파일은 저장하고, 필요하면 `/careerloop:track-application`으로 연결하라고 사용자에게 안내합니다.

### 7. 마무리

텍스트 연습 세션을 위해 **`/careerloop:mock-interview`**를 제안합니다. 출시되지 않은 기능을 주장하지 않습니다.
