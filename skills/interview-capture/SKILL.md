---
name: interview-capture
description: >
  옵트인 방식의 면접 후 캡처: 사용자 본인의 오디오(사용자 오디오만)를 전사하고,
  구조화된 핵심 내용을 추출하여 tracker.json을 갱신합니다. 고용주 정책 경고는
  한 번만 표시하며, 관할권/보관 기간은 스펙 §13.1을 따릅니다. 사용 가능한 경우
  로컬 mcp-transcribe MCP(Whisper 파일 STT)를 사용합니다. 에이전트가 아니라 도구와
  track-application 패턴을 조율하는 스킬입니다. /careerloop:interview-capture로도
  호출할 수 있습니다. Opt-in post-interview capture: transcribe the user's own
  audio (user audio only), extract structured takeaways, and update tracker.json.
  Triggers: "capture my interview", "transcribe my interview notes",
  "log interview from audio", "interview audio capture", "면접 녹음 캡처",
  "면접 메모 전사", "오디오로 면접 기록".
triggers:
  - "/interview-capture"
  - "/careerloop:interview-capture"
  - "capture my interview"
  - "transcribe my interview notes"
  - "log interview from audio"
  - "interview audio capture"
  - "면접 기록해줘"
  - "면접 녹음 정리"
  - "면접 오디오 기록"
  - "면접 녹취 전사해줘"
  - "녹음 파일로 면접 기록 남겨줘"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

## 범위 (§13.1)

- **사용자 오디오만.** 적절한 동의와 제품 범위 없이 고용주 측 음성을 캡처하거나 전사하지 않습니다. 그것은 계속 **범위 밖**입니다.
- **옵트인:** 사용자가 오디오로 캡처/기록하라고 **명시적으로** 요청하거나 **`/careerloop:interview-capture`**를 실행했을 때**만** 이 스킬을 실행합니다.
- **고용주 정책 경고(1회):** 일부 고용주는 면접 녹음을 **일절** 금지합니다. 첫 캡처 세션 전에 스펙 **§13.1**의 경고를 보여주고 확인(acknowledgment)을 받습니다. 다음 내용을 **`{user_dir}/CareerLoop/interview-capture-settings.json`**에 저장합니다.

```json
{
  "employer_warning_acknowledged": true,
  "acknowledged_at": "YYYY-MM-DD",
  "user_opted_in": true
}
```

**`employer_warning_acknowledged`**가 이미 **true**이면 전체 경고를 반복하지 않고, 한 줄 리마인더만 남깁니다.

- **보관 기간 / 관할권:** 스펙에 따라 GDPR/CCPA 관점으로 설명할 때 **`profile.md`**의 `location`을 사용합니다. 불분명하면 어떤 보관 기준을 적용할지 한 번만 묻고, 답을 **`interview-capture-settings.json`**에 **`retention_note`**로 저장합니다.

## 워크플로

### 1. `{user_dir}` 확인 및 게이트

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분할 레이아웃을 사용합니다. 읽기나 쓰기 전에 반드시 해당 문서를 읽습니다.

`CareerLoop/profile.md`와 `tracker.json`이 필요합니다. 없으면 사용자를 **`/careerloop:launch`**로 안내합니다.

### 2. 옵트인 및 경고

- **`interview-capture-settings.json`**이 없거나 **`employer_warning_acknowledged`**가 false이면 **고용주 정책 경고**를 출력하고, 사용자가 확인하면 설정 파일을 작성합니다.
- 사용자가 이번 세션의 캡처에 **옵트인**하지 않았다면 오디오를 처리하기 전에 확인합니다.

### 3. 지원 건 매칭

기록할 면접에 해당하는 **`application_id`**(또는 회사 + 직무)를 식별합니다. `tracker.json` → `applications[]`에서 `id`로 매칭하고, 실패하면 각 행의 `previous_ids`로 대체 매칭합니다. 매칭된 행의 `detail_file`, `contacts_file`, `application` 레이블을 보관해 둡니다. 5단계의 쓰기에 세 가지가 모두 필요합니다. 알 수 없으면 트래커를 갱신하기 전에 먼저 묻습니다.

