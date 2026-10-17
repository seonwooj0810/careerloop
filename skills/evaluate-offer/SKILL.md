---
name: evaluate-offer
description: >
  채용 오퍼(job offer)를 재직 중/무직 상황별 시나리오에 맞춰 솔직하게 평가합니다. 직무 적합성, 역량 활용도 분석,
  시장 벤치마크 기반 보상 공정성, 협상에 쓸 수 있는 레버리지 포인트를 다루며, 이후 협상/비교 단계에서 쓸 수 있도록
  OfferContext를 저장합니다. 다음과 같은 요청에 사용합니다: "evaluate my job offer", "should i take this offer",
  "offer evaluation", "이 오퍼 평가해줘", "오퍼 받아야 할까?", "오퍼 검토해줘".
  (Provides honest, scenario-aware evaluation of a job offer (employed vs
  unemployed context), including role fit, utilization analysis, compensation
  fairness using market benchmarks, and negotiation-readiness leverage points.
  Persists OfferContext for downstream negotiation/comparison.)
triggers:
  - "evaluate my job offer"
  - "should i take this offer"
  - "offer evaluation"
  - "help me evaluate an offer"
  - "job offer assessment"
  - "/careerloop:evaluate-offer"
  - "오퍼 평가해줘"
  - "이 오퍼 받아야 할까"
  - "오퍼 평가"
  - "오퍼 판단 도와줘"
  - "채용 제안 평가"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

> **경력 연수 인용 규칙:** 경력·도메인 연수를 말할 때는 ExperienceLibrary의 날짜로 직접 계산한 값을 쓴다. 이력서나 프로필의 표기가 계산값과 다르면 계산값을 쓰고 불일치를 한 줄로 알린다(예: 이력서 "5년" ↔ 날짜상 4년 7개월).

`evaluate-offer`를 실행해 솔직한 OfferEvaluationReport를 작성하고, `OfferContext` JSON 파일을 다음 경로에 저장합니다.
`{user_dir}/CareerLoop/offer-context-{application_id}.json`

이후 `negotiate-offer`와 `compare-offers`가 이 파일을 사용할 수 있습니다.

## 워크플로

### 디렉터리 공유 (호스트 연동)
이 스킬을 실행하는 동안 호스트 UI가 **에이전트와 공유할 디렉터리**를 요청하면, `{user_dir}` 구직 폴더(`CareerLoop/`를 포함한 폴더)만 공유합니다.

이 스킬이 읽고 쓰는 파일:
- `{user_dir}/CareerLoop/profile.md`
- `{user_dir}/CareerLoop/ExperienceLibrary.json`
- `{user_dir}/CareerLoop/tracker.json` (요약 행)
- `{user_dir}/CareerLoop/applications/<application_id>.json` (오퍼 지원(건)의 `notes[]` + `stage_history[]`)
- `{user_dir}/CareerLoop/contacts/<company-slug>.json` (해당 회사의 연락처, 리크루터 맥락이 중요할 때)
- `{user_dir}/CareerLoop/offer-context-{application_id}.json`

전체 워크스페이스나 관련 없는 폴더는 공유하지 않습니다.

### 1. 필수 데이터 존재 확인

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분리 레이아웃을 사용합니다. 읽거나 쓰기 전에 반드시 이 문서를 먼저 읽습니다.

읽을 파일:
- `{user_dir}/CareerLoop/profile.md`
- `{user_dir}/CareerLoop/ExperienceLibrary.json`
- `{user_dir}/CareerLoop/tracker.json`

필수 파일이 없으면 다음과 같이 출력합니다.
> 오퍼 평가를 건너뜁니다: `/careerloop:launch`를 실행해 `CareerLoop/`를 초기화하세요.

### 2. 오퍼 단계 지원(건) 식별
`tracker.json` 요약 행에서 다음 조건의 지원(건)을 찾습니다.
- `status`가 `"offer"`

경우별 처리:
- 해당 지원(건)이 정확히 하나면: 그 `id`를 `application_id`로 사용합니다.
- 여러 개면: 회사와 직무(또는 공고 링크/마감일)를 물어 일치하는 지원(건)을 고릅니다.
- 하나도 없으면: 먼저 `/careerloop:track-application`으로 오퍼를 기록하도록 안내합니다.

