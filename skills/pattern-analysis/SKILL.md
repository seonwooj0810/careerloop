---
name: pattern-analysis
description: >
  지원 결과 데이터를 분석해 무엇이 효과가 있고 무엇이 없는지 찾아냅니다.
  트래커 이력과 아티팩트 성과를 교차 분석해 ExperienceLibrary 가중치를 갱신하고
  search_performance 신호를 도출합니다. analyst 에이전트를 호출합니다.
  (Analyzes application outcome data to find what's working and what isn't.
  Cross-references tracker history with artifact performance to update ExperienceLibrary
  weights and surface search_performance signals. Invokes the analyst agent.)
triggers:
  - "analyze my search"
  - "what's working in my search"
  - "analyze my applications"
  - "what patterns do you see"
  - "update my weights"
  - "how is my search going"
  - "what's converting"
  - "where am I getting stuck"
  - "내 구직 활동 분석해줘"
  - "내 구직에서 통하는 게 뭐야"
  - "지원 패턴 분석해줘"
  - "어떤 패턴이 보여"
  - "가중치 업데이트해줘"
  - "구직 어떻게 되고 있어"
  - "뭐가 전환되고 있어"
  - "어디서 막히고 있어"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

`analyst` 에이전트를 호출해 사용자의 지원 이력에 대한 결과 패턴 분석을 실행합니다.

## 워크플로

### 1. 데이터 존재 확인

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분리(split) 레이아웃을 사용합니다. 읽기나 쓰기 전에 반드시 이 문서를 읽습니다.

`{user_dir}/CareerLoop/tracker.json`을 읽습니다. 임계값 확인은 요약 행의 `outcome` 필드만으로 수행하며, 아직 상세 파일은 열지 않습니다. `applications` 배열이 비어 있거나, 결과가 확정된(phone_screen, interview, offer, rejected, inactive) 항목이 3건 미만이면 다음과 같이 안내합니다.

> "아직 패턴 분석을 할 만큼 결과 데이터가 충분하지 않습니다. 결과가 확정된 지원 건이 최소 몇 건은 필요합니다. `/careerloop:track-application`으로 업데이트를 계속 기록한 뒤, 이력이 더 쌓이면 다시 실행해 주세요."

그렇지 않으면 계속 진행합니다.

### 2. 전체 이력 로드

이 분석에는 단계 이력과 노트 텍스트가 필요하며, **`tracker.json`만으로는 둘 다 알 수 없습니다.** `stage_history[]`와 `notes[]`는 지원 건별 상세 파일로 옮겨졌습니다. `tracker.json`만으로 전환율, 이탈, 타임라인 패턴을 계산하면 조용히 0이 산출되어, 패턴이 있는데도 "발견된 패턴 없음"이라고 보고하게 됩니다.

1. `{user_dir}/CareerLoop/tracker.json`을 읽고 `applications[]`를 가져옵니다.
2. 모든 행을 순회하며 각 행의 `detail_file`(`CareerLoop/` 기준 상대 경로)을 로드해 해당 지원 건의 `stage_history[]`와 `notes[]`를 가져옵니다. `stage_count`와 `notes_count`가 둘 다 `0`인 행만 건너뜁니다.
3. 요약 필드가 이미 답을 제공하는 경우(현재 단계 `latest_stage`, 마지막 단계 변경일 `latest_stage_date`, 건수 `stage_count`, `notes_count`, `contact_count`)에는 상세 파일에서 다시 계산하지 말고 그 값을 사용합니다.

### 3. analyst 호출 — Operation 1

`analyst` 에이전트에게 다음을 전달합니다.
- `CareerLoop/tracker.json`(요약 행) **그리고** 로드한 `applications/<application_id>.json` 상세 파일. 둘 다 전달하며, 요약 행만으로는 이 작업의 입력으로 충분하지 않습니다
- 전체 `artifacts-index.json`
- 전체 `CareerLoop/ExperienceLibrary.json`

에이전트는 다음을 수행합니다.
- 아티팩트 성과와 지원 결과를 교차 분석
- 변형본 성과, 경험 단위 성과, 직무/시장 적합도, 타임라인의 패턴 식별
- `CareerLoop/ExperienceLibrary.json`의 `performance_weights` 갱신
- 변경마다 `weight_update_log` 항목 기록
- `tracker.json`에 `search_performance` 요약 기록(최상위 키이며, 어떤 상세 파일에도 기록하지 않음)

### 4. 갱신 내용 확인

에이전트가 완료되면 변경된 내용을 보고합니다.

```
패턴 분석 완료.

ExperienceLibrary 가중치 갱신
  {n}개 단위 상향  — {직무명, 간단한 근거}
  {n}개 단위 하향  — {직무명, 간단한 근거}
  {n}개 단위 변경 없음  (데이터 부족)

tracker.json에 검색 성과 요약 기록
  전환율이 높은 직무 유형: {목록}
  전환율이 높은 산업:      {목록}
  피해야 할 신호:          {목록}

데이터 신뢰도: {Preliminary / Directional / Moderate / High} (결과가 있는 지원 {n}건)
```

데이터 부족으로 일부 단위의 가중치를 갱신하지 못했다면 그 사실을 알립니다. 이 안내를 생략하지 않습니다. 데이터셋이 너무 작아 변경을 뒷받침하지 못한다는 점을 사용자가 알아야 합니다.

### 5. 다음 단계 제안

> "`/careerloop:report`로 전체 analyst 리포트를 확인하거나, `/careerloop:tailor-resume`로 갱신된 가중치를 다음 이력서에 반영해 보세요."
