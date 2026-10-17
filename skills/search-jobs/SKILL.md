---
name: search-jobs
description: >
  커넥터 우선 방식으로 관련 채용 공고를 검색하고 순위를 매깁니다.
  Indeed MCP를 사용할 수 있으면 우선 사용하고, 그렇지 않으면 주/연방 채용 게시판,
  전문 채용 게시판, 회사/ATS 채용 페이지에 대해 브라우저/수동 방식으로 대체합니다.
  (Search and rank relevant job listings using connector-first discovery.
  Trigger examples: "search for jobs", "find jobs", "search indeed", "find me jobs".)
triggers:
  - "/search-jobs"
  - "search for jobs"
  - "find jobs"
  - "search jobs"
  - "look for job listings"
  - "find me jobs"
  - "search indeed"
  - "search wellfound"
  - "search state jobs"
  - "search company careers"
  - "what jobs are out there"
  - "show me job listings"
  - "일자리 검색"
  - "채용 공고 찾아줘"
  - "일자리 찾아줘"
  - "구인 공고 검색해줘"
  - "Indeed 검색해줘"
  - "회사 채용 페이지 검색해줘"
  - "어떤 일자리가 있어"
  - "채용 공고 보여줘"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

커넥터 우선 전략으로 사용자의 프로필에 맞는 채용 공고를 검색하고 순위를 매깁니다.

## 소스 모델과 정규화

다음 순서로 하이브리드 소스 모델을 사용합니다.

1. **커넥터 네이티브 MCP(권장)** — 사용 가능한 모든 소스에 적용합니다(현재 구현에서는 Indeed 우선).
2. **브라우저 지원 수집**(Claude in Chrome / computer use) — MCP가 없거나 브라우저 전용 흐름일 때만 사용합니다.
3. **수동 지원 입력(assisted-manual ingestion)** — 항상 보장되는 대체 수단입니다.

순위를 매기기 전에 모든 공고를 다음 스키마로 정규화합니다.

- `title` (필수)
- `company` (필수)
- `location` (필수)
- `apply_url` (필수)
- `source` (필수; 예: `indeed`, `illinoisjoblink`, `wellfound`, `company_direct`, `ats_greenhouse`)
- `retrieval_mode` (필수; `mcp` | `browser` | `manual`)
- `salary` (선택, 구조화된 범위가 없으면 원문 텍스트)
- `posted_date` (선택)
- `close_date` (선택; 공공 부문 공고에서 흔함)
- `employment_type` (선택)
- `job_id_or_requisition` (선택이지만 중복 제거를 위해 권장)
- `raw_description` (선택이지만 더 정확한 점수 산정을 위해 권장)

필수 필드가 누락되어 있으면 순위를 매기기 전에 누락된 필드만 질문합니다.

## 사전 점검 (커넥터 우선)

**라이브 경로:** **`search_jobs`**와 **`get_job_details`**를 사용할 수 있으면 이를 주 경로로 사용하고 아래 **§1–§5**를 따릅니다.

**이 세션에 Indeed MCP가 없는 경우:** 도구 결과를 지어내지 **않습니다**. 다음 두 가지를 모두 수행합니다.

1. **Claude Desktop**에서 라이브 검색을 활성화하는 방법을 안내합니다: **Customize → Connectors** → **Indeed** → **Connect** → 브라우저에서 **Grant access to Indeed**를 완료(**secure.indeed.com**의 Indeed OAuth — 로그인 후 **Continue**)한 다음 **새 채팅**을 시작합니다. 전체 안내는 **`/careerloop:launch`의 3단계**를 가리킵니다.

2. **수동 지원(Assisted manual):** **`search_jobs`** / **`get_job_details`**를 건너뜁니다. **§1**에서 파라미터를 로드한 뒤, 요청된 각 채널에 대해 2~3개의 맞춤 쿼리/링크 묶음을 제공합니다.
   - 주/연방 게시판(예: IllinoisJobLink, USAJobs),
   - 전문 게시판(예: Wellfound, Welcome to the Jungle),
   - 회사 직접/ATS 페이지(회사 채용 페이지, Greenhouse/Lever/Workday).
   사용자에게 **소스 모델과 정규화**의 정규화 스키마로 공고를 붙여넣도록 요청합니다. 사용자가 제공한 내용을 순위 산정을 위해 **`job-scout`**에 전달하고, 링크가 있는 경우 **§5** 레이아웃으로 제시합니다. 푸터: 커넥터가 연결되기 전까지 공고는 라이브 MCP가 아니라 **사용자 제공** 데이터임을 명시합니다.

