---
name: career-plan
description: >
  프로필 + ExperienceLibrary를 바탕으로, 시장 기반 수요와 AI/자동화 대체 전망을 반영해 현실적이고 솔직한
  단기/중기/장기 커리어 궤적과 갭 분석을 작성합니다. 보고서인 `career-trajectory.md`와 다운스트림 점수화를 위한
  `career-trajectory-data.json`(`career_trajectory_v1`)을 저장합니다. 다음과 같은 요청에 사용합니다:
  "career plan", "career trajectory", "where am i headed", "what should i target next",
  "커리어 플랜 세워줘", "내 커리어 방향이 어디일까?", "다음에 어떤 직무를 노려야 할까?".
  (Builds a realistic, honest near/medium/long-term career trajectory and gap
  analysis using profile + ExperienceLibrary, with market-informed demand and
  AI/automation displacement outlook. Saves `career-trajectory.md` (report) and
  `career-trajectory-data.json` (`career_trajectory_v1`) for downstream scoring.)
triggers:
  - "career plan"
  - "career trajectory"
  - "where am i headed"
  - "what should i target next"
  - "/careerloop:career-plan"
  - "커리어 계획"
  - "커리어 궤적"
  - "내 방향이 어디로 가고 있어"
  - "다음에 어떤 직무를 목표로 해야 할까"
  - "내 커리어 경로를 짜줘"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

`career-plan`을 실행해 현실적인 커리어 플랜, `{user_dir}/CareerLoop/career-trajectory.md`의 사람이 읽는 보고서, 그리고 `{user_dir}/CareerLoop/career-trajectory-data.json`의 구조화된 `career_trajectory_v1` 아티팩트를 만듭니다.

## 워크플로

### 디렉터리 공유 (호스트 연동)
이 스킬을 실행하는 동안 호스트 UI가 **에이전트와 공유할 디렉터리**를 요청하면, `{user_dir}` 구직 폴더(`CareerLoop/`를 포함한 폴더)**만** 공유합니다.

이 스킬의 모든 읽기/쓰기 대상:
- `{user_dir}/CareerLoop/profile.md`
- `{user_dir}/CareerLoop/ExperienceLibrary.json`
- `{user_dir}/CareerLoop/career-trajectory.md`
- `{user_dir}/CareerLoop/career-trajectory-data.json`
- `{user_dir}/CareerLoop/career-trajectory-{as_of}-{ideal_role_slug}.md` (버전별 보고서 스냅샷)
- `{user_dir}/CareerLoop/career-trajectory-data-{as_of}-{ideal_role_slug}.json` (버전별 데이터 스냅샷)

전체 워크스페이스나 관련 없는 폴더는 공유하지 않습니다.

### 1. 필수 데이터 존재 확인
읽을 파일:
- `{user_dir}/CareerLoop/profile.md`
- `{user_dir}/CareerLoop/ExperienceLibrary.json`

없으면 다음과 같이 출력합니다.
> 커리어 플랜을 건너뜁니다: 먼저 `/careerloop:launch`를 실행해 `CareerLoop/`를 초기화하세요.

### 2. 선택적 이상적 직무 인자
사용자가 명시적인 목표를 제공하면(예: "for an Applied AI PM role"("Applied AI PM 직무로") 또는 "ideal_role: Senior Product Manager"), 맞춤형 갭 분석을 위해 이를 `ideal_role`로 기록합니다. 그렇지 않으면 `ideal_role = null`로 설정합니다.

### 3. 시장 인텔리전스 확인 (수요 + AI 대체 + 보상 방향)
**`market-researcher`** 에이전트에게 다음을 넘깁니다.
- 전체 `profile.md`와 (제공된) 주요 목표 직무/지역
- 전체 `ExperienceLibrary.json` (대체 리스크를 사용자의 지속 가능한 강점과 맞출 수 있도록)
- 지시: 다음 기간별 신호를 만들 것
  - Near-term (0–18 months)
  - Medium-term (18 months–4 years)
  - Long-term (4+ years)
- 보상 추이 방향(각 기간에 걸쳐 보상이 오르거나 정체되는 경향)과 지역 경쟁도 메모

### 4. 솔직한 궤적 종합
**`honest-advisor`** 에이전트에게 다음을 넘깁니다.
- 3단계의 시장 인텔리전스 출력
- 전체 프로필 + ExperienceLibrary
- 선택적 `ideal_role` (있는 경우)
- `## Employment Context`(있는 경우)도 함께 전달해, 플랜이 이직 비용(재직 중) 또는 긴급성/runway(무직)를 반영하도록 함

