---
name: list-artifacts
description: >
  아티팩트 인벤토리에 있는 모든 생성 아티팩트를 메타데이터와 함께 나열합니다. 유형,
  생성일, 목표 직무와 회사, 가능한 경우 ATS 점수, 알려진 경우 연결된 지원 결과를 보여 줍니다.
  사용자가 생성한 문서나 아티팩트 이력을 보여 달라고 할 때 실행됩니다.
  /careerloop:list-artifacts로도 호출할 수 있습니다.
  (Lists all generated artifacts in the artifact inventory with metadata: type,
  date created, target role and company, ATS score if available, and linked
  application outcome if known. Fires when the user asks to see their generated
  documents or artifact history. Also invocable via /careerloop:list-artifacts.)
triggers:
  - "list my artifacts"
  - "show my artifacts"
  - "what have I generated"
  - "what resumes have I created"
  - "show my resumes"
  - "list my cover letters"
  - "what documents have I made"
  - "show my generated documents"
  - "what's in my artifact inventory"
  - "what have I created"
  - "/list-artifacts"
  - "내 아티팩트 목록"
  - "아티팩트 보여줘"
  - "내가 뭘 만들었지"
  - "내가 만든 이력서 보여줘"
  - "내 자기소개서 목록"
  - "생성한 문서 보여줘"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

사용자의 아티팩트 인벤토리를 읽기 쉬운 형식으로 표시합니다.

## 워크플로

### 1. 인벤토리 읽기

`{user_dir}/CareerLoop/artifacts-index.json`을 읽습니다. 파일이 없거나 `artifacts` 배열이 비어 있으면:
> "아직 아티팩트가 없습니다. 이력서는 `/careerloop:tailor-resume`를 실행하고, LinkedIn 초안을 디스크에 저장하려면 `/careerloop:content-suggest`를 실행한 뒤 전체 게시글 초안을 요청해 주세요."

### 2. 트래커와 교차 확인

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분리(split) 레이아웃을 사용합니다. 읽기나 쓰기 전에 반드시 이 문서를 읽습니다.

`{user_dir}/CareerLoop/tracker.json`을 읽습니다. 각 아티팩트가 요약 행의 `artifacts[]` 배열에 나타나는지 확인합니다. 나타나면 해당 행의 현재 `status`, `application` 라벨(`"<company> — <role>"`), `outcome`을 기록합니다. 이를 통해 사용자는 어떤 이력서와 자기소개서가 진행 중인 지원에 연결되어 있고 어떤 결과(있다면)가 나왔는지 알 수 있습니다.

이 목록에 필요한 정보는 요약 행에 모두 들어 있습니다. 여기서는
`applications/<application_id>.json`이나 `contacts/<company-slug>.json`을 열지 **않습니다**. 아티팩트
연결 정보는 행에 있으며, 목록 하나를 출력하려고 모든 지원 건의 상세 파일을 로드하는 것이
바로 분리(split) 레이아웃이 피하려는 일입니다.

### 3. 출력 구성

아티팩트를 유형별로 그룹화합니다. **이력서**를 먼저, 그다음 **자기소개서**, 그다음 **`linkedin_post`**(**`writer`**가 저장한 게시글 초안), 그 외 유형 순입니다. 각 그룹 안에서는 `date_created` 내림차순(최신순)으로 정렬합니다.

**아티팩트별 형식:**

```
{n}. {filename}
   대상:     {Company} — {Role}  (대상이 없으면 "Base / unattached", linkedin_post는 "—" 또는 notes의 주제 사용)
   생성일:   {date_created}
   ATS 점수: {ats_score}/100  (없거나 해당되지 않으면 생략)
   사용처:   {행의 `application` 라벨, status: {status}}  (어떤 지원에도 연결되어 있지 않으면 생략)
```

**`type: "linkedin_post"`**는 ATS를 생략하고 보통 **사용처**도 생략합니다. 사용자가 디스크에서 초안을 찾을 수 있도록 필요하면 **`notes`**나 경로를 표시합니다.

**목록 맨 위의 요약 줄**(목록 앞):

```
아티팩트: 이력서 {total_resume_count}건, 자기소개서 {total_cover_letter_count}건, LinkedIn 게시글 초안 {total_linkedin_post_count}건
```

### 4. 다음 단계 제안

목록 뒤에 현재 상태에 맞는 실행 항목을 보여 줍니다.

- 지원 건에 연결되지 않은 이력서가 있는 경우:
  > "일부 이력서가 아직 지원 건에 연결되어 있지 않습니다. `/careerloop:track-application`을 실행해 기록해 주세요."
- 이력서는 있는데 자기소개서가 없는 직무가 있는 경우:
  > "일부 직무에는 자기소개서가 없습니다. `/careerloop:cover-letter`를 실행해 생성해 주세요."
- 목록이 비어 있는 경우: 이 섹션을 완전히 생략합니다.
