---
name: add-source
description: >
  이력서, CV, 포트폴리오 문서를 ExperienceLibrary에 반영합니다.
  구조화된 경험 단위를 추출해 CareerLoop/ExperienceLibrary.json에 병합합니다.
  사용자가 새 소스 문서를 업로드하거나 언급하면 실행됩니다.
  /careerloop:add-source로도 호출할 수 있습니다.
  (Ingests a resume, CV, or portfolio document into the ExperienceLibrary.
  Extracts structured experience units and merges them into CareerLoop/ExperienceLibrary.json.
  Fires when the user uploads or references a new source document. Also
  invocable via /careerloop:add-source.)
triggers:
  - "add this resume"
  - "add my resume"
  - "add this CV"
  - "ingest this document"
  - "add to my ExperienceLibrary"
  - "add a source"
  - "/add-source"
  - "here's my resume"
  - "upload my resume"
  - "I have a new resume"
  - "I have another resume"
  - "add this to the ExperienceLibrary"
  - "이력서 추가해줘"
  - "이 이력서 추가해줘"
  - "이 CV 추가해줘"
  - "이 문서 가져와줘"
  - "경험 라이브러리에 추가해줘"
  - "새 이력서가 있어요"
  - "이력서 올릴게요"
  - "다른 이력서도 있어요"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

소스 문서에서 구조화된 경험 단위를 추출해 사용자의 ExperienceLibrary에 병합합니다.

## 워크플로

### 1. 소스 문서 식별

**사용자가 파일 경로를 제공했거나 문서를 업로드한 경우** — 그대로 사용합니다.

**맥락에 문서가 없는 경우** 다음과 같이 묻습니다.
> "어떤 파일을 추가할까요? 경로를 알려 주시거나 내용을 직접 붙여 넣어 주세요."

지원 형식: PDF, DOCX, TXT, MD, 일반 텍스트 붙여넣기.

### 2. 현재 ExperienceLibrary 읽기

`{user_dir}/CareerLoop/ExperienceLibrary.json`을 읽고 다음을 파악합니다.
- 기존 단위 ID(충돌 방지)
- 기존 회사와 직무(중복 감지)

파일이 없으면 진행하기 전에 빈 `units` 배열로 생성합니다.

### 3. 경험 단위 추출

소스 문서를 전부 읽습니다. 각 직무, 학력 항목, 출판물, 수상 또는 인정 사례마다 구조화된 단위를 추출합니다.

```json
{
  "id": "exp-{next_available_number}",
  "type": "role",
  "company": "...",
  "title": "...",
  "dates": "...",
  "summary": "1–2 sentence description of scope and context",
  "achievements": [
    {
      "id": "exp-{n}-a1",
      "theme": "impact | leadership | technical | commercial | operational",
      "text": "exact achievement text, preserved from source"
    }
  ],
  "skills": ["skill1", "skill2"],
  "performance_weight": 0.5,
  "source_document": "{filename of source}"
}
```

**추출 규칙:**
- 성과(achievement) 텍스트는 작성된 그대로 보존합니다. ingest 시점에 다듬거나 개선하지 않습니다. 맞춤화는 이력서 조립 단계에서 이루어집니다.
- 각 성과가 주로 보여 주는 바에 따라 `theme`을 지정합니다.
- 스킬은 나타난 그대로 추출합니다. 대소문자는 정규화하되 기술 이름을 바꾸거나 합치지 않습니다.
- 모든 새 단위의 `performance_weight`는 0.5(중립)로 설정합니다. analyst 에이전트가 결과를 바탕으로 가중치를 조정합니다.

### 4. 중복 확인

추가하기 전에 추출한 각 단위를 기존 ExperienceLibrary 항목과 대조합니다.
- 같은 회사 + 기간 겹침 = 중복 가능성 높음
- 중복 가능성이 있는 항목을 발견하면 사용자에게 알립니다.
> "ExperienceLibrary에 {Company}의 {Role}({dates}) 항목이 이미 있습니다. 교체할까요, 성과를 병합할까요, 아니면 별도 항목으로 추가할까요?"

### 5. ExperienceLibrary에 병합

새 단위를 `CareerLoop/ExperienceLibrary.json`의 `units` 배열에 추가합니다. `meta.updated` 필드를 오늘 날짜로 갱신합니다.

소스 문서가 `artifacts-index.json`에 아직 없다면 함께 추가합니다.

```json
{
  "id": "{uuid}",
  "type": "resume",
  "filename": "{filename}",
  "path": "{full path}",
  "target_company": null,
  "target_role": null,
  "date_created": "{file date or today}",
  "source": "existing",
  "notes": "Source document added to ExperienceLibrary"
}
```

### 6. 확인

```
ExperienceLibrary에 추가됨: {filename}에서 경험 단위 {n}개
  {Company}의 {Role} ({dates})
  {Company}의 {Role} ({dates})
  ...

ExperienceLibrary 전체: 단위 {total unit count}개
```

중복을 병합하거나 건너뛴 경우 그 내용을 같은 자리에서 알립니다. 확인 메시지는 간결하게 유지합니다.