## 워크플로

### 1. 검색 파라미터 로드

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분리(split) 레이아웃을 사용합니다. 읽기·쓰기 전에 반드시 해당 문서를 먼저 읽습니다.

`{user_dir}/CareerLoop/profile.md`를 읽고 다음을 추출합니다.
- **직무/쿼리** — `## Target Roles`의 첫 1~2개 항목을 검색 쿼리로 사용
- **위치 선호** — `## Location`을 다음으로 분해
  - 주요 근무 방식 선호(예: remote-first)
  - 허용 가능한 근무 방식(remote, hybrid, on-site)
  - 지역 제약(사용자가 열려 있는 도시/주, 그리고 명시된 경우 피하거나 후순위로 둘 지역)
  - 이주/출장 의향

프로필이 "remote-first"만 암시하고 보조적인 유연성을 명확히 정의하지 않았다면, 검색 전에 짧게 한 번 확인 질문을 합니다.
> "원격을 최우선으로 두되 일부 하이브리드/이주 옵션도 포함할 수 있습니다. 보조 대상으로 포함할 지역(예: 뉴욕, 샌프란시스코)은 어디이고, 제외할 지역이 있나요?"

사용자가 요청에 명시적인 검색어를 제공한 경우(예: "find AI PM jobs in New York"), 프로필 값 대신 또는 프로필 값과 함께 그 검색어를 사용합니다. 항상 사용자의 명시적 의도를 우선합니다.

`profile.md`가 없거나 목표 직무가 없으면 다음과 같이 묻습니다.
> "어떤 직무와 지역을 검색할까요?"

제공된 경우 선택적 소스 선호를 수집합니다.
- 선호 채널(`state/federal`, `niche`, `company_direct`, `aggregator`)
- 목표 회사 목록(회사 직접 및 ATS 탐색용)
- 사용자가 원하지 않는 소스

### 1.25 수동 지원 플레이북 (MCP가 없거나 사용자가 추가 채널을 요청할 때)

요청된 채널을 세션에서 MCP로 라이브 검색할 수 없는 경우, 간결한 플레이북을 생성합니다.

1. **주/연방 게시판**
   - 직무 + 위치 + 등급/연차 힌트를 사용한 소스별 쿼리 문자열을 제공합니다.
   - `close_date`가 있으면 요청합니다.
   - 예시 게시판: IllinoisJobLink, USAJobs.

2. **전문 게시판**
   - 직무 유사어와 remote/on-site 변형을 포함한 게시판별 쿼리를 제공합니다.
   - 가능하면 연봉 텍스트와 지분(equity) 상세를 요청합니다.
   - 예시 게시판: Wellfound, Welcome to the Jungle.

3. **회사 직접 및 ATS**
   - 각 목표 회사마다 직접 채용 쿼리 하나와 ATS 쿼리 변형 하나를 제공합니다(`site:boards.greenhouse.io`, `site:jobs.lever.co`, `site:myworkdayjobs.com`).
   - 확인 가능한 경우 정식 `apply_url`과 requisition ID를 요청합니다.

### 1.5 경력 궤적 컨텍스트 로드 (점수 산정용)

검색하기 전에 `{user_dir}/CareerLoop/career-trajectory-data.json`이 있는지 확인합니다.

- 있으면 `career_trajectory_v1`로 읽습니다(특히 `as_of`, `near_term_roles`, `medium_term_roles`).
- 없으면 궤적 컨텍스트 없이 계속 진행합니다.
- 있지만 JSON을 파싱할 수 없으면, 계속 진행하되 파싱 오류로 궤적을 사용할 수 없음으로 표시합니다(이 신호를 조용히 버리지 않습니다).

결과를 제시할 때 점수 헤더 뒤에 궤적 관련 한 줄 메모를 포함합니다.
- `Trajectory context: used (as_of {YYYY-MM-DD})`
- 또는 `Trajectory context: unavailable (missing or unparseable)`

