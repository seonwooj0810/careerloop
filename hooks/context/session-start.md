# CareerLoop — 세션 시작

이 세션에서 **CareerLoop** 플러그인이 활성화되어 있습니다.

**권장:** 중요 알림만 즉시 받고 싶다면 `skills/focus-career/SKILL.md`에 정의된 그대로 **`focus-career`** 스킬을 실행합니다.

우선순위 규칙(중요): 사용자가 **`/careerloop:launch`**를 실행 중이거나(또는 현재 작업이 명백히 launch/설정 워크플로인 경우) `focus-career`를 자동으로 실행하지 **않고** `launch`를 진행합니다.

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분할 레이아웃을 사용합니다. 읽기나 쓰기 전에 반드시 이 문서를 먼저 읽습니다.

- `{user_dir}`(사용자의 구직 폴더 — Cowork에서 첨부한 워크스페이스 또는 폴더인 경우가 많음)를 확인합니다.
- `CareerLoop/` 데이터가 없으면 해당 스킬의 최초 실행 온보딩을 제공합니다.
- 그렇지 않으면 `CareerLoop/tracker.json`을 읽고 **중요 알림만** 표시합니다. 임박한 오퍼 마감, 오늘(또는 몇 시간 내) 도래하는 후속 조치, 즉시 확인이 필요한 당일 면접 관련 조치가 해당합니다. 이 모든 항목은 **요약 행만으로** 답합니다 — `status`, `follow_up_date`, `latest_stage`, `latest_stage_date`, `notes_count`는 행에 들어 있습니다. 세션 시작은 가볍게 유지해야 하므로 모든 `applications/<application_id>.json`이나 `contacts/<company-slug>.json`을 순회하지 않습니다.

여기서 전체 **`daily-schedule`** 다이제스트는 실행하지 **않습니다** — 이 스킬은 Cowork **`/schedule`**(일간 주기)을 통한 **사용자 예약** 실행용입니다.