### 4. 전사 (STT)

다음 순서로 전사본을 확보합니다. 어느 단계에서도 전사본을 지어내지 **않습니다**.

1. **사용자가 이미 전사본을 가지고 있음** — 그것을 사용합니다. 전사는 완전히 건너뜁니다.
2. **녹음 오디오 파일이 있고 `mcp-transcribe`가 아직 설치되지 않음** — `/careerloop:setup-transcribe` 실행을 제안합니다. 이 명령은 사용자가 터미널을 쓰지 않아도 설치와 등록을 해 줍니다. 사용자가 거절하면 3번 항목으로 넘어갑니다.
3. **녹음 오디오 파일 + `mcp-transcribe` MCP 사용 가능** — 정상 경로입니다. **`transcribe_file`**을 호출합니다.
   - 매칭된 트래커 행에서 실행 시점에 구성한 **`initial_prompt`**를 전달합니다. 회사, 직무, `contacts_file`의 면접관 이름과 함께 발화될 가능성이 있는 제품, 프로젝트, 약어를 포함합니다. 사용자 본인의 데이터로 구성하며, 공개 저장소로 배포되는 이 스킬에 실제 이름을 절대 하드코딩하지 않습니다. 트래커에 없는 공통 용어는 서버의 gitignore 처리된 `vocabulary.local.json`에 두고 `vocabulary_group`으로 선택할 수 있습니다.
   - 이것은 선택 사항이 아닙니다. 없으면 Whisper가 낯선 고유명사를 심하게 왜곡합니다. 벤더 이름은 흔한 영어 단어로, 성은 다른 성으로 바뀝니다.
   - 이전 호출이 실패한 경우에만 먼저 **`backend_info`**를 호출합니다. 이 호출은 잘못된 파일과 로드된 적 없는 백엔드를 구분해 줍니다.
4. **녹음 오디오 파일이 있고 MCP가 없으며 사용자가 설치를 거절함** — 세션 샌드박스에서 `faster-whisper`로 전사합니다. 최종 사용할 모델로 한 번만 수행합니다.
   - `medium.en`, `compute_type="int8"`, `cpu_threads=<nproc>`. 코어 2개에서 대략 실시간의 2배 속도입니다. 25분 녹음에 약 11분을 예상하고, 트래커와 준비 브리프 파일을 읽는 동안 백그라운드에서 시작합니다.
   - **`vad_filter=False`.** VAD는 무음 경계에서 발화를 잘라냅니다. 실제 23분짜리 스크리닝에서 프로세스에 대한 면접관의 답변을 포함해 약 28초를 조용히 제거했습니다.
   - `initial_prompt`는 3번 항목과 똑같이 구성합니다.
   - 더 작은 모델로 먼저 정찰용으로 돌린 뒤 더 큰 모델로 다시 돌리지 **않습니다**. 소요 시간만 두 배가 되고 남는 결과가 없습니다.
5. **녹음 대신 라이브 구두 요약** — 사용자가 업로드하지 않고 말로 설명하길 원하면 라이브 마이크 도구가 필요합니다. `mcp-transcribe`에는 의도적으로 그 기능이 없습니다. 사용자에게 휴대폰이나 Mac으로 녹음한 뒤 파일 경로를 알려달라고 요청합니다.
6. **사용 가능한 것이 없음** — 붙여넣은 전사본을 요청합니다.

**화자 분리(Diarization):** 이 백엔드들은 어느 것도 화자를 구분해 주지 않습니다. 내용으로 발화를 귀속시킵니다. 질문하는 쪽인지 답하는 쪽인지, 자기 언급, 이름, 방언과 관용구 단서 등을 활용하고, 확신이 낮은 구간은 조용히 추측하지 말고 대괄호로 표시합니다.

### 5. 구조화 및 트래커 작성

전사본(사용자 측만)에서 다음을 추출합니다.

- 전반적인 분위기 / 진행 상황
- 단계, 참석자(사용자 진술 기준)
- 주제, 예상 밖 내용, 위험 신호 / 긍정 신호
- 약속된 후속 조치
- 다음 라운드나 결과에 대한 힌트

