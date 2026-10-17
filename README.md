# CareerLoop

[![License](https://img.shields.io/github/license/seonwooj0810/careerloop)](LICENSE) [![Release](https://img.shields.io/github/v/release/seonwooj0810/careerloop)](https://github.com/seonwooj0810/careerloop/releases) ![Claude Code plugin](https://img.shields.io/badge/Claude%20Code-plugin-D97757)

Claude Cowork 플러그인으로 만든 AI 기반 end-to-end 구직 동반자입니다. 리크루터, 커리어 코치, 리버스 리크루터, 시장 분석가의 기능을 하나의 지능형 플랫폼에 담았고, 시간이 지날수록 무엇이 나에게 효과가 있는지 학습합니다.

> **English:** CareerLoop is an AI job-search companion for Claude Code and Cowork. It tracks applications, tailors résumés and cover letters from your own verified experience, prepares interviews, evaluates and negotiates offers, and learns what works for you. 46 skills and 8 agents. Data stays in a folder you choose; the plugin bundles no servers, hooks or telemetry. It never invents experience: gaps are reported, not filled. Output language is Korean.
>
> `claude plugin marketplace add seonwooj0810/careerloop` → `claude plugin install careerloop@careerloop-github`

## 하는 일

CareerLoop는 구직 활동 전체를 한곳에서 관리합니다.
- 구조화된 경험 라이브러리(Library of Experiences)로 목표에 맞춘 이력서를 만듭니다
- 모든 이력서를 ATS 시스템에 맞게 점수화하고 최적화합니다
- 모든 지원 건을 전체 단계 이력과 함께 추적합니다
- 내 역량과 결과 이력을 기준으로 채용 기회의 순위를 매깁니다
- 헛된 격려가 아니라 솔직하고 정직한 평가를 제공합니다

핵심 차별점은 모든 지원 결과가 시스템에 되먹임된다는 점입니다. 시간이 지나면 어떤 경험 단위, 이력서 변형, 소통 스타일이 나에게 실제로 효과가 있는지 학습합니다.

---

## 예시 출력

가상 인물(김테스트)로 실행한 `/careerloop:daily-schedule` 결과의 일부입니다.

```
CareerLoop — Daily Brief [2026-10-17]

파이프라인
  지원 완료        1
  전화 스크리닝    0
  면접             0
  오퍼             0

후속 조치 기한     0건 기한 초과 (바나나페이먼츠 후속 확인 예정일: 10/20)
오늘의 미팅        예정 없음
```

---

## 설치

### Claude Code로 설치

```
/plugin marketplace add seonwooj0810/careerloop
/plugin install careerloop --marketplace seonwooj0810/careerloop
```

### Claude Desktop으로 설치

1. zip 다운로드: [직접 링크](https://github.com/seonwooj0810/careerloop/archive/refs/heads/main.zip)
2. Claude Desktop에서 **Browse plugins → Personal → Upload a plugin**을 선택하고 ZIP 파일을 지정합니다
3. 이력서, 자기소개서, 지원 서류 등을 보관하는 디렉터리를 추가합니다
4. CareerLoop가 활성화된 새 채팅에서 **`/careerloop:launch`**를 실행해 구직 워크스페이스(설정 마법사)를 시작합니다

> **참고(Claude Code vs Desktop Cowork):** CareerLoop는 **Claude Desktop Cowork** 사용을 전제로 설계됐습니다. 마켓플레이스 설치·로드를 CLI에서도 검증할 수 있도록 **Claude Code 터미널 호환성 테스트 환경**도 함께 유지합니다. Claude Code에서 command-bridge 항목이 보이더라도 테스트용이라 정상이며, 의도한 Desktop Cowork 경험에는 영향이 없습니다.

---

## 플러그인이 실행하고 전송하는 것

- **로컬 스크립트:** `scripts/build_timeline.py`(`python3`로 지원 타임라인 `timeline.html` 생성, 네트워크 사용 없음)와 `scripts/load-context.sh`(선택 훅용, 기본으로는 등록되지 않음). 모든 데이터 파일은 내가 지정한 폴더의 `CareerLoop/`에 저장됩니다.
- **웹 조회:** 일부 스킬(`search-jobs`, `salary-research`, `market-brief`, `event-radar`, `event-intelligence` 등)은 세션에서 WebSearch/WebFetch를 허용한 경우에만 웹을 조회합니다. 이때 직무·지역·회사명 같은 검색어가 나갈 수 있고, 이력서 원문은 보내지 않습니다.
- **선택 연동:** Gmail·Calendar·Microsoft 365·Indeed·Apify·Chrome 등은 내가 Claude 앱에서 직접 연결하고 승인한 경우에만 읽기 전용으로 사용합니다. 번들된 MCP 서버나 훅은 없습니다(`.mcp.json`, `hooks/hooks.json`은 비어 있음).
- **선택 설치:** 면접 전사 기능의 설치 과정은 아래 "면접 오디오 전사"에 적었습니다.

---

## 플러그인 마켓플레이스

CareerLoop는 **Phase 1G — 마켓플레이스 공개**의 일환으로 GitHub 기반 마켓플레이스 피드를 통해 배포됩니다. 비개발자도 Claude Desktop의 **Browse plugins**에서 클릭 한 번으로 설치할 수 있습니다.

---

## 빠른 시작

### 1. 구직 폴더를 채팅에 추가

CoWork에서 **+** 버튼(또는 폴더 아이콘)을 눌러 이력서와 자기소개서가 있는 로컬 폴더를 추가합니다. 이렇게 하면 해당 세션 동안 CareerLoop가 파일에 접근할 수 있습니다.

### 2. 시작

```
/careerloop:launch
```

구직 폴더 안의 이력서, 자기소개서, 과거 지원 서류를 모두 읽어 프로필과 ExperienceLibrary를 자동으로 만듭니다. 라이브 채용 공고 검색을 위한 JobSearch 설정도 함께 진행합니다.

### 3. 폴더에 문서 넣기

CareerLoop는 구직 폴더를 자동으로 감시합니다. 이력서나 자기소개서를 추가하면 다음 시작 시점 또는 자정 동기화 때 반영되며, 별도 명령이 필요 없습니다.

### 4. 맞는 직무 검색

```
/careerloop:search-jobs
```

**Indeed** MCP 커넥터가 연결돼 있으면(아래 **채용 검색 및 저장소 설정** 참고) 라이브 검색과 순위가 매겨진 결과를 받을 수 있습니다. 연결돼 있지 않으면 `search-jobs`가 Indeed를 **Connect**하는 방법(브라우저 OAuth)을 안내하고, 커넥터를 쓸 수 있을 때까지 **보조 수동** 검색 문자열로 대체할 수 있습니다(`/careerloop:launch` 3단계).

### 5. 첫 이력서 맞춤화

```
/careerloop:tailor-resume
```

채용 공고(JD)를 붙여 넣으세요. CareerLoop가 ExperienceLibrary에서 최적의 이력서를 조립하고, ATS 호환성 점수를 매긴 뒤 아티팩트 인벤토리에 저장합니다.

---

## Phase 1 스킬

CareerLoop는 **스킬 중심**입니다. 대부분의 워크플로는 평소 대화(채용 공고 붙여넣기, 어딘가에 지원했다고 말하기, 시장 동향 묻기)에서 시작합니다. 슬래시 명령은 아래에 표시된 곳에만 있습니다.

**구성 요소가 맞물리는 방식** — 생애 주기 순서에 가까운 여섯 개 영역입니다.

```text
시작 & 리듬             →  {user_dir}을 건강하게 유지하고 시간에 민감한 항목을 계속 보이게 함
        ↓
문서 & ATS              →  원본 문서 수집, 이력서/자기소개서 맞춤화, ATS 점수화 및 수정
        ↓
탐색 & 파이프라인       →  직무 검색, 지원 기록, 결과로부터 학습
        ↓
시장 & 직무 전략        →  수요, 연봉, 인접 직무, AI 리스크, 교육 ROI
        ↓
네트워킹 & 존재감       →  계획, 경로 지도, 이벤트, 아웃리치 & LinkedIn 콘텐츠
        ↓
인사이트 & 대시보드     →  전체 분석가 보고서 + 파이프라인 시각화
```

---

### 1. 시작 & 세션 리듬

| 스킬 / 명령 | 실행 시점 | 용도 |
|-----------------|--------------|---------|
| **`/careerloop:launch`** | 한 번 실행(재설정 시 다시 실행) | `{user_dir}`, 핵심 `CareerLoop/` 파일, 커넥터 안내(Indeed, Apify, Gmail/M365/Google Calendar, LinkedIn 분석), 보이스 수집을 설정합니다. 첫 스냅샷이 필요하면 선택 스킬 **`linkedin-post-analytics`**를 **제안**합니다 |
| **`focus-career`** | 새 세션(훅) 또는 `/schedule` | 핵심만: 마감일, 당일 후속 조치, 긴급 면접 액션 |
| **`daily-schedule`** | **권장:** Cowork **`/schedule`**로 매일 | 정기 요약. PDF/DOCX 아티팩트를 맞춰야 하면 **`artifact-saved`**를 실행하고, 트래커에 **오늘** 면접/리크루터/스크리닝이 있으면 **면접 전 브리프(오늘)**를 만듭니다 |
| **`/careerloop:setup-schedule`** | 시작 후 한 번 실행 | **Phase 3:** `careerloop-daily-brief` Cowork 예약 작업을 만듭니다. 2단계 Gmail 받은편지함 스캔(7일 전체 + 30일 회사별 보충), 후속 조치 알림, 상위 신규 채용 추천이 매일 아침 `recommendations.json`에 자동으로 추가됩니다. 선택적으로 `pipeline-status.html`을 매일 밤 재생성하는 두 번째 예약 작업 `careerloop-pipeline-refresh`도 만듭니다 |
| **`/careerloop:pipeline-status`** | 언제든 실행하거나 `setup-schedule`로 매일 밤 예약 | 파이프라인 상태 페이지를 생성합니다. 지원 타임라인이 포함된 필터 가능한 표(진행 중 / 집중 / 종료 / 패스)이며, `tracker.json`, `recommendations.json`, `passed.json`을 읽어 브라우저에서 엽니다 |
| **`prep-interview`** | "~준비시켜줘", 리크루터/채용 담당자/기술 면접, `/careerloop:prep-interview` | **`interview-coach`**를 통한 전체 준비. `CareerLoop/interview-prep/*.md`를 저장하고 해당 지원 건의 **`applications/<application_id>.json`**에 **`[prep]`** 메모를 남깁니다 |
| **`mock-interview`** | "모의 면접~", `/careerloop:mock-interview` | 텍스트 전용 연습 세션: 가이드/무작위/적응형, 단계 + 분위기. **모드/분위기를 생략하면 기본값이 선택됩니다**(스킬 §2.1 참고) |
| **`interview-capture`** | 옵트인, `/careerloop:interview-capture` | **스킬**(에이전트 아님): 녹음 오디오 파일 STT → **`applications/<application_id>.json`**과 **`tracker.json`** 요약 행에 구조화된 메모. §13.1 경고 포함. **`mcp-transcribe`** 사용(`/careerloop:setup-transcribe` 참고) |
| **`mine-stories`** | 설정 시 또는 새 메모/일지가 생겼을 때 | 일지, PKM, 디브리프 및 관련 문서에서 **`StoryCorpus.json`**을 만드는 1회성/증분 추출 파이프라인 |
| **`story-retrieval`** | 준비/모의 면접 흐름 중 | 일지 전체를 불러오지 않고 STAR 매핑용으로 **`StoryCorpus.json`**에서 역량에 맞는 스토리(보통 8~12개)를 가져옵니다 |
| **`artifact-saved`** | 저장 후 또는 **`daily-schedule`**에서 | **`artifacts-index.json`**을 디스크의 파일과 동기화합니다. 분석 핸드오프 스텁 |

---

### 2. 문서, 자기소개서 & ATS

| 스킬 / 명령 | 실행 시점 | 용도 |
|-----------------|--------------|---------|
| **`add-source`** | 새 이력서/CV를 올리거나 언급했을 때 | **`ExperienceLibrary.json`**에 수집 |
| **`tailor-resume`** | JD를 붙여 넣거나 "X에 지원" 의도가 있을 때 | **`resume-coach`**로 이력서 조립. 선택적으로 **`writer`**가 요약(Summary) 문체를 다듬음 |
| **`cover-letter`** | 맞춤화 후 또는 명시적 요청 시 | **CoverLetterBrief** → **`writer`**가 최종 자기소개서 작성 |
| **`resume-score`** | 이력서 + JD를 함께 줬지만 맞춤화 요청은 없을 때 | ATS + 서사 점수 |
| **`ats-optimization`** | "ATS 고쳐줘", 서식/키워드 문제 | 우선순위가 매겨진 ATS 수정안 |
| **`/careerloop:list-artifacts`** | 명시적 호출 | 생성된 이력서, 자기소개서, LinkedIn 초안, 연결된 결과 목록 |

---

### 3. 채용 탐색, 지원 & 학습 루프

| 스킬 / 명령 | 실행 시점 | 용도 |
|-----------------|--------------|---------|
| **`search-jobs`** | "일자리 찾아줘~", `/careerloop:search-jobs` | 순위가 매겨진 검색(연결 시 Indeed MCP 사용) |
| **`track-application`** | "지원했어요~", 상태 업데이트 | 지원 기록 — **`tracker.json`** 요약 행과 **`applications/`**, **`contacts/`** 파일 |
| **`application-update`** | **`track-application`**이 기록한 직후 | job-scout 갱신 / 이정표 시점의 **pattern-analysis**를 유도 |
| **`follow-up`** | 대기열 / 기한 초과 / "무응답인가?" | 회사별 응답 기간 → **FollowUpBrief** → **`writer`**가 메시지 작성 |
| **`pattern-analysis`** | "뭐가 통하고 있어?", 결과 검토 | 내 이력을 바탕으로 ExperienceLibrary의 **performance_weights** 갱신 |

---

### 4. 시장, 직무 & "뭘 해야 하지?"

| 스킬 / 명령 | 실행 시점 | 용도 |
|-----------------|--------------|---------|
| **`market-brief`** | 수요, 트렌드, `/careerloop:market-brief` | **`market-researcher`**: 직무 수요, 대체, 지역 |
| **`suggest-roles`** | 인접/비자명한 목표 직무, `/careerloop:suggest-roles` | 직무 아이디어 + **`job-scout`**용 **`strategy_signals`** |
| **`salary-research`** | 보수 관련 질문 | Apify MCP를 통한 벤치마크(연결 시) |
| **`benchmark`** | "시장 대비", 퍼널 건강도 | 직무 / 레벨 / 회사 규모별 기준값 |
| **`ai-analysis`** | AI 대체, 미래 대비 | 작업 단위 리스크 + 차별화 요소(**`analyst`**) |
| **`skill-transfer`** | "또 뭘 할 수 있을까?" | 전이 가능한 강점 → 인접 직무/산업 |
| **`training-roi`** | 자격증, 부트캠프, 학위 | 비용-시간-편익 학습 경로 |
| **`career-plan`** | "내 경로는 어떻게 가야 할까?" | 단기/중기/장기 관점의 궤적 계획 + ROI 순위 갭 계획 |
| **`assessment`** | 특정 직무에 대한 솔직한 경쟁력 | **`honest-advisor`**의 갭 / 재포지셔닝 평가 |
| **`evaluate-offer`** | 오퍼 의사결정 지원 | 시나리오 인지형 오퍼 평가(재직 중 vs 무직 맥락) + 시장 적정성 점검 |
| **`compare-offers`** | 복수 오퍼 의사결정 | 보수, 적합성, 궤적, 리스크 전반에 걸친 오퍼 나란히 비교 |
| **`negotiate-offer`** | 보수 협상 준비 | 협상 전략 + 레버리지 목록 + 최종 메시지 초안을 위한 **`writer`** 핸드오프 브리프 |

---

### 5. 네트워킹, 이벤트 & 대외 목소리

| 스킬 / 명령 | 실행 시점 | 용도 |
|-----------------|--------------|---------|
| **`networking-strategy`** | 누구를/언제/어떻게 만날지 계획 | **`networking-strategist`**, 메시지 작성은 **`writer`**로 핸드오프 |
| **`network-map`** | 목표 고용주로 가는 경로 | 서술 + **`network_map_v1`**(그래프 UI는 Phase **3**) |
| **`event-intelligence`** | 특정 이벤트 ROI, 발표/CFP | 심층 평가 |
| **`event-radar`** | 상시 탐색 | 지역 → 해외, ROI 등급 |
| **`draft-outreach`** | DM, 이메일, InMail 초안 | **`writer`** |
| **`contact-context`** | 웜 아웃리치 전 | 읽기 전용 Gmail/M365 + 캘린더(연결 시): 과거 + **예정된** 미팅 → **`draft-outreach`** / **`writer`**를 위한 **ContactContextBrief**(**warm_networking**, **upcoming_meetings**) |
| **`content-suggest`** | 게시물 아이디어, 전체 초안 | 주제 + **`LinkedIn Posts/`** 아래에 저장된 **`linkedin_post`** 초안 |
| **`evaluate-post`** | 게시 전 | 독자층 + 문화적/정치적/평판 리스크를 **`profile.md`** 목표 대비 평가 |
| **`linkedin-post-analytics`** | 주간/격주 또는 **`/schedule`** | **내** LinkedIn 게시물 지표의 읽기 전용 스냅샷 → **`networking.json`**의 `networking[]`(**Claude in Chrome** 또는 **컴퓨터/브라우저 사용**과 명시적 승인 필요) |

---

### 6. 인사이트 & 대시보드

| 스킬 / 명령 | 실행 시점 | 용도 |
|-----------------|--------------|---------|
| **`report`** | "전체 분석", 통합 분석 | **`analyst`** + 트래커 + EL + 아티팩트 |
| **`pipeline-status`** | 대시보드 갱신, 또는 `setup-schedule`로 매일 밤 | **`pipeline-status.html`** + `pipeline-data.js` + `timeline.html` |

---

**슬래시 명령:** 일부 스킬에만 **`/careerloop:…`** 별칭이 있습니다(위에 표시됨). 나머지는 `skills/<name>/SKILL.md`에 적힌 각 스킬의 트리거에 맞는 **자연어**로 호출하거나, 채팅에서 스킬 이름을 직접 불러 호출합니다.

---

## 데이터 저장

모든 것은 하나의 폴더, 즉 내가 지정한 구직 디렉터리에 있습니다. CareerLoop는 그 폴더에서 문서를 읽고 모든 결과를 다시 그 안에 저장합니다.

```
~/Documents/Job Search/          ← 내 폴더(원하는 위치 어디든)
│
├── resume-2026.pdf              ← 내 원본 문서
├── resume-staff-eng.docx
├── cover-letter-acme.pdf
│
├── resume-acme-pm-2026-03.md    ← CareerLoop 산출물(여기에 바로 저장)
├── cover-letter-acme-pm-2026-03.md
│
├── CareerLoop/
│   ├── profile.md               — 목표, 최소 보수, 차별화 요소
│   ├── ExperienceLibrary.json   — 원본 이력서/CV에서 추출한 경험 단위
│   ├── StoryCorpus.json         — 일지/PKM/디브리프에서 추출한 면접 스토리 코퍼스
│   ├── tracker.json             — 제출한 지원 건당 요약 행 하나(메모, 단계 이력, 연락처는 인라인으로 두지 않음)
│   ├── applications/            — 지원 건당 파일 하나: 해당 지원의 stage_history[] + notes[]를 담은 <application_id>.json
│   ├── contacts/                — 회사당 파일 하나: 그 회사의 모든 연락처를 담은 <company-slug>.json, 각 연락처에 해당 지원 건이 태그됨
│   ├── recommendations.json     — 지원 전 파이프라인(검토 중인 직무)
│   ├── passed.json              — 지원 전에 명시적으로 패스/거절한 직무
│   ├── networking.json          — 리크루터 관계 + **`networking[]`**(예: **`linkedin-post-analytics`**의 **`linkedin_post`** + **`analytics_history`**)
│   ├── artifacts-index.json     — 생성된 이력서와 자기소개서의 색인
│   ├── company-windows.json     — 후속 조치 타이밍을 위한 회사별 응답 기간
│   ├── career-trajectory.md     — `career-plan`이 만든 사람이 읽는 궤적 보고서
│   ├── career-trajectory-data.json — `career-plan`이 만든 `career_trajectory_v1` 구조화 데이터
│   ├── offer-context-*.json     — 협상/비교 워크플로를 위해 저장된 오퍼 평가 맥락
│   ├── voice-profile.md         — 선택: 붙여 넣은 게시물 + **`writer`** 보이스 노트 / `voice_profile_v1`
│   ├── analyst-graph-data.json  — 대시보드 렌더링용 그래프 친화적 분석가 출력
│   ├── interview-prep/          — **`prep-interview`**가 만든 마크다운 브리프
│   ├── pipeline-status.html     — 생성된 파이프라인 상태 페이지(브라우저에서 열림)
│   ├── pipeline-data.js         — pipeline-status.html의 데이터, 실행할 때마다 재생성
│   └── timeline.html            — 생성된 지원 타임라인, pipeline-status.html에 임베드
```

**지원 데이터가 나뉘는 방식:** `tracker.json`은 파이프라인을 한눈에 보여 줍니다. 지원 건당 요약 행 하나에 회사, 직무, 상태, 날짜, 작은 카운터(`notes_count`, `stage_count`, `contact_count`, `latest_stage`, `latest_stage_date`)가 들어 있습니다. 덩치가 큰 부분은 옆에 따로 있습니다. 각 지원 건의 단계 이력과 메모는 `applications/<application_id>.json`에, 회사별 모든 연락처는 `contacts/<company-slug>.json`에 있으며, 각 연락처에는 소속 지원 건의 `"<company> — <role>"` 레이블이 붙습니다. 스킬은 개요를 위해 `tracker.json`을 읽고, 실제로 진행 중인 지원 건에 대해서만 상세 파일이나 연락처 파일을 엽니다. 지원 건 id는 읽을 수 있는 슬러그(`app-hex-senior-pm`)라서 이름으로 해당 지원 건의 파일을 찾을 수 있습니다. 필드별 전체 정의는 [references/tracker-schema.md](references/tracker-schema.md)에 있습니다.

클라우드 커넥터를 설정하지 않는 한 어떤 데이터도 내 컴퓨터를 벗어나지 않습니다([CONNECTORS.md](CONNECTORS.md) 참고).

**백업하려면**: 구직 폴더 전체를 복사하세요.

---

## 채용 검색 및 저장소 설정

`/careerloop:launch`를 실행해 연동을 설정합니다. 마법사가 대화형으로 모든 것을 처리하므로 파일을 직접 편집할 필요가 없습니다.

**채용 검색(커넥터 우선):** CareerLoop는 현재 라이브 공고에 **Indeed** MCP 커넥터(`search_jobs`, `get_job_details`)를 사용하며, 그 밖의 채널(주/연방 정부 게시판, 틈새 게시판, 회사 직접/ATS 포털)은 브라우저/수동 대체를 지원합니다. **Claude Desktop**에서 **Customize → Connectors**에 Indeed를 추가하고, **Indeed**를 열어 **Connect**를 누른 뒤, 브라우저에서 **Grant access to Indeed**를 완료합니다(**secure.indeed.com**의 Indeed OAuth — 로그인 후 **Continue**). 도구가 로드되지 않으면 **새 채팅**을 시작하세요. 전체 안내는 `/careerloop:launch` 3단계를 참고하세요.

세션에서 Indeed 이외의 커넥터를 쓸 수 없을 때도 `search-jobs`는 정규화된 필드(`title`, `company`, `location`, `apply_url`, `source`, `retrieval_mode`)와 출처 인지형 중복 제거/신뢰도 표시를 갖춘 보조 수동 수집으로 실행할 수 있습니다. [CONNECTORS.md](CONNECTORS.md)와 `skills/search-jobs/SKILL.md`를 참고하세요.

**이메일 & 캘린더 맥락(선택 — 웜 아웃리치):** **Connectors**에서 **Gmail** 및/또는 **Microsoft 365** 및/또는 **Google Calendar**를 연결하면 **`draft-outreach`**, **`follow-up`**, **`contact-context`** 등의 스킬이 **내** 메일을 검색하고 연락처와의 **과거 및 예정** 미팅을 요약할 수 있습니다. 단, 조회할 때마다 **내가 승인한 경우에만** 가능합니다(예정된 미팅은 **웜** 식별에 도움이 되므로, 이미 통화가 잡혀 있다면 콜드 오프닝을 피하세요). Anthropic이 브라우저에서 **OAuth**를 제공하므로 채팅에 비밀번호를 입력하지 않습니다. **Microsoft 365**는 **Team/Enterprise** 플랜과 관리자 설정이 필요할 수 있습니다. 전체 단계, 플랜 참고 사항, 공식 문서 링크는 [CONNECTORS.md](CONNECTORS.md)와 `/careerloop:launch` 6단계에 있습니다.

**PKM 스토리 소스(선택 — 면접 스토리 인텔리전스):** `mine-stories`는 로컬 파일 외에 PKM 시스템에서도 가져올 수 있습니다. 지원 경로로는 호스트 세션에서 사용 가능한 경우 **공식 Notion 커넥터**와 **MCP를 통한 Capacities**가 있으며, 대체 수단으로 로컬 내보내기/파일 마이닝을 씁니다. 설정 패턴과 출처 규칙은 [CONNECTORS.md](CONNECTORS.md)를 참고하세요.

**저장소:** 모든 데이터는 내 구직 폴더(`{user_dir}`)에 로컬로 저장됩니다. 기본적으로 어떤 것도 내 컴퓨터를 벗어나지 않습니다. 이식성을 위해 클라우드 기반 저장소를 쓸 수 있습니다.
- **Google Drive, OneDrive, Dropbox 등:** Claude의 기본 커넥터는 일반적인 구직 파일(JSON/DOCX 등)에 안정적이지 않으므로 **애플리케이션 동기화**(또는 수동 백업/복원)를 권장합니다.
설정과 대체 동작은 [CONNECTORS.md](CONNECTORS.md)를 참고하세요.

### 연봉 벤치마킹용 Apify MCP(선택 — Claude Desktop 커넥터)

`/careerloop:salary-research`는 MCP를 통해 **Apify**를 사용합니다. 플러그인은 토큰을 `.mcp.json`에 넣지 **않습니다**(MCP `args`의 환경 변수 치환이 안정적으로 확장되지 않기 때문입니다). 대신 Claude에 Apify를 **Desktop 커넥터**로 추가하면 앱이 토큰과 도구 목록을 저장해 줍니다.

1. [apify.com](https://apify.com)에서 계정을 만들고 **Console → Settings → Integrations**에서 **Personal API token**을 복사합니다.
2. Claude Desktop에서 **Customize**(또는 **Settings**)를 열고 **Connectors**로 이동합니다.
3. **Desktop** 아래에서 **Apify**(**apify-mcp-server**로 표시될 수 있음)를 선택합니다.
4. **Configure**(또는 커넥터 설정)를 클릭합니다.
5. **Apify token (Required)**에 토큰을 붙여 넣습니다.
6. **Enabled tools**에서 기본값을 아래의 정확한 쉼표 구분 목록(공백 없음)으로 교체합니다.

   `call-actor,get-actor-run,get-dataset-items,cheapget/best-job-search`

7. **Save**를 클릭하고 커넥터가 **활성화**되어 있는지 확인한 뒤, 도구가 로드되도록 **새 채팅**을 시작합니다.

8. `/careerloop:salary-research`를 실행하거나 직무와 지역에 대한 연봉 범위를 물어보세요.

토큰을 이 저장소나 신뢰할 수 없는 채팅 로그에 붙여 넣지 마세요. 도구 권한 프롬프트(예: "needs approval")는 정상이며, 연봉 조사를 실행하려는 의도일 때 승인하면 됩니다.

### 선택: 면접 오디오 전사(`mcp-transcribe`)

> **`/careerloop:setup-transcribe`가 실행하는 것**(선택 기능이며, 실행하기 전에 단계별로 안내합니다)
> 1. `command -v uv`, `ffmpeg`, `brew`로 설치 여부만 확인합니다(읽기 전용). `uv`나 `ffmpeg`가 없으면 `brew install`을 실행해도 되는지 먼저 묻고, 승낙한 뒤에만 설치합니다.
> 2. `mcp-transcribe/install_transcribe_mcp.py`를 실행합니다. 환경을 점검한 뒤 `uv sync`로 Python 의존성을 `mcp-transcribe/.venv`에 설치합니다(Apple Silicon은 `--extra mlx`).
> 3. Claude Desktop 설정 파일(`~/Library/Application Support/Claude/claude_desktop_config.json`)에 `mcp-transcribe` 서버를 등록합니다. 수정 전에 `claude_desktop_config.json.transcribe_backup`으로 백업하고, 점검이 하나라도 실패하면 설정 파일을 건드리지 않습니다.
> 4. 첫 전사 때 라이브러리가 Whisper 모델 파일을 Hugging Face에서 내려받을 수 있습니다. 오디오 자체는 외부로 전송하지 않고 내 컴퓨터에서만 처리합니다.

`interview-capture`는 로컬 **`mcp-transcribe`** MCP 서버(Whisper 기반, 전적으로 내 컴퓨터에서 실행되며 클라우드 계정 불필요)를 통해 녹음된 면접 오디오 파일을 자동으로 전사할 수 있습니다. 준비와 모의 면접 자체는 텍스트 전용이며, 이 기능은 녹음 후 전사하는 용도로만 쓰입니다.

`/careerloop:setup-transcribe`를 실행하세요. 터미널 없이도 사전 요건을 확인하고, 설치하고, Claude Desktop에 서버를 등록해 줍니다. 고급 사용자는 대신 [`mcp-transcribe/README.md`](mcp-transcribe/README.md)의 수동 단계를 따를 수 있습니다.

자세한 내용: [CONNECTORS.md](CONNECTORS.md)(면접 전사 절). 저장소의 **`.mcp.json`**은 선택적 HTTP 커넥터(예: Gmail, Calendar, Microsoft 365)용일 뿐이며, 이 서버는 포함하지 **않습니다**. 현재 `.mcp.json`은 비어 있으므로 Gmail·Calendar·Microsoft 365는 Claude 앱의 커넥터로 직접 추가합니다.

### 선택: 지역 이벤트 — Luma 탐색

이벤트 인텔리전스 워크플로(**`event-radar`**, **`event-intelligence`**)에서 CareerLoop는 세션에서 MCP 서버를 쓸 수 있다면 Luma 이벤트 탐색 도구를 사용할 수 있습니다. 이 서버는 포함돼 있지도, 필수도 아닙니다. 원한다면 오픈소스 **[`alx1p/luma-mcp`](https://github.com/alx1p/luma-mcp)** 프로젝트(Claude Desktop 확장)를 독립적으로 설치할 수 있으며, 설정은 해당 프로젝트의 README를 참고하세요. 없으면 `event-radar` / `event-intelligence`는 브라우저 보조 또는 수동 이벤트 수집으로 대체됩니다.

---

## 스케줄링 & 세션 동작

**스킬이 실체이고, Cowork가 내가 고른 주기로 이를 실행합니다.**

- **`focus-career`** — 세션을 열 때 사용합니다(선제적인 핵심 점검을 원하면 `/schedule`로 촘촘한 주기를 예약). 임박한 오퍼 마감, 오늘 해야 할 후속 조치, 당일 면접 액션 같은 긴급 항목만 보여 줍니다.
- **`daily-schedule`** — Claude Cowork **`/schedule`**로 **매일** 실행하는 것을 권장합니다. 정기 요약(파이프라인, 후속 조치, 오늘 면접, 아티팩트)을 전달합니다. 집계 전에 `{user_dir}`에 PDF/DOCX 아티팩트가 있으면 **`artifact-saved`**를 실행해 `artifacts-index.json`이 디스크와 어긋나지 않게 합니다.
- **`daily-schedule`** — 또한 월 단위로 career-plan 노후화 점검을 수행하고, 궤적 데이터가 오래됐으면 `/careerloop:career-plan`을 권합니다.
- **`application-update`** — **`track-application`**이 지원 기록(`tracker.json` 요약 행과 그 상세/연락처 파일)을 갱신한 뒤, 같은 턴에 이 워크플로를 실행해 갱신 안내와 pattern-analysis 유도를 받습니다.
- **`follow-up-timing`** — 지원 건이 오퍼 단계에 도달했는데 평가 맥락이 아직 없으면, 마감 압박이 커지기 전에 `/careerloop:evaluate-offer`를 권합니다.
- **`artifact-saved`** — 맞춤 이력서/자기소개서를 저장한 뒤, 또는 `daily-schedule`이 디스크에서 아티팩트 파일을 감지했을 때 실행합니다.

**Cowork 호스트 훅:** 기본으로 등록된 훅은 없습니다(`hooks/hooks.json`은 비어 있음). 세션 시작 때 `focus-career`를 자동 실행하고 싶다면 `SessionStart` 훅에서 `scripts/load-context.sh`를 실행하도록 직접 등록하세요. 등록하지 않은 경우에는 `/careerloop:focus-career`를 수동으로 실행합니다.

**중요(현재 동작):** `SessionStart` 훅은 신뢰성 문제를 조사하는 동안 현재 **비활성화**돼 있습니다. 핵심만 담은 브리핑을 받으려면 세션을 시작할 때마다 **`/careerloop:focus-career`**를 직접 실행하세요.

**반복** 요약은 Cowork에서 **사용자가 설정**합니다(예: `daily-schedule`에 **`/schedule`**). 첫 예약 실행이 성공하면 Cowork가 학습한 내용(경로, 커넥터, 맥락)으로 프롬프트를 다듬습니다.

---

## 설계 원칙

- **격려보다 정직** — 거짓 안심이 아니라 솔직한 평가
- **기계적이기보다 지능적** — 입력만이 아니라 결과에 따라 출력이 적응
- **커넥터 기반** — 저장소와 분석은 교체 가능하며, 명령을 바꾸지 않고 백엔드를 바꿀 수 있음
- **프라이버시 우선** — 모든 데이터는 기본적으로 로컬에 머물며, 민감한 기능은 명시적 옵트인이 필요
- **크로스 플랫폼** — macOS, Windows, Linux에서 동작

---

## 로드맵

### Phase 3 — 상시 가동 커리어 에이전트

상태: 진행 중

Phase 3은 CareerLoop를 "함께 앉아서 쓰는 강력한 어시스턴트"에서, 맥락을 유지하며 정해진 주기로 돌아가고 내가 이미 쓰는 채널에서 만나 주는 상시 가동 커리어 운영 계층으로 발전시킵니다. 이 방향은 **OpenClaw**가 촉발한 업계 흐름(영속 스레드, 비동기 디스패치, 이벤트 기반 채널)을 반영하되, 호스트에 종속되지 않습니다(Anthropic/Claude와 NemoClaw는 예시일 뿐 의존성이 아닙니다).

- **모닝 다이제스트** ✅: *밤사이 온 리크루터 회신을 요약하고, 오래된 후속 조치를 표시하고, 노트북을 열기 전에 맞는 신규 직무를 띄워 줍니다.* **`/careerloop:setup-schedule`**로 자동화되며, 2단계 Gmail 받은편지함 스캔(7일 전체 + 30일 회사별 보충), 후속 조치 알림, 신규 채용 탐색을 수행하는 Cowork 예약 작업을 만듭니다. **임팩트:** 이메일, 채용 게시판, 트래커를 매일 수동으로 확인하는 일이 사라짐.
- **파이프라인 상태 페이지** ✅: *진행 중인 지원, 집중/추천 직무, 종료된 건, 패스한 직무까지 전체 파이프라인을 필터로 볼 수 있는 표로, 지원 타임라인이 임베드되어 있습니다.* **`/careerloop:pipeline-status`**로 생성하며, **`/careerloop:setup-schedule`**로 매일 밤 갱신하도록 예약할 수 있습니다. **임팩트:** 수동으로 재생성하지 않아도 항상 최신인 상태 페이지.
- **주간 시장 브리프** ✅: *직무 수요 변화, 목표 회사의 채용 신호, 내 목표와 관련된 이벤트/CFP를 다루는 월요일 보고서.* **임팩트:** 즉흥적인 조사를 일관된 인텔리전스 주기로 대체.
- **후속 조치 알림** ✅: *기준 대비 응답 지연을 감지하고, 모바일에서 검토하고 보낼 수 있는 후속 조치 초안을 미리 작성합니다.* **임팩트:** 놓치는 일 없이 시스템이 파이프라인의 시계를 관리.
- **주간 인사이트 보고서**: *금요일에 쉬운 말로 쓴 퍼널 요약과, 무엇이 통하고 있는지에 근거한 구체적인 포지셔닝 조정 한 가지.* **임팩트:** 구직 활동을 느낌 기반에서 데이터 기반으로 전환.
- **고급 분석 내보내기**: *맞춤 리포팅과 심층 분석을 위한 Power BI, Qlik, D3 내보내기 인터페이스.* **임팩트:** 핵심 워크플로를 바꾸지 않고도 파워 유저와 코치가 유연한 외부 대시보드를 쓸 수 있음.
- **대시보드 & 시각화 개선**: *파이프라인 전망 오버레이, 보이스 주기 표시, 네트워크 그래프 UI 개선이 Phase 3 제공 범위로 이동합니다.* **임팩트:** 같은 상시 가동 운영 계층에서 더 풍부한 계획 수립과 관계 가시성을 확보.
- **디스패치 모바일 계층**: *휴대폰에서 메시지 하나("내일 면접 준비시켜줘")를 보내면 데스크톱에 전체 브리프가 준비됩니다.* **임팩트:** 어디서든 데스크톱 수준의 역량.
- **채널(Telegram, Slack)**: *채팅으로 즉시 면접 디브리프와 트래커 업데이트를 하고, 다음 라운드를 위한 준비 공백을 표시합니다.* **임팩트:** "나중에 기록해야지"를 환경 속 자동 기록이 대체.
- **컴퓨터 사용(범용 커넥터 대체 수단)**: *1급 커넥터가 없거나 너무 제한적일 때(예: LinkedIn 워크플로) 에이전트가 (명시적 승인 아래) UI 자동화로 탐색하고, 상태를 추출하고, 메시지를 작성하고, 검토용 액션을 준비합니다.* **임팩트:** "커넥터 없음"이 end-to-end 워크플로의 확정적 장애물이 되지 않음.
- **프로젝트(아티팩트 & 워크스페이스 정리)**: *사람이 만든 아티팩트와 기계가 생성한 아티팩트를 회사/직무별로 묶고 트래커 단계에 연결해, 폴더나 채팅 기록을 뒤지지 않고도 무엇을 보냈고, 무엇이 바뀌었고, 무엇을 재사용할지 늘 분명하게 합니다.* **임팩트:** 아티팩트 난립을 줄이고 세션 간 멀티 에이전트 작업을 읽기 쉽게 함.

### Phase 4 — 엔터프라이즈 & 생태계

- **커리어 코치용 화이트 라벨**: *코치가 일일 브리핑, 파이프라인 추적, 시장 인텔리전스를 자기 브랜드로 제공해 고객 8명이 아니라 40명을 담당합니다.* **임팩트:** 더 높은 기본 서비스 품질로 5배 수용력.
- **익명화된 벤치마크 데이터**: *집계된 패턴(단계/직무/지역별 응답 기간, 지원하기 좋은 요일)이 모든 사용자의 타이밍과 전략을 개선합니다.* **임팩트:** 규모가 커질수록 조언이 더 똑똑해짐.
- **정부 / American Job Center 연동**: *상담사가 자동화된 브리프와 후속 조치 알림으로 많은 케이스를 담당하고, 사람의 시간을 예외 상황에 집중합니다.* **임팩트:** 양질의 지원을 소외된 계층으로 확장.
- **참전용사 & 장애인 경로 모듈**: *군 복무 직무와 제약을 민간의 대응 직무로 변환하고, 보안 인가/자격 요건을 매핑하고, 채용 담당자가 알아볼 수 있는 언어를 생성합니다.* **임팩트:** 구조적인 번역 불이익을 제거.
- **사회초년생 / 대학생 경로**: *학생은 학기 단위 운영 주기를 받습니다. 수업/프로젝트 기반의 기본 이력서, 인턴십별 변형, 지원 추적, 커리어 페어/캠퍼스 리크루팅 일정 표시, 동문/리크루터 아웃리치 초안, 기한 초과 후속 조치 알림이 포함됩니다.* **임팩트:** 사회초년생이 겪는 채용 학습 곡선을 반복 가능한 워크플로로 압축해, 일관되지 못한 후속 조치 때문에 마감을 놓치거나 기회를 잃지 않게 함.

---

## 사양

모든 에이전트, 스킬, 스케줄링, 데이터 모델, 설계 철학을 다루는 전체 제품 사양은 [careerloop-spec.md](references/careerloop-spec.md)를 참고하세요.

## 기여

기여를 환영합니다. 중요한 변경은 풀 리퀘스트를 보내기 전에 이슈를 먼저 열어 주세요. 가이드라인은 [CONTRIBUTING.md](CONTRIBUTING.md)를 참고하세요.

## 라이선스

Apache License 2.0 — 자세한 내용은 [LICENSE](LICENSE)를 참고하세요. 단, `mcp-transcribe/manifest.json`은 MIT로 표기돼 있습니다.
