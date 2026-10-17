---
name: skill-transfer
description: >
  사용자의 ExperienceLibrary에서 핵심 이전 가능 역량을 식별하고, 현재 트랙을 넘어서는
  직무 유형과 산업에 매핑합니다. 뻔하지 않은 진로 방향을 제시하고, 도메인 의존적
  강점과 이식 가능한 강점을 구분해 표시합니다. analyst 에이전트를 호출합니다.
  트리거 예: "what are my transferable skills", "where else could I work",
  "what roles could I transition to", "what industries could I move into",
  "career pivot analysis" (내 이전 가능 역량은, 다른 어디서 일할 수 있을까, 어떤 직무로 전환할 수 있을까, 커리어 전환 분석).
triggers:
  - "what are my transferable skills"
  - "where else could I work"
  - "what roles could I transition to"
  - "what industries could I move into"
  - "analyze my transferable strengths"
  - "what are my core strengths"
  - "where do my skills apply"
  - "career pivot analysis"
  - "what could I do besides"
  - "내가 가진 전이 가능한 역량이 뭐야"
  - "다른 곳에서 일할 수 있을까"
  - "어떤 직무로 옮길 수 있어"
  - "어떤 산업으로 이동할 수 있어"
  - "내 핵심 강점 분석해줘"
  - "내 역량이 어디에 쓰일까"
  - "커리어 전환 분석"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

`analyst` 에이전트를 호출해 사용자의 이전 가능 강점을 식별하고 새로운 진로 방향에 매핑합니다.

## 워크플로

### 1. 데이터 존재 확인

`{user_dir}/CareerLoop/ExperienceLibrary.json`과 `{user_dir}/CareerLoop/profile.md`를 읽습니다. ExperienceLibrary의 `units` 배열이 비어 있으면:

> "ExperienceLibrary가 비어 있습니다. 먼저 `/careerloop:add-source`를 실행해 이력서를 추가해 주세요."

그렇지 않으면 계속 진행합니다.

### 2. analyst 호출 — Operation 2

다음 항목과 함께 `analyst` 에이전트에 넘깁니다.
- 전체 `CareerLoop/ExperienceLibrary.json`
- 전체 `CareerLoop/profile.md`

에이전트는 핵심 역량, 그 이전 가능한 형태, 그리고 사용자가 고려하지 못했을 수 있는 방향을 포함해 가치가 높게 평가되는 직무 유형과 산업을 식별합니다.

### 3. 분석 결과 제시

```
**이전 가능 강점 분석**

{1–2문장 하이라이트: 가장 설득력 있거나 놀라운 강점 발견 하나 — 서론 없이 역량부터 제시}

식별된 핵심 역량
1. {역량 이름} — {근거가 보여주는 내용 1문장 설명}
   근거: {이 역량을 보여주는 구체적인 역할/성과}
   가치가 높은 진로: {이 역량이 높이 평가되는 직무 유형과 산업}

2. ...

산업 간 이식 가능
{최소한의 재포지셔닝으로 폭넓게 이전되는 강점}

도메인 의존적
{가치는 있지만 이전하려면 특정 맥락이나 자격이 필요한 강점}

뻔하지 않은 기회
{사용자가 고려하지 못했을 가능성이 큰 직무 유형이나 산업과 구체적 근거}
```

### 4. 다음 단계 제안

> "이 강점 중 어떤 것이 가장 오래 유지될지 확인하기 위해 AI 대체 가능성 평가를 실행해 볼까요? `/careerloop:ai-analysis`를 실행해 주세요."
