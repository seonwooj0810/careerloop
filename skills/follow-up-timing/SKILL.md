---
name: follow-up-timing
description: >
  트래커 상태를 바탕으로 오퍼 평가와 후속 조치 시점을 알려주는 상시 알림입니다.
  활성 오퍼가 있는데 OfferContext가 아직 만들어지지 않았다면 사용자에게
  evaluate-offer 실행을 안내합니다. 트리거 예: "offer evaluation due",
  "i have an offer", "offer deadline", "offer evaluation" (오퍼 평가 시점,
  오퍼를 받았어요, 오퍼 마감일, 오퍼 평가).
triggers:
  - "offer evaluation due"
  - "i have an offer"
  - "offer deadline"
  - "offer evaluation"
  - "/careerloop:follow-up-timing"
  - "오퍼 평가 필요"
  - "오퍼를 받았어요"
  - "오퍼 마감일"
  - "오퍼 마감이 언제야"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

`follow-up-timing`을 실행하면 트래커를 바탕으로 짧은 시점 알림을 받습니다.
- 오퍼 평가 필요: 트래커의 지원(건)에 `status: "offer"`가 있는데
  `{user_dir}/CareerLoop/offer-context-{application_id}.json` 파일이
  아직 없을 때.

## 워크플로

### 1. 트래커와 필수 파일 로드

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분할 레이아웃을 사용합니다. 읽기·쓰기 전에 반드시 이 문서를 먼저 읽습니다.

읽을 파일:
- `{user_dir}/CareerLoop/tracker.json`

파일이 없으면:
> follow-up-timing을 건너뜁니다. `/careerloop:launch`를 실행해 주세요.

이 스킬은 상시 알림이므로 비용이 낮아야 합니다. 필요한 모든 필드(`id`, `company`,
`role`, `status`, `offer.deadline`, `follow_up_date`, `latest_stage`,
`latest_stage_date`)는 `tracker.json`의 요약 행에 있습니다. 이 스킬에서는
`applications/<application_id>.json`이나 `contacts/<company-slug>.json`을 절대 열지 않습니다.

### 2. 오퍼 평가 확인
`tracker.json` → `applications[]`의 각 요약 행 중 다음 조건에 해당하는 항목을 확인합니다.
- `status`가 `"offer"`
- `offer.deadline`이 설정되어 있을 수 있음(있는 경우)
- 그리고 `{user_dir}/CareerLoop/offer-context-{id}.json`이
  없음(행의 `id`를 사용하며, 저장된 컨텍스트 파일이 이전 id를 쓰고 있다면
  평가가 누락되었다고 판단하기 전에 행의 `previous_ids`를 확인)

행의 `application` 레이블을 그대로 사용해 짧은 안내를 출력합니다.
> {application}의 오퍼 평가가 필요합니다. `/careerloop:evaluate-offer`를 실행해 주세요.

### 3. 출력 형식
오퍼 평가가 필요한 항목이 없으면:
> 대기 중인 오퍼 평가가 없습니다.
