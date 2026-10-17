---
name: ai-analysis
description: >
  Anthropic Economic Index를 사용해 사용자의 현재 직무와 목표 직무에 대한 AI 및 자동화 대체 위험을
  업무(task) 단위로 평가합니다. 오래 가치를 유지하는 차별화 요소를 찾고, 사용자의 포지셔닝이
  위험도가 높은 업무에 치우쳐 있으면 내러티브 재구성을 제안합니다. analyst 에이전트를 호출합니다.
  Evaluates AI and automation displacement risk for the user's current and
  target roles at the task level, using the Anthropic Economic Index. Triggers on
  "AI displacement", "AI risk", "is my job at risk from AI", "future-proof my career",
  "AI 대체 위험", "내 직업이 AI에 대체될까", "AI 시대에 내 커리어는 안전한가".
triggers:
  - "AI displacement"
  - "AI risk"
  - "is my job at risk from AI"
  - "how AI-proof is my career"
  - "future-proof my career"
  - "what parts of my job will AI replace"
  - "assess AI risk"
  - "AI automation risk"
  - "how durable are my skills"
  - "what's my AI displacement risk"
  - "AI 대체 위험"
  - "AI 위험도 평가"
  - "내 직업이 AI에 대체될까"
  - "내 커리어는 AI 시대에 안전한가"
  - "AI가 대체할 내 업무"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

`analyst` 에이전트를 호출해 사용자의 현재 직무와 목표 직무에 대한 AI 및 자동화 대체 위험을 평가합니다.

## 워크플로

### 1. 데이터 존재 여부 확인

`{user_dir}/CareerLoop/ExperienceLibrary.json`과 `{user_dir}/CareerLoop/profile.md`를 읽습니다. ExperienceLibrary의 `units` 배열이 비어 있거나 `profile.md`에 목표 직무가 없으면 다음과 같이 안내합니다.

> "대체 위험 평가를 실행하려면 ExperienceLibrary와 목표 직무가 필요합니다. `/careerloop:add-source`로 이력서를 추가한 뒤 `/careerloop:launch`로 목표 직무를 설정해 주세요."

그렇지 않으면 다음 단계로 진행합니다.

### 2. analyst 호출 — Operation 3

`analyst` 에이전트에 다음을 전달합니다.
- 전체 `CareerLoop/ExperienceLibrary.json`
- 전체 `CareerLoop/profile.md`
- 분석 전에 Anthropic, “Labor market impacts of AI: A new measure and early evidence” (Massenkoff·McCrory, 2026-03-05, https://www.anthropic.com/research/labor-market-impacts)를 확인하라는 지시(웹 도구로 원문 확인 → 작업 폴더의 PDF → 둘 다 불가하면 수치를 인용하지 말고 “보고서 미확인”을 명시)

에이전트는 사용자의 현재 직무와 목표 직무를 업무 단위로 분해하고, 각 업무를 Economic Index 기준으로 점수화하며, 직무 수준의 위험 프로필을 만들고, 오래 가치를 유지하는 차별화 요소를 찾아 필요한 경우 내러티브 재구성을 제안합니다.

### 3. 평가 결과 제시

```
**AI 대체 위험 평가** — {Role}

{1~2문장 요약: 전체 위험 수준과 가장 앞세워야 할 지속 가능한 차별화 요소 한 가지}

전체 위험 프로필
  대체 위험이 높은 업무:    {n}%  — {예시}
  대체 위험이 중간인 업무:  {n}%  — {예시}
  대체 위험이 낮은 업무:    {n}%  — {예시}

자동화 가능성이 가장 높은 업무 (2~5년 전망)
- {Task} — {Economic Index 데이터상 위험한 이유}

지속 가능한 강점
- {Capability} — {위험이 낮고 앞으로 가치가 커질 가능성이 높은 이유}

내러티브 재구성
{사용자의 포지셔닝이 위험도 높은 업무에 치우쳐 있다면, 이력서 요약·자기소개서·아웃리치에서 지속 가능한 역량 쪽으로 재구성하는 구체적 제안}

함께 키우면 좋은 인접 역량
- {Skill/area} — {사용자의 기존 기반을 고려할 때 전략적으로 가치 있는 이유}

출처: Anthropic Economic Index, {report date}
```

`profile.md`에 목표 직무가 여러 개 있으면 각각 별도로 평가를 실행해 순서대로 제시합니다.

### 4. 다음 단계 제안

> "이 결과를 검색 패턴 및 전이 가능한 강점과 합친 전체 analyst 리포트를 실행할까요? `/careerloop:report`를 실행해 주세요."
