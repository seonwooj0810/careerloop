---
name: compare-offers
description: >
  오퍼 단계에 있는 여러 활성 지원 건을 보상, 직무 적합성, 시나리오별 리스크, 커리어 궤적 정합성 기준으로 나란히 비교합니다. 솔직한 순위를 제시하고 협상 핸드오프를 안내합니다.
  Compares multiple active offer-stage applications with side-by-side
  compensation, role fit, scenario-specific risk, and trajectory alignment.
  Produces an honest ranking and prompts negotiation handoff.
triggers:
  - "compare offers"
  - "compare job offers"
  - "which offer should i take"
  - "side by side offer comparison"
  - "/careerloop:compare-offers"
  - "오퍼 비교해줘"
  - "여러 오퍼 비교"
  - "어느 오퍼를 받아야 할까"
  - "오퍼 나란히 비교해줘"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

> **경력 연수 인용 규칙:** 경력·도메인 연수를 말할 때는 ExperienceLibrary의 날짜로 직접 계산한 값을 쓴다. 이력서나 프로필의 표기가 계산값과 다르면 계산값을 쓰고 불일치를 한 줄로 알린다(예: 이력서 "5년" ↔ 날짜상 4년 7개월).

`compare-offers`를 실행하여 트래커의 모든 활성 오퍼 단계 지원 건에 대한 **OfferComparisonReport**를 생성합니다. 가능하면 `evaluate-offer`에서 저장한 OfferContext 파일을 사용합니다.

## 워크플로

### 디렉터리 공유 (호스트 연동)
이 스킬을 실행하는 동안 호스트 UI가 **에이전트와 공유할 디렉터리**를 물으면, `{user_dir}` 구직 폴더(`CareerLoop/`가 들어 있는 폴더)만 공유합니다.

이 스킬이 읽는 파일:
- `{user_dir}/CareerLoop/profile.md`
- `{user_dir}/CareerLoop/ExperienceLibrary.json`
- `{user_dir}/CareerLoop/tracker.json` (요약 행)
- `{user_dir}/CareerLoop/applications/<application_id>.json` (비교 대상 오퍼당 하나)
- `{user_dir}/CareerLoop/contacts/<company-slug>.json` (협상 상대를 지목할 때만)
- `{user_dir}/CareerLoop/offer-context-{application_id}.json` (있는 경우)

전체 워크스페이스나 관련 없는 폴더는 공유하지 않습니다.

### 1. 필수 데이터 존재 확인

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분리 레이아웃을 사용합니다. 읽기/쓰기 전에 반드시 이 문서를 읽습니다.

읽을 파일:
- `{user_dir}/CareerLoop/profile.md`
- `{user_dir}/CareerLoop/ExperienceLibrary.json`
- `{user_dir}/CareerLoop/tracker.json`

없으면 다음을 출력합니다.
> 오퍼 비교를 건너뛰었습니다. `/careerloop:launch`를 실행하여 `CareerLoop/`를 초기화해 주세요.

### 2. 오퍼 단계 지원 건 모두 로드
`tracker.json` 요약 행에서 다음 조건의 지원 건을 선택합니다.
- `status`가 `"offer"`

하나도 없으면 다음을 출력합니다.
> 트래커에 활성 오퍼가 없습니다. 먼저 `/careerloop:track-application`으로 오퍼를 기록해 주세요.

**선택된 오퍼에 한해서만**(파이프라인의 나머지에는 절대 적용하지 않음) `{user_dir}/CareerLoop/` + 해당 행의 `detail_file`을 읽습니다. 비교는 `stage_history[]`와 `notes[]`에 담긴 전체 면접 및 협상 이력을 근거로 하며, 이 두 배열은 더 이상 `tracker.json`에 존재하지 않습니다. 요약 행만으로 비교하면 이력이 없는 오퍼가 만들어집니다. 각 행의 `application` 라벨, `latest_stage`, `latest_stage_date`, `contacts_file`, `contact_count`는 상세 정보와 함께 보관합니다.

비교에 오퍼 상대방(리크루터, 채용 관리자)이 필요하면 `{user_dir}/CareerLoop/` + 해당 행의 `contacts_file`을 읽고, **`application`**이 행의 **`application`** 라벨과 같은 항목만 남기며, **`name`으로 중복을 제거**합니다. 회사 파일 하나가 그 회사의 모든 지원 건을 담당하기 때문입니다. `contacts_file`이 없는 행은 등록된 연락처가 없는 것이며, 슬러그를 직접 만들어 내지 않습니다.

### 3. 지원 건별 OfferContext 로드, 없으면 인라인 평가
각 오퍼 지원 건에 대해:
- `offer_context_path = {user_dir}/CareerLoop/offer-context-{application_id}.json`으로 설정합니다
  (행의 `id`를 사용하며, 파일이 없으면 컨텍스트가 없다고 판단하기 전에 행의 `previous_ids`를 확인합니다)
- 있으면: 로드합니다
- 없으면: 평가 로직을 인라인으로 실행합니다.
  - `honest-advisor` + `market-researcher`를 사용해 OfferEvaluationReport를 생성합니다
  - 그런 다음 OfferContext JSON을 예상 경로에 저장합니다

세부 정보 부족으로 인라인 평가를 수행할 수 없으면, 사용자에게 최소한의 오퍼 기본 정보를 요청하고 부분 비교로 진행합니다.

### 4. 커리어 궤적 정합성 통합
`{user_dir}/CareerLoop/career-trajectory-data.json`이 있으면:
- `career_trajectory_v1`으로 읽습니다
- 단기 궤적 직무(0–18개월)를 사용해 각 오퍼의 궤적 정합성을 `high|medium|low`로 표시합니다

없으면:
- 궤적 정합성은 `unknown`이 되며 그렇게 명시적으로 표시합니다.

### 5. OfferComparisonReport 생성
로드한 모든 OfferContext 객체를 바탕으로 다음을 종합합니다.
- 나란히 비교하는 보상 표(기본급/보너스/지분/사이닝/총액, 벤치마크 격차 포함)
- 직무 적합성 매트릭스(궤적 정합성, 활용도 분석, 직급 일치, 프로필 타기팅)
- 오퍼별 프로세스 이력: §2에서 로드한 각 상세 파일에서 가져옵니다(도달한 단계, 날짜, 지금까지 협상이 진행된 양상). 각 오퍼에 해당 `application` 라벨을 붙입니다
- 리스크 비교(시나리오별 리스크, 마감 압박이 평가 순서에 영향)
- 궤적 정합성 섹션(`career_trajectory_v1`이 있으면 연결)
- 솔직한 추천 순위:
  - 하나가 명백히 우월하면: 1위로 매기고 이유를 설명합니다
  - 정말 근소하면: 결정적 차이를 만들 상위 1–2개 요소를 짚고 사용자가 결정하게 합니다

### 6. 협상 핸드오프 안내
선호하는 오퍼가 시장 수준보다 낮거나 협상 여지가 있으면:
> `/careerloop:negotiate-offer`를 실행하여 바로 보낼 수 있는 역제안/요청안을 작성해 보세요.

협상이 필요 없을 가능성이 높으면:
> 문구나 타이밍을 다듬고 싶을 때만 `/careerloop:negotiate-offer`를 실행하세요.

### 7. 결과 제시
채팅에 보고서를 제시합니다.

