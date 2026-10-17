---
name: linkedin-post-analytics
description: >
  사용자 본인의 LinkedIn 게시물 분석 데이터를 읽기 전용으로 스냅샷하여 networking.json의 networking 항목에 기록합니다.
  브라우저 제어(Claude in Chrome MCP 또는 승인된 computer/browser use)가 필요합니다. 스케줄 실행에 적합합니다.
  Read-only snapshot of the user's own LinkedIn post analytics into networking.json networking entries.
  Requires browser control (Claude in Chrome MCP or approved computer/browser use). Scheduled-friendly.
triggers:
  - "linkedin post analytics"
  - "linkedin-post-analytics"
  - "snapshot linkedin analytics"
  - "append linkedin analytics to tracker"
  - "/careerloop:linkedin-post-analytics"
  - "링크드인 게시물 분석"
  - "링크드인 분석 스냅샷"
  - "링크드인 분석을 트래커에 추가해줘"
  - "링크드인 게시물 지표 가져와줘"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

## 게이트 (가장 먼저 실행)

1. **패턴:** 이 연동에는 [CONNECTORS.md](CONNECTORS.md)의 **3단계**를 적용합니다. **탐색(Discover)** — 여기에는 표준 LinkedIn MCP가 없습니다. **설정(Configure)** — 사용자가 호스트 브라우저에서 **LinkedIn에 로그인**된 상태여야 합니다(로그인은 **사용자**가 직접 합니다). **브라우저 접근(Browser access)** — **Claude in Chrome** 및/또는 **computer use**를 **묻습니다**(**둘 다 아님** / 하나 / 둘 다). **둘 다 아니거나** 도구가 없으면 **중단**합니다. 선택한 모드에 대한 **읽기 전용** 승인 없이 스크래핑하지 **않습니다.**
2. **`{user_dir}`:** 구직 폴더를 확인합니다. 네트워킹 데이터는 `{user_dir}/CareerLoop/networking.json`입니다.
3. **스케줄 무인 실행:** 이번 호출이 `/schedule`에서 왔거나 사용자가 무인 실행을 요청했다면, 브라우저/도구에 대한 대화형 질문을 하지 **않습니다.** `{user_dir}/CareerLoop/profile.md`의 `## LinkedIn` 아래에 이전 동의가 이미 저장되어 있을 때만 계속합니다.
   - `LinkedIn slug: <value>`
   - `LinkedIn analytics permission: granted`
   - `LinkedIn analytics mode: chrome | computer | either`
   이 중 하나라도 없으면, 대화형 설정을 한 번 실행하라는 간결한 설정 안내 메시지와 함께 중단합니다.

## 도구 호출 가이드

**우선순위:** **대화형** 실행에서는 사용자가 승인한 모드(`chrome`, `computer`, `either`)를 사용합니다. 모드가 `either`이면 **Claude in Chrome**을 먼저 시도하고, 그다음 computer를 시도합니다.

**Claude in Chrome 경로 (엄격한 타입 지정 파라미터):**
- 먼저 올바른 타입의 값으로 `tabs_context_mcp`를 시도합니다(예: `createIfEmpty`는 문자열 `"true"`가 아니라 불리언 `true`여야 합니다).
- 컨텍스트 초기화가 계속 실패하면 `tabs_create_mcp`를 호출한 뒤 `tabs_context_mcp`를 한 번 재시도합니다.
- 그다음 `navigate`로 LinkedIn URL에 이동합니다.
- `tabId` 타입이 잘못되어 `navigate`가 실패하면, 숫자 `tabId`(따옴표 없는 정수)로 한 번 재시도합니다.
- 그래도 실패하면 다음 메시지와 함께 중단합니다: "Claude in Chrome이 유효한 탭 컨텍스트를 초기화하지 못했습니다. Chrome을 열고 LinkedIn에 로그인되어 있는지 확인한 뒤 `linkedin-post-analytics`를 다시 실행해 주세요."

**순환 폴백 루프 금지:**
- 실패한 단계당 재시도는 최대 한 번입니다.
- 도구 사이를 반복해서 오가지 않습니다.
- 선택한 모드가 실패하면, 저장/승인된 모드가 `either`일 때만 대체 모드를 시도합니다.

