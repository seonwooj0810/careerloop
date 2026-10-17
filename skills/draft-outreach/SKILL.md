---
name: draft-outreach
description: "사용자의 의도와 networking-strategist 핸드오프(선택)를 바탕으로 바로 보낼 수 있는 아웃리치 문안(LinkedIn, 이메일, InMail)을 작성합니다. writer를 호출합니다. 메일/캘린더 커넥터가 있으면 contact-context와 ContactContextBrief를 통해 이전 커뮤니케이션 이력을 기본으로 반영하며, 사용자가 건너뛰거나 수신자가 지정되지 않은 일반/콜드 메시지인 경우는 예외입니다. Produces send-ready outreach copy (LinkedIn, email, InMail) from user intent and optional networking-strategist handoffs. Invokes writer. Prior communication history is folded in by default when mail/calendar connectors exist via contact-context and ContactContextBrief."
triggers:
  - "draft outreach"
  - "write a linkedin message"
  - "cold email to"
  - "connection request note"
  - "inmail draft"
  - "/careerloop:draft-outreach"
  - "아웃리치 초안"
  - "링크드인 메시지 써줘"
  - "콜드 메일 써줘"
  - "연결 요청 메모 써줘"
  - "인메일 초안 써줘"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

> **경력 연수 인용 규칙:** 경력·도메인 연수를 말할 때는 ExperienceLibrary의 날짜로 직접 계산한 값을 쓴다. 이력서나 프로필의 표기가 계산값과 다르면 계산값을 쓰고 불일치를 한 줄로 알린다(예: 이력서 "5년" ↔ 날짜상 4년 7개월).

**`writer`**를 **`draft-outreach`** 모드로 호출합니다.

## 호출

- 에이전트 이름은 정확히 **`writer`**를 사용합니다. 호출에 실패하면 같은 이름으로 한 번 재시도합니다.

## 워크플로

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분리 레이아웃을 사용합니다. 읽기/쓰기 전에 반드시 이 문서를 읽습니다.

0. **이전 커뮤니케이션 이력 (보강 — 지정된 수신자에게는 기본 적용):** **특정 인물** 또는 **회사의 알려진 연락처**에게 보내는 아웃리치는 호스트가 허용하는 한 추측이 아니라 **실제 메일/캘린더 맥락**에 근거해야 합니다.

   1. **ContactContextBrief**가 채팅에 **이미** 있으면 그대로 사용합니다(전체 블록을 **`writer`**에 전달).
   2. 그렇지 않고 **이 세션**에 **Gmail/M365 받은편지함** 및/또는 **캘린더** 도구가 보이면, 사용자가 이력을 **건너뛰라**고 명시적으로 말하거나("no prior thread", "brand-new contact", "template only" / "이전 스레드 없음", "처음 연락하는 사람", "템플릿만") 아직 지정된 수신자가 **없는** 순수 일반 요청이 아닌 한, **`writer`**를 호출하기 **전에** **`contact-context`**를 끝까지 실행합니다. 스레드를 **지어내지 않습니다.**
   3. 그 외(세션에 메일/캘린더 도구가 **없음**)에는 **`writer`**를 그대로 호출하되 한 줄을 전달합니다: **`Prior communication:`** *not retrieved — inbox/calendar tools not available in this session; do not imply prior email or meetings.*

   사용자가 메일을 **보냈다**고 하는데 주소가 틀렸거나 검색 결과가 비어 있으면 **`contact-context`**의 **"User said they sent"** 절차를 따릅니다. **`email_address_notes`**에 주소 후보가 담깁니다. **`calendar_notes`**, **`upcoming_meetings`**, **`warm_networking`**이 있으면 핸드오프에 포함합니다. **`upcoming_meetings`**가 비어 있지 않으면 아웃리치가 콜드 첫 접촉처럼 읽히지 **않아야** 합니다.

