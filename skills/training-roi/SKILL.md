---
name: training-roi
description: >
  자격증, 학위, 부트캠프, 독학 전반에 걸쳐 비용-효과-시간 ROI 분석으로 학습 투자를
  추천합니다. honest-advisor 에이전트를 training-roi 모드로 호출합니다.
  (Recommends learning investments using a cost-benefit-time ROI analysis across
  certifications, degrees, bootcamps, and self-study. Invokes the
  honest-advisor agent in training-roi mode.)
triggers:
  - "training roi"
  - "learning roi"
  - "what should i learn next"
  - "is a bootcamp worth it"
  - "is a certification worth it"
  - "should i get a degree"
  - "upskilling plan"
  - "best training path for my target role"
  - "교육 ROI"
  - "학습 ROI"
  - "다음에 뭘 배워야 할까"
  - "부트캠프 가치 있어"
  - "자격증 딸 가치 있어"
  - "학위를 따야 할까"
  - "역량 개발 계획"
  - "내 목표 직무에 맞는 교육 경로"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

`honest-advisor`를 `training-roi` 모드로 호출해 학습 옵션을 비교하고, 사용자의 목표 직무에 가장 ROI가 높은 경로를 추천합니다.

## 워크플로

### 1. 기본 맥락 확인

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분리(split) 레이아웃을 사용합니다. 읽기나 쓰기 전에 반드시 이 문서를 읽습니다.

다음을 읽습니다.
- `{user_dir}/CareerLoop/profile.md`
- `{user_dir}/CareerLoop/ExperienceLibrary.json`

목표 직무가 없으면:
> "교육 ROI 분석을 실행하려면 목표 직무가 필요합니다. 먼저 `/careerloop:launch`를 실행하거나 `CareerLoop/profile.md`를 업데이트해 주세요."

ExperienceLibrary `units`가 없거나 비어 있으면:
> "학습 ROI를 추정하려면 ExperienceLibrary가 필요합니다. 먼저 `/careerloop:add-source`로 이력서를 추가해 주세요."

신뢰도와 병목 맥락을 위해 `{user_dir}/CareerLoop/tracker.json`을 선택적으로 읽을 수 있습니다. 이 스킬에 필요한 정보는 요약 행에 모두 들어 있습니다. `status`, `outcome`, `latest_stage`, `latest_stage_date`로 지원이 어디서 정체되는지 알 수 있으므로 `detail_file`은 열지 않습니다.

### 2. 선택적 제약 조건 수집

대화에서 아직 제공되지 않았다면 한 번만 질문합니다.
> "특정 예산과 기간에 맞춰 최적화할까요? 그렇다면 최대 예산과 희망 기간을 알려 주세요(예: '300만 원, 4개월')."

사용자가 제약 조건을 제공하지 않아도 계속 진행합니다.

### 3. honest-advisor 호출 — training-roi 모드

각 목표 직무(또는 명시적으로 요청된 직무)마다 `honest-advisor`에게 다음을 전달합니다.
- `analysis_mode: training-roi`
- `target_role_type`
- `target_level`(알고 있거나 추론한 경우)
- `target_geography`
- `time_horizon_months`(제공된 경우, 없으면 기본값 12)
- `budget_range`(제공된 경우)

지시:
- 자격증, 학위, 부트캠프, 독학을 비교합니다.
- ROI 점수가 포함된 비용-효과-시간 옵션 매트릭스를 작성합니다.
- 주 경로와 대체 경로를 추천합니다.
- 명시적 가정과 데이터 공백을 포함합니다.

### 4. 추천 엔진 출력 제시

다음과 같이 렌더링합니다.

```
**교육 ROI 분석** — {Target Role}
기간: {n개월}
예산: {값 또는 "제공되지 않음"}
신뢰도: {Preliminary / Directional / Moderate / High}

주요 역량 격차
1. ...
2. ...

옵션 매트릭스 (비용-효과-시간)
| 경로 | 유형 | 예상 비용 | 예상 기간 | 신호 강도 | ROI 점수 | 주요 리스크 |
|---|---|---|---|---|---:|---|
| ... |

추천 계획
- 주 경로: ...
- 대체 경로: ...
- 첫 30일: ...
- 만들어야 할 증빙 아티팩트: ...

가정과 데이터 공백
- ...
```

이 사용자에게 유료 경로가 독학보다 ROI가 낮다면 그 점을 직접 밝히고 이유를 설명합니다.

### 5. 다음 단계 제안

제시한 후:
- 첫 마일스톤 이후 경쟁력을 다시 점검하도록 `/careerloop:assessment`를 제안합니다.
- 증빙 아티팩트를 만들면 `/careerloop:tailor-resume`를 제안합니다.
