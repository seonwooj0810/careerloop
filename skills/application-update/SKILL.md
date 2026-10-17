---
name: application-update
description: "트래커 기록이 변경될 때마다 실행됩니다. 결과(outcome)의 최신성을 재점검하고, job-scout 신호를 갱신해야 하는지 표시하며, 확정된 결과가 주요 마일스톤에 도달하면 pattern-analysis 실행을 권유합니다. Runs whenever tracker records change. Re-checks outcome freshness, flags when job-scout signals should be refreshed, and triggers pattern-analysis nudges at key resolved-outcome milestones."
triggers:
  - "application update"
  - "after I logged an application"
  - "tracker updated"
  - "just updated my application tracker"
  - "after track application"
  - "지원 업데이트"
  - "지원 기록 후 갱신"
  - "트래커 업데이트했어요"
  - "방금 지원 트래커를 갱신했어요"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

`track-application` 스킬이 `{user_dir}/CareerLoop/tracker.json`을 쓰거나 갱신한 **직후**(같은 대화 턴) 실행합니다. 별도의 플러그인 훅 파일은 없으며, 오케스트레이션은 대화형이거나 호스트가 정의합니다.

## 워크플로

### 1. 트래커 상태 읽기

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분리 레이아웃을 사용합니다. 읽기/쓰기 전에 반드시 이 문서를 읽습니다.

`{user_dir}/CareerLoop/tracker.json`을 읽고 **요약 행만** 확인합니다.
- 최근 지원 건 업데이트 — `status`, `latest_stage`, `latest_stage_date`와
  `notes_count` / `stage_count` / `contact_count` 카운터만으로 상세 파일을 하나도 열지 않고도 무엇이 바뀌었는지 알 수 있습니다
- `outcome` 분포
- `search_performance`가 존재하는지, `as_of`가 있는지

여기서는 `applications/<application_id>.json`이나 `contacts/<company-slug>.json`을 훑지 않습니다.
**§1.5**의 특정 지원 건 일관성 점검이 실패해 기저 배열을 확인해야 할 때만 상세 파일 하나를 엽니다.

### 1.5 방금 실행된 쓰기 검증

`track-application`은 **다중 파일 트랜잭션**을 기록합니다. 무엇이든 조언하기 전에, 방금 변경된 지원 건에 대해 트랜잭션이 완료되었는지 확인합니다.
- 행의 `detail_file`이 `{user_dir}/CareerLoop/` 아래에서 해석되는지
- `notes_count`와 `stage_count`가 상세 파일의 `notes[]`와 `stage_history[]` 길이와 같은지
- `latest_stage`와 `latest_stage_date`가 `stage_history`의 **마지막** 항목과 일치하는지
- 행에 `contacts_file`이 있다면, `contact_count`가 해당 파일에서 `application`이 행의 `application` 라벨과 같은 항목 수와 일치하는지

점검이 실패하면 어느 파일의 어느 필드가 동기화되지 않았는지 정확히 말하고, 사용자에게 해당 지원 건에 대해 `/careerloop:track-application`을 다시 실행하라고 안내합니다. 복구는 [references/tracker-schema.md](../../references/tracker-schema.md)의 쓰기 규칙에 따라서만 수행합니다. 상세 파일과 연락처 파일에서 카운터를 다시 계산하고 영향받는 모든 파일을 같은 패스에서 기록하며, `tracker.json`만 단독으로 패치하지 않습니다.

### 2. 갱신 필요 여부 판단

변경 유형에 따라 갱신 안내를 설정합니다.
- 최종 결과(`hired`, `rejected`, `withdrew`)가 바뀌었다면 **high-priority refresh**로 표시합니다
- 최종 결과 없이 단계/상태가 바뀌었다면 **standard refresh**로 표시합니다
- 점수에 영향을 주는 필드가 바뀌지 않았다면 **no refresh needed**로 표시합니다

### 3. analyst 갱신을 위한 마일스톤 권유

확정된 결과(`outcome != "pending"`)의 수를 셉니다. 개수가 다음에 해당하면:
- `5`, `10`, `15`, 또는 `10`의 배수: `/careerloop:pattern-analysis` 실행 권유를 덧붙입니다

`search_performance.as_of`가 14일보다 오래되었고 새 결과가 기록되었다면 다음을 덧붙입니다.
> 마지막 점수 갱신 이후 결과 데이터가 변경되었습니다. `/careerloop:pattern-analysis`를 실행하여 job-scout 가중치를 업데이트하세요.

### 4. 출력 형식

짧게 유지합니다.
```
지원 업데이트를 처리했습니다.
갱신: {high-priority | standard | none}
확정된 결과: {n}건
{선택: 한 줄 권유}
```

## 가드레일

- 이 워크플로에서 지원 기록을 덮어쓰지 않습니다. 이 스킬은 자문/오케스트레이션 전용입니다. 유일한 예외는 §1.5의 일관성 복구로, 카운터를 다시 계산하며 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 전체 다중 파일 트랜잭션(트래커 행, 상세 파일, 연락처 파일을 함께)으로 기록해야 합니다
- 이 JSON 파일을 손으로 편집하지 않습니다. 프로그램적으로 로드하고 다시 덤프(`json.load` / `json.dump`, `indent=2`, `ensure_ascii=False`)한 뒤 다시 로드하여 검증합니다
- analyst/pattern-analysis가 실제로 실행되지 않았다면 가중치가 갱신되었다고 주장하지 않습니다
- 출력은 간결하고 실행 지향적으로 유지합니다
