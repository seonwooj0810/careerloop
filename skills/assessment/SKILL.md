---
name: assessment
description: >
  `honest-advisor` 에이전트의 norm/exception/strategy 패턴을 사용해, 사용자의 목표 직무
  요건에 대한 솔직하고 근거 기반의 평가와 격차 분석을 제공합니다.
  (Provides a candid, evidence-based assessment and gap analysis against the
  user's target role requirements using the `honest-advisor` agent's
  norm/exception/strategy pattern.)
triggers:
  - "assessment"
  - "role readiness"
  - "gap analysis"
  - "what gaps do I have"
  - "am I qualified"
  - "honest assessment"
  - "how competitive am I for"
  - "do I meet the requirements"
  - "솔직한 평가"
  - "직무 준비도"
  - "갭 분석"
  - "내게 부족한 점이 뭐야"
  - "내가 자격이 될까"
  - "이 직무에 얼마나 경쟁력 있어"
  - "요건을 충족하고 있나"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

`honest-advisor` 에이전트를 호출해 norm/exception/strategy 평가를 실행한 뒤, 결과를 사용자의 목표 직무 요건 대비 격차 분석으로 제시합니다.

## 워크플로

### 1. 데이터 존재 확인

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분리(split) 레이아웃을 사용합니다. 읽기나 쓰기 전에 반드시 이 문서를 읽습니다.

`{user_dir}/CareerLoop/profile.md`를 읽습니다. `target_roles`(또는 이에 상응하는 목표 직무 필드)가 없으면:

> "평가를 실행하려면 목표 직무가 필요합니다. `/careerloop:launch`를 실행하거나 `CareerLoop/profile.md`를 업데이트해 주세요."

`{user_dir}/CareerLoop/ExperienceLibrary.json`을 읽습니다. ExperienceLibrary의 `units` 배열이 비어 있으면:

> "ExperienceLibrary가 비어 있습니다. 먼저 `/careerloop:add-source`로 이력서를 추가해 주세요."

근거 기반이 얼마나 탄탄한지 추정하기 위해 `{user_dir}/CareerLoop/tracker.json`을 선택적으로 읽을 수 있습니다. 요약 행의 `outcome` 필드로 확정된 결과를 집계하며, 이를 위해 `detail_file`은 열지 않습니다. 확정된 결과가 5건 미만이면 신뢰도는 `Preliminary`일 것으로 예상합니다.

### 2. honest-advisor 호출 — 평가 + 격차 분석

`CareerLoop/profile.md`의 각 목표 직무마다 `honest-advisor` 에이전트에게 다음을 전달합니다.

- 해당 직무의 `target_role_type`
- `target_level`(프로필에 있으면 그 값, 없으면 직무명에서 추론)
- `target_geography`(프로필 기준, 원격/전국이면 "Remote (national pool)"로 처리)
- 지시: "Treat your `EXCEPTIONS` as the concrete gaps vs. the target requirements in `CareerLoop/profile.md`. Explicitly map each exception back to which requirement(s) are most likely under-covered (ATS relevance, narrative/seniority fit, or targeting)."

목표 직무가 여러 개이면 직무별로 순차 실행하고 각 섹션에 라벨을 붙입니다.

### 3. 격차 분석 제시

에이전트 출력을 다음과 같이 렌더링합니다.

```
**평가 (격차 분석)** — {Target Role}
신뢰도: {Preliminary/Directional/Moderate/High} (확정된 결과 {resolved_outcomes}건)

목표 요건 (프로필 기준):
- {요건 1}
- {요건 2}

근거 기반 격차:
1. {exception 제목 + 편차 방향}
   - 영향: {이로 인해 약해질 가능성이 높은 요건}
   - 근거: {트래커/아티팩트/ExperienceLibrary 근거 인용}
2. ...

리포지셔닝 계획:
즉시 보완:
- ...

파이프라인 조정:
- ...

복리 투자:
- ...

신뢰도를 높이려면:
- ...
```

간결하게 유지합니다. 직무당 요건은 최대 3~4개, 격차는 2~4개입니다.

### 4. 다음 단계 제안

가장 영향이 큰 격차를 기준으로 합니다.

- ATS/관련성 격차인 경우: 가장 약한 아티팩트에 `/careerloop:resume-score` 또는 `/careerloop:ats-optimization`을 제안합니다.
- 타기팅 exception(직무/회사 불일치)인 경우: 다듬어진 직무 프레이밍으로 `/careerloop:search-jobs`를 제안합니다.
- 서사/연차 exception인 경우: `/careerloop:tailor-resume`를 제안하고, 이어서 `/careerloop:cover-letter`를 제안합니다.
- 교육 ROI 격차인 경우: 해당 추천을 계획으로 삼고 1~2회 지원 사이클 후 결과를 기록하도록 제안합니다.
