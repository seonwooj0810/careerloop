# **CAREERLOOP**

Claude Cowork 플러그인 — 제품 전체 사양서

버전 1.0.2 — 2026년 10월

채용 담당자, 커리어 코치, 리버스 리크루터, 시장 분석가의 역량을
하나의 지능형 플랫폼으로 결합한 AI 기반 구직 동반자입니다.

# **목차**

[1장. 개요](#1-개요)
>[1.1 설계 원칙](#11-설계-원칙)
>[1.2 플러그인 아키텍처](#12-플러그인-아키텍처)

[2장. 플러그인 파일 구조](#2-플러그인-파일-구조)

[3장. 슬래시 커맨드](#3-슬래시-커맨드)
>[3.0 실행 및 설정](#30-실행-및-설정)
>[3.1 이력서 및 자기소개서 커맨드](#31-이력서-및-자기소개서-커맨드)
>[3.2 구직 및 트래킹 커맨드](#32-구직-및-트래킹-커맨드)
>[3.3 면접 준비 커맨드](#33-면접-준비-커맨드)
>[3.4 네트워킹 커맨드](#34-네트워킹-커맨드)

[4장. 에이전트](#4-에이전트)

[5장. 스킬](#5-스킬)

[6장. 스케줄링 및 반복 실행](#6-스케줄링-및-반복-실행)
>[6.1 호스트 훅 (`hooks/hooks.json`)](#61-호스트-훅-hookshooksjson)

[7장. 스토리지 커넥터](#7-스토리지-커넥터)
>[7.1 인터페이스](#71-인터페이스)
>[7.2 사용 가능한 커넥터](#72-사용-가능한-커넥터)

[8장. 분석 커넥터](#8-분석-커넥터)

[9장. 외부 서비스 연동 (.mcp.json)](#9-외부-서비스-연동-mcpjson)

[10장. 핵심 데이터 모델](#10-핵심-데이터-모델)
>[10.1 ExperienceLibrary](#101-experiencelibrary)
>[10.2 지원 기록(Application Record)](#102-지원-기록application-record)
>[10.3 아티팩트 기록(Artifact Record)](#103-아티팩트-기록artifact-record)
>[10.4 네트워킹 항목 및 LinkedIn 게시물 분석](#104-네트워킹-항목-및-linkedin-게시물-분석)
>[10.5 스토리 코퍼스(Story Corpus)](#105-스토리-코퍼스story-corpus)
>[10.6 커리어 궤적 및 오퍼 컨텍스트 아티팩트](#106-커리어-궤적-및-오퍼-컨텍스트-아티팩트)

[11장. 인텔리전스 피드백 루프](#11-인텔리전스-피드백-루프)

[12장. 일일 리듬 및 스케줄링](#12-일일-리듬-및-스케줄링)
>[12.1 권장 주기 (Cowork `/schedule`)](#121-권장-주기-cowork-schedule)
>[12.2 시간 민감 항목과 일상 항목의 노출 방식](#122-시간-민감-항목과-일상-항목의-노출-방식)

[13장. 면접 캡처 (Phase 2B)](#13-면접-캡처-phase-2b)
>[13.1 MVP 오디오 범위](#131-mvp-오디오-범위)
>[13.2 대체 수단: 면접 후 Q&A 흐름](#132-대체-수단-면접-후-qa-흐름)

[14장. 정직한 어드바이저 설계 철학](#14-정직한-어드바이저-설계-철학)

[15장. 단계별 제공 계획](#15-단계별-제공-계획)
- [Phase 1 — 핵심 플랫폼](#phase-1--핵심-플랫폼)
  - [Phase 1A — 핵심 플랫폼: 플러그인 스캐폴드, 설정, 세션 시작, 실시간 구직](#phase-1a--핵심-플랫폼-플러그인-스캐폴드-설정-세션-시작-실시간-구직)
  - [Phase 1B — 스킬 계층 및 인텔리전스: 워크플로 스킬, 지원 트래커, ATS 점수 산정, 분석가 에이전트](#phase-1b--스킬-계층-및-인텔리전스-워크플로-스킬-지원-트래커-ats-점수-산정-분석가-에이전트)
  - [Phase 1C — 어드바이저 계층: 정직한 직무 평가, 스킬 격차 분석, 교육 ROI](#phase-1c--어드바이저-계층-정직한-직무-평가-스킬-격차-분석-교육-roi)
  - [Phase 1D — 선제적 발굴: 결과 가중 공고 점수화 및 시장 동향 모니터링](#phase-1d--선제적-발굴-결과-가중-공고-점수화-및-시장-동향-모니터링)
  - [Phase 1E — 전문가 프레즌스: 네트워킹 전략, 이벤트 레이더, LinkedIn 작성기](#phase-1e--전문가-프레즌스-네트워킹-전략-이벤트-레이더-linkedin-작성기)
  - [Phase 1F — 커리어 계획, 오퍼 평가 및 연봉 협상](#phase-1f--커리어-계획-오퍼-평가-및-연봉-협상)
  - [Phase 1G — 마켓플레이스 배포](#phase-1g--마켓플레이스-배포)

- [Phase 2 — 연동](#phase-2--연동)
  - [Phase 2A — 이메일 및 캘린더 연동](#phase-2a--이메일-및-캘린더-연동)
  - [Phase 2B — 면접 인텔리전스](#phase-2b--면접-인텔리전스)
  - [Phase 2C — 확장 연동](#phase-2c--확장-연동)
  - [Phase 2D — 이벤트 인텔리전스 및 면접 스토리 인텔리전스](#phase-2d--이벤트-인텔리전스-및-면접-스토리-인텔리전스)

- [Phase 3 — 상시 가동 커리어 에이전트](#phase-3--상시-가동-커리어-에이전트)

- [Phase 4 — 엔터프라이즈 및 생태계](#phase-4--엔터프라이즈-및-생태계)

[16장. 미해결 질문 및 보류된 결정](#16-미해결-질문-및-보류된-결정)

[부록: 커맨드 빠른 참조](#부록-커맨드-빠른-참조)

# **1. 개요**

*진입점:* `README.md`, `CLAUDE.md`.

CareerLoop는 구직의 전 과정을 아우르는 인텔리전스를 제공하는 Claude Cowork 플러그인입니다. 공고 발굴과 지원 자료 맞춤 작성에서 시작해 면접 준비와 네트워킹 전략을 거쳐, 결과 추적과 결과로부터의 학습까지 다룹니다. 경력 수준, 목표 산업, 지역에 관계없이 모든 구직자를 지원하도록 설계되었습니다.

이 플러그인은 피드백 루프를 중심으로 설계되었습니다. 수행한 모든 행동과 관찰된 결과가 시스템에 다시 반영되어 이후 추천이 더 정교해집니다. 시간이 지날수록 CareerLoop는 사용자 개인에게 효과적인 방식을 학습하고 그에 맞춰 안내를 조정합니다.

## **1.1 설계 원칙**

* 격려보다 정직 — 시스템은 근거 없는 안심 대신 솔직한 평가를 제공합니다
* 기계적 처리보다 지능적 처리 — 입력만이 아니라 결과에 따라 출력이 조정됩니다
* 커넥터 기반 — 스토리지, 분석, 외부 서비스는 교체 가능한 어댑터입니다
* 프라이버시 우선 — 오디오 캡처 같은 민감한 기능은 명시적 옵트인이 필요합니다
* 크로스 플랫폼 — 스킬과 데이터는 macOS, Windows, Linux에서 동작하며, 반복 실행은 플러그인이 제공하는 데몬이 아니라 사용자가 Claude Cowork의 `/schedule`(또는 동등한 기능)로 직접 구성합니다
* 공감 — 구직이 스트레스가 큰 일임을 이해하고 그에 맞게 어조를 조절합니다

## **1.2 플러그인 아키텍처**

| 플러그인 이름 | careerloop |
| --- | --- |
| **버전** | 1.0.2 |
| **플랫폼** | Claude Cowork (macOS / Windows / Linux) (Claude Code와도 호환) |
| **아키텍처** | 스킬 우선 — 행동 지능은 대화형 트리거를 갖는 스킬에 있으며, 커맨드는 핵심 워크플로를 명시적으로 호출하기 위한 별칭입니다 |
| **스케줄링** | Claude Cowork에서 사용자가 구성 — 스킬이 실행 페이로드이며, 권장 주기는 스킬 파일에 문서화되어 있음 (예: `/schedule`로 `daily-schedule`을 매일 실행) |
| **알림 / 노출** | 세션 내 UX (예: 중요 항목용 `focus-career`)와 예약 작업 실행 시 Cowork가 제공하는 방식 — 플러그인은 별도의 알림 데몬을 포함하지 않음 |
| **스토리지 계층 (Phase 1)** | 로컬 파일시스템 — `{user_dir}` (클라우드 커넥터는 Phase 2C) |
| **분석 계층 (Phase 1)** | SQLite + D3 시각화 (추가 커넥터는 Phase 3) |
| **AI 서비스** | Claude API (MCP 경유); 선택적으로 **로컬** 파일 전사 STT용 **`mcp-transcribe`** MCP (`/careerloop:setup-transcribe`로 설치); 준비·모의 면접은 텍스트 전용 |
| **구직 (Phase 1)** | Claude Desktop **Customize → Connectors**를 통한 **Indeed** MCP — **Connect** → **secure.indeed.com**에서 브라우저 OAuth 진행; 도구 **`search_jobs`**, **`get_job_details`** (커넥터 `https://mcp.indeed.com/claude/mcp`). 사용자가 OAuth를 완료해야 하며, 커넥터를 사용할 수 없을 때는 반자동 수동 대체 수단 제공 |
| **연봉 벤치마크 (Phase 1, 선택)** | Claude Desktop **Customize → Connectors → Desktop → Apify**에서 추가하는 Apify MCP (커넥터 UI의 토큰 + **Enabled tools** 목록); 프로젝트 **`.mcp.json`**에는 저장하지 않음 |

# **2. 플러그인 파일 구조**

**careerloop/**

**├── .claude-plugin/**

**│ └── plugin.json**

**├── .mcp.json** — Gmail / Google Calendar용 Anthropic **HTTP MCP** 항목 및/또는 대체 채널로서의 **`ms365`**(Outlook / Microsoft 365)를 포함할 수 있음(비밀 정보 없음). 그 외 MCP(예: 연봉용 Apify)는 호스트 앱에서 구성합니다. **`mcp-transcribe`는 포함하지 않습니다** — 아래 참고.

**├── mcp-transcribe/** — 녹음된 면접 파일 전사를 위한 로컬 MCP 서버(`/careerloop:setup-transcribe`로 소스 설치, 사전 빌드 번들 없음). GitHub Releases로 배포하지 않음

**├── agents/**

**├── skills/**

**├── hooks/**

**│ ├── hooks.json**

**│ └── context/** — 예: `SessionStart` 시 주입되는 `session-start.md`

**├── references/**

**├── career/** *(`{user_dir}` 예시 — 개인용이면 gitignore 처리)*\*\*

**└── README.md**

# **3. 슬래시 커맨드**

*구현:* 각 커맨드의 동작과 트리거는 `skills/<skill-name>/SKILL.md`에 있습니다(아래 하위 절 참고). 플러그인 매니페스트 `.claude-plugin/plugin.json`이 skills 디렉터리를 등록합니다.

모든 커맨드는 careerloop: 네임스페이스로 구분되며 Claude Cowork의 슬래시 커맨드 인터페이스(및 Claude Code)에서 사용할 수 있습니다. 커맨드는 대화로도 트리거할 수 있습니다 — 플러그인이 커맨드 의도에 맞는 자연어 프롬프트를 인식해 적절한 커맨드를 자동으로 호출합니다.

## **3.0 실행 및 설정**

*스킬 파일:* `skills/launch/SKILL.md`.

| 이름 | 유형 | 설명 |
| --- | --- | --- |
| **/careerloop:launch** | 커맨드 | 사용자의 구직 워크스페이스를 **시작**합니다. `{user_dir}`를 구성하고, 기존 문서를 읽고, 사용자 프로필과 ExperienceLibrary를 구축하며, 실시간 구직용 커넥터(Indeed, 선택적 Apify 등) 설정을 안내하는 대화형 마법사입니다. 사용자가 첫 실행을 원하면 선택 기능 **`linkedin-post-analytics`**를 **제안**합니다 — 호스트 브라우저 자동화와 명시적 동의를 전제로, 본인 게시물의 읽기 전용 스냅샷을 **`networking.json`**(**`networking[]`**)에 저장합니다. 설정 담당 범위는 기존과 같으며, 검색을 시작하는 진입점으로 구성되었습니다. 저장 전에 입력값을 검증하며, 키를 갱신하거나 재구성하기 위해 다시 실행할 수 있습니다. |

## **3.1 이력서 및 자기소개서 커맨드**

| 이름 | 유형 | 설명 |
| --- | --- | --- |
| **/careerloop:tailor-resume** | 커맨드 | ExperienceLibrary의 원본 문서 하나 이상과 채용 공고(JD)를 받아 해당 직무에 가장 적합한 이력서를 조립·재작성하고, ATS 호환성 점수를 산정한 뒤 아티팩트 인벤토리에 저장합니다. |
| **/careerloop:cover-letter** | 커맨드 | **CoverLetterBrief**를 만든 뒤 **`writer`**를 호출해 최종 문장을 작성합니다(문체 반영). 아티팩트 인벤토리에 저장합니다. |
| **/careerloop:resume-score** | 커맨드 | 기존 이력서 또는 자기소개서를 채용 공고 기준으로 ATS 키워드 일치도, 서식 준수 여부, 서사 강도를 점수화합니다. |
| **/careerloop:add-source** | 커맨드 | 이후 맞춤 작성에 쓸 수 있도록 새 원본 문서(이력서, CV, 포트폴리오)를 ExperienceLibrary에 추가합니다. |
| **/careerloop:list-artifacts** | 커맨드 | 인벤토리에 생성된 모든 아티팩트를 메타데이터(생성일, 지원한 공고, 알려진 경우 결과)와 함께 나열합니다. |

## **3.2 구직 및 트래킹 커맨드**

| 이름 | 유형 | 설명 |
| --- | --- | --- |
| **/careerloop:search-jobs** | 커맨드 | 구성된 구인 사이트를 검색해 순위가 매겨진 결과를 반환합니다. 순위에는 스킬 일치도, 결과 이력, 시장 인텔리전스가 반영됩니다. 직무, 지역, 회사 규모, 산업, 연봉 범위 필터를 지원합니다. |
| **/careerloop:track-application** | 커맨드 | 새 지원(건)을 기록하거나 기존 지원(건)을 갱신합니다. 대화형 입력을 받아 트래커 데이터베이스에 맞게 자동으로 구조화합니다. |
| **/careerloop:pipeline-status** | 커맨드 | 타임라인 뷰, 벤치마크 비교, 단계 경과 기간별로 표시한 조치 항목을 포함한 전체 지원 파이프라인 대시보드를 표시합니다. **로드맵:** 타임라인에 **예측(forecast)** 오버레이와 **음성 케이던스(voice cadence)**를 추가할 예정입니다 — §15의 **Phase 3 — 대시보드 및 시각화 개선**를 참고하세요. |
| **/careerloop:follow-up** | 커맨드 | 지원(건)을 응답 기한별로 분류하고, **FollowUpBrief** 항목을 만들며, **`writer`**를 호출해 바로 보낼 수 있는 메시지를 작성합니다. 이메일/캘린더 보강은 Phase 2A. |
| **/careerloop:market-brief** | 커맨드 | 사용자의 목표 직무와 산업에 대한 최신 시장 인텔리전스 리포트를 생성합니다. 동향 데이터, 경쟁 수준, AI/자동화 영향 평가를 포함합니다. |
| **/careerloop:suggest-roles** | 커맨드 | 사용자의 전체 ExperienceLibrary를 분석해 보유 스킬을 적용할 수 있는, 자명하지 않은 직무 유형을 각각의 근거와 함께 제안합니다. |
| **/careerloop:career-plan** | 커맨드 | ROI 순으로 격차 우선순위를 매긴 현실적인 커리어 궤적 계획(단기/중기/장기)을 생성하며, 리포트는 `career-trajectory.md`에, `career_trajectory_v1`은 `career-trajectory-data.json`에 저장합니다. |
| **/careerloop:evaluate-offer** | 커맨드 | 상황 인지형 오퍼 평가(재직 중/무직 상황), 직무 적합도·활용도 분석, 보상 공정성 판단을 수행합니다. 후속 작업에서 쓸 수 있도록 `offer-context-{application_id}.json`을 저장합니다. |
| **/careerloop:compare-offers** | 커맨드 | 진행 중인 오퍼들을 보상, 적합도, 궤적 정합성, 리스크 기준으로 나란히 비교한 뒤 정직한 순위를 반환합니다. |
| **/careerloop:negotiate-offer** | 커맨드 | 협상 전략과 레버리지 포인트를 구성한 뒤, `NegotiationHandoffBrief`를 `writer`에 넘겨 바로 보낼 수 있는 초안을 받습니다. |

## **3.3 면접 준비 커맨드**

| 이름 | 유형 | 설명 |
| --- | --- | --- |
| **/careerloop:prep-interview** | 커맨드 | 특정 직무에 대한 전체 면접 준비 세션을 시작합니다. 기업 리서치를 가져오고, 예상 질문을 생성하며, 선택적으로 모의 면접을 시작합니다. |
| **/careerloop:mock-interview** | 커맨드 | 모의 면접 세션을 시작합니다. mode(guided/random/adaptive), stage(recruiter/HM/technical/panel/executive), vibe(supportive/neutral/challenging/antagonistic/bored)를 받습니다. **mode 또는 vibe를 생략하면 시스템이 기본값을 선택합니다**(`skills/mock-interview/SKILL.md` §2.1 참고). |
| **/careerloop:interview-capture** | 커맨드 | 선택 가입형 **스킬**(에이전트 아님): 사용자 본인 면접의 **녹음 오디오 파일**을 전사하고, 핵심 시사점을 추출하며, 지원 기록을 다중 파일 트랜잭션으로 갱신합니다(상세 파일 **`applications/<application_id>.json`**과 **`tracker.json`** 요약 행). 고용주 경고는 1회 표시하며 §13.1의 보관 정책을 따릅니다. 사용 가능한 경우 **`mcp-transcribe`**(`/careerloop:setup-transcribe`로 설치)를 사용합니다. |

## **3.4 네트워킹 커맨드**

| 이름 | 유형 | 설명 |
| --- | --- | --- |
| **/careerloop:networking-strategy** | 커맨드 | 근거 기반 네트워킹 계획(우선순위, 순서, 격차)을 수립합니다. 메시지 작성이 필요하면 **`writer`**용 선택적 인계 브리프를 만듭니다. **`networking-strategist`**를 호출합니다. |
| **/careerloop:network-map** | 커맨드 | 목표 기업으로 이어지는 개연성 있는 경로와 격차를 매핑하며, 서술형 결과와 함께 **`network_map_v1`** JSON을 출력합니다(`network-map.md`에 저장할 수도 있음). **인터랙티브 그래프 UI**는 **Phase 3**입니다 — §15 참고. |
| **/careerloop:draft-outreach** | 커맨드 | 아웃리치 문안(LinkedIn, 이메일, InMail 등)을 작성합니다. **`writer`**를 호출합니다. 관계의 흐름을 이어야 할 때는 **`contact-context`**를 먼저 실행하는 것을 권장하며, Phase 2A 커넥터가 있으면 사용자 승인을 받아 이전 맥락을 이메일·캘린더 이력에서 검색하기도 합니다. |
| **/careerloop:contact-context** | 커맨드 | 지정한 연락처 또는 기업에 대해 이메일(도구가 허용하면 캘린더도)을 읽기 전용으로 검색합니다 — **과거** 및 **예정된** 캘린더 일정 포함. **`draft-outreach`** / **`writer`**용 **ContactContextBrief**(**upcoming_meetings**, **warm_networking**)를 출력합니다. 조회 전에 사용자의 명시적 승인이 필요합니다. |
| **/careerloop:event-intelligence** | 커맨드 | 특정 이벤트를 심층 평가합니다: ROI, 청중 적합도, 비용/시간, **발표 / 연사** 기회 표시. **`networking-strategist`**를 호출합니다. |
| **/careerloop:content-suggest** | 커맨드 | 현재 산업 동향, 사용자의 목표 직무, 해당 분야의 최근 활동을 바탕으로 LinkedIn 게시물 주제를 제안합니다. **`writer`**를 호출합니다. |
| **/careerloop:evaluate-post** | 커맨드 | 게시물 초안을 청중 적합도, 알고리즘 성과, 목표 기업 대비 **문화적 / 정치적 / 평판상** 리스크 관점에서 평가합니다. 목표 프로필별 리스크 평가를 위해 **`writer`**와 **`market-researcher`**를 호출합니다. |
| **/careerloop:linkedin-post-analytics** | 커맨드 | 사용자 **본인**의 LinkedIn 게시물 분석을 **읽기 전용**으로 스냅샷해 **`networking.json`**의 `networking[]`에 저장합니다(게시물별 **`analytics_history`**). 호스트 **브라우저 제어**(예: **Claude in Chrome** MCP 또는 **computer / browser use**)와 이동 전 **사용자의 명시적 승인**이 필요합니다. **`linkedin-post-analytics`** 스킬을 참고하세요. |
| **/careerloop:event-radar** | 커맨드 | **지역, 광역, 전국, 국제** 범위(적절한 경우)의 이벤트를 발굴하며, ROI 등급과 발표 표시와 함께 순위를 매깁니다. **`networking-strategist`**를 호출합니다. |

# **4. 에이전트**

에이전트는 특정 역할에 집중하는 전문화된 Claude 인스턴스입니다. 직접 호출하거나 커맨드가 오케스트레이션할 수 있으며, 복잡한 작업에서는 여러 에이전트가 협업할 수 있습니다.

**모델 선택(비용 대 추론):** 기본적으로 시스템은 일상적인 워크플로와 예약 실행에 빠르고 비용 효율적인 추론 모델(예: Sonnet급)을 가정합니다. 복잡한 작업(다단계 전략, 모호한 트레이드오프, 대규모 종합 분석, 중요도 높은 메시지 작성)에는 더 강력한 추론 모델(예: Opus급)을 활성화할 수 있습니다. 사용자는 이를 명확하게 제어할 수 있어야 하며(전역 기본값 + 실행별 재정의), 그래야 비용을 의도적으로 관리하면서도 중요한 순간에는 더 높은 추론 능력을 “투입”할 수 있습니다.

| 이름 | Phase | 설명 |
| --- | --- | --- |
| **resume-coach** | 1B | ExperienceLibrary를 분석하고, 격차와 강점을 파악하며, ATS 호환성을 최적화하고, 서사 코칭을 제공합니다. `tailor-resume`와 `resume-score` 스킬이 호출합니다. `tailor-resume`가 문체에 맞춘 요약(Summary) 다듬기를 요청하면 **`writer`**용 **ResumeSummaryBrief**를 내보낼 수 있습니다. |
| **analyst** | 1B | 지원 결과 데이터를 분석해 무엇이 진행되고 무엇이 막히는지 패턴을 파악합니다. 사용자 경험 중 여러 직무와 산업에 걸쳐 적용되는 이전 가능한 강점과 핵심 역량을 식별합니다. Anthropic Economic Index를 활용해 현재 및 목표 직무의 AI·자동화 대체 위험을 평가합니다. ExperienceLibrary 성과 가중치를 갱신하고 `job-scout`와 `resume-coach`에 추천을 전달합니다. |
| **honest-advisor** | 1C | 특정 직무에 대한 사용자의 경쟁력, 채용 담당자가 우려할 만한 점, 장벽을 극복할 전략을 솔직하게 평가합니다. 일반적 기준과 다른 기업·산업별 예외를 조사합니다. 공감하되 가차 없습니다. |
| **market-researcher** | 1C | 거시 채용 동향, 직무별 수요 신호, AI/자동화 대체 위험, 지역별 수요 패턴, 업종별 사이클을 모니터링합니다. `market-brief` 커맨드와 `job-scout` 에이전트에 결과를 전달합니다. 또한 게시물 평가 시 `writer`가 호출해 목표 기업·산업별 문화적/정치적 리스크 맥락을 제공하므로, 정적 평가표가 아니라 동적인 리스크 평가가 가능합니다. |
| **job-scout** | 1D | 구성된 모든 구인 사이트에서 채용 기회를 검색하고 순위를 매깁니다. 점수에 결과 이력과 시장 인텔리전스를 반영합니다. 사용자가 결과를 기록할수록 순위가 개선됩니다. 매칭도가 높은 기회를 선제적으로 제시합니다. |
| **networking-strategist** | 1E | 네트워크 분석, 격차 식별, 웜 패스(warm-path) 계획. ROI 평가를 포함한 이벤트 발굴 및 평가, **발표 기회** 표시, 다중 범위 **이벤트 레이더**(**`event-intelligence`**, **`event-radar`** 스킬 경유). 사용자가 LinkedIn 가시성을 키우는 중이면 **`linkedin-post-analytics`** 스킬(주간/격주 또는 **`/schedule`**)을 권장합니다 — 호스트 브라우저 자동화와 명시적 동의가 전제입니다. 메시지 작성이 필요하면 **`writer`**용 구조화된 **인계 브리프**를 내보낼 수 있으며, 아웃리치 문안은 **직접 작성하지 않습니다**. |
| **writer** | 1E | **CareerLoop의 사용자 대상 문안**을 담당합니다: 아웃리치(LinkedIn, 이메일, InMail), **자기소개서**(**CoverLetterBrief** 기반), **후속 조치**(**FollowUpBrief** 기반), 선택적 **이력서 요약(Summary)** 다듬기(**ResumeSummaryBrief**), 게시물 초안(**`{user_dir}/LinkedIn Posts/`** 아래에 저장하고 **`artifacts-index.json`**에 **`linkedin_post`**로 기록), **`/careerloop:draft-outreach`**, **`content-suggest`**, **`evaluate-post`**. 어조 일치를 위해 **`voice-profile.md`**(및 선택적 **`voice_profile_v1`**)를 유지하며, 음성 메타데이터의 **타임라인 노출**은 **Phase 3**입니다. **`networking-strategist`**, **`resume-coach`**(요약 경로), **`cover-letter`**, **`follow-up`**의 인계를 받습니다. 게시물 리스크 평가 시에는 문화적·정치적 리스크를 평가하기 전에 목표 기업/산업 규범에 대한 **`market-researcher`** 브리프를 받아 사용합니다. 아웃리치 이메일/캘린더 보강은 **Phase 2A**. |
| **interview-coach** | 2B | 면접 **준비**, **모의 면접**, 그리고 `daily-schedule`용 당일 **`morning_section`** 요점. 단계에는 **recruiter**(일급 지원), hiring manager, technical, panel, executive, final이 있습니다. 모드: guided / random / adaptive, 분위기(vibe): supportive부터 bored까지. 텍스트 전용이며, 사용자가 받아쓰기를 하면 붙여넣은 호스트 STT 전사본을 **user_audio_transcript**로 받습니다(**사용자 본인의 입력만** — §13.1의 취지 참고). 준비와 모의 면접에서 스토리 근거는 주로 **`story-retrieval`**을 통해 **`StoryCorpus.json`**에서 가져옵니다(ExperienceLibrary는 대체 수단). 사양 파일: `agents/interview-coach/AGENT.md`. |

# **5. 스킬**

스킬은 관련 맥락이 감지되면 명시적인 커맨드 호출 없이 Claude가 활성화하는 자동 트리거 기능입니다. 이것이 CareerLoop의 기본 상호작용 모델이며, 커맨드는 이를 선호하는 사용자를 위한 명시적 별칭이고 행동 지능은 스킬이 담당합니다.

**워크플로 스킬**은 핵심 구직 작업을 처리하며 대화 의도에 따라 실행됩니다.

| 이름 | 유형 | 설명 |
| --- | --- | --- |
| **tailor-resume** | 스킬 | 사용자가 채용 공고를 공유·붙여넣거나 특정 직무에 지원하려는 의도를 표현하면 실행됩니다. ExperienceLibrary를 읽고 **`resume-coach`**를 호출해 ATS에 최적화된 이력서를 조립하며, 사용자가 **문체에 맞춘 요약(Summary)** 문장을 요청하면 **`writer`**(**`resume-summary`** 모드)를 호출할 수 있습니다. 아티팩트 인벤토리에 저장합니다. `/careerloop:tailor-resume`로도 호출할 수 있습니다. |
| **cover-letter** | 스킬 | 직무에 맞춰 이력서를 작성한 뒤, 또는 사용자가 특정 공고용 자기소개서를 명시적으로 요청하면 실행됩니다. **CoverLetterBrief**를 만들고 **`writer`**를 호출해 최종본을 작성합니다. 아티팩트 인벤토리에 저장합니다. `/careerloop:cover-letter`로도 호출할 수 있습니다. |
| **track-application** | 스킬 | 사용자가 공고에 지원했다고 언급하거나, 새 지원(건)을 기록하거나, 기존 지원(건)을 갱신할 때 실행됩니다(예: "I just applied to Acme" 또는 "I got a callback from Google"). 대화형 입력을 트래커 데이터베이스에 맞게 자동으로 구조화합니다. `/careerloop:track-application`로도 호출할 수 있습니다. |
| **add-source** | 스킬 | 사용자가 새 이력서, CV, 포트폴리오 문서를 업로드하거나 언급하면 실행됩니다. 경험 단위를 추출해 ExperienceLibrary에 추가합니다. `/careerloop:add-source`로도 호출할 수 있습니다. |
| **resume-score** | 스킬 | 사용자가 맞춤 작성을 명시적으로 요청하지 않고 이력서를 채용 공고와 함께 공유하면 실행됩니다. ATS 키워드 일치도, 서식 준수 여부, 서사 강도를 점수화합니다. `/careerloop:resume-score`로도 호출할 수 있습니다. |
| **list-artifacts** | 스킬 | 사용자가 생성된 문서, 아티팩트 이력, 지금까지 만든 결과물을 보여 달라고 요청하면 실행됩니다. `/careerloop:list-artifacts`로도 호출할 수 있습니다. |
| **assessment** | 스킬 | 사용자가 목표 직무 요건 대비 정직한 평가와 격차 분석을 요청하면 실행됩니다. `honest-advisor` 에이전트의 규범/예외/전략 패턴을 사용해 근거 기반의 격차와 재포지셔닝 옵션을 제시합니다. |
| **market-brief** | 스킬 | 사용자가 현재 시장 상황을 물으면 실행됩니다. `market-researcher`를 호출해 직무 수요 동향, AI/자동화 대체 신호, 지역별 경쟁력을 요약합니다. `/careerloop:market-brief`로도 호출할 수 있습니다. |
| **suggest-roles** | 스킬 | 사용자가 목표로 삼을 만한 인접 직무나 자명하지 않은 직무를 물으면 실행됩니다. `honest-advisor`와 `market-researcher`를 호출한 뒤, job-scout 점수 개선을 위해 `tracker.json`에 `strategy_signals`를 기록합니다. `/careerloop:suggest-roles`로도 호출할 수 있습니다. |
| **training-roi** | 스킬 | 사용자가 다음에 무엇을 배워야 할지 물으면 실행됩니다. 자격증, 학위, 부트캠프, 독학을 비용-편익-시간 ROI 프레임워크로 비교하고 주 경로와 대체 경로를 추천합니다. 정적 지식으로 대체하기 전에, 사용 가능한 MCP(연결된 경우 CareerOneStop DOL API 포함)에 자격증 가치와 노동시장 성과에 대한 실시간 데이터를 먼저 조회합니다. §15의 Phase 1C 참고 사항을 보세요. |
| **career-plan** | 스킬 | `CareerTrajectoryReport`(단기/중기/장기 + ROI 순 격차)를 생성하며, 리포트는 `{user_dir}/CareerLoop/career-trajectory.md`에, `career_trajectory_v1`은 `{user_dir}/CareerLoop/career-trajectory-data.json`에 저장합니다. `/careerloop:career-plan`로도 호출할 수 있습니다. |
| **evaluate-offer** | 스킬 | 상황 인지형 컨텍스트, 직무 적합도/활용도, 보상 공정성을 담은 `OfferEvaluationReport`를 생성하고, 후속 협상/비교에서 쓸 수 있도록 `offer-context-{application_id}.json`을 저장합니다. `/careerloop:evaluate-offer`로도 호출할 수 있습니다. |
| **compare-offers** | 스킬 | 진행 중인 오퍼 전체에 대한 `OfferComparisonReport`를 생성하고, 필요하면 동점 처리 기준과 함께 정직한 순위를 출력합니다. `/careerloop:compare-offers`로도 호출할 수 있습니다. |
| **negotiate-offer** | 스킬 | `NegotiationBrief`를 생성하고, `writer`가 바로 보낼 수 있는 협상 메시지를 작성하도록 `NegotiationHandoffBrief`를 내보냅니다. `/careerloop:negotiate-offer`로도 호출할 수 있습니다. |
| **networking-strategy** | 스킬 | 사용자가 구직을 위한 네트워킹 계획을 원할 때 실행됩니다. **networking-strategy** 모드로 **`networking-strategist`**를 호출합니다(전략과 인계 요점만 다루며, 아웃리치 문안은 **`writer`**가 담당). `/careerloop:networking-strategy`로도 호출할 수 있습니다. |
| **network-map** | 스킬 | 사용자가 목표 기업(드림 잡 레버리지 포함)으로 이어지는 경로와 격차의 구조화된 지도를 원할 때 실행됩니다. 이후 **Phase 3** 그래프 시각화에 쓰일 **`network_map_v1`** JSON을 생성합니다. **`networking-strategist`**를 호출합니다. `/careerloop:network-map`로도 호출할 수 있습니다. |
| **event-intelligence** | 스킬 | 사용자가 특정 이벤트 참석 여부를 묻거나, ROI 또는 연사/CFP 평가를 원하거나, 발표 기회를 물을 때 실행됩니다. **event-intelligence** 모드로 **`networking-strategist`**를 호출합니다. `/careerloop:event-intelligence`로도 호출할 수 있습니다. |
| **event-radar** | 스킬 | 사용자가 지역, 광역, 전국, 국제 범위의 이벤트를 지속적으로 발굴하길 원할 때 실행됩니다. **event-radar** 모드로 **`networking-strategist`**를 호출합니다. `/careerloop:event-radar`로도 호출할 수 있습니다. |
| **follow-up** | 스킬 | **company-windows.json**을 사용해 후속 조치 대기열을 보여 주고, **FollowUpBrief** 항목을 만들며, **`writer`**를 호출해 바로 보낼 수 있는 메시지를 작성합니다. `/careerloop:follow-up`로도 호출할 수 있습니다. |
| **draft-outreach** | 스킬 | 아웃리치 문안(LinkedIn, 이메일, InMail)을 위해 **`writer`**를 호출합니다. `/careerloop:draft-outreach`로도 호출할 수 있습니다. |
| **content-suggest** | 스킬 | LinkedIn/전문 분야 주제 추천을 위해 **`writer`**를 호출합니다. `/careerloop:content-suggest`로도 호출할 수 있습니다. |
| **evaluate-post** | 스킬 | 청중 적합도와 목표 기업 프로필 대비 **문화적 / 정치적 / 평판상 리스크**를 위해 **`writer`**를 호출합니다. 리스크 평가는 동적입니다: 평가 전에 **`market-researcher`**에 목표 기업/산업별 규범을 조회합니다. 시스템은 사용자에게 리스크 맥락을 알릴 뿐, 콘텐츠 결정을 억제하거나 지시하지 않습니다. `/careerloop:evaluate-post`로도 호출할 수 있습니다. |
| **linkedin-post-analytics** | 스킬 | 사용자 **본인**의 LinkedIn 게시물 분석을 실제 사이트 UI에서 **읽기 전용**으로 수집해, **`networking.json`**의 `networking[]`에 **`type: "linkedin_post"`** 항목으로 추가하고 날짜별 스냅샷 배열인 **`analytics_history`**를 함께 기록합니다. 게시, 좋아요, 댓글은 **하지 않습니다**. 실행 전 호스트 브라우저 자동화(**Claude in Chrome** 또는 **computer / browser use**)와 **사용자의 명시적 승인**이 **필요**하며, 사용할 수 없으면 모델이 중단하고 사용자에게 도구를 활성화해 달라고 안내하도록 스킬에 지시되어 있습니다. `/careerloop:linkedin-post-analytics`로도 호출할 수 있습니다. |
| **prep-interview** | 스킬 | 추적 중인(또는 지정한) 직무에 대한 전체 면접 준비: 기업/뉴스 맥락, **단계별** 질문(**recruiter**부터 **final**까지), ExperienceLibrary 기반 말하기 요점, **`CareerLoop/interview-prep/`** 아래 저장되는 브리프, 지원(건) 상세 파일에 추가되는 **`[prep]`** 메모(**`applications/<application_id>.json`** → **`notes[]`**, `tracker.json` 요약 행의 **`notes_count`** 증가). **`interview-coach`**(`prep` 모드)를 호출합니다. `/careerloop:prep-interview`로도 호출할 수 있습니다. |
| **mock-interview** | 스킬 | 모의 세션: **guided** / **random** / **adaptive**, **stage** + **vibe**, mode/vibe를 생략하면 **기본값을 선택**합니다(스킬 §2.1 참고). **`interview-coach`**(`mock` 모드)를 호출합니다. 텍스트 전용. `/careerloop:mock-interview`로도 호출할 수 있습니다. |
| **interview-capture** | 스킬 | **에이전트가 아닙니다.** **녹음 오디오 파일**(**`mcp-transcribe`** 또는 호환 STT 경유)을 면접 후 선택 가입 방식으로 전사하고, 구조화된 시사점 도출, 지원 기록 갱신(상세 파일 **`applications/<application_id>.json`**과 **`tracker.json`** 요약 행)을 수행합니다. 고용주 경고는 1회 표시하며 §13.1의 보관 정책을 따릅니다. `/careerloop:interview-capture`로도 호출할 수 있습니다. |
| **mine-stories** | 스킬 | 일지, PKM 노트, 디브리프 및 관련 자료를 대상으로 한 오프라인/저비용 추출 패스로 **`StoryCorpus.json`**을 구축·갱신합니다. 실행(launch)/설정 시, 그리고 `{user_dir}`에 새 원본 문서가 나타날 때 증분 갱신으로 실행됩니다. |
| **story-retrieval** | 스킬 | 면접 준비/모의 면접의 STAR 매핑을 위해 **`StoryCorpus.json`**에서 역량이 일치하는 소규모 부분집합(보통 8~12개)을 가져옵니다. 이것이 기본 면접 스토리 선택 계층이며, 질의 시점에 원본 일지를 다시 읽는 일은 피합니다. |

**컨텍스트 스킬**은 모든 세션에서 주변 신호에 따라 실행됩니다.

| 이름 | 유형 | 설명 |
| --- | --- | --- |
| **ats-optimization** | 스킬 | 이력서를 편집하거나 생성할 때 자동으로 실행됩니다. ATS에 불리한 서식, 누락된 키워드, 구조적 문제를 점검하고 그 자리에서 수정안을 제안합니다. |
| **salary-research** | 스킬 | 어떤 맥락에서든 보상이 언급되면 실행됩니다. 논의 중인 직무, 레벨, 지역에 대한 최신 시장 데이터를 가져옵니다. |
| **follow-up-timing** | 스킬 | 트래커에서 지원(건)을 볼 때 실행됩니다. 경과 시간을 기업별 기준과 비교하고, 후속 조치가 필요한 경우 표시합니다. |
| **cultural-risk-flag** | 스킬 | LinkedIn 콘텐츠나 아웃리치 메시지를 작성할 때 실행됩니다. 평가를 **`evaluate-post`** / **`writer`** + **`market-researcher`**로 라우팅해 대상별로 하나의 리스크 평가표를 적용하며, 게시 전에 **`evaluate-post`** 실행을 사용자에게 권유할 수 있습니다. |
| **contact-context** | 스킬 | 목표 기업의 연락처가 식별되거나 사용자가 아웃리치 전에 이전 대화 맥락을 요청하면 실행됩니다. 이메일과 캘린더(**과거** + **예정된** 미팅)에서 주고받은 내용과 웜 네트워킹 신호를 검색하고, **`writer`** / **`draft-outreach`**용 **ContactContextBrief**를 제공합니다(Phase 2A). 사용 전 사용자 승인이 필요합니다. **`/careerloop:contact-context`**로도 호출할 수 있습니다. |

# **6. 스케줄링 및 반복 실행**

CareerLoop는 플러그인 저장소 안에 자체 cron 데몬이나 훅 런타임을 **포함하지 않습니다**. **Claude Cowork**에서의 실용적인 방식은 다음과 같습니다.

1. **스킬이 페이로드입니다** — 각 스킬(`daily-schedule`, `focus-career` 등)이 무엇을 할지와 데이터를 어디서 읽을지(`{user_dir}/CareerLoop/...`)를 정의합니다.
2. **사용자가 실행을 예약합니다** — 예: Cowork의 **`/schedule`**(또는 동등한 스케줄링 UI)로 `/careerloop:daily-schedule`(또는 `daily-schedule` 스킬을 호출하는 자연어)을 일정 주기로 실행하는 반복 작업을 만듭니다.
3. **Cowork가 프롬프트를 학습합니다** — 첫 실행이 성공한 뒤, 호스트가 예약된 프롬프트를 해석된 경로, 커넥터, 컨텍스트로 정제합니다. 이것이 전통적인 “훅”에 대응하는 Cowork의 방식입니다.

| 이름 | 유형 | 설명 |
| --- | --- | --- |
| **focus-career** | 스킬 | 사용자가 세션을 열 때(또는 선제적인 중요 항목 점검을 원하면 `/schedule`로 짧은 주기로) 실행합니다. **중요 항목만** 알립니다(임박한 마감, 당일 후속 조치, 면접 당일 긴급 조치). |
| **daily-schedule** | 스킬 | `/schedule`을 통한 **매일 실행을 권장**합니다. 요약 전에 `{user_dir}`의 아티팩트 파일을 확인하고 있으면 `artifact-saved`를 실행한 뒤, 파이프라인 요약, 후속 조치, **오늘의 미팅**(면접/리크루터/스크리닝 — 스킬 §3.1 참고), 해당 시 **조건부 면접 전 브리프**, 시장/전략 프롬프트를 제공합니다. "morning brief before my interview" 같은 요청은 **집중** 실행(면접 전 부분만)을 트리거합니다. |
| **setup-schedule** | 스킬 | **Phase 3.** launch 후 한 번 실행해 `careerloop-daily-brief` Cowork 예약 작업을 만들고, 선택적으로 두 번째 `careerloop-pipeline-refresh` 작업도 만듭니다. 완전히 자체 완결된 작업 프롬프트(해석된 `{user_dir}` 경로)를 구성합니다. 일일 브리프는 사용자가 정한 주기(기본 매일 오전 7시)로 daily-schedule 워크플로를 실행합니다: 2단계 Gmail 받은편지함 스캔(7일 전체 + 30일 기업별 백필), 후속 조치 알림, `recommendations.json`에 추가되는 신규 공고 발굴. 선택적 파이프라인 새로 고침은 `pipeline-status` 스킬을 매일 밤(기본 매일 오전 2시) 실행해 `pipeline-status.html`을 재생성합니다. 중복을 막기 위해 기존 작업(둘 중 어느 쪽이든 독립적으로)을 감지해 갱신합니다. `/careerloop:setup-schedule`로 호출할 수 있습니다. |
| **pipeline-status** | 스킬 | `tracker.json`, `recommendations.json`, `passed.json`으로부터 파이프라인 상태 페이지를 생성합니다 — `{user_dir}/CareerLoop/pipeline-status.html`에 위치한 정적 자체 완결형 HTML 페이지이며, 같은 위치의 `pipeline-data.js`와 내장 `timeline.html`을 함께 사용합니다. 상태 / 섹션 / 평점으로 필터링할 수 있고, 진행 중 / 집중 / 종료 / 제외 섹션과 지원 타임라인 iframe을 갖습니다. 요청 시 항상 최신 스냅샷이며, `setup-schedule`을 통해 매일 밤 재생성하도록 예약할 수 있습니다. 브라우저에서 자동으로 열립니다. `/careerloop:pipeline-status`로 호출할 수 있습니다. |
| **application-update** | 스킬 | `track-application`이 지원 기록(`tracker.json` 요약 행 + 상세/연락처 파일, 같은 턴)을 쓴 **뒤에** 실행합니다. 결과 가중 점수화를 위한 새로 고침 우선순위를 분류하고, 마일스톤마다 `pattern-analysis`를 상기시킵니다. |
| **artifact-saved** | 스킬 | 새 이력서/자기소개서가 저장된 **뒤에**, 및/또는 PDF/DOCX 아티팩트가 있을 때 `daily-schedule`에서 실행합니다. `artifacts-index.json`을 디스크의 파일과 정합시키고, 커넥터가 있으면 분석 인계 메타데이터를 준비합니다. |

## **6.1 호스트 훅 (`hooks/hooks.json`)**

Claude Cowork는 플러그인 수준의 **`hooks/hooks.json`**을 지원합니다(**cowork-plugin-management** 참고). 사용 가능한 호스트 이벤트에는 `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `Stop`, `PreToolUse`, `PostToolUse`, `SubagentStop`, `PreCompact`, `Notification` 등이 있으며, 그 외는 호스트 문서를 따릅니다.

CareerLoop는 기본으로 훅을 등록하지 않습니다(`hooks/hooks.json`은 비어 있음). 다음은 사용자가 직접 등록할 수 있는 선택 구성입니다.

* **`SessionStart`** — `command` 훅이 `cat "${CLAUDE_PLUGIN_ROOT}/hooks/context/session-start.md"`를 실행해 지침을 주입함으로써, 모델이 중요 항목만 알리는 **`focus-career`** 스킬(`skills/focus-career/SKILL.md`)을 실행하도록 합니다.

**프롬프트 기반** 훅(`type: "prompt"`)은 호스트 문서에 따라 일부 이벤트에서만 지원되며, **커맨드 기반** 훅은 결정적인 컨텍스트 주입에 쓸 수 있습니다(위 `SessionStart` 예시처럼).

이는 **`/schedule`**과 **별개**입니다: 호스트 훅은 세션/도구 수명주기 이벤트에서 실행되며, **`daily-schedule`** 스킬은 사용자가 Cowork에서 구성하는 반복 작업의 권장 **일일** 페이로드로 남습니다.

# **7. 스토리지 커넥터**

*사양:* 이 절(인터페이스 + 로드맵). *관련 문서:* `CONNECTORS.md`(OAuth / 호스트 커넥터). 클라우드 스토리지 백엔드는 Phase **2C**입니다.

플러그인은 표준 아티팩트 스토리지 인터페이스를 정의합니다. 사용자는 플러그인 설정에서 활성 커넥터를 하나만 구성합니다. 모든 플러그인 구성 요소는 어떤 백엔드가 활성인지 알지 못한 채 인터페이스 메서드를 호출합니다.

## **7.1 인터페이스**

| 이름 | 유형 | 설명 |
| --- | --- | --- |
| **save\_artifact()** | 메서드 | 생성된 문서(이력서, 자기소개서 등)를 메타데이터와 함께 구성된 스토리지 백엔드에 저장합니다. |
| **list\_artifacts()** | 메서드 | 유형, 날짜, 관련 공고, 결과 등의 메타데이터와 함께 모든 아티팩트의 필터링 가능한 목록을 반환합니다. |
| **get\_artifact()** | 메서드 | ID로 특정 아티팩트를 가져와 표시하거나 재사용합니다. |
| **save\_event()** | 메서드 | 트래커 이벤트(지원 갱신, 면접 결과 등)를 구조화된 이벤트 데이터베이스에 기록합니다. |
| **query\_events()** | 메서드 | 분석에서 사용할 구조화된 이벤트 데이터를 반환합니다. 날짜 범위, 직무 유형, 기업, 결과별 필터링을 지원합니다. |

## **7.2 사용 가능한 커넥터**

| 이름 | 유형 | 설명 |
| --- | --- | --- |
| **local** | 커넥터 | 기본 커넥터. 모든 데이터를 `{user_dir}`에 로컬로 저장합니다. 클라우드 의존성과 자격 증명이 필요 없습니다. Phase 1의 모든 기능이 이 커넥터를 사용합니다. |

클라우드 스토리지 커넥터(Google Drive, OneDrive, Dropbox)는 Phase 2C에서 도입됩니다. **Google Drive, OneDrive, Dropbox**의 경우 이식성은 **Google Drive 애플리케이션 동기화** 또는 수동 백업/복원으로 처리합니다(일반적인 구직 파일에는 호스트 커넥터를 쓰지 않음).\.

# **8. 분석 커넥터**

*사양:* 이 절. *현재 제공되는 가장 가까운 동작:* 로컬 데이터를 사용하는 파이프라인/대시보드 흐름은 `skills/pipeline-status/SKILL.md`.

분석 계층은 스토리지 커넥터의 구조화된 이벤트 데이터를 받아 인사이트, 시각화, 대시보드 뷰를 생성합니다. BI 도구가 없는 사용자를 위해 플러그인에는 SQLite 기반 분석 엔진이 기본 내장되어 있습니다.

| 이름 | 유형 | 설명 |
| --- | --- | --- |
| **sqlite-builtin** | 커넥터 | 기본 커넥터. 내장 쿼리 엔진을 갖춘 로컬 SQLite 데이터베이스입니다. /careerloop:pipeline-status 대시보드와 인사이트 엔진을 네이티브로 구동합니다. |
| **power-bi** | 커넥터 | 이벤트 데이터를 Power BI 스트리밍 데이터셋으로 푸시합니다. Power BI Desktop 또는 Service에서 맞춤 대시보드를 만들 수 있게 합니다. |
| **qlik** | 커넥터 | Qlik Engine API를 통해 Qlik Sense 또는 QlikView와 연동합니다. 전체 지원 데이터셋에 걸친 연관 분석을 가능하게 합니다. |
| **d3** | 커넥터 | 맞춤 시각화 개발을 위해 구조화된 이벤트 데이터를 D3 호환 JSON 형식으로 내보냅니다. |

# **9. 외부 서비스 연동 (.mcp.json)**

플러그인은 **Gmail**, **Google Calendar**, 및/또는 **`ms365`**(Microsoft 365 / Outlook — 받은편지함과 캘린더 맥락에서 Google의 대안, 파일 참고)용 선택적 Anthropic **HTTP MCP** 서버가 포함된 **`.mcp.json`**을 제공하며, 그 밖의 커넥터는 사용자가 Claude를 실행하는 **클라이언트**에서 구성합니다. **`search-jobs`**의 경우 사용자는 **Claude Desktop → Customize → Connectors**에서 **Indeed** 커넥터를 추가하고 **Connect**를 클릭한 뒤 **secure.indeed.com**에서 **브라우저 OAuth**를 완료합니다(앱 내 **Grant access to Indeed**, 도구 **`search_jobs`**, **`get_job_details`**). **salary-research**의 경우 사용자는 **Apify** **Desktop** 커넥터를 추가하고 **Apify 토큰**을 붙여넣은 뒤 **Enabled tools**를 **`call-actor,get-actor-run,get-dataset-items,cheapget/best-job-search`**로 설정하고 저장·활성화한 다음 새 세션을 시작합니다. 토큰은 호스트의 커넥터 UI에 직접 입력되어 그곳에 보관되며, 플러그인은 로컬 환경 변수, 도트파일, 설정 파일에서 이를 읽지 않습니다. 이는 JSON 인자의 셸 스타일 변수 참조가 확장되지 않고 문자 그대로 전달되는 취약한 원격 MCP 구성을 피하기 위함입니다. **받은편지함 및 캘린더 맥락**(**`draft-outreach`**, **`follow-up`**, **`contact-context`**)을 위해 사용자는 Anthropic의 **Gmail** 및/또는 **Microsoft 365** 커넥터 및/또는 **Google Calendar**를 추가합니다(브라우저에서 **OAuth** — 저장소 JSON에 비밀번호나 리프레시 토큰을 두지 않음). 아래 표와 **`CONNECTORS.md`**를 참고하세요. **Google Calendar**는 커넥터 카탈로그에서 **Gmail**과 별개의 커넥터입니다. **PKM 기반 면접 스토리 발굴**(**`mine-stories`**)을 위해 사용자는 1st-party 커넥터로 **Notion**을 연결하거나, 호스트 세션에서 사용 가능한 MCP 연동을 통해 **Capacities**를 사용할 수 있으며, 사용할 수 없으면 워크플로는 `{user_dir}`의 파일 기반 내보내기로 대체됩니다.

대화형 안내는 `/careerloop:launch`를 실행하세요. 각 연동은 선택 사항이며, 커넥터가 없으면 스킬은 기능을 축소해 동작합니다.

**멀티 채널 소싱 정책(구현 지침):**
- 커넥터 우선 순서를 사용합니다: 먼저 MCP 도구, 필요하면 브라우저 보조 수집, 그다음 반수동 입력 대체 수단.
- 순위를 매기기 전에 모든 채널의 공고를 필수 필드 `title`, `company`, `location`, `apply_url`, `source`, `retrieval_mode`로 정규화합니다.
- 출처 인지형 신뢰도 등급(`high`, `moderate`, `directional`)을 적용하고, 채널 간 중복 제거 우선순위는 기업 직접 URL > ATS 요청서(requisition) URL > 커넥터 기반 애그리게이터 > 수동 입력 순입니다.
- 출력에 출처(provenance)를 명시해 사용자가 어떤 결과가 실시간 커넥터 데이터이고 어떤 결과가 브라우저/수동 수집인지 알 수 있게 합니다.

| 이름 | 유형 | 설명 |
| --- | --- | --- |
| **Apify** | MCP (Desktop 커넥터) | **cheapget/best-job-search** 및 관련 도구를 통해 **`salary-research`**를 구동합니다. Claude Desktop 커넥터 UI에서 구성하며 `.mcp.json`에는 커밋하지 않습니다. |
| **Indeed** | MCP (Claude 커넥터) | 공식 **`search-jobs`** 경로: **`search_jobs`**, **`get_job_details`**. **Customize → Connectors**에서 **Connect** 후 **secure.indeed.com**에서 OAuth를 진행합니다. 커넥터 엔드포인트 `https://mcp.indeed.com/claude/mcp`. 안내는 `/careerloop:launch` Step 3에 있습니다. |
| **LinkedIn** | MCP | 채용 공고 검색, 연결 그래프 접근, InMail 초안 작성, 게시물 발행 및 분석. 네트워킹 전략 기능에 필요합니다. |
| **JobSearch** | MCP | 더 폭넓은 공고 데이터 연동(스크래핑 API, 추가 구인 사이트). Phase 1A의 주요 실시간 검색은 위의 **Indeed** MCP이며, 이 행은 대체/향후 소스를 다룹니다. |
| **Glassdoor** | MCP | 기업 문화 리서치, 면접 경험 데이터, 연봉 벤치마크, 리크루터 프로세스 타임라인. |
| **CareerOneStop** | MCP | 미국 노동부 API. 무료. 노동시장 데이터, 연봉 범위, 직업 전망, American Job Center 위치를 제공합니다. `training-roi` 스킬의 실시간 데이터 소스 후보이기도 합니다 — §15의 Phase 1C 참고 사항을 보세요. |
| **IllinoisJobLink** | MCP | 일리노이 전용 구인 사이트. 주 정부 고용 자원과 지역 공고 발굴. |
| **Gmail** | Claude 1st-party 커넥터 | **Settings / Customize → Connectors → Gmail → Connect** — 브라우저에서 Google **OAuth**를 진행하며, `.mcp.json`에 토큰을 커밋하지 않습니다. Anthropic은 메일 **검색 및 분석**만 문서화하고 있으며, 이 연동으로는 **생성/발송/수정이 불가**합니다. Claude 문서상 **Pro / Max / Team / Enterprise**(제품에서 확인). CareerLoop: **`draft-outreach`**, **`follow-up`**, **`contact-context`**는 조회마다 **사용자의 명시적 승인**을 받은 뒤에만 메일을 사용합니다. `CONNECTORS.md`, [Gmail integration](https://claude.com/docs/connectors/google/gmail)을 참고하세요. |
| **Microsoft 365** (제품 범위에 따라 Outlook 메일, SharePoint, OneDrive, Teams) | Claude 1st-party 커넥터 | **Connectors → Microsoft 365 → Connect** — Microsoft **OAuth**. Anthropic 안내에 따라 **Team/Enterprise**이며 대개 **테넌트 관리자** 설정이 필요합니다. **읽기 전용**으로 문서화되어 있습니다(커넥터를 통한 수정/삭제/생성 불가). Outlook 스레드 검색은 Gmail과 동일한 CareerLoop 스킬을 지원합니다. `CONNECTORS.md`, [Microsoft 365 connector](https://claude.com/docs/connectors/microsoft/365)를 참고하세요. |
| **Google Calendar** | Claude 1st-party 커넥터 (Google) | **Settings / Customize → Connectors → Google Calendar → Connect** — 브라우저에서 Google **OAuth**(**Gmail**과 별개의 카드). Anthropic은 [Google Calendar integration](https://claude.com/docs/connectors/google/calendar)에 따라 일정 및 이벤트 접근을 문서화하고 있습니다. CareerLoop: **`contact-context`**(및 이후 초안 작성)는 조회마다 **사용자의 명시적 승인** 후 **읽기 전용**으로 **과거** 및 **예정된** 미팅 맥락을 사용합니다 — 미팅이 예정되어 있으면 **웜(warm)** 관계로 식별하며, 사용자가 요청하지 않는 한 이벤트를 만들거나 옮기지 않습니다. `CONNECTORS.md`를 참고하세요. |
| **Notion** | Claude 1st-party 커넥터 | 면접 스토리 발굴을 위한 선택적 PKM 소스. 연결되면 `mine-stories`가 적격한 노트/페이지를 읽어 스토리 후보를 `StoryCorpus.json`으로 추출할 수 있습니다(커넥터 권한 범위 적용). |
| **Outlook Calendar / Teams Calendar** | Microsoft 365 커넥터 | 활성화된 경우 **Microsoft 365** 행에 포함됩니다. |
| **Capacities** | MCP (호스트 확장/서버) | 면접 스토리 발굴을 위한 선택적 PKM 소스. 이를 지원하는 호스트에서는 Capacities MCP 연동으로 연결할 수 있으며, 사용할 수 없으면 노트를 `{user_dir}`로 내보내 파일에서 발굴합니다. |
| **Greenhouse / Workday / Lever** | MCP | 이 플랫폼을 통해 제출한 지원(건)의 ATS 상태 추적. 지원 상태에 대한 읽기 전용 접근. |
| **mcp-transcribe** (로컬 MCP 서버) | 소스 설치, 번들 없음 | **`interview-capture`**용 **로컬** 파일 전사(녹음 오디오만 해당 — `prep-interview`와 `mock-interview`는 텍스트 전용). `/careerloop:setup-transcribe`로 설치하거나 `mcp-transcribe/README.md`에 따라 수동 설치합니다. 소스: **`mcp-transcribe/`**, 도구 **`transcribe_file`**, **`backend_info`**. 프로젝트 **`.mcp.json`**에는 선언되지 않습니다. |
| **Meetup / Eventbrite / Luma** | MCP + 호스트 브라우저/수동 대체 | 네트워킹 레이더용 이벤트 발굴. Luma는 선택 사항이며 제공되지 않습니다 — 사용자 세션에 이미 있는 Luma MCP(예: 독립 프로젝트 **`alx1p/luma-mcp`**)를 사용하세요. Meetup/Eventbrite는 선택적으로 **Claude in Chrome**, **computer use**, 또는 **수동 복사/붙여넣기** 대체 수단을 사용합니다. |
| **호스트 브라우저 자동화** | 호스트 기능 (플러그인 MCP 아님) | **Claude in Chrome**, **computer use** 또는 동등 기능: **`linkedin-post-analytics`**가 로그인된 브라우저를 **읽기 전용**으로 탐색해 본인 게시물 지표를 **`networking.json`**(**`networking[]`**)에 기록할 수 있게 합니다. 사용자가 세션 또는 스케줄마다 옵트인해야 하며, **LinkedIn** MCP 행(검색, 메시징 같은 선택적 커넥터 기능을 설명)과는 별개입니다. |

# **10. 핵심 데이터 모델**

지원 데이터는 [tracker-schema.md](tracker-schema.md)에 정의된 분리 레이아웃을 사용합니다 — 읽거나 쓰기 전에 반드시 먼저 읽으세요. 아래 §10.2는 필드 수준의 공식 정의이며, `tracker-schema.md`는 에이전트와 스킬이 따르는 운영 참조 문서입니다.

## **10.0 사용자 프로필**

`{user_dir}/CareerLoop/profile.md`에 저장됩니다. `/careerloop:launch`가 생성하며, `{user_dir}`의 문서를 스캔해 기존 이력서와 자기소개서로부터 프로필을 구성하고, 문서가 없으면 대화형 Q&A로 대체합니다. 모든 에이전트가 모든 작업을 시작할 때 자동으로 읽으며, 에이전트는 프로필에 이미 있는 정보를 다시 묻지 않아야 합니다.

* **identity** — 이름, 위치, 연락처, 직무 요약, 핵심 차별점
* **target\_roles** — 선호 직함, 최소 직급 수준
* **target\_companies** — 1순위, 2순위, 3순위 목표 기업, 우선할 산업과 피할 산업
* **compensation\_floor** — 최소 총 보상(기본급 + 보너스 + 연 환산 주식 보상), 기업 유형별 기대 범위
* **location** — 지역 선호, 이주 가능성, 원격/하이브리드 선호. `location` 필드는 데이터 보관 정책을 위한 관할권 감지에도 사용됩니다(§13.1 및 Phase 2B 참고). 관할권을 판단할 수 없으면 첫 녹음 세션에서 사용자에게 정책을 선택하도록 안내합니다.
* **key\_skills** — ATS 매칭과 ExperienceLibrary 태깅을 위한 우선순위 스킬 목록
* **differentiators** — 맞춤 작성한 모든 이력서에 반드시 들어가야 하는, 이름이 지정된 고가치 요소
* **search\_notes** — 에이전트에 대한 상시 지침: 선호 채널, 기업별 메모, 모든 검색과 지원에 반영되어야 하는 고정 정보

**선택적 동반 파일 — `{user_dir}/CareerLoop/voice-profile.md`**

**`/careerloop:launch`**는 **launch voice harvest**를 통해 이 파일을 생성하거나 갱신합니다: **PDF/DOCX/MD/TXT** 이력서(résumé), CV, 자기소개서를 스캔하고(플러그인이 생성한 아티팩트와 구분해 등급화), **LinkedIn**(붙여넣기, 파일 드롭, 또는 건너뛰기)을 요청하며, 어조가 갈릴 때는 **`## Voice by context`**를, 어조·“AI 슬롭” 티·비꼬는 말투 등 실용적 위험에 대해서는 **`## Voice quality flags (launch)`**를 기록할 수 있습니다. 이후 **`writer`**가 사용자가 붙여넣은 **`## User writing samples`** 블록과 **`voice_profile_v1`**을 유지하며, 초안 작성 시 다중 컨텍스트와 플래그를 존중합니다.

## **10.1 ExperienceLibrary**

*주요 파일:* `{user_dir}/CareerLoop/ExperienceLibrary.json`.

ExperienceLibrary는 개별 이력서의 모음이 아니라, 재조합할 수 있는 경험 단위의 구조화된 풀입니다. 각 단위에는 원본 문서, 직무 유형 관련성, 산업 태그, 성과 이력을 나타내는 메타데이터가 있습니다.

* source\_documents[ ] — 업로드된 원본 파일(이력서, CV, 포트폴리오)
* experience\_units[ ] — 원본 문서에서 추출한 개별 불릿, 성과, 직무
* skill\_tags[ ] — 모든 단위에 걸쳐 매핑되는 정규화된 스킬 분류 체계
* performance\_weights{ } — 단위별 결과 보정 가중치, 인사이트 엔진이 갱신

## **10.2 지원 기록(Application Record)**

*저장 위치:* `{user_dir}/CareerLoop/` 아래 세 가지 파일 유형 — `tracker.json` → `applications[]`의 요약 행, `applications/<application_id>.json`의 상세 파일, `contacts/<company-slug>.json`의 기업별 연락처 파일. *운영 참조:* [tracker-schema.md](tracker-schema.md).

```
{user_dir}/CareerLoop/
├── tracker.json                       요약 행만 저장
├── applications/<application_id>.json 지원 1건의 notes[] + stage_history[]
└── contacts/<company-slug>.json       한 기업의 모든 연락처
```

`tracker.json`의 `applications[]` 안에는 `notes`, `stage_history`, `contacts`가 들어 있지 않습니다. `tracker.json`만 읽어도 상세 정보를 불러오지 않고 전체 파이프라인을 한눈에 볼 수 있으며, 이것이 분리의 목적입니다. 상세 파일과 연락처 파일은 실제로 진행 중인 지원(건)에 대해서만 불러옵니다.

**application\_id**는 `app-<company-slug>-<role-keywords>` 형태의 서술형 슬러그입니다(예: `app-hex-senior-pm`, `app-anthropic-research-pm-labs`) — UUID, 단순 일련번호(`app-001`), 날짜 접미사가 붙은 id는 절대 사용하지 않습니다.

### 요약 행 — `tracker.json` → `applications[]`

| 이름 | 유형 | 설명 |
| --- | --- | --- |
| **id** (application\_id) | Slug | 고유 식별자, `app-<company-slug>-<role-keywords>` |
| **application** | String | 표시용 라벨, 정확히 `"<company> — <role>"`. 연락처 파일에서 조인 값으로 사용 |
| **company** | String | 기업명 |
| **role** (role\_title) | String | 지원한 직함 |
| **location** | String | 공고 근무지 |
| **job\_link** / **req\_id** | String | 공고를 찾은 위치와 요청서(requisition) id |
| **salary\_range** | String | 공고에 게시되었거나 협상된 범위 |
| **date\_applied** | Date | 지원 제출일 |
| **status** | Enum | Applied / Phone Screen / HM Interview / Panel / Final / Offer / Rejected / Withdrawn / Ghosted |
| **follow\_up\_date** / **next\_step** / **priority** | Date / Text / Enum | 후속 조치 일정 및 분류(triage) |
| **resume\_version** / **artifacts[ ]** | String / Array | 이력서 버전과 제출한 아티팩트의 ID |
| **outcome** | Enum | Pending / Hired / Rejected / Withdrew |
| **outcome\_notes** | Text | 알려진 경우 결과의 사유 |
| **detail\_file** | String | `CareerLoop/` 기준 상대 경로, 예: `applications/app-hex-senior-pm.json`. 항상 존재 |
| **contacts\_file** | String | `CareerLoop/` 기준 상대 경로, 예: `contacts/hex.json`. 지원(건)에 연락처가 있을 때만 존재 |
| **notes\_count** | Int | 상세 파일의 `notes[]` 항목 수 |
| **stage\_count** | Int | 상세 파일의 `stage_history[]` 항목 수 |
| **contact\_count** | Int | 이 지원(건)에 연결된 해당 기업 연락처 수 |
| **latest\_stage** | String | 마지막 `stage_history` 항목의 `stage` |
| **latest\_stage\_date** | Date | 마지막 `stage_history` 항목의 `date` |
| **previous\_ids[ ]** | Array | 이 지원(건)의 이전 id. 이름이 변경된 경우에만 존재 |

### 상세 파일 — `applications/<application_id>.json`

| 이름 | 유형 | 설명 |
| --- | --- | --- |
| **schema** | String | `application_detail_v1` |
| **application\_id** | Slug | 요약 행의 `id`와 일치 |
| **application** | String | `"<company> — <role>"` 라벨 |
| **company** / **role** | String | 요약 행에서 비정규화한 값 |
| **stage\_history[ ]** | Array | 모든 상태 변경의 타임스탬프 로그: `stage`, `date`, `notes`, `interview_type`, `interviewers[ ]`, `post_notes`. 단계 이력이 존재하는 유일한 위치 |
| **notes[ ]** | Array | 대화형 입력이나 면접 디브리프에서 나온 자유 형식 `{ date, text }` 항목. 메모 텍스트가 존재하는 유일한 위치 |

### 연락처 파일 — `contacts/<company-slug>.json`

| 이름 | 유형 | 설명 |
| --- | --- | --- |
| **company** | String | 기업명 |
| **contacts[ ]** | Array | 해당 기업의 알려진 연락처: `name`, `application`(이 항목이 속한 지원(건)의 라벨), `title`, `relationship`, `notes`, `interactions[ ]`(`date`, `type`, `notes`) |
| **contact\_count** | Int | `contacts[]` 항목 수 |

기업 파일 하나가 해당 기업의 모든 지원(건)을 담당합니다. 읽을 때는 요약 행의 `application` 라벨로 `contacts[]`를 필터링하고, 표시할 때는 `name` 기준으로 중복을 제거합니다. 기업 슬러그는 기업명을 소문자로 바꾸고 악센트를 제거한 뒤, 영숫자가 아닌 문자의 연속을 하이픈 하나로 치환한 값입니다(`84.51°` → `84-51`).

### 쓰기 규칙

지원 데이터를 변경하는 모든 쓰기는 **다중 파일 트랜잭션**입니다 — 요약 행의 카운터(`notes_count`, `stage_count`, `contact_count`, `latest_stage`, `latest_stage_date`)는 상세 파일이나 연락처 파일에 추가하는 것과 같은 작업에서 함께 갱신됩니다. id 이름 변경과 검증 단계를 포함한 전체 규칙은 [tracker-schema.md](tracker-schema.md)에 있습니다.

## **10.3 아티팩트 기록(Artifact Record)**

*인덱스:* `{user_dir}/CareerLoop/artifacts-index.json`.

| 이름 | 유형 | 설명 |
| --- | --- | --- |
| **artifact\_id** | UUID | 고유 식별자 |
| **type** | Enum | Resume / Cover Letter / LinkedIn post draft (`linkedin_post`) / Portfolio / Other |
| **application\_id** | Slug | 연관된 지원 id, 예: `app-hex-senior-pm` (템플릿은 null 허용) |
| **source\_units[ ]** | Array | 이 아티팩트에 포함된 경험 단위 ID |
| **jd\_keywords[ ]** | Array | 이 아티팩트가 겨냥한 키워드 |
| **ats\_score** | Float | 생성 시점의 ATS 호환성 점수 |
| **created\_at** | Timestamp | 생성일 |
| **storage\_path** | String | 구성된 스토리지 커넥터의 경로 또는 URL |

## **10.4 네트워킹 항목 및 LinkedIn 게시물 분석**

*데이터:* `{user_dir}/CareerLoop/networking.json` → `networking[]` 및 `recruiter_relationships[]`. *수집 동작:* `skills/linkedin-post-analytics/SKILL.md`.

`{user_dir}/CareerLoop/networking.json`은 `tracker.json`과 분리된 전용 파일이며 두 개의 최상위 배열을 갖습니다. **`networking`** 배열은 관계 및 가시성 아티팩트를 담습니다 — **`type: "linkedin_post"`**인 LinkedIn 게시물 분석 항목으로, 안정적인 **`url`**(LinkedIn activity URN URL), 선택적 **`description`** / **`date_posted`**, 그리고 **`analytics_history`**를 갖습니다. **`analytics_history`**는 노출 수, 도달 수, 반응, 댓글, 리포스트, 저장, 전송, 게시물에 기인한 프로필 조회자, 신규 팔로워, 링크 방문, 선택적 **`links`**, 그리고 UI가 제공하는 경우 선택적 **`top_audience`**(산업, 직급, 회사 규모)를 담은 날짜별 객체의 배열입니다. **`recruiter_relationships`** 배열은 리크루터와 에이전시 연락처를 단계 이력, 진행 중인 의뢰(mandate), 후속 조치 날짜와 함께 담습니다. **`networking-strategist`**는 관계 맥락을 위해 두 배열을 모두 읽으며, `networking[]`의 스키마 상세는 **`skills/linkedin-post-analytics/SKILL.md`**에 정의되어 있습니다.

## **10.5 스토리 코퍼스(Story Corpus)**

*주요 파일:* `{user_dir}/CareerLoop/StoryCorpus.json`.

스토리 코퍼스는 원본 일지, PKM 노트, 디브리프 및 관련 원본 문서에서 추출한 지속적이고 압축된 면접 근거 계층입니다. 면접 흐름이 매번 큰 원본을 다시 읽지 않고도 집중된 근거를 가져올 수 있도록 존재합니다.

**3계층 아키텍처:**

1. **추출(오프라인/1회성 또는 증분):** `mine-stories`가 원본 항목을 청크로 나누고, 저비용 추출 패스를 실행해 구조화된 후보를 저장합니다.
2. **영속 코퍼스:** 평탄화된 스토리 레코드가 역량/주제 태그와 품질/결과/주도성 신호와 함께 `StoryCorpus.json`에 저장됩니다.
3. **동적 매핑(질의 시점):** `story-retrieval`이 준비/모의 워크플로를 위해 적합도 순으로 정렬한 소규모 부분집합(기본 8~12개 스토리)을 가져옵니다.

권장 레코드 형태:

- `story_id`
- `source` (`journal` | `pkm` | `debrief` | `resume` | `other`)
- `date`
- `raw_summary`
- `themes[]`
- `competencies[]`
- `result_signal`
- `ownership_signal`
- `star_ready`
- 선택적 `embedding[]`

면접 준비/모의 면접은 이 코퍼스를 "내가 어떻게 해왔는가"에 대한 단일 진실 공급원으로 사용하며, ExperienceLibrary는 맞춤 작성과 더 넓은 커리어 워크플로를 위한 핵심 성과 인벤토리로 남습니다.

## **10.6 커리어 궤적 및 오퍼 컨텍스트 아티팩트**

의사결정 지원용 아티팩트 두 가지가 스킬 간 재사용을 위해 저장됩니다.

- **`{user_dir}/CareerLoop/career-trajectory.md`**  
  `career-plan`이 생성합니다. 사람이 읽을 수 있는 궤적 리포트입니다(마크다운 전용, 내장 JSON 없음).

- **`{user_dir}/CareerLoop/career-trajectory-data.json`**  
  `career-plan`이 생성합니다. `job-scout`, `search-jobs`, `compare-offers`, `daily-schedule`의 최신성(staleness) 점검에서 사용하는 기계가 읽을 수 있는 `career_trajectory_v1` 스키마입니다.

- **`{user_dir}/CareerLoop/offer-context-{application_id}.json`**  
  `evaluate-offer`가 생성합니다. 시나리오 분류, 벤치마크 프레이밍, 레버리지 맥락을 담아 `negotiate-offer`와 `compare-offers`가 중복 수집 없이 이어서 작업할 수 있게 합니다.

# **11. 인텔리전스 피드백 루프**

*관련 구현:* `agents/analyst/AGENT.md`, `agents/job-scout/AGENT.md`, `agents/resume-coach/AGENT.md`, `skills/pattern-analysis/SKILL.md`, `skills/ai-analysis/SKILL.md` (및 `track-application` / 맞춤 작성 스킬의 트래커 쓰기).

CareerLoop의 핵심 차별점은 모든 결과를 이후 추천에 다시 연결하는 폐쇄형 피드백 루프입니다. 루프는 다음과 같이 동작합니다.

* 사용자가 경험 단위 X, Y, Z로 조립한 아티팩트 A로 지원합니다
* 결과(콜백 / 불합격 / 무응답)를 기록합니다
* 인사이트 엔진이 모든 지원(건)에 걸친 결과 패턴을 분석합니다 — 단계 이력은 상세 파일에만 있으므로 `tracker.json` 요약 행과 각 지원(건)의 `detail_file`을 함께 읽습니다
* 패턴을 파이프라인 대시보드와 일일 요약에서 사용자에게 보여 줍니다
* 결과와의 상관관계에 따라 경험 단위의 성과 가중치를 조정합니다
* Job scout가 갱신된 가중치를 이후 직무 순위에 반영합니다
* Resume coach가 갱신된 가중치를 이후 아티팩트 조립 추천에 반영합니다
* Interview coach가 시사 이슈와 기업 리서치를 모의 면접 세션에 반영합니다
* Morning brief가 같은 시사 이슈를 면접 당일 준비에 반영합니다

시간이 지나면서 시스템은 일반적인 모범 사례가 아니라, 이 사용자가 속한 특정 시장에서 무엇이 통하는지에 대한 개인화된 모델을 구축합니다.

# **12. 일일 리듬 및 스케줄링**

*스킬 파일:* `skills/daily-schedule/SKILL.md`, `skills/focus-career/SKILL.md`, `skills/artifact-saved/SKILL.md`, `skills/follow-up/SKILL.md` (정리 작업에 필요한 경우).

스케줄링 역할 분담(단일 진실 공급원):

* **`focus-career` 스킬** = 중요 항목만, 시간에 민감한 노출(일반적으로 사용자가 세션을 열 때, 원하면 `/schedule`로 짧은 주기로도 실행).
* **`daily-schedule` 스킬** = 일상 운영 브리프 — Claude Cowork **`/schedule`**로 **매일 실행하도록 설계**됨(사용자가 시간/주기를 구성).

플러그인은 스킬 안에 **권장 주기**를 문서화하며, **실행**은 Cowork의 스케줄러가 담당합니다.

## **12.1 권장 주기 (Cowork `/schedule`)**

| 이름 | 권장 주기 | 실행 방법 |
| --- | --- | --- |
| **일일 운영 브리프** | 매일 (사용자가 시간 선택) | 페이로드가 `daily-schedule` 스킬을 호출하는 작업을 예약합니다(예: `/careerloop:daily-schedule` 또는 그에 상응하는 자연어). |
| **커리어 궤적 갱신 점검** | 일일 실행 안에서 월 단위 체크포인트 | `daily-schedule`이 `career-trajectory-data.json`의 최신성(staleness)을 점검하고(대체: `career-trajectory.md` 제목), 갱신 시점이 되면 `/careerloop:career-plan`을 권유합니다. |
| **후속 조치 / 파이프라인 정리** | 매일 (보통 위와 같은 작업) | `daily-schedule`과 필요 시 대화형 `follow-up`이 처리합니다. |
| **시장 인텔리전스** | 매주 | `/careerloop:market-brief`를 예약합니다(또는 `market-brief` 스킬 호출). |
| **결과 패턴 갱신** | 매주 또는 주요 결과가 나온 뒤 | 사용자가 `/careerloop:pattern-analysis`를 실행하거나 주요 트래커 갱신 후 실행하도록 예약합니다. |
| **LinkedIn 게시물 분석 스냅샷** | 매주 또는 격주 | 사용자가 호스트 브라우저 자동화를 승인하고 해당 브라우저에서 LinkedIn에 로그인한 상태일 때 **에만** **`linkedin-post-analytics`** 스킬(또는 `/careerloop:linkedin-post-analytics`)을 호출하는 작업을 예약합니다. |

## **12.2 시간 민감 항목과 일상 항목의 노출 방식**

| 상황 | 위치 |
| --- | --- |
| 임박한 마감, 당일 후속 조치, 면접 당일 긴급 조치 | `focus-career` 스킬(중요 항목만). |
| 파이프라인 요약, 아티팩트 수, 주간형 프롬프트 | `daily-schedule` 스킬(예약 실행). |
| 저장 후 인벤토리 불일치(디스크의 PDF/DOCX 대 인덱스) | `artifact-saved` 스킬(파일이 있을 때 `daily-schedule`에서, 또는 저장 후). |

향후 단계에서 더 풍부한 "이벤트 레이더"와 오퍼/면접 프롬프트가 추가될 수 있으며, 호스트가 나중에 일급 훅을 제공하지 않는 한 이들은 사용자가 Cowork에서 예약하거나 호출하는 **스킬 페이로드**로 남습니다.

# **13. 면접 캡처 (Phase 2B)**

*구현:* Phase **2B** — `agents/interview-coach/AGENT.md`가 존재합니다(`prep-interview`, `mock-interview`, `daily-schedule`의 면접 전 하위 절). **`interview-capture`**는 **`skills/interview-capture/SKILL.md`**로 구현되어 있습니다(에이전트 아님). 구조화된 면접 후 캡처를 위한 **`interview-debrief`**는 출시 예정으로 남아 있습니다.

면접 캡처는 사용자 본인 면접의 **녹음 오디오 파일**을 전사해(**`mcp-transcribe`** 또는 호환 STT 경유) 면접 내용을 기록하는 선택 가입형 기능입니다. 면접 준비와 캡처 경험이 하나의 통합 계층으로 개발·테스트되도록, Phase 2B에서 전체 면접 준비 시스템과 함께 묶어 출시합니다. 면접 후 Q&A 디브리프(`interview-debrief`)는 오디오 캡처를 쓰지 않는 사용자를 위한 기본 디브리프 경로로 계획돼 있으나 아직 스킬이 없습니다(보류). 그동안은 붙여넣은 메모와 전사본을 `/careerloop:interview-capture`로 기록합니다.

## **13.1 MVP 오디오 범위**

Phase 2B MVP는 **사용자 오디오만** 녹음합니다. 다른 참여자의 오디오는 캡처하지 않으며, 시스템은 상대방 내용에 대해 사용자의 면접 메모(붙여넣은 메모와 전사본을 `/careerloop:interview-capture`로 기록)에 의존합니다. 이 범위 설정은 MVP 릴리스에서 대부분의 관할권에서 요구하는 다자간 동의 요건을 피해 갑니다.

**고용주 정책 경고:** 사용자의 첫 녹음 세션에서 한 번만 표시하며, 일부 고용주는 면접 녹음을 일체 금지한다는 점을 알립니다. 이후 세션에서는 경고를 반복하지 않습니다.

**데이터 보관:** `profile.md`의 사용자 `location` 필드를 사용해 적용되는 현지 보관 정책(예: EU 사용자는 GDPR, 캘리포니아 사용자는 CCPA)을 결정합니다. 프로필 위치로 관할권을 판단할 수 없으면 첫 녹음 세션 시작 시 사용자에게 정책을 선택하도록 안내합니다. 모든 오디오 및 전사 데이터는 요청 시 언제든 사용자가 삭제할 수 있습니다.

**완전한 양자 캡처**(대화 양측 녹음)는 Phase 2B MVP의 범위 밖이며, 검토하기에 앞서 완전한 다자간 동의 모델, 관할권 간 법률 검토, 스토리지 아키텍처 설계가 필요합니다.

## **13.2 대체 수단: 면접 후 Q&A 흐름**

오디오 캡처를 쓰지 않는 사용자를 위해 면접 디브리프 커맨드는 동등한 구조화 데이터를 수집하는 대화형 Q&A를 제공합니다.

* 면접은 전반적으로 어떻게 진행되었나요?
* 어떤 단계였고, 누구를 만났나요?
* 예상하지 못한 주제는 무엇이었나요?
* 위험 신호나 특히 긍정적인 신호가 있었나요?
* 후속 조치로 어떤 것을 약속했나요?
* 직무, 팀, 회사에 대해 기록해 둘 만한 정보가 있었나요?

Claude는 응답을 지원 기록에 자동으로 구조화하며, 감정(sentiment)을 추론하고 실행 항목을 추출합니다.

# **14. 정직한 어드바이저 설계 철학**

*구현:* `agents/honest-advisor/AGENT.md`, 스킬 `skills/assessment/SKILL.md`, `skills/training-roi/SKILL.md`, `skills/suggest-roles/SKILL.md` (`market-researcher`와 함께).

honest-advisor 에이전트는 장벽이나 어려움이 걸린 모든 평가에서 특정한 3단계 패턴으로 동작합니다.

* 일반 규범을 제시합니다 — 이런 상황에서 시장 전반에 걸쳐 통상 무슨 일이 일어나는가
* 예외를 조사합니다 — 규범이 무너지는 특정 지역, 기업, 산업, 맥락과 그 이유
* 실행 가능한 전략을 제공합니다 — 사용자가 규범이 아니라 예외 범주에 속하도록 자신을 포지셔닝하기 위해 취할 수 있는 구체적 단계

어드바이저는 사용자에게 무엇을 믿어야 하는지, 어떤 결정을 내려야 하는지 절대 말하지 않습니다. 세상이 어떻게 돌아가는지, 어디에서 다르게 작동하는지, 어떤 선택지가 있는지에 대한 정직한 정보를 제공합니다. 결정은 사용자가 합니다.

사용자가 바꿀 수 없는 요인(나이, 경력 공백, 비전형적 배경)에 대해서는 편견의 현실을 정직하게 인정하면서도, 그런 요인이 덜 중요하거나 강점으로 작용하는 전략과 맥락에 에너지를 집중합니다.

어드바이저는 사용자의 면접이 임박했거나, 최근에 불합격했거나, 그 밖의 스트레스 신호가 있을 때 덜 직설적으로 조정됩니다. 정직한 전달은 정확성을 해치지 않으면서 시점에 맞게 조정됩니다.

# **15. 단계별 제공 계획**

*상세:* `references/careerloop-spec.md`(이 문서).
*테스트 / 검증 노트:* `references/phase-test-plan.md`.

## **Phase 1 — 핵심 플랫폼**

단계 상태:

* Phase 1A: 완료
* Phase 1B: 완료
* Phase 1C: 완료
* Phase 1D: 완료
* Phase 1E: 완료
* Phase 1F: 완료
* Phase 1G: 완료
* Phase 2A: 완료
* Phase 2B: 완료

Phase 1은 로컬 우선의 완전한 구직 인텔리전스 플랫폼을 구축합니다. Phase 1A의 기반은 플러그인 스캐폴드, 설정 흐름, 실시간 구직을 마련합니다. Phase 1B는 전체 스킬 계층을 구성합니다 — 대화 맥락에서 활성화되는 워크플로 스킬, 지원 결과를 이후 추천에 연결하는 폐쇄형 피드백 루프, 파이프라인 대시보드. Phase 1C는 솔직한 직무 평가와 스킬 격차 분석을 추가합니다. Phase 1D는 job-scout 에이전트를 결과 가중 점수화와 선제적 기회 발굴로 확장합니다. Phase 1E는 네트워킹 전략, 이벤트 레이더, LinkedIn 콘텐츠 자문이라는 전문가 프레즌스 도구로 플랫폼을 완성합니다. Phase 1이 끝나면 모든 핵심 구직 워크플로가 지능적이고, 로컬에서 자체 완결되며, 외부 서비스 의존성이 필요하지 않습니다.

### **Phase 1A — 핵심 플랫폼: 플러그인 스캐폴드, 설정, 세션 시작, 실시간 구직**

상태: 완료

* 플러그인 스캐폴드: 매니페스트, 디렉터리 구조
* **`launch` 스킬**과 대화형 구성 마법사 — 구직 폴더를 스캔하고, 기존 이력서를 ExperienceLibrary로 자동 가져오며, 보유한 문서로 사용자 프로필을 구축합니다. 원본 문서가 없으면 대화형 Q&A로 대체하고, 모든 데이터 스키마(ExperienceLibrary, 트래커, 아티팩트 인덱스)를 초기화하며, Indeed(및 선택적 Apify) 설정을 안내합니다. 사용자가 옵트인하면 선택적 **Gmail** / **Microsoft 365** 받은편지함 커넥터, 선택적 **Google Calendar**, 선택적 **`linkedin-post-analytics`**를 **제안**합니다. 슬래시 커맨드: **`/careerloop:launch`**.
* `search-jobs` 스킬 — Indeed 커넥터를 통한 실시간 구직, 반수동 대체 수단
* `focus-career` 스킬 — 사용자가 세션을 시작할 때(또는 Cowork `/schedule`로 사용자가 예약한 주기에) 중요 항목만 알림, 첫 실행 시 온보딩
* 로컬 파일시스템 스토리지 — 모든 데이터를 `{user_dir}`에 기록, 클라우드 의존성 없음

### **Phase 1B — 스킬 계층 및 인텔리전스: 워크플로 스킬, 지원 트래커, ATS 점수 산정, 분석가 에이전트**

상태: 완료

* **도입된 에이전트:** `resume-coach`(이력서 조립, ATS 최적화, 서사 코칭), `analyst`(결과 패턴 분석, 이전 가능한 강점 식별, AI 대체 평가), `job-scout`(결과 가중 공고 순위 전체 구현, 선제적 기회 알림, 이전 가능한 스킬 분석)
* 구축되어 자동 트리거되는 워크플로 스킬: `tailor-resume`, `cover-letter`, `track-application`, `add-source`, `resume-score`, `list-artifacts` — 대화 의도에서 활성화되며 명시적 커맨드로도 호출 가능
* 지원 트래커 — 단계 이력, 연락처, 메모, 결과 기록을 포함한 완전한 대화형 트래킹
* ATS 점수 산정 — 생성한 이력서와 기존 이력서에 대한 키워드 일치도, 서식 준수 여부, 서사 강도 점수화
* `ats-optimization`과 `salary-research` 컨텍스트 스킬
* 인사이트 엔진과 피드백 루프 — 결과 데이터가 ExperienceLibrary 성과 가중치와 job-scout 점수화에 다시 반영됨
* 직무, 레벨, 회사 규모, 지역별 산업 기준 벤치마킹
* 기업별 응답 기간 데이터를 활용한 후속 조치 타임라인 인텔리전스
* 타임라인 뷰와 벤치마크 비교를 갖춘 D3 파이프라인 대시보드 *(**예측(forecast)** + **음성 케이던스(voice cadence)** 오버레이는 §15의 **Phase 3 — 대시보드 및 시각화 개선**에 해당하며 Phase 1B 범위가 아님)*
* `/careerloop:pipeline-status`, `/careerloop:follow-up`

### **Phase 1C — 어드바이저 계층: 정직한 직무 평가, 스킬 격차 분석, 교육 ROI**

상태: 완료

* **도입된 에이전트:**

  + `honest-advisor` 솔직한 직무 경쟁력 평가, 규범/예외/전략 패턴
  + `market-researcher` 직무 수요 동향, AI/자동화 대체, 지역 신호

    `/careerloop:market-brief` 스킬을 통해 트리거
* 목표 직무 요건 대비 스킬 평가 및 격차 분석
* 비용-편익-시간 ROI 분석을 갖춘 교육 추천 엔진(자격증, 학위, 부트캠프, 독학)
  * **참고:** `training-roi` 스킬은 현재 자격증 가치와 결과 데이터를 정적 지식으로 실행합니다. 프로덕션 품질로 간주하기 전에 실시간 데이터 소스를 평가해야 하며, 먼저 CareerOneStop DOL API(§9에 이미 기재됨)와 부트캠프 결과나 노동시장 전망을 제공하는 사용 가능한 MCP부터 살펴봅니다. 실행 가능한 커넥터가 확인되면 다음 유지보수 주기에 `training-roi`와 통합합니다.
* `/careerloop:suggest-roles`, 결과 데이터 기반의 job scout 점수화 개선

  + 참고: Phase 2B 모의 면접 성과 데이터가 프로필에 반영되면 스킬 평가가 훨씬 풍부해집니다

### **Phase 1D — 선제적 발굴: 결과 가중 공고 점수화 및 시장 동향 모니터링**

상태: 완료

* 결과 이력이 쌓이면서 `job-scout`의 가중치와 순위 동작을 확장/조정
* 이전 가능한 스킬에 기반한 자명하지 않은 직무 제안
* 중대한 변화에 대한 선제적 알림을 갖춘 시장 동향 모니터링
* AI/자동화 대체 신호를 반영한 직무 수요 예측

### **Phase 1E — 전문가 프레즌스: 네트워킹 전략, 이벤트 레이더, LinkedIn 작성기**

상태: 완료

**범위(1E가 책임지는 것):** 네트워킹 전략, 네트워크 매핑(**`network_map_v1`** / 선택적 `network-map.md` 저장), 이벤트 인텔리전스와 다중 범위 **event-radar**(선택적 **`event_radar_v1`** / `event-radar.md` 포함)를 위한 대화형 **스킬 + 에이전트 + 슬래시 커맨드**, 그리고 **`writer`**를 통한 모든 **사용자 대상 문안**(아웃리치, 자기소개서, 후속 조치, 이력서 Summary 다듬기, 주제 아이디어, 게시물 초안, 리스크 평가). **`/careerloop:launch`**는 디스크의 이력서(résumé)/CV/자기소개서로 **`voice-profile.md`**를 생성하고 LinkedIn 샘플을 요청하며, **`writer`**는 샘플, 다중 컨텍스트 어조 메모, 품질 플래그를 유지합니다. 검토용 전체 **게시물 초안**은 **`{user_dir}/LinkedIn Posts/`** 아래에 **저장**되고 **`artifacts-index.json`**에 **`linkedin_post`**로 색인됩니다.

**문화적/정치적 리스크 평가:** `writer`는 게시물 리스크를 평가하기 전에 `market-researcher`를 호출해 목표 기업과 산업별 규범을 평가합니다. 리스크 출력은 사용자에게 정보를 제공할 뿐이며 콘텐츠 결정을 지시하거나 정당한 표현을 억제하지 않습니다.

**1E 산출물(목표 체크리스트):**

* **에이전트:** `networking-strategist`, `writer`(§4에서 정한 범위대로).
* **스킬:** `networking-strategy`, `network-map`, `event-intelligence`, `event-radar`, `draft-outreach`, `content-suggest`, `evaluate-post`. `cover-letter`와 `follow-up`은 **CoverLetterBrief** / **FollowUpBrief**를 통해 **`writer`**를 오케스트레이션합니다.
* 적절한 경우(사용 가능한 도구 범위 내) **지역, 광역, 전국, 국제** 발굴을 갖춘 이벤트 레이더.
* 발표 기회 표시, **`event-intelligence`**의 CFP / 가시성 평가.
* LinkedIn 주제 추천, 디스크에 저장되는 전체 **게시물 초안**, **`evaluate-post`**(`market-researcher` + 목표 프로필을 통한 문화적/정치적/평판상 리스크).
* 어조 일치를 위한 **`voice-profile.md`** / **`voice_profile_v1`**(launch harvest + 사용자 샘플).
* 커맨드: `/careerloop:networking-strategy`, `/careerloop:network-map`, `/careerloop:event-intelligence`, `/careerloop:event-radar`, `/careerloop:draft-outreach`, `/careerloop:content-suggest`, `/careerloop:evaluate-post`. (**`/careerloop:contact-context`**는 Phase **2A**(완료)에서 제공됩니다. §3.4 참고.)

### **Phase 1F — 커리어 계획, 오퍼 평가 및 연봉 협상**

상태: 완료

Phase 1F는 `honest-advisor` + `market-researcher`를 확장해 “의사결정 수준”의 커리어 계획과 오퍼 평가 / 협상 기능을 Phase 1에 추가합니다. 현실적인 궤적 계획, 상황 인지형 오퍼 평가, 협상 인계를 위한 스킬과 슬래시 커맨드를 도입하며, `job-scout` / `daily-schedule`이 새 아티팩트를 월 단위로 사용하도록 연결합니다.

**제공된 핵심 메커니즘:**

- **`career-plan`**은 후속 재사용을 위해 궤적 리포트를 `career-trajectory.md`에, `career_trajectory_v1`을 `career-trajectory-data.json`에 씁니다.
- **`evaluate-offer`**는 이후 워크플로가 반복적인 데이터 수집을 건너뛸 수 있도록 `offer-context-{application_id}.json`을 씁니다.
- **`compare-offers`**는 기존 오퍼 컨텍스트를 사용하며, 컨텍스트가 없을 때만 인라인 평가를 실행합니다.
- **`negotiate-offer`**는 `writer`가 최종적으로 바로 보낼 수 있는 협상 문안을 작성하도록 소비하는 `NegotiationHandoffBrief`를 생성합니다.
- **통합된 넛지:** `daily-schedule`이 월 단위 궤적 갱신 점검을 수행하고, 오퍼 단계 정리 과정에서 오퍼 컨텍스트가 없으면 평가를 권유합니다.



### **Phase 1G — 마켓플레이스 배포**

상태: 완료

**산출물: Claude 플러그인 마켓플레이스 배포**

오스틴에서 해고된 기술직 종사자가 플러그인 마켓플레이스에서 CareerLoop를 찾아 10분 만에 설치하고, MCP, 로컬 도구 구성, 에이전트 런타임이 어떻게 동작하는지 이해할 필요 없이 그날이 가기 전에 동작하는 구직 에이전트를 돌리게 됩니다.

**효과:** CareerLoop를 개인 도구에서 실제 사용자 검증(다운로드와 활성화가 수요의 측정 가능한 증거가 됨)을 갖춘 공개 제품으로 전환합니다.

## **Phase 2 — 연동**

Phase 2는 CareerLoop를 완전한 구직 경험을 완성하는 외부 서비스에 연결합니다: 받은편지함 + 캘린더 맥락, 면접 캡처, 이식 가능한 스토리지, 이벤트 인텔리전스, 면접 스토리 인텔리전스. 각 하위 단계는 독립적으로 배포할 수 있습니다.

### **Phase 2A — 이메일 및 캘린더 연동**

상태: 완료

**산출물: 받은편지함 + 캘린더 컨텍스트**

*채용 담당자에게 연락하려는데, 이미 대화한 적이 있는지, 지난 통화에서 무엇을 약속했는지 기억나지 않습니다. CareerLoop는 (명시적 허락을 받아) 관련 이메일 스레드와 최근 미팅 맥락을 가져와 찾아낸 내용만 요약하고, 그 맥락을 아웃리치와 후속 조치에 반영하므로 같은 말을 실수로 반복하거나 이전 약속을 놓치는 일이 없습니다.*

**효과:** “웜 아웃리치”를 추측에서 실제 이력에 근거한 증거 기반 커뮤니케이션으로 바꿉니다.

**포함 범위:**

* Gmail 및 Outlook OAuth 커넥터(읽기 전용 범위)
* Google Calendar 및 Outlook Calendar 읽기 전용 접근
* 네트워킹 맥락을 위한 연락처 서신 이력 검색
* 연락처 컨텍스트 스킬: 아웃리치 초안 작성 전에 이전 이메일/미팅 이력을 제시
* 이전 커뮤니케이션 이력으로 보강한 아웃리치 초안 작성
* 웜 네트워킹 식별을 위한 미팅 이력 인지 — 연락처와의 **과거** 및 **예정된(upcoming)** 캘린더 이벤트. **`contact-context`**가 **`upcoming_meetings`**와 **`warm_networking`**을 내보내므로, 이미 캘린더에 미팅이 잡혀 있을 때는 아웃리치가 차갑게(cold) 시작하지 않습니다
* **`linkedin-post-analytics`** 스킬과 **`/careerloop:linkedin-post-analytics`** 커맨드: 사용자 **본인**의 LinkedIn 게시물 분석을 **읽기 전용**으로 스냅샷해 **`networking.json`**의 `networking[]`에 저장합니다(§10.4, §12.1 참고). **호스트 브라우저 자동화**(**Claude in Chrome**, **computer / browser use** 또는 동등 기능)와 **사용자의 명시적 승인**에 의존하며, **`networking-strategist`**가 가시성 중심 사용자를 위한 주기를 권장합니다. **`/careerloop:launch`**는 사용자가 첫 실행을 원하면 Indeed/Apify 이후 선택 단계로 이를 **제안**합니다.

### **Phase 2B — 면접 인텔리전스**

상태: 완료

**산출물: 전체 면접 루프(준비 → 연습 → 캡처 → 디브리프)**

*내일 채용 담당 매니저 면접이 있습니다. CareerLoop는 모닝 브리프(기업 뉴스, 면접관 맥락, 말하기 요점)를 생성하고, 단계와 분위기(vibe)에 맞춘 적응형 모의 면접을 진행하며, 면접 후에는 일어난 일을 캡처합니다(옵트인했다면 오디오 캡처, 아니면 구조화된 Q&A 디브리프). 트래커가 자동으로 갱신되므로 후속 조치와 다음 라운드 준비는 일주일 뒤 어렴풋이 기억나는 내용이 아니라 실제로 일어난 일을 기반으로 합니다.*

**효과:** 면접을 “일회성 이벤트”에서 라운드를 거칠수록 개선되는 반복 가능하고 측정 가능한 루프로 끌어올립니다.

**포함 범위:**

* **도입된 에이전트:** `interview-coach`(모든 단계와 분위기에 걸친 모의 면접, 적응형 난이도, 시사 이슈 통합)
* **도입/확장된 스킬:** `interview-capture`(에이전트가 아닌 **스킬** — **`mcp-transcribe`** 또는 호환 STT를 통한 녹음 오디오 파일 전사, 구조화된 트래커 채우기 — 옵트인 전용, MVP 범위: 사용자 본인의 녹음만)
* 모의 면접 시스템: guided, random, adaptive 모드
* 모든 단계: 리크루터 스크린, 채용 담당 매니저, 기술, 패널, 임원, 최종
* 전체 분위기 스펙트럼: supportive, neutral, challenging, antagonistic, bored(보정됨 — 사기를 꺾지 않도록 조정, antagonistic 모드의 정확한 보정은 출시 전 사용자 테스트로 확정)
* 모의 면접 질문에 녹여 낸 시사 이슈 통합
* 기업 뉴스, 면접관 리서치, 말하기 요점을 담은 모닝 브리프
* 면접 후 Q&A 디브리프 흐름(`interview-debrief`, 보류 — 아직 스킬 없음) — 구조화된 대화형 캡처이며, 오디오 캡처를 쓰지 않는 사용자의 기본 디브리프 경로
* `/careerloop:prep-interview`, `/careerloop:mock-interview`* 모의 면접 성과가 Phase 1C 스킬 프로필에 다시 반영됨
* **오디오 캡처 — MVP 범위:** 사용자 오디오만, 고용주 정책 경고는 첫 세션에서만, 프로필 `location`에서 도출한 관할권 기반 보관 정책, 관할권을 알 수 없으면 사용자에게 선택 요청. 완전한 양자 캡처는 다자간 동의 모델과 법률 검토가 끝날 때까지 보류.
* 프라이버시에 민감한 사용자를 위한 로컬 Whisper 처리 옵션
* 사용자가 보관과 삭제를 제어하는 오디오 및 전사 저장
* 면접 전사로부터 트래커 자동 채우기

### **Phase 2C — 확장 연동**

상태: 완료

**산출물: 이식성 + 고용주 시스템 인지**

*노트북을 바꾸거나 구직 데이터를 단일 폴더 밖에 백업하고 싶습니다. CareerLoop는 아티팩트를 클라우드 드라이브 커넥터에 저장하고, 주요 ATS 플랫폼에서 읽기 전용 상태 업데이트를 가져오며, 추가 구인 사이트 소스를 통합할 수 있어, 공고와 고용주 시스템이 제각각이어도 워크플로가 일관되게 유지됩니다.*

**효과:** 시스템이 기기 간에 지속되게 하고, 지원이 제3자 시스템에 존재한다는 현실에 더 잘 맞춥니다.

**포함 범위:**

* Drive 앱 동기화 또는 수동 백업/복원을 통한 Google Drive, OneDrive 또는 Dropbox 이식성(구직 파일에 권장)
* IllinoisJobLink 구인 사이트 커넥터
* Greenhouse, Workday, Lever용 ATS 읽기 전용 커넥터

### **Phase 2D — 이벤트 인텔리전스 및 면접 스토리 인텔리전스**

상태: 완료

**산출물: 이벤트 인텔리전스 + 스토리 근거 루프**

*네트워킹에 시간을 어디에 투자할지 고르고, 약한 스토리가 강한 이력서를 무너뜨릴 수 있는 면접을 준비하고 있습니다. Phase 2D는 더 나은 기회 선택을 위한 커넥터 기반 이벤트 피드를 추가하고, 일지, 노트, PKM 아티팩트를 발굴해 고품질 스토리를 식별, 다듬기, 리허설하는 면접 스토리 인텔리전스를 도입합니다.*

**효과:** 근거 기반 준비를 통해 상단 깔때기(top-of-funnel) 네트워킹 결정과 후반 단계 면접 성과를 모두 개선합니다.

**포함 범위:**

* `event-radar` / `event-intelligence`용 **이벤트 인텔리전스 소스**: 사용자 세션에 있는 경우 선택적이며 제공되지 않는 MCP 서버를 통한 Luma, Meetup/Eventbrite는 선택적 **Claude in Chrome**, **computer use**, 또는 **수동 복사/붙여넣기** 대체 경로로 처리.
* **이벤트 발굴 설계 세부 사항:** 벤더 순서, OAuth 대 API 키, 호스트 패키징, MCP 도구 이름, 사용자가 편집한 `{user_dir}/CareerLoop/event-radar.md`에 대한 중복 제거 동작.
* **면접 스토리 인텔리전스 목표:** 사용자가 소유한 일지, 노트, PKM 소스(예: 주간 로그, 디브리프 노트, 지식 베이스 항목)를 발굴해 강한 면접 스토리를 식별·준비한 뒤, 스토리를 직무 역량과 흔한 면접 질문에 매핑합니다.
* **PKM 커넥터 경로:** 공식 **Notion** 커넥터와, 세션에서 사용 가능한 경우 선택적 **Capacities** MCP 연동. 파일 내보내기 대체 수단도 계속 일급으로 유지됩니다.
* **면접 스토리 아키텍처:** 3계층 파이프라인 — **`mine-stories`**를 통한 추출, 영속 **`StoryCorpus.json`**, **`story-retrieval`**을 통한 질의 시점 역량 매핑으로 간결한 준비 입력을 생성.
* **면접 스토리 준비 산출물:** 재사용 가능한 스토리 뱅크, 품질 점검(명료성, 결과, 주도성, 신뢰성), STAR 준비 플래그, 예정된 면접에 연결된 맞춤 리허설 프롬프트.

## **Phase 3 — 상시 가동 커리어 에이전트**

상태: 진행 중

Phase 3은 CareerLoop를 “함께 앉아 쓰는 강력한 어시스턴트”에서, 일정한 주기로 실행되고 이미 쓰고 있는 채널에서 사용자를 만나는, 맥락을 유지하는 상시 가동 커리어 운영 계층으로 발전시킵니다.

이 단계는 **OpenClaw**가 촉발한 업계 트렌드 — 지속되는 스레드, 비동기 작업 오케스트레이션(“dispatch”), 이벤트 기반 채널 — 와 AI 제품 전반의 더 넓은 “clawification” 경쟁에 의해 명시적으로 형성되었습니다. 현재 제품은 Claude Cowork용 플러그인으로 패키징되어 있지만, Phase 3의 의도는 **호스트에 구애받지 않는 것**입니다: 예약 실행, 커넥터 접근, 모바일/원격 상호작용을 지원할 수 있는 모든 런타임을 염두에 두고 설계합니다.

**산출물: 모닝 다이제스트**

*아침에 일어나 휴대폰을 보니 Stripe의 리크루터가 밤사이 지원서에 회신했습니다. 다이제스트는 이미 그 이메일을 요약했고, Salesforce 후속 조치가 응답 없이 6일째 지연되고 있음을 알렸으며, Anthropic이 프로필에 맞는 새 직무를 올렸다는 점도 보여 줍니다. 노트북을 열기도 전에 오늘 무엇을 해야 할지 정확히 알고 하루를 시작합니다.*

**효과:** 이메일, 구인 사이트, 트래커를 매일 수작업으로 확인하는 일을 없앱니다.

**산출물: 고급 분석 내보내기**

*파워 유저와 코치는 채팅 화면 밖에서의 분석이 필요합니다. Phase 3은 외부 BI 및 시각화 도구로의 내보내기 경로를 추가해, 사용자가 맞춤 리포팅 뷰를 만들면서도 CareerLoop를 운영상의 기준 시스템(system of record)으로 유지할 수 있게 합니다.*

**효과:** 제품 내 핵심 워크플로를 바꾸지 않고도 외부 대시보드와 더 깊은 장기 분석이 가능해집니다.

**포함 범위:**

* Power BI 스트리밍 데이터셋 커넥터
* Qlik Engine API 커넥터
* 맞춤 시각화를 위한 D3 데이터 내보내기 커넥터

**대시보드 및 시각화 개선** *(Phase 1E에서 이월됨, 1E 산출물의 안정적인 상호 교환에 의존):*

* **파이프라인 타임라인 — 예측(forecast) 오버레이:** **`/careerloop:pipeline-status`**(D3)을 확장해 **타임라인**에 **`networking-strategist`** 출력 — 계획되었거나 권장되는 관계 활동, ROI가 높은 이벤트, 가시성 마일스톤 — 에서 도출한 미래 지향적 **예측**을 **과거** 지원 단계와 함께 표시합니다. `networking-strategy`, `event-radar`, **`network_map_v1`**, **`event_radar_v1`** 및 관련 아티팩트에서 구조화된 데이터를 영속화하거나 도출해야 하며, 새로 고침 주기와 스키마는 미정입니다.
* **파이프라인 타임라인 — 음성 케이던스(voice cadence):** **`voice_profile_v1`** / **`voice-profile.md`** 메타데이터(예: 마지막 수집(harvest), 샘플 날짜, 어조 요약)를 타임라인 위나 옆에 표시해, **대외 노출 케이던스**가 지원 및 네트워킹과 어떻게 맞물리는지 사용자가 볼 수 있게 합니다.
* **네트워크 맵 그래프 UI:** 영속화된 **`network_map_v1`**을 소비하는 인터랙티브 그래프(또는 내보내기 경로) — 채팅 / `network-map.md`의 서술 + JSON을 넘어서는 기능입니다.

**산출물: 주간 시장 브리프**

*매주 월요일 아침, 시카고의 "Head of AI Product" 공고가 이번 주 23% 늘었고, 목표 기업 두 곳이 채용 동결을 발표했으며, 2주 뒤 연사를 모집하는 관련 콘퍼런스가 있다는 리포트가 도착합니다. 낡은 가정으로 움직이는 대신 그에 맞춰 아웃리치 우선순위를 조정합니다.*

**효과:** 즉흥적인 조사를 목표 목록과 직접 연결된 일관된 인텔리전스 주기로 대체합니다.

**산출물: 후속 조치 알림**

*한 회사의 최종 면접 후 6일이 지났지만 연락이 없습니다. 시스템이 이를 감지해 표준 응답 벤치마크 대비 지연으로 표시하고, 미리 작성한 후속 메시지를 휴대폰으로 전달합니다 — 검토 후 바로 보낼 수 있는 상태입니다. 한 군데만 고쳐서 기차 안에서 보냅니다.*

**효과:** 놓치는 일이 없습니다. 파이프라인의 시계는 시스템이 관리하므로 직접 챙길 필요가 없습니다.

**산출물: 주간 인사이트 리포트**

*매주 금요일 오후, 시스템이 한 주를 쉬운 말로 정리해 전달합니다: 지원 4건, 응답 2건, 면접 1건 확정. 이번 달 긍정적인 응답은 모두 AI 연구 경험을 앞세운 직무에서 나왔고, "data science leadership"으로 프레이밍한 직무는 무응답이라는 점을 짚습니다. 그리고 다음 주를 위한 구체적인 포지셔닝 조정 한 가지를 권장합니다.*

**효과:** 구직을 감정에 기대는 경험에서 데이터에 기반한 경험으로 바꿉니다.

**산출물: Dispatch 모바일 계층**

*점심 중에 내일 Anthropic 면접이 떠오릅니다. 휴대폰으로 "Prep me for my Anthropic interview tomorrow."라고 메시지를 보냅니다. 책상으로 돌아올 즈음에는 기업 뉴스, 예상 질문, 말하기 요점, 지난주 채용 담당 매니저가 LinkedIn에 올린 글에 대한 메모까지 담긴 전체 브리프가 기다리고 있습니다.*

**효과:** 데스크톱 에이전트의 모든 기능을 컴퓨터를 열지 않고 어디서든 사용할 수 있습니다.

**산출물: 채널 (Telegram, Slack)**

*어려운 면접을 마치고 곧바로 Telegram 봇에 메시지를 보냅니다. "Just wrapped my Google interview, it went pretty well but they asked about distributed systems and I fumbled." 시스템이 구조화된 디브리프를 안내하고, 세부 내용을 캡처하고, 트래커를 갱신하며, 다음 라운드 전에 보완해야 할 준비 격차를 표시합니다 — 면접의 기억이 생생한 동안, 모두 휴대폰에서 이루어집니다.*

**효과:** 결코 지켜지지 않는 "나중에 기록해야지"라는 약속을, 사용자가 있는 곳으로 찾아오는 상시 캡처 흐름으로 대체합니다.

**산출물: Computer Use (범용 커넥터 대체 수단)**

*LinkedIn 프로필 업데이트, 리크루터에게 메시지 보내기, 공고 저장, 독자 포털에서 지원 상태 확인처럼, 안정적인 API/커넥터가 없는 도구에서 레버리지가 큰 작업을 하고 싶습니다. 전용 MCP를 기다리며 막히는 대신, 시스템이 (명시적 허락을 받아) “computer use”로 실제 UI를 조작할 수 있습니다: 브라우저를 열고, 이동하고, 관련 페이지 상태를 추출하고, 메시지 초안을 작성하고, 사용자가 검토할 수 있도록 동작을 준비 상태로 둡니다. 생태계가 커넥터 수준의 접근을 제공하지 않아도 커넥터 수준의 결과를 얻습니다.*

**효과:** “커넥터 없음”이라는 하드 제약을 없애 승인과 가드레일을 명시적으로 유지하면서 엔드투엔드 워크플로(특히 네트워킹 및 LinkedIn 인접 작업)를 가능하게 합니다.

**산출물: Projects (아티팩트 및 워크스페이스 정리)**

*수십 개의 직무가 진행 중이고 맞춤 이력서, 자기소개서, 후속 메시지, 면접 브리프, 대시보드, 시장 리포트 등 수백 개의 생성 자산이 있습니다. Projects는 사람이 만든 아티팩트와 기계가 생성한 아티팩트를 기업/직무별로 묶고(트래커 단계와 다시 연결) 정리하는 계층이 되어, 폴더나 채팅 기록을 뒤지지 않고도 “이 직무의 최신 이력서는 무엇인가?” 또는 “지난번에 무엇을 보냈지?”에 즉시 답할 수 있습니다.*

**효과:** 아티팩트 난립을 줄이고 멀티 에이전트 작업을 읽기 쉽게 만듭니다 — 사용자는 출처가 분명한 상태로 세션 간 산출물을 검토, 승인, 재사용할 수 있습니다.

## **Phase 4 — 엔터프라이즈 및 생태계**

**산출물: 커리어 코치용 화이트 라벨**

*월 $500로 일대일 구직 지원을 제공하는 커리어 코치가 자신의 브랜드로 CareerLoop를 라이선스해, 8명 대신 40명의 고객을 동시에 응대합니다. 고객은 일일 브리핑, 파이프라인 트래킹, 시장 인텔리전스를 받습니다. 코치는 사람의 판단이 필요한 밀도 높은 대화에 시간을 집중합니다.*

**효과:** 코치의 처리 역량을 5배로 늘리면서 모든 고객이 받는 서비스의 기본 품질을 높입니다.

**산출물: 익명화된 벤치마크 데이터**

*수천 명의 사용자가 CareerLoop로 검색한 뒤, 시스템은 시카고의 AI 연구 직무가 전화 스크린 단계에서 평균 11일의 응답 기간을 보이고, 화요일부터 목요일 사이에 제출한 지원이 월요일과 금요일 제출보다 통계적으로 유의미하게 더 나은 성과를 낸다는 것을 알게 됩니다. 시스템이 일반적인 조언이 아니라 실제 집계 결과를 기준으로 보정되기 때문에 모든 사용자의 후속 조치 타이밍과 전략이 개선됩니다.*

**효과:** 규모가 커질수록 조언이 더 똑똑해집니다 — 개별 사용자는 혼자서는 결코 볼 수 없는 패턴의 혜택을 누립니다.

**산출물: 정부 / American Job Center 연동**

*시카고 AJC의 인력 개발 상담사가 CareerLoop로 실직 근로자 60명을 동시에 지원합니다. 각 고객은 개인화된 일일 브리프와 자동 후속 조치 리마인더를 받습니다. 상담사는 모든 고객의 모든 지원을 수작업으로 추적하는 대신, 사람의 개입이 필요한 예외 사례를 검토합니다.*

**효과:** 현재 획일적이고 자원이 부족한 지원을 받는 인구 집단에까지 고품질 구직 지원을 확대합니다.

**산출물: 군 전역자 및 장애인 경로 모듈**

*12년간 복무하고 전역하는 군인은 뛰어난 경력이 있지만 민간 직함 어휘가 없습니다. CareerLoop의 군 전역자 모듈은 복무 직무를 민간 직무로 번역하고, 보안 인가(clearance)를 지원 가능한 직무에 매핑하며, 채용 담당자가 알아보는 이력서 문구를 생성합니다 — 본인이 직접 번역할 방법을 알아낼 필요가 없습니다.*

**효과:** 충분히 예방할 수 있는 이유로 자격을 갖춘 지원자가 간과되게 만드는 구조적 불이익을 없앱니다.

**산출물: 사회초년생 / 대학생 경로**

*대학 3학년생이 인턴십 채용을 시작하지만 제대로 된 체계가 없습니다: 반쯤 쓴 이력서, 흩어진 공고 링크, 놓친 마감. CareerLoop는 학기를 하나의 운영 주기로 바꿉니다 — 수업, 프로젝트, 아르바이트 경험으로 깔끔한 기본 이력서를 만들고, 인턴십용 직무별 변형본을 생성하며, 지원과 채용 단계를 추적하고, 취업박람회와 캠퍼스 리크루팅 일정을 알려 주고, 동문과 리크루터에게 보낼 아웃리치 초안을 작성하며, 후속 조치가 지연되면 표시합니다. 기말고사 주간이 되면 학생은 추측하지 않고도 다음에 무엇을 해야 하는지 정확히 압니다.*

**효과:** 사회초년생 채용의 학습 곡선을 반복 가능한 워크플로로 압축해, 학생이 마감을 놓치거나, 적합도 낮은 지원에 시간을 낭비하거나, 일관성 없는 후속 조치로 기회를 잃지 않게 합니다.

# **16. 미해결 질문 및 보류된 결정**

*작업 노트:* `references/phase-test-plan.md` (점검 항목과 미해결 항목이 이 표와 겹칠 수 있음).

| 이름 | 유형 | 설명 |
| --- | --- | --- |

# **부록: 커맨드 빠른 참조**

*전체 표는 §3과 §5에 있습니다.

| 커맨드 | 용도 |
| --- | --- |
| **/careerloop:launch** | 구직 워크스페이스 시작: 폴더 구성, ExperienceLibrary와 프로필 구축, 커넥터 설정. 선택적 **`linkedin-post-analytics`** 제안 |
| **/careerloop:tailor-resume** | **`resume-coach`**로 이력서 조립, 선택적 **`writer`** Summary 다듬기 |
| **/careerloop:cover-letter** | **CoverLetterBrief** + **`writer`**의 최종 문장 작성 |
| **/careerloop:resume-score** | 이력서를 채용 공고 기준으로 점수화 |
| **/careerloop:add-source** | ExperienceLibrary에 원본 문서 추가 |
| **/careerloop:list-artifacts** | 생성된 모든 아티팩트 나열 |
| **/careerloop:search-jobs** | 채용 기회 검색 및 순위 산정 |
| **/careerloop:track-application** | 지원(건) 기록 또는 갱신 |
| **/careerloop:pipeline-status** | 전체 지원 대시보드 보기 (타임라인, **Phase 3:** 예측 + 음성 케이던스 오버레이) |
| **/careerloop:follow-up** | **FollowUpBrief** + **`writer`** 메시지 |
| **/careerloop:market-brief** | 최신 시장 인텔리전스 리포트 |
| **/careerloop:suggest-roles** | 자명하지 않은 직무 기회 발굴 |
| **/careerloop:career-plan** | 궤적 분석 + ROI 순 격차 계획 (`career-trajectory.md` + `career-trajectory-data.json`) |
| **/careerloop:evaluate-offer** | 상황 인지형 오퍼 평가 + 저장된 오퍼 컨텍스트 |
| **/careerloop:compare-offers** | 여러 오퍼의 나란히 비교 및 추천 |
| **/careerloop:negotiate-offer** | 협상 전략 + 바로 보낼 수 있는 초안을 위한 `writer` 인계 |
| **/careerloop:networking-strategy** | 네트워킹 계획 (전략, 아웃리치는 **content-advisor** 경유) |
| **/careerloop:network-map** | 네트워크 경로/격차 + **`network_map_v1`** (Phase 3: 그래프 UI) |
| **/careerloop:event-intelligence** | 이벤트 ROI 및 발표 기회 평가 |
| **/careerloop:event-radar** | 다중 범위 이벤트 발굴 |
| **/careerloop:prep-interview** | 전체 면접 준비 세션 |
| **/careerloop:mock-interview** | 모의 면접 (guided/random/adaptive), mode/vibe 생략 시 기본값 사용 |
| **/careerloop:interview-capture** | 선택 가입형 사용자 오디오 캡처 → 전사 → 트래커 (**스킬**) |
| **/careerloop:draft-outreach** | 아웃리치 초안 작성 (**`writer`**) |
| **/careerloop:contact-context** | 이전 이메일/캘린더 스레드 요약 (**과거** + **예정된** 미팅, **warm_networking**) → **ContactContextBrief** (읽기 전용, 사용자 승인) |
| **/careerloop:content-suggest** | LinkedIn 주제 아이디어 (**`writer`**) |
| **/careerloop:evaluate-post** | 게시물 리스크 검토 — 청중 + 문화적/정치적 리스크를 **`market-researcher`** + **`writer`**로 평가 |
| **/careerloop:linkedin-post-analytics** | 본인 LinkedIn 게시물 지표를 읽기 전용으로 **`networking.json`**의 `networking[]`에 기록 (브라우저 자동화 + 사용자 동의) |
