---
name: suggest-roles
description: >
  전이 가능한 강점과 시장 상황을 바탕으로 눈에 띄지 않는 직무 기회를 제안합니다.
  honest-advisor와 market-researcher를 호출한 뒤, job-scout 스코어링 개선에 쓸
  결과 중심의 직무 신호를 기록합니다.
  (Suggests non-obvious role opportunities based on transferable strengths and
  market conditions. Invokes honest-advisor and market-researcher, then writes
  outcome-driven role signals for job-scout scoring improvements.)
triggers:
  - "suggest roles"
  - "what roles should i target"
  - "non-obvious roles for me"
  - "what else could i apply to"
  - "role pivot suggestions"
  - "/careerloop:suggest-roles"
  - "직무 추천"
  - "어떤 직무를 목표로 해야 할까"
  - "의외의 직무 추천해줘"
  - "또 어디에 지원할 수 있을까"
  - "직무 전환 제안"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

> **경력 연수 인용 규칙:** 경력·도메인 연수를 말할 때는 ExperienceLibrary의 날짜로 직접 계산한 값을 쓴다. 이력서나 프로필의 표기가 계산값과 다르면 계산값을 쓰고 불일치를 한 줄로 알린다(예: 이력서 "5년" ↔ 날짜상 4년 7개월).

`honest-advisor`와 `market-researcher`를 모두 호출해 직무 제안을 생성하고, `job-scout` 랭킹을 개선할 실행 가능한 신호를 기록합니다.

중요한 호출 규칙:
- 에이전트 이름 `honest-advisor`와 `market-researcher`를 정확히 그대로 사용합니다.
- 에이전트 유형을 임의로 만들거나 별칭을 쓰지 않습니다(예: "career-assessment"나 "market-analysis" 에이전트 유형을 호출하지 않음).
- 어느 한쪽 에이전트 호출이 실패하면 오류를 반환하기 전에 위의 정확한 이름으로 한 번 재시도합니다.

## 워크플로

### 1. 데이터 존재 확인

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분리(split) 레이아웃을 사용합니다. 읽기나 쓰기 전에 반드시 이 문서를 읽습니다.

다음을 읽습니다.
- `{user_dir}/CareerLoop/profile.md`
- `{user_dir}/CareerLoop/ExperienceLibrary.json`

프로필에 목표 직무가 없으면:
> "먼저 현재 목표 직무가 필요합니다. 직무 제안을 실행하기 전에 `/careerloop:launch`를 실행하거나 `CareerLoop/profile.md`를 업데이트해 주세요."

ExperienceLibrary의 `units`가 비어 있으면:
> "ExperienceLibrary가 비어 있습니다. 직무 제안을 실행하기 전에 `/careerloop:add-source`로 이력서를 추가해 주세요."

신뢰도와 결과 맥락을 위해 `{user_dir}/CareerLoop/tracker.json`을 선택적으로 읽을 수 있습니다. 요약 행으로 충분하며, 행마다 `outcome`, `latest_stage`, `latest_stage_date`만 있으면 되므로 `detail_file`은 열지 않습니다.

### 2. advisor 패스 실행 (경쟁력 + 전이 가능 적합도)

사용자의 주요 목표 직무에 대해 `honest-advisor`를 `assessment` 모드로 호출합니다. 다음을 요청합니다.
- 충족도가 낮은 요건 식별
- 사용자의 가장 강한 신호가 더 경쟁력 있는 인접 직무 변형 식별
- 근거와 함께 후보 직무 3~6개 반환

### 3. 시장 패스 실행 (수요 + 대체 + 지역)

같은 직무 집합과 지역에 대해 `market-researcher`를 호출합니다. 다음을 요청합니다.
- 후보 직무별 수요 상태 분류(rising/stable/softening)
- 대체(displacement) 위험 상태 표시
- 지역별 경쟁력 제약/기회 식별

### 4. 제안 종합

두 결과를 합쳐 순위가 매겨진 직무 목록을 만듭니다.
- 전이 가능 적합도가 강하고 **동시에** 수요 상태가 우호적인 직무를 우선
- 적합도가 약하거나, 수요가 약화되거나, 지역 불일치가 심한 직무는 순위 하향
- 근거가 뒷받침하면 "도전적이지만 현실성 있는" 옵션을 최소 하나 포함

### 5. job-scout 스코어링 신호 기록

`{user_dir}/CareerLoop/tracker.json`에 `strategy_signals` 객체를 기록합니다(없으면 생성). `strategy_signals`는 `tracker.json`의 최상위 키이며 분리(split)의 영향을 받지 않으므로 상세 파일이나 연락처 파일에는 기록하지 않습니다.

```json
{
  "strategy_signals": {
    "as_of": "YYYY-MM-DD",
    "recommended_role_types": ["..."],
    "adjacent_role_types": ["..."],
    "deprioritize_role_types": ["..."],
    "market_tailwinds": ["..."],
    "market_headwinds": ["..."],
    "preferred_geographies": ["..."],
    "avoid_geographies": ["..."],
    "signal_confidence": "Preliminary | Directional | Moderate | High",
    "source": ["honest-advisor", "market-researcher"]
  }
}
```

이 신호는 `job-scout`가 랭킹을 개선하는 데 사용합니다.

### 6. 결과 제시

형식:

```
**제안 직무** — {오늘 날짜}
신뢰도: {등급}

상위 직무 기회
1. {직무}
   - 적합한 이유: {전이 가능 적합도 근거}
   - 시장 신호: {수요/지역/대체 요약}
2. ...

당분간 후순위로 둘 직무
- {직무}: {이유}

Job-scout 업데이트
- 기록한 추천 직무 유형: {목록}
- 기록한 후순위 직무 유형: {목록}
- 기록한 지역 신호: {목록}
```

### 7. 다음 단계 제안

제시한 후:
- 갱신된 직무/지역 전략 신호로 랭킹을 실행하도록 `/careerloop:search-jobs`를 제안합니다.
- 상위 제안 직무에 대해 `/careerloop:tailor-resume`를 제안합니다.

실패 시 대체 처리:
- 재시도 후에도 한 에이전트가 계속 실패하면, 성공한 에이전트의 출력으로 계속 진행하고 부분 완료 상태임을 명확히 표시하며, 실패한 에이전트의 정확한 이름을 사용자에게 알립니다.