1. `{user_dir}/CareerLoop/profile.md`와 **`{user_dir}/CareerLoop/voice-profile.md`**를 읽습니다(없으면 스텁 생성).
2. **보이스 사전 점검:** `voice-profile.md`의 **`## User writing samples`** 또는 **`## User writing samples (launch)`** 아래에 사용자가 붙여넣은 블록(실질적인 발췌문)이 **없으면**, **`writer`**를 호출하기 **전에** 먼저 묻습니다. **LinkedIn 게시물 2–5개** 또는 짧은 업무 글을 붙여넣어 달라고 요청하고, 선택 사항인 **런치 보이스 수집**(디스크의 이력서/CV/자기소개서 텍스트 활용)을 안내하며, 사용자는 **skip**이라고 답할 수 있습니다(보이스 일치도 **낮음**). 붙여넣으면 날짜가 붙은 **`## User writing samples`** 섹션을 추가합니다. 샘플이 이미 있으면 이 질문은 건너뜁니다.
3. 대화에서 **채널**, **수신자 유형**(알려진 경우 직책/회사), **목적**(정보 대화, 추천 안부 확인, 행사 후 인사), 그리고 **StrategistHandoff**, **ContactContextBrief** 또는 사용자가 붙여넣은 사실을 파악합니다.
4. 구조화된 브리프를 **`draft-outreach`** 모드의 **`writer`**에 전달합니다. **필수:** 가능하면 전체 **`## ContactContextBrief`** 마크다운 블록을 포함하고, 없으면 0단계의 **`Prior communication:`** 대체 문구를 포함합니다. **`writer`**는 **summary**, **open_loops**, **hooks_for_writer**, **calendar_notes**, **upcoming_meetings**, **warm_networking**이 있을 때 이를 초안에 녹여야 합니다. **`agents/writer/AGENT.md`**를 참조하세요. 이 스킬에서 최종 문안을 직접 작성하지 **않고** 위임합니다.
5. **`writer`**의 출력을 보여줍니다(제공된 경우 여러 버전 포함). 커넥터가 있으면 따뜻한 스레딩을 지원한다는 점을 안내합니다.
6. **발송 확인 + 자동 트래킹:** 문안을 보여준 뒤 다음과 같이 말합니다.
   > "발송하셨으면 알려주세요. 트래커에 기록해 드리겠습니다."

   사용자가 확인하면(예: "sent", "I sent it", "done", "sent it just now" / "보냈어요", "발송했어요", "완료") [references/tracker-schema.md](../../references/tracker-schema.md)의 다중 파일 트랜잭션을 기록합니다. 한 파일만 갱신하고 나머지를 오래된 상태로 두면 안 됩니다.
   - `{user_dir}/CareerLoop/tracker.json`(요약 행만)을 읽고 같은 회사의 행을 찾습니다
   - 일치하는 행이 있으면 `{user_dir}/CareerLoop/` + 해당 행의 `contacts_file`(`contacts/<company-slug>.json`)을 로드합니다. 경로는 행에서 가져오며 슬러그를 직접 만들어 내지 않습니다. `name`이 수신자와 일치하고 **그리고** `application`이 행의 `application` 라벨과 같은 항목을 찾아 해당 연락처의 `interactions[]`에 추가합니다.
     ```json
     { "date": "YYYY-MM-DD", "type": "linkedin | email", "notes": "Sent outreach: {one-line summary of message objective}" }
     ```
     행에 `contacts_file`이 없거나 해당 인물이 아직 없으면, 스키마의 **Adding or updating a contact** 규칙에 따라 연락처를 추가합니다(필요하면 `contacts/<slug>.json` 생성, `application`을 행의 라벨로 설정, 파일과 행 양쪽의 `contact_count` 재계산).
     또한 `{user_dir}/CareerLoop/` + 해당 행의 `detail_file`(`applications/<application_id>.json`)의 `notes[]`에 `{ "date": "YYYY-MM-DD", "text": "Outreach sent via {channel} to {recipient} — {objective}" }`를 추가한 뒤, 행의 `notes_count`를 새 배열 길이로 설정합니다
     요약 행의 `next_step`을 "Await response"로 갱신합니다
   - 일치하는 지원 건이 없지만 수신자가 목표 회사 소속이면: `networking.json`의 `networking[]`에 새 네트워킹 항목을 기록할지 제안합니다
   - 확인 메시지: `기록 완료: {company}의 {recipient}에게 보낸 아웃리치 ({channel}) — {date}`

## 참고

- 사용자에게 전략 관련 질문만 있으면 먼저 **`networking-strategy`** / **`network-map`**을 안내하고, 문안이 필요할 때 이 스킬로 돌아옵니다.