일치한 행에서 `application`(`"<company> — <role>"` 라벨), `detail_file`, `contacts_file`, `latest_stage`, `latest_stage_date`, `notes_count`, `stage_count`를 유지합니다. 그런 다음 **이 지원(건) 하나**에 대해 `{user_dir}/CareerLoop/` + `detail_file`을 읽습니다. 해당 파일의 `stage_history[]`와 `notes[]`가 평가의 근거가 되는 면접 기록이며, 이 정보는 더 이상 `tracker.json` 안에 없습니다. 다른 지원(건)의 상세 파일은 불러오지 않습니다.

### 3. 시나리오 A/B/C 판정 (사용자에게 직접 밝히게 하지 않음)
다음 시나리오 중 하나로 능동적으로 분류합니다.
- 시나리오 A: 현재 재직 중이며 새 오퍼를 평가하는 경우 (이직 여부 결정)
- 시나리오 B: 현재 무직이며 오퍼를 평가하는 경우 (긴급성 + 생활 자금 여유 기간(runway))
- 시나리오 C: 상황이 불분명한 경우

판단 기준:
- 프로필에 `## Employment Context` 섹션이 있으면:
  - 재직 중이라고 되어 있거나(또는 현재 보상 패키지가 나열돼 있으면): 시나리오 A를 사용합니다.
  - 무직이라고 되어 있거나(또는 실업급여/퇴직금/소득원 + runway가 나열돼 있으면): 시나리오 B를 사용합니다.
  - unknown이라고 되어 있으면: 시나리오 C를 사용합니다.
- 그렇지 않고 §2에서 불러온 상세 파일(`notes[]` 또는 최근 `stage_history[]` 항목)에 재직 상황이 나와 있으면 그것을 사용합니다. (요약 행의 `notes_count: 0`, `stage_count: 0`은 읽을 내용이 없다는 뜻입니다.)
- 그렇지 않고 사용자가 메시지에서 "I have a job"("현재 재직 중입니다") 또는 "I'm between roles"("지금은 쉬는 중입니다")라고 명시했다면 그것을 사용합니다.
- 그래도 불분명하면: A와 B를 가르기 위해 명확화 질문을 딱 하나만 합니다.

### 4. 오퍼 세부 정보 추출/확인
오퍼 필드는 다음 중 한 곳 이상에서 수집합니다.
- 이 `application_id`에 해당하는 요약 행의 스칼라 값(`salary_range`, `offer`, `next_step`, `follow_up_date`)과 §2에서 불러온 상세 파일의 `notes[]` / `stage_history[]`에 기록된 오퍼 조건
- 사용자의 메시지 (부족한 부분)

가능하면 추출할 필드:
- 기본급, 보너스, 지분(equity), 복리후생 메모
- 마감일(`offer.deadline`)과 의사결정 시점

핵심 정보(예: 마감일, 보상 전반)를 알 수 없으면 빠진 항목만 질문합니다.

### 5. 시장 벤치마크 확인 (보상 공정성)
**`market-researcher`**에게 다음 조건의 보상 벤치마크를 요청합니다.
- 직무 + 레벨 (프로필과 직무명에서 추론)
- 지역 범위 (프로필의 위치 사용)
- 회사 유형 (오퍼/회사 정보에서 추론)

에이전트에게 줄 지침: 이 호스트에서 실시간 보상 조회 도구를 쓸 수 없다면, 보수적이면서 현지 기준에 근거한 벤치마크를 만들고 신뢰도를 표기합니다.

또한 벤치마크에 `unknown`/누락된 범위 값이 있거나 신뢰도가 High가 아니면, 추출한 직무와 지역으로 `/careerloop:salary-research`를 통해 데이터를 가져오는 방법을 다음 단계로 반드시 명시적으로 제안해야 합니다(Claude Desktop에서는 Apify 커넥터가 필요할 수 있다는 점도 함께 안내).

### 6. 솔직한 평가 종합 + 레버리지 포인트
**`honest-advisor`**에게 다음 내용을 담은 **OfferEvaluationReport**를 작성하도록 넘깁니다.
- 직무 적합성 평가 (커리어 궤적상 전진/수평 이동/후퇴)
- 학력/자격증/ExperienceLibrary 단위의 활용도 분석
- 보상 공정성 판정 (시장 대비 낮음/비슷함/높음)
- 시나리오별 리스크 평가 (이직 리스크 vs runway 압박)
- 직접적인 권고: 수락 / 거절 / 협상 / 구직 계속

보고서에는 중앙값을 웃도는 요구를 뒷받침하는 명시적 레버리지 포인트(자격, 성과, ExperienceLibrary 단위)가 반드시 포함돼야 합니다.