지시: norm/exception/strategy 패턴을 적용해 다음을 담은 **CareerTrajectoryReport**를 출력할 것
- 현재 위치 평가 (경쟁 우위 수준 + 이유, 가능하면 트래커/ExperienceLibrary에 근거)
- 달성 가능성 순으로 정렬한 현실적인 단기 궤적 (0–18개월)
- 분기(예: IC vs 매니지먼트, 스타트업 vs 대기업)를 포함한 중기 궤적 (18개월–4년)
- 장기 전망 (4년 이상), 천장 리스크/선택지에 대한 솔직한 프레이밍
- ROI(비용 x 시간 x 영향) 순으로 정렬한 시장 기반 갭 분석

`ideal_role`이 설정돼 있으면:
- "Ideal role gap analysis" 섹션(제목은 영문 그대로)을 추가해, 이상적인 직무가 현실적으로 달성 가능한지, 어떤 조건/기간에서 가능한지, 어떤 단계가 결과 확률을 가장 크게 바꿀지 서술합니다.

### 5. 보고서 + `career_trajectory_v1` 데이터 저장 (버전별 이력 포함)
실행할 때마다 두 개의 아티팩트를 씁니다.

1) **마크다운 보고서** (사람이 읽는 용도, JSON 내장 없음):
- 버전별 스냅샷: `{user_dir}/CareerLoop/career-trajectory-{as_of}-{ideal_role_slug}.md`
- 정본 보고서: `{user_dir}/CareerLoop/career-trajectory.md`

2) **`career_trajectory_v1` JSON** (기계가 읽는 용도, `job-scout`, `search-jobs`, `compare-offers`, `daily-schedule`이 사용):
- 버전별 스냅샷: `{user_dir}/CareerLoop/career-trajectory-data-{as_of}-{ideal_role_slug}.json`
- 정본 데이터: `{user_dir}/CareerLoop/career-trajectory-data.json`

여기서:
- `as_of` = 현재 날짜 `YYYY-MM-DD`
- `ideal_role_slug` = `ideal_role`을 소문자로 바꾸고, 앞뒤 공백을 제거하고, 공백은 `-`로 합치고, `\ / : * ? " < > |` 문자를 제거한 값. `ideal_role = null`이면 `no-ideal-role`을 사용합니다.

**쓰기 순서 (권장):**
- 먼저 **버전별 스냅샷** 두 개(`.md` + `.json`)를 씁니다.
- 그다음 **정본 파일** 두 개(`.md` + `.json`)를 써서, 다운스트림 소비자가 항상 최신 쌍을 읽도록 합니다.

**마크다운 제목 요구사항:**
다음과 같은 줄을 포함합니다.
`## Career trajectory analysis ({YYYY-MM-DD})`
이렇게 하면 독자(그리고 `daily-schedule` 폴백)가 보고서 날짜를 한눈에 알 수 있습니다.

**`career_trajectory_v1` JSON 요구사항:**
데이터 파일은 다음 형태의 유효한 JSON이어야 합니다.
```json
{
  "schema": "career_trajectory_v1",
  "as_of": "{YYYY-MM-DD}",
  "ideal_role": "{string or null}",
  "near_term_roles": [
    { "rank": 1, "role_title": "...", "achievability_label": "high|med|low", "rationale": "..." }
  ],
  "medium_term_roles": [
    { "rank": 1, "role_title": "...", "achievability_label": "high|med|low", "rationale": "..." }
  ],
  "gap_analysis": [
    { "priority_rank": 1, "gap_area": "...", "why_it_matters": "...", "roi_score_0_100": 0, "cost_time_estimate": "...", "execution_risks": "..." }
  ]
}
```

이 JSON을 `career-trajectory.md`에 내장하지 **않습니다**. 다운스트림 스킬은 `career-trajectory-data.json`을 직접 읽습니다.

디스크 쓰기 도구가 실패하면:
- 저장한 것처럼 꾸미지 않습니다.
- 전체 마크다운 보고서와 JSON 페이로드를 각각 별도의 코드 블록으로 보여주고, 위의 버전별 + 정본 경로에 직접 저장하도록 사용자에게 안내합니다.

### 6. 결과 제시
대화형 CareerTrajectoryReport를 채팅으로 제시하고 다음과 같이 확인합니다.
> 스냅샷을 `{user_dir}/CareerLoop/career-trajectory-{as_of}-{ideal_role_slug}.md`와 `{user_dir}/CareerLoop/career-trajectory-data-{as_of}-{ideal_role_slug}.json`에 저장했습니다(다운스트림 점수화를 위해 정본 `career-trajectory.md` + `career-trajectory-data.json`도 업데이트했습니다).

