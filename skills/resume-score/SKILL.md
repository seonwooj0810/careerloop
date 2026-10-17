---
name: resume-score
description: >
  resume를 job description에 대해 ATS 키워드 일치, 서식 준수, 서사 강도 기준으로
  점수화한다. 사용자가 tailoring을 명시적으로 요청하지 않고 resume와 job
  description을 함께 공유하거나, 점수를 명시적으로 요청할 때 작동한다.
  /careerloop:resume-score로도 호출할 수 있다.
triggers:
  - "/resume-score"
  - "score my resume"
  - "score this resume"
  - "how does my resume score"
  - "check my resume against"
  - "rate my resume"
  - "evaluate my resume"
  - "ATS score"
  - "how does this resume match"
  - "resume check"
  - "how well does my resume match"
  - "이력서 점수"
  - "이력서 점수 매겨줘"
  - "이력서 평가해줘"
  - "ATS 점수"
  - "이력서가 공고와 얼마나 맞는지"
  - "이력서 채점"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

resume를 job description에 대해 점수화한다. 솔직해야 한다. 낮은 점수는 완곡하게 돌려 말할 대상이 아니라 유용한 정보다.

콘텐츠 규칙은 프로젝트 지침(AGENTS.md / CLAUDE.md)이 이 스킬보다 우선한다. resume가 이미 뒷받침하지 않는 키워드, 수치, 주장은 추가하라고 권하지 않는다.

점수화 분석은 `resume-coach` 에이전트를 호출해 수행한다.

## 워크플로

### 1. 입력 수집

**Resume** — 필수. 다음을 받는다.
- `{user_dir}`에 있는 기존 문서의 파일 경로
- `CareerLoop/artifacts-index.json`의 아티팩트 이름(파일명으로 조회)
- 대화에 직접 붙여넣은 내용

**Job description** — 필수. 제공되지 않았으면:
> "점수를 매길 job description을 붙여넣어 주세요."

사용자가 JD 없이 resume만 제공했고 맥락에 진행 중인 직무가 있으면(예: 최근 `search-jobs` 결과나 트래커 항목), 이렇게 묻는다:
> "어떤 job description에 대해 점수를 매길까요?"

### 2. resume-coach 호출

분석을 위해 resume 텍스트와 JD를 `resume-coach`에 전달한다. 에이전트가 ATS 호환성, 서사 강도, 전략적 적합성 평가 기준을 적용해 차원별 점수를 돌려준다.

### 3. 점수 제시

```
**Resume Score** — {Resume filename} vs. {Company/Role or "제공된 JD"}

종합: {n}/100

ATS 호환성    {n}/40
  {키워드 일치 수, 서식 지적 사항, 각 한 줄}

서사 강도  {n}/35
  {솔직한 평가 2–3문장: 성과의 질, Summary 관련성, 시니어리티 신호}

전략적 적합성       {n}/25
  {1–2문장: 직무 정합성과 차별점 가시성}

---
보완할 주요 공백
1. {누락된 키워드 또는 구조적 문제} — {왜 중요한가}
2. ...
3. ...
```

공백 목록은 5개로 제한한다. ATS 통과율에 미치는 영향을 먼저, 서사를 그다음 순서로 정렬한다.

### 4. 다음 단계 제안

점수를 보여준 뒤 이렇게 제안한다:
> "이 직무에 맞춰 resume 새 버전을 만들어 드릴까요? `/careerloop:tailor-resume`를 실행하거나 '맞춤화해줘'라고 말씀해 주세요."

tailoring을 자동으로 실행하지 않는다. 점수화와 tailoring은 별개의 작업이다. 사용자가 결정하게 한다.