### 2. Indeed 검색

위치 선호로부터 소규모 검색 계획을 세운 뒤 `search_jobs`를 호출합니다.

다음 순서로 최대 3개의 레인(lane)을 만듭니다.
1. **주 레인** — 최우선 선호(대개 `remote`)
2. **보조 레인** — 가장 적합한 하이브리드/이주 지역(예: 뉴욕)
3. **3차 레인** — 사용자가 열려 있는 경우에만 추가 지역(예: 샌프란시스코)

추출한 파라미터로 각 레인마다 `search_jobs`를 호출합니다.
- `search` — 직무 또는 키워드 문자열(예: `"Director of AI Product"`)
- `location` — 도시/주(예: `"New York, NY"`) 또는 `"remote"`
- `country_code` — 사용자의 위치가 다른 나라를 나타내지 않으면 `"US"`
- `job_type` — 사용자가 지정하지 않으면 생략(fulltime, parttime, contract 등)

레인을 병렬로 실행한 뒤 작업 ID/링크 기준으로 병합하고 중복을 제거합니다.

사용자가 추가 채널을 요청했는데 동등한 MCP 도구가 없으면 **§1.25**의 수동 지원 플레이북을 덧붙이고, 공고가 붙여넣어지면 계속 진행합니다.

### 3. 공고 상세 조회

검색 결과에서 가장 관련성이 높은 상위 5개 공고를 선정합니다. 각 공고마다 `search_jobs`가 반환한 job ID로 `get_job_details`를 호출해 전체 설명, 확정 연봉, 지원 링크를 가져옵니다.

5개의 `get_job_details` 호출을 모두 병렬로 실행합니다.

Indeed가 아닌 공고나 수동 입력 공고는 붙여넣은 메타데이터를 상세 페이로드로 간주하고, 누락된 필드를 명시적으로 표시합니다.

### 4. job-scout로 점수 산정 및 순위 결정

결과 가중 점수 산정을 위해 가져온 모든 공고를 `job-scout` 에이전트에 전달합니다. job-scout는 다음을 수행합니다.
- `tracker.json`에서 `search_performance`와 `strategy_signals`(둘 다 최상위 키이며 분리 레이아웃의 영향을 받지 않음)를, `CareerLoop/ExperienceLibrary.json`에서 `performance_weights`를 읽음
- `{user_dir}/CareerLoop/career-trajectory-data.json`이 있으면 읽어서 `career_trajectory_v1`의 궤적 정합성 가산점을 적용
- 신뢰도 등급별 적응형 가중치를 사용해 결과 신호, ExperienceLibrary 적합도, 프로필 적합도, 전략 신호 전반에 걸쳐 각 공고의 점수를 산정
- 제한된 보정(최신성, 결과 품질, 이전 가능성)을 적용
- 종합 점수, 요인별 근거, 추천 등급(`critical` | `high` | `watch` | `none`)과 함께 순위대로 정렬된 공고를 반환

`job-scout`를 호출할 때 다음을 명시적으로 전달합니다.
- 전체 공고 페이로드(전체 JD/메타데이터 포함),
- `profile.md`, `tracker.json`(요약 행 — 점수 산정에는 `company`, `role`, `status`, `outcome`, `latest_stage`가 필요하고 단계 이력은 필요하지 않으므로 `detail_file` 내용은 전달하지 않음), `ExperienceLibrary.json`,
- 그리고 존재하는 경우 `{user_dir}/CareerLoop/career-trajectory-data.json`.

`career-trajectory-data.json`이 있지만 파싱할 수 없으면, `job-scout`를 건너뛰지 말고 점수 산정을 계속하며 궤적 정합성을 사용 불가로 표시합니다.

최종 제시에는 job-scout가 정한 순위를 사용합니다. job-scout가 동점(5점 이내)을 반환하면, 동점 그룹 내에서는 원래의 Indeed 관련도 순서를 유지합니다.

최종 순위 결정 전에 출처(provenance) + 신뢰도 + 중복 제거 정책을 적용합니다.

