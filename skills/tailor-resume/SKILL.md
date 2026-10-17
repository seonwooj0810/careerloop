---
name: tailor-resume
description: >
  특정 직무에 맞춰 ExperienceLibrary에서 최적화된 resume를 조립하고, ATS
  호환성을 점수화한 뒤 아티팩트 인벤토리에 저장한다. 사용자가 job description을
  공유하거나 붙여넣거나, 특정 직무에 지원하려는 의사를 밝히면 자동으로
  작동한다. /careerloop:tailor-resume로도 호출할 수 있다.
triggers:
  - "tailor my resume"
  - "tailor resume for"
  - "customize my resume"
  - "optimize my resume for"
  - "/tailor-resume"
  - "I want to apply to"
  - "I'm applying to"
  - "help me apply for"
  - "write a resume for"
  - "build a resume for"
  - "here's the job description"
  - "here's a JD"
  - "I found a job posting"
  - "이력서 맞춤화"
  - "이력서 맞춰줘"
  - "이 공고에 맞게 이력서"
  - "이 직무에 지원하려고"
  - "채용공고 올려줄게"
  - "지원용 이력서 만들어줘"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

특정 직무에 가장 잘 맞는 resume를 사용자의 ExperienceLibrary에서 조립한다. 작업은 `resume-coach` 에이전트를 호출해 맡긴다.

## 워크플로

### 1. 입력 수집

**Job description** — 필수. 사용자가 제공하지 않았으면:
> "job description을 붙여넣어 주시면 그에 맞춰 resume를 맞춤화하겠습니다."

**JD를 정본(canonical source)과 대조한다 — 항상.** `resume-coach`에 무엇이든 넘기기 전에, 해당 회사의 자체 채용 페이지나 ATS(Greenhouse, Lever, Ashby, Workday, SmartRecruiters)에서 공고를 가져온다. 어그리게이터 목록 — Indeed, LinkedIn, Ladders, ZipRecruiter, Jobgether, BuiltIn — 은 잘려 있거나, 오래됐거나, 문구가 바뀐 경우가 잦고, `recommendations.json`에 저장된 `job_link`도 그런 곳을 가리킬 수 있다.

정본 공고를 찾는 방법: `{Company} {Role} careers` 또는 `{Company} greenhouse OR lever OR ashby {Role}`을 검색한 뒤 가져온다. 어그리게이터 링크가 단축 링크(예: `to.indeed.com/...`)면 대개 쓸 만한 텍스트로 해석되지 않는다 — 가져오기를 재시도하지 말고 실제 공고를 찾아간다.

그런 다음 정본 JD를 사용자나 `recommendations.json`이 제공한 내용과 대조하고, **resume를 만들기 전에 모든 모순을 사용자에게 알린다.** 담백하게 보고한다:

> "{source}의 전체 JD가 보관 중인 공고와 다릅니다: {모순}. 이로 인해 {바뀌는 것}이(가) 달라집니다. 정본 기준으로 진행할까요?"

타기팅을 바꾸거나 직무를 부적합하게 만들기 때문에 가장 중요한 모순:

- **인력 관리 범위** — "PM 팀을 이끈다" 대 IC/개별 기여자 프레이밍
- **시니어리티 또는 직함** — Director 대 Senior PM 대 Principal
- **근무지와 근무 형태** — 출근/하이브리드/원격, 그리고 어느 사무실인지
- **보상 구간** — 특히 급여 투명성 공시가 정본 공고에만 있는 경우
- **필수 요건** — 학위 조건, 경력 연수, 보안 인가, 취업 자격
- **필수 지원 서류** — 어그리게이터가 통째로 빼먹는 에세이, 작업 샘플, 포트폴리오, 과제

모순이 원래의 적합성 근거를 무효로 만들면 그렇다고 직접 말하고, `recommendations.json`에 저장된 `fit_signals`나 `gaps`를 바로잡는다 — 틀린 신호가 트래커까지 남게 두지 않는다. 정본 공고를 찾거나 가져올 수 없으면, 조용히 진행하지 말고 JD가 검증되지 않았음을 사용자에게 알리고 구체적인 위험을 밝힌다.

**목표 직무와 회사** — 명시되지 않았으면 정본 JD에서 추출한다.

**ExperienceLibrary** — `{user_dir}/CareerLoop/ExperienceLibrary.json`을 읽는다. 파일이 없거나 `units` 배열이 비어 있으면:
> "ExperienceLibrary가 비어 있습니다. 먼저 `/careerloop:add-source`를 실행해 resume를 추가하세요. 그러면 이 직무에 맞춰 만들어 드릴 수 있습니다."

**프로필** — 차별점, 스킬, 목표 선호도를 위해 `{user_dir}/CareerLoop/profile.md`를 읽는다. 이미 프로필에 있는 것은 사용자에게 묻지 않는다.

### 2. resume-coach 호출