## 목표

**본인** 게시물에 한해서: 최근 활동을 열고, 게시물별 분석 데이터를 수집하여 **오늘** 스냅샷을 `networking.json`(`networking[]`)에 추가하고, 게시물당 한 줄 요약을 보고합니다.

## 입력 (없으면 한 번만 질문)

- **프로필 경로:** `{user_dir}/CareerLoop/profile.md` → `## LinkedIn` → `LinkedIn slug:`를 읽습니다. 값이 있으면 사용합니다. 없거나 비어 있으면 한 번 묻고, 진행하기 전에 `profile.md`의 해당 제목 아래에 저장합니다.
- **동의 상태 (저장):** 대화형 실행에서 없으면 한 번 묻고 저장합니다.
  - `LinkedIn analytics permission: granted | denied`
  - `LinkedIn analytics mode: chrome | computer | either`
  스케줄 실행에는 `permission: granted`와 모드가 필요합니다.
- **기간:** 기본값은 **최근 약 60일** 게시물입니다(사용자가 "몇 달"이라고 밝히면 그 기간)

## 단계

1. 위의 **최근 활동 / 공유** URL로 이동합니다. 사용자는 이미 로그인되어 있어야 하며, LinkedIn이 재인증을 요구하면 **중단**하고 사용자에게 알립니다.
2. **읽기 전용:** 게시, 반응, 댓글, DM을 하지 않습니다. 게시물의 분석 컨트롤이 없거나 패널에 오류가 나면 **기록하고 해당 게시물은 건너뜁니다.**
3. 기간 내 각 게시물에 대해: **게시물 URL**(`…/feed/update/urn:li:activity:…`), **게시일**(최선의 추정), **주제**(짧은 라벨)를 수집합니다. **View analytics**(막대 차트)를 열어 노출 수, 도달 회원 수, 반응, 댓글, 리포스트, 저장, LinkedIn 내 전송, 게시물을 통한 프로필 조회자, 팔로워 증가, 링크 방문, 그리고 **표시되는 경우** 상위 오디언스(산업 / 직급 / 회사 규모)를 읽습니다.
4. `networking.json`을 읽습니다. 각 게시물에 대해:
   - `networking`에 `type: "linkedin_post"`이고 `url`이 일치하는 항목이 있으면: `analytics_history`에 객체 하나를 추가합니다: `{ "date": "YYYY-MM-DD", …metrics… }` (필드 이름은 아래와 동일).
   - 없으면 새 항목을 만듭니다: `id` = 다음 `net-NNN`(기존 최대값 + 1), `type: "linkedin_post"`, `description`, `url`, `date_posted`, `analytics_history: [ { … } ]`, `notes`(예: 자동 발견 + 날짜), `outcome: "active"`.
5. `networking.json`을 다시 씁니다. 관련 없는 키(`recruiter_relationships` 등)는 보존합니다.

**`analytics_history` 객체 (알 수 없으면 0 또는 `[]` / `"—"` 사용):**

`impressions`, `members_reached`, `reactions`, `comments`, `reposts`, `saves`, `sends`, `profile_viewers_from_post`, `followers_gained`, `link_visits`, `links` (배열), `top_audience`: `{ "industry", "seniority", "company_size" }` (문자열).

## 보고

게시물당 한 줄: `[주제], 노출 수: X(+Y), 반응: X(+Y), 댓글: X(+Y), 리포스트: X(+Y), 링크 방문: X(+Y), [날짜]`. 직전 스냅샷 대비 **일 단위 증가폭이 의미 있는**(Y) 게시물은 표시합니다. 기간 내 **게시물이 없으면** 그렇게 알리고 종료합니다.

## 사용자를 위한 실행 주기 안내

권한을 부여하고 모드를 저장한 사용자에게는 아침 **`/schedule`** 실행이 지원됩니다. 대부분의 구직 가시성 루프에는 주 1회 또는 격주 주기면 충분하지만, 네트워킹을 집중적으로 진행하는 기간에는 매일 실행해도 무방합니다.