- **출처:** 모든 공고에는 `source`와 `retrieval_mode`가 있어야 합니다.
- **신뢰도 등급:**
  - `high` — 공고에 title/company/location/apply URL + 설명 + 게시일이 있는 경우.
  - `moderate` — 필수 필드는 있지만 설명/날짜가 일부만 있는 경우.
  - `directional` — 필수 필드는 있지만 여러 선택 필드가 누락된 경우.
- **중복 제거 우선순위:** 다음 순서로 공고를 우선합니다.
  1) 정식 회사 직접 URL,
  2) requisition ID가 있는 ATS URL,
  3) 커넥터에서 가져온 애그리게이터 URL,
  4) 수동 복사본.
  정규화한 title/company/location과 URL/requisition 겹침을 함께 사용해 중복을 탐지합니다.

상위 결과를 확정하기 전에 가벼운 위치 균형 점검을 적용합니다.
- 전체 최고 순위 공고는 유지하되, 보조 레인에서 강력한 매칭이 나왔는데도 원격 공고만 반환하는 것은 피합니다.
- 상위 5개의 목표 구성(가능한 경우): 점수가 5번째 순위 공고와 8점 이내라면 비주 레인에서 최소 1개 결과를 포함합니다.
- 사용자가 제외한 지역은 절대 포함하지 않습니다.

### 5. 결과 제시

형식을 갖춘 요약을 출력합니다. **지원 링크를 항상 공고 제목에 포함**해 사용자가 바로 클릭해서 지원할 수 있게 합니다 — 이는 Indeed 커넥터의 요구 사항입니다.

job-scout가 판정한 신뢰도 등급을 보여주는 한 줄 헤더로 시작합니다.

> *점수 산정: {Preliminary | Directional | Moderate | High confidence} — {사유, 예: "해결된 결과 3건 기반" 또는 "아직 결과 데이터 없음, 프로필 매칭만 반영"}*

이어서 다음을 포함합니다.
> *Trajectory context: {used (as_of YYYY-MM-DD) | unavailable (missing/unparseable)}*

이어서 다음을 포함합니다.
> *소스 구성: {소스별 건수} · 수집 방식: {mcp/browser/manual 건수}*

각 공고마다 다음 형식을 사용합니다.

---

**{#}. [{공고 제목}]({apply_link})**
회사: {회사명}
위치: {도시, 주 | 원격 | 하이브리드}
연봉: {명시된 경우 범위, 그렇지 않으면 "미기재"}
점수: {composite}/100 · ExperienceLibrary 적합도 {ExperienceLibrary fit %}% · 추천: {critical|high|watch|none}{회피 신호 경고가 있으면 표시}

> {공고 설명에서 가져온 직무 요약 2~3문장 — 업무 범위, 핵심 책임, 눈에 띄는 점에 초점}

---

모든 공고 뒤에 다음을 추가합니다.
> 공고는 {today's date}에 Indeed에서 가져왔습니다. 지원한 공고는 `/careerloop:track-application`을 실행해 기록하세요.

소스가 섞여 있으면 위 문구를 다음으로 바꿉니다.
> 공고는 {today's date}에 다음 소스에서 가져왔습니다: {소스 목록}. 수집 방식: {mcp/browser/manual 건수}. 지원한 공고는 `/careerloop:track-application`을 실행해 기록하세요.

이어서 다음을 추가합니다.
> 검색 구성: 원격 {remote_count}건, 하이브리드 {hybrid_count}건, 현장 근무 {onsite_count}건. 우선 반영: {primary preference}; 포함된 보조 지역: {목록 또는 "없음"}.

`critical` 또는 `high` 공고가 하나라도 있으면 다음을 덧붙입니다.
> 우선 추천: critical {critical_count}건, high {high_count}건. 최상위 추천부터 시작하세요.

**`search_jobs`가 결과를 반환하지 않는 경우:**
> "'{location}'에서 '{query}'에 대한 Indeed 검색 결과가 없습니다. 더 넓은 직함이나 다른 지역으로 다시 시도해 보세요."

**반환된 공고가 5개 미만인 경우** 찾은 만큼만 제시합니다 — 채우거나 지어내지 않습니다.

`directional` 공고가 있으면 한 줄을 추가합니다.
> 데이터 품질 참고: 일부 공고는 메타데이터가 부분적이므로, 누락된 필드가 채워지기 전까지 순위 신뢰도가 낮습니다.