다음을 갖춰 `resume-coach` 에이전트에 넘긴다:
- job description 전체 텍스트
- ExperienceLibrary 전체(`CareerLoop/ExperienceLibrary.json`)
- 사용자 프로필(`CareerLoop/profile.md`)
- 사용자가 제공한 특별 지시(강조, 제외, 어조)

`resume-coach`가 하는 일:
- `performance_weights`를 사용해 가장 관련 있는 경력 단위를 선택한다
- 대상 직무에 맞게 조립하고 다시 쓴다
- JD 용어는 ExperienceLibrary가 뒷받침하는 곳에서만 쓴다. 뒷받침되지 않는 요건은 공백으로 나열한다(ATS를 통과하려고 키워드를 끼워 넣는 일은 절대 없다)
- 완성된 resume 텍스트와 ATS 점수를 돌려준다

**목소리를 맞춘 Summary(선택):** 사용자가 **Summary만** 자신의 **LinkedIn 목소리** / **`voice-profile.md`**에 맞추길 명시적으로 요청하면, `resume-coach`에 `agents/resume-coach/AGENT.md`에 따른 **ResumeSummaryBrief**를 요청한다. **`writer`**를 호출하기 **전에** **`draft-outreach`**와 같은 **voice preflight**를 수행한다(**`## User writing samples`** / **`## User writing samples (launch)`**를 요청하거나 **건너뛰기**). 그런 다음 **`resume-summary`** 모드로 **`writer`**를 호출하고, 돌려받은 **## Summary**를 초안에 대입한 뒤 아래 ATS 제시 단계로 이어간다.

### 3. 점수와 검토

저장하기 전에 `resume-coach`가 돌려준 전체 평가를 보여준다:

```
{Company}의 {Role}용 resume 조립 완료
JD 출처: {canonical URL} {(보관 중인 공고와 대조 완료 | 모순 발견 — 아래 참조)}

ATS 점수: {n}/100
키워드 커버리지: 필수 키워드 {total_required}개 중 {matched_keywords}개 일치

JD 모순 (없으면 이 블록은 생략)
- {보관 중인 공고의 내용} → {정본 JD의 실제 내용} → {바뀌는 것}

강점
- {이 직무에 대해 ExperienceLibrary가 잘 덮는 것}

공백 (솔직하게)
- {ExperienceLibrary 커버리지가 없거나 약한 요건}
- {수치나 보강이 필요한 성과}
```

점수가 70 미만이면 저장하기 전에 묻는다:
> "이 resume의 ATS 점수는 {n}/100입니다. 주요 공백은 {keywords}입니다. 저장하기 전에 이를 보완할까요?"

공백을 보완한다는 것은 뒷받침되는 근거를 드러내거나 사용자에게 사실을 묻는다는 뜻이다. 키워드를 끼워 넣는다는 뜻이 아니다.

콘텐츠 규칙은 프로젝트 지침(AGENTS.md / CLAUDE.md)이 이 스킬보다 우선한다.

### 4. 아티팩트 저장

사용자가 확인하면(또는 점수가 70 이상이고 지적된 공백이 없으면) resume를 저장한다:

**파일명(호스트 / MCP 검증 오류 방지):** **ASCII 안전** 이름만 쓴다—하이픈 `-`을 쓰고 em dash나 스마트 따옴표는 쓰지 않는다. 회사와 직무는 **정리한다**: `\ / : * ? " < > |`와 줄바꿈을 제거하고, 공백을 하나로 합치고, 기본 이름은 길이를 제한한다(~100자).
**예시:** `Anthropic-PM-Claude-Code-Resume-2026-03-24.md`

- **파일명 형식:** `{SanitizedCompany}-{SanitizedRole}-Resume-{YYYY-MM-DD}.md`
- **경로**: `{user_dir}/`
- **`{user_dir}/CareerLoop/artifacts-index.json`에 기록**:

```json
{
  "id": "{uuid}",
  "type": "resume",
  "filename": "{filename}",
  "path": "{user_dir}/{filename}",
  "target_company": "{company}",
  "target_role": "{role}",
  "date_created": "{today}",
  "source": "generated",
  "ats_score": {n},
  "source_units": ["{unit_ids used}"],
  "jd_keywords": ["{keywords matched}"],
  "jd_source_url": "{canonical careers-page or ATS URL the JD was verified against}",
  "notes": "{record any JD contradictions found during verification}"
}
```

`{user_dir}`에 다른 아티팩트 파일(PDF/DOCX)이 있으면, 저장한 뒤 **`artifact-saved`** 워크플로를 한 번 실행해 `artifacts-index.json`이 디스크와 어긋나지 않게 한다.

사용자에게 확인한다:
> "**{filename}**으로 저장했습니다. `/careerloop:cover-letter`를 실행하면 이에 맞는 커버레터를 생성합니다."

### 5. 다음 단계 제안

사용자가 이 직무의 지원을 아직 기록하지 않았다면 제안한다:
> "이 지원을 트래커에 추가할까요? '네'라고 하시거나 지원 정보를 알려주세요."
