# 커넥터

## 도구 참조 방식

플러그인 파일은 `~~category`를 해당 카테고리에서 사용자가 연결한 도구의 자리표시자로 씁니다. 예를 들어 `~~project tracker`는 Asana, Linear, Jira 등 MCP 서버가 있는 모든 프로젝트 트래커를 뜻할 수 있습니다.

플러그인은 **도구 중립적**입니다. 특정 제품이 아니라 카테고리(채팅, 프로젝트 트래커, 지식 베이스 등)로 워크플로를 설명합니다.

**이 저장소의 `.mcp.json`**은 **Google** 메일/캘린더(**Gmail**, **Google Calendar**) 또는 대체 채널인 **Microsoft 365**를 위한 Anthropic **HTTP MCP** 서버를 선언할 수 있습니다(예: `https://gmail.mcp.claude.com/mcp`, `https://gcal.mcp.claude.com/mcp`, 키 **`ms365`** 아래의 `https://microsoft365.mcp.claude.com/mcp`). 프로젝트 파일을 읽는 호스트가 **Connectors**와 같은 방식으로 도구를 로드하게 하려는 것이며, JSON에 토큰은 **절대** 넣지 않습니다. Google 워크스페이스 커넥터를 쓰지 않는다면 Outlook 메일과 M365 캘린더에는 Google 쌍 **또는** **`ms365`** 중 **하나만** 고르세요. 그 밖의 호스트 기본 커넥터(**Indeed**, **Apify**)는 프로젝트 MCP로 연결하지 않을 때 **Claude** 앱의 **Settings / Customize → Connectors** UI에서 추가합니다. **Indeed**는 **브라우저 OAuth**(**secure.indeed.com**의 Indeed)를 쓰고, **Apify**는 커넥터 폼에서 토큰 + **Enabled tools**를 씁니다. **Gmail**, **Microsoft 365**, **Google Calendar**는 Anthropic의 연동 문서에 따라 사용자(또는 조직) 계정에 **OAuth**로 연결합니다.

## 3단계 패턴(모든 연동 공통)

**Indeed**, **Apify**, **Gmail**, **Microsoft 365**, **Google Calendar**, **LinkedIn**, **PKM 소스**(Capacities, Notion)(해당하는 경우), 그리고 이 플러그인에 문서화되는 **향후** 커넥터에 이 순서를 사용합니다.

1. **탐색(Discover)** — **먼저** **이 채팅 세션**에 해당 연동의 호스트 도구가 이미 노출돼 있는지 확인합니다(도구 이름은 다를 수 있음). 도구가 있고 동작하면 그 서비스는 이번 세션에서 **연결된 것**입니다. 해당 연동은 여기서 **멈춥니다**. 사용자가 뭔가 고장 났다고 말하지 않는 한 설정, OAuth, 브라우저 접근을 **묻지 않습니다**.

2. **설정(Configure)** — 1단계에서 도구가 **없다고** 확인되거나 사용자가 커넥터가 **꺼져 있다/로그인되지 않았다**고 확인한 **경우에만**, 사용자에게 **설치하거나 고칠지** **묻습니다**. **Connectors** + OAuth 또는 토큰 설정을 **안내**하되, 클릭과 로그인은 **사용자가 직접** 합니다. 커넥터를 설치, 활성화, OAuth 하는 데 **Claude in Chrome**이나 **컴퓨터 사용**을 **쓰지 않습니다**.

3. **브라우저 접근(Browser access)** — 이 세션에서 MCP로 해당 연동을 충분히 쓸 수 **없을 때만**(설정 후에도 도구가 없거나, 워크플로가 **브라우저 전용**인 경우. 예: LinkedIn MCP가 없는 **LinkedIn** 게시물 분석) 진행합니다. 그 접근을 위해 **Claude in Chrome** 및/또는 **컴퓨터 사용**을 허용할지 **묻습니다**(**둘 다 안 함** / Chrome / 컴퓨터 사용 / 둘 다). 호스트 도구로 **이미 연결된** 서비스(예: **Indeed** `search_jobs`가 있는 경우 — 추가 질문 없음)에는 3단계를 **묻지 않습니다**.