`honest-advisor`에게 다음을 지시합니다.
- **OfferEvaluationReport** 출력 구조를 따릅니다.
- “What would make this more reliable”(이 섹션 제목은 영문 그대로 사용)에서, 벤치마크/시장 데이터가 빠져 있다면 신뢰도 주의 문구와 함께 가능한 최선의 벤치마크 값을 제시하거나, 다음 명령으로 데이터를 가져오는 다음 단계를 명시적으로 제안합니다.
  - `/careerloop:salary-research` (직무 + 지역)
  - 선택적으로 `/careerloop:market-brief` (수요/AI 전망)

### 7. `OfferContext` JSON 저장
다음 경로에 씁니다.
`{user_dir}/CareerLoop/offer-context-{application_id}.json`

`OfferContext`는 분리 레이아웃 **밖**에 있습니다. 이를 쓰는 작업은 트래커 파일을 건드리지 않으므로 이 단계만으로는 트랜잭션이 필요하지 않습니다.

스키마 요구사항 (최소 필드, 필요하면 더 추가):
```json
{
  "schema": "offer_context_v1",
  "as_of": "{YYYY-MM-DD}",
  "application_id": "{application_id}",
  "company": "{company}",
  "role": "{role}",
  "scenario": "A|B|C",
  "offer_details": {
    "base": "...",
    "bonus": "...",
    "equity": "...",
    "benefits_notes": "...",
    "deadline": "YYYY-MM-DD|null"
  },
  "compensation_benchmark": {
    "currency": "USD|...",
    "percentile_or_range": "...",
    "market_range": { "low": "...", "median": "...", "high": "..." },
    "confidence": "Preliminary|Directional|Moderate|High",
    "notes": "..."
  },
  "leverage_points": [
    { "rank": 1, "claim": "...", "evidence": "ExperienceLibrary/profile references" }
  ],
  "evaluation_summary": "short 3–6 lines",
  "fairness_verdict": "below_market|at_market|above_market|borderline",
  "recommendation": "accept|decline|negotiate|continue_searching"
}
```

디스크 쓰기에 실패하면:
- 저장된 것처럼 꾸미지 않습니다.
- OfferEvaluationReport와 OfferContext JSON을 코드 블록으로 보여주고, 위 경로에 직접 저장하도록 사용자에게 안내합니다.

### 7.5 평가 결과를 지원(건)에 기록 (사용자가 요청한 경우에만)
사용자가 평가 결과, 확보한 마감일, 상태 변경을 기록하길 원하면 [references/tracker-schema.md](../../references/tracker-schema.md)의 **다중 파일 트랜잭션**으로 씁니다. 한 파일만 수정하고 나머지를 건너뛰어서는 안 됩니다.

- **노트:** 상세 파일의 `notes[]`에 `{ "date": "YYYY-MM-DD", "text": "[offer] evaluation: {verdict} — {recommendation}" }`를 추가한 뒤, 요약 행의 `notes_count`를 새 배열 길이로 설정합니다.
- **단계:** 오퍼 자체가 새 단계라면 상세 파일의 `stage_history[]`에 추가한 뒤, 요약 행의 `stage_count`, `latest_stage`, `latest_stage_date`, `status`를 설정합니다.
- **오퍼 스칼라 값**(`offer.deadline`, `salary_range`, `next_step`, `follow_up_date`)은 요약 행에 그대로 둡니다.

각 파일을 프로그램으로 불러와 다시 덤프하고(`json.load` / `json.dump`, `indent=2`, `ensure_ascii=False`), 다시 읽어 `notes_count` / `stage_count`가 배열과 일치하는지, `latest_stage`가 `stage_history`의 마지막 항목과 일치하는지 검증합니다.

### 8. 다음 단계로 안내
보고서가 협상이 적절하다고 판단하면 사용자에게 다음과 같이 안내합니다.
> `/careerloop:negotiate-offer`를 실행해 바로 보낼 수 있는 협상 메시지를 작성하세요.

보상 벤치마크가 없거나 불완전했다면 다음도 안내합니다.
> 더 정확한 수치가 필요하면 이 직무 + 지역으로 `/careerloop:salary-research`를 실행하세요. 가져온 벤치마크로 평가를 다시 실행해 드립니다.

오퍼 단계의 진행 중인 지원(건)이 여러 개면 다음도 안내합니다.
> `/careerloop:compare-offers`를 실행해 나란히 비교 평가하세요.

### 9. 결과 제시
대화형 OfferEvaluationReport를 제시하고 다음과 같이 확인합니다.
> OfferContext를 `{user_dir}/CareerLoop/offer-context-{application_id}.json`에 저장했습니다.

