---
name: focus-career
description: "사용자가 세션을 시작하거나 Cowork에서 설정한 주기로 이 스킬을 실행할 때, 중요하고 시간에 민감한 알림만 보여줍니다. 일상적인 요약은 daily-schedule의 몫입니다. Surfaces only critical, time-sensitive notifications when the user begins a session or runs this skill on a cadence they configured in Cowork. Routine summaries belong in daily-schedule."
triggers:
  - "careerloop critical alerts"
  - "any urgent job search deadlines"
  - "critical application alerts"
  - "session start job search"
  - "focus career"
  - "/careerloop:focus-career"
  - "/focus-career"
  - "start a new session with careerloop"
  - "커리어 긴급 알림"
  - "급한 구직 마감 있어"
  - "중요 지원 알림"
  - "세션 시작 구직 점검"
  - "커리어 포커스"
---

사용자가 CareerLoop로 새 Cowork 세션을 열 때, **또는** Cowork **`/schedule`**로 이 스킬을 예약해 둔 경우(선택 사항 — 더 촘촘한 선제적 긴급 점검용)에 실행합니다.

**호스트 연동(선택):** 기본으로 등록된 훅은 없습니다. 사용자가 `SessionStart` 훅에서 `scripts/load-context.sh`를 실행하도록 등록하면 `hooks/context/session-start.md`가 주입되어 세션 시작 시 이 워크플로가 명시적으로 요청됩니다. 사용자가 해당 훅 없이 이 스킬을 수동으로 호출하면 아래 단계를 동일하게 따릅니다.

**수동 폴백:** `SessionStart` 훅이 안정적으로 자동 실행되지 않는 환경에서는 작업/세션 시작 시 `/careerloop:focus-career`를 실행합니다.

이 스킬은 `daily-schedule`의 **긴급 전용** 짝입니다. 일일 다이제스트를 대체하지 **않습니다.**

## 워크플로

### 1. `{user_dir}` 및 핵심 파일 찾기

현재 작업 디렉터리와 사용자가 제공한 경로를 확인합니다. 이를 `{user_dir}`로 사용합니다.

다음을 확인합니다.
- `{user_dir}/CareerLoop/profile.md`
- `{user_dir}/CareerLoop/ExperienceLibrary.json`
- `{user_dir}/CareerLoop/tracker.json`
- `{user_dir}/CareerLoop/artifacts-index.json`

없으면 첫 실행으로 간주하고 다음을 출력합니다.

> **CareerLoop에 오신 것을 환영합니다**
>
> `/careerloop:launch`를 실행하여 `CareerLoop` 데이터 파일을 초기화하고 자동화를 활성화하세요.

### 2. 재방문 세션: 긴급 항목만 점검

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분리 레이아웃을 사용합니다. 읽기/쓰기 전에 반드시 이 문서를 읽습니다.

`{user_dir}/CareerLoop/tracker.json`을 읽습니다. 아래 점검 1과 2는 **요약 행만으로**(`status`, `offer.deadline`, `follow_up_date`, `latest_stage`, `latest_stage_date`, `notes_count`) 판단할 수 있고, 점검 3만 상세 파일을 열며 그마저 이미 해당 조건에 부합하는 지원 건에 한합니다. 이 스킬은 가볍게 유지해야 하므로 모든 `applications/<application_id>.json`을 훑지 않습니다.

**긴급** 알림만 표시합니다.

1. **임박한 오퍼 마감**
   - `status: "offer"`이고 `offer.deadline`이 향후 24시간 이내인 지원 건.
   - 해당 지원 건에 `{user_dir}/CareerLoop/offer-context-{application_id}.json`이
     없으면, 긴급 사유를 다음과 같이 표기합니다.
     "Offer evaluation due (run `/careerloop:evaluate-offer`)."

2. **임박한 후속 조치 마감**
   - `follow_up_date`가 오늘인 지원 건.
   - 현지 시각이 하루의 마지막 6시간 이내이면 긴급 "몇 시간 후 마감"으로 표시합니다.

3. **오늘 일정이 있는데 준비 기록이 없음**
   - `daily-schedule` **§3.1**의 **meeting-today** 규칙과 동일하게 요약 행에 대해 실행합니다. **`latest_stage_date` = 오늘**이고 **`latest_stage`**(대소문자 무시)에 `interview`, `recruiter`, `phone screen`, `phone_screen`, `hiring manager`, `hm `, `hm interview`, `technical`, `panel`, `onsite`, `executive`, `final round`, `final interview` 중 하나가 포함되면 해당 행이 조건에 부합합니다. `stage_count: 0`인 행은 건너뜁니다. `latest_stage_date`가 **오늘보다 이후**인 행은 `detail_file`을 읽어 `stage_history[]`에서 오늘 날짜의 허용 목록 일치 항목을 찾습니다(미래 날짜로 예약된 단계가 오늘 행을 가립니다).
   - 조건에 부합하는 각 지원 건에 대해 상세 파일에서 **준비가 기록되었는지** 판단합니다. 행의 `notes_count`가 `0`이면 노트가 전혀 없으므로 준비가 기록되지 않은 것으로 보고 읽기를 건너뜁니다. 그렇지 않으면 `{user_dir}/CareerLoop/` + `detail_file`을 읽고 **최근 48시간** 내 `notes[]` 항목 중 `text`가 **`[prep]`**로 시작하는 것이 있는지 확인합니다(`notes[]`는 더 이상 `tracker.json`에 없습니다).
   - 오늘 일정이 있고 48시간 내 조건에 맞는 **`[prep]`** 노트가 **없으면** → **긴급**(당일 브리프 + 심층 준비 제안).

여기서는 전체 파이프라인 다이제스트, 기한 초과 요약, 아티팩트 개수를 출력하지 **않습니다.** 그것들은 `daily-schedule`의 몫입니다.

### 3. 출력 형식

긴급 항목이 없으면:
> **CareerLoop — 세션 시작**: 지금은 긴급 알림이 없습니다.

긴급 항목이 있으면:
```
**CareerLoop — 긴급 알림** [{today}]

- {Company} — {Role}: {긴급 사유} ({남은 시간})
- {Company} — {Role}: {긴급 사유} ({남은 시간})
```

알림을 나열한 뒤 실행 안내 한 줄을 덧붙입니다.
> 다음 단계를 갱신하려면 `/careerloop:track-application` 또는 `/careerloop:follow-up`을 실행하세요. 당일 면접은 `/careerloop:daily-schedule`(면접 전 하위 섹션)과 전체 준비를 위한 `/careerloop:prep-interview`를 사용하세요(오퍼 평가 마감 항목이 나타났다면 `/careerloop:evaluate-offer`).