**스킬**(`skills/launch/SKILL.md`, **`draft-outreach`**, **`linkedin-post-analytics`** 등)은 스킬이 더 좁은 예외를 명시하지 않는 한 이 패턴을 따릅니다.

## 이 플러그인의 커넥터

| 카테고리 | 자리표시자 | 저장소 내 / 호스트 기본 경로 | 기타 옵션 |
|----------|-------------|----------------------------|---------------|
| 커리어 | `~~career` | **Indeed** MCP — Claude **Connectors** → **Indeed** → **Connect** → 브라우저 OAuth(`search_jobs`, `get_job_details`; 커넥터 URL `https://mcp.indeed.com/claude/mcp`) | LinkedIn, Glassdoor, Monster, ZipRecruiter, Dice, Handshake |
| 연봉 벤치마크 | — | Claude **Desktop** 커넥터를 통한 **Apify** MCP. **Enabled tools:** `call-actor,get-actor-run,get-dataset-items,cheapget/best-job-search` | 향후 MCP. Apify가 꺼져 있어도 스킬은 우아하게 기능을 낮춰 동작해야 함 |
| 저장소 | `~~storage` | **Google Drive:** 구직 파일(PDF/DOCX 등)에는 **Drive 앱 동기화**(또는 수동 백업/복원) 권장. **OneDrive:** 구직 파일에는 **OneDrive 앱 동기화**(또는 수동 백업/복원) 권장(플러그인의 JSON 아티팩트는 Claude의 Microsoft 365 커넥터로는 안정적으로 파일 접근이 되지 않음). **Dropbox:** 구직 파일에는 **Dropbox 앱 동기화**(또는 수동 백업/복원) 권장. | `{user_dir}`의 로컬 파일 시스템 대체 |
| 받은편지함 / Outlook(읽기) | `~~inbox` | **Gmail** 및/또는 **Microsoft 365** 1st-party 커넥터(아래) | 향후: 문서화되는 경우 다른 호스트의 이메일 MCP |
| 캘린더(Google) | — | **Google Calendar** 1st-party 커넥터(아래) | 활성화된 경우 **Microsoft 365**를 통한 Outlook/Teams 캘린더 |
| PKM 지식 베이스(스토리 마이닝) | `~~pkm` | **Notion** 1st-party 커넥터(공식) 및/또는 호스트 세션에서 사용 가능한 경우 로컬 MCP 확장/서버를 통한 **Capacities** | Obsidian, Roam, Logseq, 수동 내보내기/가져오기 워크플로 |
| 이벤트(Luma) | — | 선택 사항, 미포함 — **`event-radar`** / **`event-intelligence`** 워크플로를 위해 사용자 세션에 이미 있는 Luma MCP 서버(예: 독립 프로젝트 **[`alx1p/luma-mcp`](https://github.com/alx1p/luma-mcp)**)를 사용. | **Claude in Chrome**, **컴퓨터 사용**, **수동 복사/붙여넣기**를 통한 Meetup/Eventbrite 대체 |
| 면접 전사 | — | 선택적 로컬 MCP 서버 — **`mcp-transcribe`**, `/careerloop:setup-transcribe`로 설치(또는 `mcp-transcribe/README.md`에 따라 수동 설치). 녹음된 면접 오디오용 **`transcribe_file`**을 제공하며 **`interview-capture`**가 사용. 전적으로 로컬(mlx-whisper 또는 faster-whisper 기반 Whisper). | 세션 샌드박스의 `faster-whisper`, 또는 붙여 넣은 전사본 |

---

## 면접 스토리 PKM 소스

`mine-stories`는 로컬 파일 외에 PKM 시스템에서도 면접 증거를 가져올 수 있습니다.

선호하는 커넥터 경로:

1. **Notion(공식 커넥터):** 호스트의 Connectors 카탈로그에 있으면 Claude의 1st-party Notion 커넥터를 사용합니다.
2. **Capacities:** 활성 호스트 세션에서 사용 가능하면 로컬 MCP 서버/확장 경로를 사용합니다(예: `tboothie-capacitiesmcp` 같은 Capacities MCP 연동).
3. **대체:** PKM 노트를 `{user_dir}`로 내보내기/동기화하고 파일에서 직접 마이닝합니다.

PKM의 3단계 동작:

1. **탐색:** Notion/Capacities 도구가 세션에 이미 보이면 연결된 것으로 보고 설정을 다시 묻지 않습니다.
2. **설정:** 없으면 Notion 및/또는 Capacities를 연결할지 사용자에게 묻고, 커넥터 설정/OAuth/토큰 단계는 사용자가 호스트 UI에서 직접 완료합니다.
3. **브라우저/수동 대체:** PKM 커넥터 도구를 계속 쓸 수 없으면 `{user_dir}`의 내보낸 파일을 마이닝하며 계속 진행합니다.

가드레일:
- 면접 스토리 워크플로에 PKM 커넥터를 필수로 요구하지 않습니다. 로컬 파일 마이닝은 계속 지원됩니다.
- 사용자가 일지 출처와 PKM 출처를 감사할 수 있도록 각 스토리 후보에 출처(`source`와 `source_path`)를 유지합니다.
- PKM 커넥터가 연결돼 있지만 권한 범위가 좁으면, 가능한 범위를 마이닝하고 한계를 명확히 보고합니다.

Capacities MCP 목록 참고: [Capacities MCP Server](https://lobehub.com/nl/mcp/tboothie-capacitiesmcp).

---

## 멀티 채널 채용 소싱 정책

CareerLoop는 다음 전반에 걸쳐 커넥터 우선 소싱 전략을 지원합니다.
- 주/연방 게시판(예: IllinoisJobLink),
- 틈새 게시판(예: Wellfound, Welcome to the Jungle),
- 회사 직접 및 ATS 포털(예: Greenhouse/Lever/Workday 채용 페이지).

다음 순서를 사용합니다.

1. **커넥터 우선:** 소스 도구가 세션에 있으면 그것을 사용합니다.
2. **브라우저 보조 수집:** MCP를 쓸 수 없거나 브라우저 전용일 때만.
3. **보조 수동 수집:** 항상 사용 가능한 대체 수단.

### 정규화된 공고 스키마(모든 채널)

순위를 매기기 전에 다음 필드를 요구합니다.
- `title`
- `company`
- `location`
- `apply_url`
- `source`
- `retrieval_mode`(`mcp` | `browser` | `manual`)

가능하면 수집:
- `salary`, `posted_date`, `close_date`, `employment_type`, `job_id_or_requisition`, `raw_description`

### 출처, 신뢰도, 중복 제거

- 모든 공고는 `source`와 `retrieval_mode`를 가져야 합니다.
- 신뢰도 등급:
  - **high**: 필수 필드 + 설명 + 게시일
  - **moderate**: 필수 필드 + 일부 선택 메타데이터
  - **directional**: 필수 필드만 있거나 메타데이터가 빈약함
- 중복 제거 우선순위:
  1. 회사 직접 정규 URL
  2. requisition ID가 있는 ATS 공고
  3. 커넥터에서 가져온 애그리게이터 공고
  4. 수동 복사/붙여넣기 항목

중복이 발견되면 가장 우선순위가 높은 레코드를 유지하고, 우선순위가 낮은 레코드에서 빠진 메타데이터를 병합합니다.

### 채널별 보조 수동 플레이북

- **주/연방:** 있는 경우 마감일과 급여 등급/밴드를 묻습니다.
- **틈새 게시판:** 있는 경우 보상 문구/지분을 묻습니다.
- **회사/ATS:** 있는 경우 정규 지원 URL + requisition ID를 묻습니다.

이 규칙은 `skills/search-jobs/SKILL.md`를 보완하며, 라이브 도구를 쓸 수 없을 때 사용합니다.

---

## 이벤트 인텔리전스 — Luma(선택, 미포함)

CareerLoop는 Luma MCP 서버를 포함하지 않습니다. 사용자 세션에 Luma 이벤트 탐색 MCP가 있으면 **`event-radar`**와 **`event-intelligence`**가 이를 사용하고, 없으면 아래의 Meetup/Eventbrite 경로나 수동 수집으로 대체합니다.

사용자가 Luma 이벤트 탐색을 원하면, 독립 오픈소스 프로젝트 **[`alx1p/luma-mcp`](https://github.com/alx1p/luma-mcp)**가 Claude Desktop 확장으로 제공합니다. 설치와 설정은 해당 프로젝트의 README를 안내하세요. 이 저장소는 이를 포함하거나 배포하지 않습니다.

| 단계 | 동작 |
| --- | --- |
| **1 — 탐색** | **이 세션**에 Luma 이벤트 도구가 보이면 사용하고, 설정을 **묻지 않습니다**. |
| **2 — 설정** | 사용자가 Luma 도구를 얻는 방법을 물을 때만 GitHub의 `alx1p/luma-mcp`를 안내합니다. 직접 설치를 안내하지는 않습니다. |
| **3 — 대체** | 사용 가능한 Luma MCP가 없으면 커넥터 우선 정책으로 계속합니다. 가능한 다른 MCP 소스, 그다음 브라우저 보조 수집, 그다음 수동 수집 순입니다. |

---

## 이벤트 인텔리전스 — Meetup & Eventbrite(대체 경로)

Meetup과 Eventbrite는 이 플러그인의 이벤트 워크플로에서 **선택적 브라우저/수동 소스**로 취급합니다.

이 이벤트를 소싱할 때의 선호 순서:

1. **Claude in Chrome**(사용자가 승인한 경우)
2. **컴퓨터 사용**(사용자가 승인한 경우)
3. **수동 복사/붙여넣기** 수집(항상 사용 가능)

사용 규칙:

- 브라우저 자동화를 쓰기 전에 명시적 승인을 요청합니다.
- 각 이벤트에 수집 출처(`retrieval_mode`: `browser` 또는 `manual`)를 유지합니다.
- 브라우저 도구를 쓸 수 없거나 거절되면 수동 수집으로 계속 진행하고, 이벤트 워크플로를 막지 않습니다.

---

## 이메일 & 캘린더 맥락 — Gmail, Microsoft 365, Google Calendar

**목표:** **`draft-outreach`**, **`follow-up`**, **`contact-context`**를 실행하기 전에, 모델이 채용 담당자나 리크루터와 오간 스레드를 **내** 메일에서 검색하고, **Google Calendar**(또는 M365 캘린더)가 연결돼 있으면 그 연락처가 포함된 **과거 및 예정 미팅을 읽을** 수 있습니다. 단, 메일이나 캘린더를 조회할 때마다 **내가 명시적으로 승인한 뒤에만** 가능합니다. 그러면 웜 아웃리치가 **증거에 근거한** 메시지가 됩니다(통화에서 약속한 내용을 기억하고, 미팅이 **이미 잡혀 있을 때** 콜드 오프닝을 하지 않습니다).

**모범 사례(Anthropic):** Claude 앱의 **1st-party 커넥터**를 사용하세요. **OAuth**로 인증하므로(브라우저에서 로그인하며, Claude가 Google이나 Microsoft 비밀번호를 채팅에 붙여 넣으라고 요구하지 않습니다) 권한은 **위임형**이라 Claude는 내가 이미 접근할 수 있는 메일에만 닿을 수 있습니다. 이 플러그인에서는 장기 토큰을 `.mcp.json`에 넣어 Gmail이나 Microsoft 365를 설정하지 **마세요**.

### Gmail

- **이미 추가했는데 꺼져 있나요?** **Connectors**에 **Gmail**이 보이지만 **토글이 꺼져 있거나** **Connect** / **Reconnect**가 표시되면, **`/careerloop:launch`** 6단계에서 **읽기 전용** 스레드 검색(사용자를 대신해 보내지 않음)을 위해 **활성화**하거나 **OAuth를 마칠**지 묻습니다. Gmail 도구가 이미 채팅에 보이면 다시 설치할 필요가 없습니다.
- **위치:** Claude **Settings** / **Customize** → **Connectors** → **Gmail** → **Connect** → 브라우저에서 **Google** 로그인과 동의를 완료합니다.
- **문서:** [Gmail integration (Claude Docs)](https://claude.com/docs/connectors/google/gmail) · [Google Workspace connectors (Help Center)](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors)
- **동작(Anthropic 기준):** 이메일 내용을 검색하고 분석하며 출처를 인용합니다. **Claude는 이 연동으로 이메일을 작성, 전송, 수정할 수 없습니다.** CareerLoop의 **읽기 전용** 사용과 일치합니다(초안 작성을 위해 채팅에서 스레드를 요약하고, 전송은 내 클라이언트에서 합니다).
- **플랜:** Claude의 Gmail 문서에는 **Pro, Max, Team, Enterprise**에서 사용 가능하다고 설명돼 있습니다(현재 플랜 요건은 제품 내에서 확인).
- **조직 / 워크스페이스:** **Team / Enterprise**에서는 개인이 연결하기 전에 **Owner** 또는 **Primary Owner**가 워크스페이스에 대해 연동을 활성화해야 할 수 있습니다.

### Google Calendar

- **이미 추가했는데 꺼져 있나요?** **Connectors**에 **Google Calendar**가 보이지만 **토글이 꺼져 있거나** **Connect** / **Reconnect**가 표시되면, **`/careerloop:launch`** 6단계에서 **활성화**하거나 **OAuth를 마칠**지 묻습니다. 캘린더 관련 도구가 이미 채팅에 보이면 다시 설치할 필요가 없습니다.
- **위치:** Claude **Settings** / **Customize** → **Connectors** → **Google Calendar** → **Connect** → 브라우저에서 **Google** 로그인과 동의를 완료합니다(**Gmail**과 같은 호스트 흐름이며, 카탈로그에서는 별도의 커넥터 카드입니다).
- **문서:** [Google Calendar integration (Claude Docs)](https://claude.com/docs/connectors/google/calendar) · [Google Workspace connectors (Help Center)](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors)
- **동작(Anthropic 기준):** Claude는 내 일정, 이벤트, 참석자, 가능 시간을 읽고 추론할 수 있습니다. **CareerLoop**는 이를 **오직** 지정된 연락처와의 **과거** 및 **예정** 이벤트(제목, 시간, 참석자, 호스트가 노출하는 메모/설명 필드)를 **`contact-context`** / **`draft-outreach`**를 위해 요약하는 데에만 쓰며, 조회할 때마다 **명시적 승인 후에** 합니다. **예정된** 미팅은 **웜 네트워킹 식별**에 쓰입니다(그 연락처와의 미래 이벤트가 있으면 콜드 관계가 아닙니다). 채팅에서는 **읽기 전용**으로 다루는 것을 우선하고, 사용자가 세션에서 명시적으로 요청하지 않는 한 사용자를 대신해 이벤트를 만들거나 일정을 바꾸지 않습니다.
- **플랜:** Claude의 Google Calendar 문서에는 **Pro, Max, Team, Enterprise**에서 사용 가능하다고 설명돼 있습니다(제품 내에서 확인).
- **조직 / 워크스페이스:** **Team / Enterprise**에서는 개인이 연결하기 전에 **Owner** 또는 **Primary Owner**가 워크스페이스에 대해 연동을 활성화해야 할 수 있습니다(Gmail과 같은 패턴).

### Microsoft 365(Outlook 메일 등)

CareerLoop의 Outlook 메일은 Anthropic의 **Microsoft 365** 커넥터(제품 문서 기준 Outlook, SharePoint, OneDrive, Teams 등)로 제공됩니다.

- **선택적 HTTP MCP(같은 연동, Connectors UI의 대안):** 프로젝트 **`.mcp.json`**이 **`ms365`** → **`https://microsoft365.mcp.claude.com/mcp`**를 선언할 수 있습니다. 파일을 읽는 호스트가 **Gmail** / **Google Calendar** HTTP MCP처럼 M365 도구를 로드하게 하는 것이며, JSON에 비밀 값은 **넣지 않고** 연결할 때 호스트에서 OAuth를 합니다.
- **위치:** **Team / Enterprise**에서는 관리자 활성화가 필요할 수 있고, 이후 각 사용자가 **Settings** → **Connectors** → **Microsoft 365** → **Connect** → **Microsoft** OAuth를 진행합니다.
- **문서:** [Microsoft 365 connector (Claude Docs)](https://claude.com/docs/connectors/microsoft/365) · [Enabling and using the Microsoft 365 connector (Help Center)](https://support.claude.com/en/articles/12542951-enabling-and-using-the-microsoft-365-connector) · [Microsoft 365 connector: Security Guide](https://support.claude.com/en/articles/12684923-microsoft-365-connector-security-guide)
- **동작(Anthropic 기준):** **읽기 전용** 접근입니다. Claude는 이 커넥터로 Outlook(또는 다른 M365 영역)의 콘텐츠를 수정, 삭제, 생성**할 수 없으며**, 내가 이미 접근할 수 있는 이메일 스레드와 관련 맥락을 검색하고 분석합니다.
- **플랜:** Claude의 Microsoft 365 문서에는 **Team 및 Enterprise** 사용자에게 제공된다고 명시돼 있고, 테넌트에 **Global Administrator** 설정이 필요할 수 있습니다. **Outlook.com**에 의존하는 **개인 / Pro 전용** 사용자는 호스트가 커넥터 경로를 제공하는지 확인하거나, 해당되면 **Gmail**을 사용하세요.

### CareerLoop 사용 규칙

1. **3단계 패턴:** **탐색** → 연결돼 있지 **않을** 때만 **설정** → MCP가 여전히 없거나 흐름이 브라우저 전용일 때만 **브라우저 접근**. 세션에서 이미 연결된 서비스는 **다시 묻지 마세요**. 위의 **§ 3단계 패턴**을 참고하세요.
2. **명시적 승인:** 스킬(**`draft-outreach`**, **`follow-up`**, **`contact-context`**)은 도구를 호출하기 전에 특정 사람이나 회사에 대해 **메일** 및/또는 **캘린더**를 검색할지 **한 번 물어야** 합니다. **`agents/networking-strategist/AGENT.md`**, **`agents/writer/AGENT.md`**와 일관됩니다. 커넥터가 하나만 있으면 그 범위에 대해서만 묻습니다.
3. **지어내기 금지:** 커넥터가 꺼져 있거나 사용자가 거절하면 스레드 요약을 **지어내지 마세요**. 단독으로 성립하는 문안을 쓰세요.
4. **최소 공개:** 아웃리치나 후속 조치에 필요한 것만 요약하고, 본문 전체를 쏟아내기보다 스레드 발췌와 날짜를 우선합니다.
5. **연결 후 새 채팅:** OAuth 후에도 도구가 보이지 않으면 **새 채팅**을 시작합니다(**Indeed** / **Apify**와 같은 패턴).

**`/careerloop:launch`** 중 대화형 설정 제안은 **`skills/launch/SKILL.md`** 6단계도 참고하세요.

---

## 클라우드 저장소 커넥터 — Google Drive, OneDrive, Dropbox

**목표:** 로컬 우선 동작을 유지하면서 기기 간에 아티팩트 저장소를 이식 가능하게 합니다.

**현실 점검(중요):** Claude Desktop의 **공식 Google Drive** 커넥터는 주로 **네이티브 Google 문서 파일**을 위한 것입니다. 보통 저장하는 구직 파일(PDF, DOC, 스크린샷, 이력서, 자기소개서)에는 CareerLoop가 다음을 통한 이식성을 권장합니다.
- Google Drive **애플리케이션 동기화**(권장), 또는
- 구직 폴더의 수동 **백업/복원**.

**OneDrive**는 Word/PowerPoint/PDF 같은 네이티브 Microsoft 형식에 맞춰진 Claude의 Microsoft 365/OneDrive 파일 접근 커넥터에 의존하지 말고, 플러그인의 JSON 아티팩트를 위해 **OneDrive 애플리케이션 동기화**(또는 수동 백업/복원)를 사용하세요.

**Dropbox**는 호스트 커넥터의 파일 접근에 의존하지 말고 **Dropbox 애플리케이션 동기화**(또는 수동 백업/복원)를 사용하세요.

### 3단계 패턴(저장소)

1. **탐색:** 사용자가 선택한 제공자에 대해 로컬 클라우드 동기화를 이미 켜 두었는지, `{user_dir}`을 지금 사용할 수 있는지 확인합니다.
2. **설정:** 도구가 없거나 사용자가 커넥터가 꺼져 있다고 말할 때만:
   - **Google Drive, OneDrive 또는 Dropbox:** 폴더 내용을 모든 기기에서 로컬로 쓸 수 있도록 **애플리케이션 동기화**(권장) 또는 구직 폴더의 수동 백업/복원을 사용합니다.
3. **브라우저 접근:** 이 경로의 저장소 설정에는 필요하지 않습니다. 커넥터 설치나 로그인을 클릭해서 진행하려고 브라우저 자동화를 쓰지 마세요.

### CareerLoop 저장소 동작 규칙

1. **활성 저장소는 하나만:** Google Drive, OneDrive, Dropbox, 로컬 전용 중에서 제시하고, 한 번의 설정 과정에서 여러 클라우드 커넥터를 강요하지 않습니다.
2. **로컬 우선 대체:** 저장소 도구를 쓸 수 없거나, 연결이 끊겼거나, 거절되면 워크플로를 끊지 않고 `{user_dir}`의 로컬 파일을 계속 사용합니다.
3. **아티팩트 연산 동등성:** `save_artifact`, `list_artifacts`, `get_artifact`의 동작은 저장소 백엔드와 관계없이 사용자 관점에서 일관되어야 합니다.
4. **동기화 상태를 지어내지 않음:** 클라우드 커넥터가 꺼져 있으면 그 사실을 분명히 말하고, 클라우드 쓰기나 읽기가 일어난 것처럼 암시하지 않습니다.

**`/careerloop:launch`** 중 대화형 설정은 **`skills/launch/SKILL.md`** 7단계도 참고하세요.

---

## 준비 & 모의 면접 — 텍스트 전용

**`prep-interview`**와 **`mock-interview`**는 전적으로 채팅 텍스트로 실행되며, 이 플러그인에 실시간 TTS/STT는 없습니다. 사용자가 호스트 자체의 음성 인식으로 받아쓰기한 뒤 결과를 붙여 넣으면 `interview-coach`가 이를 `user_audio_transcript`로 받습니다. 이는 사용자가 텍스트를 제공하는 것이지, 에이전트가 오디오를 캡처하는 것이 아닙니다.

## 면접 전사 — `mcp-transcribe`(선택적 MCP 서버)

**`mcp-transcribe`** MCP는 이 저장소의 **`mcp-transcribe/`**에 소스가 있는 로컬 서버이며, 라이브 마이크가 아니라 **디스크에 이미 있는 녹음 오디오 파일**을 전사합니다. **mlx-whisper**(Apple Silicon) 또는 **faster-whisper**(CPU 대체)를 사용합니다. 클라우드 자격 증명이 필요 없으며 오디오는 내 컴퓨터에 머뭅니다.

**설치(최종 사용자):** `/careerloop:setup-transcribe`를 실행하세요. 사전 요건 점검과 설치 프로그램을 대신 실행해 주며 터미널 사용이 필요 없습니다. 고급 사용자는 대신 **`mcp-transcribe/README.md`**의 수동 단계를 따를 수 있습니다.

| 단계 | 동작 |
| --- | --- |
| **1 — 탐색** | `backend_info` / `transcribe_file`이 **이 세션**에 보이면 `mcp-transcribe`를 쓸 수 있는 것이므로 설정을 **묻지 않습니다**. |
| **2 — 설정** | 도구가 없고 사용자가 녹음된 면접 전사를 원할 **때만** `/careerloop:setup-transcribe`를 제안합니다. |
| **3 — 도구** | **`transcribe_file(path, initial_prompt, vocabulary_group, language, model, out_dir, write_files)`** — 녹음을 전사하고 텍스트 + 시간 정보가 있는 세그먼트를 반환합니다. **`backend_info()`** — 사용 중인 백엔드와 `ffmpeg` 유무를 보고합니다. |

**면접 후 기록:** **`interview-capture`** 스킬은 사용자가 이미 만든 녹음에 **`transcribe_file`**을 사용한 뒤 구조화된 메모를 기록합니다. 오디오를 아예 쓰지 않는 사용자를 위한 **`interview-debrief`**를 대체하지는 **않습니다**.