**`track-application`**과 같은 패턴으로 다중 파일 트랜잭션으로 작성합니다.

1. **노트** — 상세 파일 **`CareerLoop/applications/<application_id>.json`** → `notes[]`에 `{ "date": "YYYY-MM-DD", "text": "[capture] ..." }`를 추가합니다. 기존 항목은 절대 덮어쓰지 않습니다. 그런 다음 요약 행의 **`notes_count`**를 새 배열 길이로 설정합니다.
2. **단계** — 캡처가 상세 파일의 `stage_history[]`에 아직 없는 면접을 기록하는 경우, 그 단계 항목을 추가합니다(또는 일치하는 기존 항목의 `post_notes`를 채웁니다). 그런 다음 요약 행의 **`stage_count`**, **`latest_stage`**, **`latest_stage_date`**를 설정하고, 단계가 바뀌면 **`status`**도 갱신합니다.
3. **연락처** — 사용자가 면접관 이름을 언급하면 **`CareerLoop/contacts/<company-slug>.json`**에 행의 `application` 레이블을 각 항목에 붙여 추가하거나 갱신하고, 그 파일의 `contact_count`와 요약 행의 `contact_count`를 다시 계산합니다. 행에 `contacts_file`이 없었다면 설정합니다.
4. **행 필드** — 사용자가 후속 조치를 약속했다면 `tracker.json` 요약 행의 **`next_step`**과 **`follow_up_date`**를 갱신합니다.

각 JSON 파일을 프로그램으로 로드하고 다시 덤프(`json.load` / `json.dump`, `indent=2`, `ensure_ascii=False`)한 뒤 다시 로드해 검증합니다. 쓰기 후 `notes_count`와 `stage_count`가 상세 배열과 일치하는지, `latest_stage`가 마지막 `stage_history` 항목과 일치하는지 확인합니다.

### 6. 아티팩트 (필수)

아래 두 파일은 완료 정의의 일부입니다. 요청받지 않아도 작성합니다.

1. **전사본** — (`CareerLoop/` 폴더 안이며 `{user_dir}` 바로 아래가 아니다) `{user_dir}/CareerLoop/interview-capture/{application_id}-{YYYY-MM-DD}-transcript.md`
   타임코드가 붙은 ASR 세그먼트가 아니라 화자 라벨이 붙은 블록(`**Name:** text`)으로 작성합니다. 헤더에는 날짜, 참석자, 단계, 소요 시간, 캡처가 양쪽 채널을 다루는 경우의 동의/범위 메모, 대괄호 텍스트를 설명하는 정확도 메모를 담습니다. 대화가 깔끔하게 구분되는 곳에는 `## Topic: ...` 헤더를 둡니다.
2. **디브리프** — `{user_dir}/interview-debrief/{company}_{interviewer-first-name}_{M.D.YY}.md`
   다섯 개 섹션: 전체 평가(Overall Assessment, 다음 단계 진출 가능성에 대한 솔직한 판단 포함), 잘된 점(What Went Well), 아쉬웠던 점(What Could Have Gone Better), 확보한 직무 및 회사 인텔리전스(Role & Company Intelligence Gathered), 다음 단계(Next Steps). 푸터: 생성 날짜, 원본 전사본 경로, 준비 브리프 경로, 다음 액션.

해당하는 `interview-prep/` 브리프가 있으면 핵심 인텔리전스를 그 브리프에 **Debrief** 섹션으로도 반영하여 다음 라운드가 그 내용에서 출발하게 합니다.

## 가드레일

- 성과를 요약할 때는 격려보다 **정직함**이 우선입니다.
- 다자간 녹음을 주장하지 **않습니다**. 다른 화자의 발언을 사용자 기억에서 인용한 경우 전사본을 **사용자 채널만(user channel only)**으로 표기합니다. 사용자가 양쪽 채널 녹음을 명시적으로 승인한 경우에는 전사본 헤더에 그 사실을 밝히고 파일을 비공개 작업 자료로 표시합니다.
- 디브리프를 파일이 아닌 채팅 본문으로 전달하지 **않습니다**. 산출물은 파일입니다.
