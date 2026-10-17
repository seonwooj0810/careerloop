---
name: mock-interview
description: >
  설정 가능한 모드(guided, random, adaptive), 단계(recruiter, hiring manager, technical, panel, executive, final), 분위기(supportive부터 bored까지)로 모의 면접 세션을 시작합니다. 모드나 분위기를 생략하면 시스템이 기본값을 선택하고 알려줍니다. interview-coach에 위임합니다. 텍스트 전용입니다. /careerloop:mock-interview로도 호출할 수 있습니다.
  Starts a mock interview session with configurable mode (guided, random,
  adaptive), stage (recruiter, hiring manager, technical, panel, executive,
  final), and vibe (supportive through bored). If mode or vibe are omitted,
  the system selects defaults and announces them. Delegates to interview-coach.
  Text-only. Also invocable via /careerloop:mock-interview.
triggers:
  - "/mock-interview"
  - "/careerloop:mock-interview"
  - "mock interview"
  - "practice interview"
  - "run a mock interview"
  - "interview practice"
  - "모의 면접"
  - "면접 연습"
  - "모의 면접 해줘"
  - "면접 연습하고 싶어요"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

## 워크플로

### 1. `{user_dir}` 확인 및 게이트

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분리 레이아웃을 사용합니다. 읽기/쓰기 전에 반드시 이 문서를 읽습니다.

`prep-interview`와 동일합니다. `CareerLoop/profile.md`, `ExperienceLibrary.json`, `tracker.json`이 필요합니다. 단, 사용자가 붙여넣은 JD로 일반 모의 면접만 원하는 경우는 예외입니다(이때도 최소한 profile + EL은 필요하며, 트래커가 비어 있으면 최소 컨텍스트 노트를 만듭니다).

### 2. 파라미터 (없으면 한 번만 질문)

| 파라미터 | 값 |
| --- | --- |
| **mock_mode** | `guided` \| `random` \| `adaptive` |
| **interview_stage** | `recruiter` \| `hiring_manager` \| `technical` \| `panel` \| `executive` \| `final` |
| **vibe** | `supportive` \| `neutral` \| `challenging` \| `antagonistic` \| `bored` |
| **target** | `application_id` 또는 회사 + 직무 (일반 연습이면 선택) |

#### 2.1 모드나 분위기가 지정되지 **않은** 경우 — **시스템 선택**

모델은 시작 전에 구체적인 `mock_mode`와 `vibe`를 **반드시** 선택해야 하며, 첫 마디에서 **절대** 암묵적으로 두지 않습니다.

- **`mock_mode`(사용자가 생략한 경우):** **`adaptive`**를 사용합니다(학습과 피드백의 기본값). 사용자가 "surprise me", "mix it up"(또는 "알아서 해줘", "랜덤으로 섞어줘")처럼 요청했다면 `random`을 **무작위로** 고르고 그렇게 했다고 밝힙니다.
- **`vibe`(사용자가 생략한 경우):** **`neutral`**을 사용합니다. 사용자가 "surprise" / "mix it up"(또는 "알아서 해줘", "랜덤으로 섞어줘")처럼 요청했다면 허용된 다섯 값 중 **하나**를 **무작위로** 고르고 밝힙니다.
- **`interview_stage`(사용자가 생략한 경우):** 진행 중인 지원 건의 **`tracker.json` 요약 행**에서 추론합니다. 행의 `status`, `latest_stage`, `latest_stage_date`로 아무것도 열지 않고 다음 유력 단계를 알 수 있습니다(예: `phone_screen` / `latest_stage: "recruiter"` → **`recruiter`**, 그 외에는 **`hiring_manager`**). 사용자가 실제 면접 이력을 기준으로 연습하길 요청할 때만, 그리고 그 지원 건 하나에 대해서만 행의 `detail_file`(`applications/<application_id>.json`)을 읽습니다. 지원 건 컨텍스트가 없으면 기본값은 **`hiring_manager`**입니다.
- 첫 질문 전에 한 줄로 **알립니다.** 예:  
  `선택됨: mode=adaptive, vibe=neutral, stage=hiring_manager (기본값 — 다르게 원하시면 말씀해 주세요).`

**Recruiter 연습:** 사용자가 **recruiter** 또는 **phone screen** 연습을 요청하면 `interview_stage`를 **`recruiter`**로 설정합니다.

### 3. **interview-coach** 호출

다음 입력으로 **`agents/interview-coach/AGENT.md`**를 읽고 따릅니다.

- `mode`: **`mock`**
- `mock_mode`, `vibe`, `interview_stage`
- 대상 컨텍스트(지원 건 id, 회사, 직무, 있으면 JD)

사용자가 종료하거나 에이전트 지침에 따른 자연스러운 마무리 지점에 이를 때까지 채팅에서 모의 면접을 **한 턴씩** 진행합니다.

### 4. 선택적 트래커 노트

사용자가 기록을 요청하거나(또는 후속 조치에 분명히 도움이 될 때)에만, 노트를 추가하는 **다중 파일 트랜잭션**을 [references/tracker-schema.md](../../references/tracker-schema.md)에 따라 기록합니다. 한 파일만 편집하고 다른 파일을 건너뛰면 안 됩니다.

1. `tracker.json`에서 해당 지원 건의 요약 행을 찾아(`id`로 일치시키고, id가 이전 브리프에서 온 것이면 `previous_ids`를 확인) `detail_file`을 가져옵니다.
2. 해당 파일의 `notes[]`에 추가합니다. 기존 항목을 덮어쓰거나 순서를 바꾸지 않습니다.
   ```json
   { "date": "YYYY-MM-DD", "text": "[mock] {interview_stage} mock — {mode}/{vibe}, {one-line takeaway}" }
   ```
3. 요약 행의 `notes_count`를 새 배열 길이로 설정합니다.

모의 면접은 실제 면접이 아닙니다. `stage_history[]`에 추가하지 **말고**, `status`, `latest_stage`, `latest_stage_date`를 건드리지 않습니다.

두 파일을 프로그램적으로 로드하고 다시 덤프(`json.load` / `json.dump`, `indent=2`, `ensure_ascii=False`)한 뒤 다시 로드하여 검증합니다. 이 JSON을 손으로 편집하다가 파일이 손상된 적이 있습니다.
