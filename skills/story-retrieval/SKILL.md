---
name: story-retrieval
description: >
  면접 준비 및 모의 면접 워크플로를 위해 CareerLoop/StoryCorpus.json에서 역량과 잘 맞는 소수의 면접 스토리만
  가져옵니다. 적합도가 가장 높은 스토리만 반환하므로, 원본 저널 전체를 불러오지 않고도 모델이 STAR 답변으로 확장할 수
  있습니다. 다음과 같은 요청에 사용합니다: "retrieve interview stories", "find stories for this interview",
  "story retrieval", "pull stories for competency", "면접 스토리 찾아줘", "이 면접에 쓸 스토리 가져와줘".
  (Retrieves a small, competency-matched subset of interview stories from
  CareerLoop/StoryCorpus.json for prep and mock interview workflows.
  Returns only the highest-fit stories so the model can expand into STAR
  responses without loading full raw journals.)
triggers:
  - "retrieve interview stories"
  - "find stories for this interview"
  - "story retrieval"
  - "pull stories for competency"
  - "면접 스토리 찾아줘"
  - "이 면접에 쓸 스토리 가져와줘"
  - "스토리 검색"
  - "역량별 스토리 불러와줘"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

면접에 바로 쓸 수 있도록 영구 스토리 코퍼스에서 목적에 맞는 스토리를 선별합니다.

## 워크플로

### 1. `{user_dir}` 확인 및 게이트

`{user_dir}/CareerLoop/StoryCorpus.json`이 필요합니다.

파일이 없거나 비어 있으면:
- 먼저 `mine-stories`를 실행하도록 안내합니다(적절하다면 사용자 승인을 받아 지금 바로 실행).
- 사용자가 바로 진행하길 원할 때만 `ExperienceLibrary.json`만으로 신뢰도를 낮춘 대체 경로로 계속 진행합니다.

### 2. 검색 의도 구성

사용 가능한 면접 맥락을 활용합니다.
- `application_id` 또는 `company` + `role`
- `interview_stage`
- JD 텍스트 (있는 경우)
- 사용자가 밝힌 중점 영역 (리더십, 갈등, 모호성, 기술 깊이 등)

이번 면접에 맞는 목표 역량/테마를 도출합니다.

### 3. 스토리 순위 매기기

코퍼스의 각 스토리를 다음 기준으로 점수화합니다.
- 역량 일치도
- 테마 일치도
- 단계 관련성 (예: 임원 면접 -> 전략/영향력, 기술 면접 -> 아키텍처/디버깅)
- 품질 신호 (명확성/구체성/신뢰성)
- 결과 + 주도성(ownership) 신호
- 최신성/다양성 (거의 같은 스토리 10개를 반환하지 않도록 함)

### 4. 간결한 컨텍스트 세트 반환 (Layer 3)

소수의 스토리만 반환합니다.
- 기본: 8-12개
- 짧은 준비: 5-8개
- 심층 준비: 사용자가 명시적으로 요청하면 최대 15개

각 항목은 다음과 같이 출력합니다.
- `story_id`
- 한 줄 `raw_summary`
- 매핑된 역량/테마
- 이번 면접에 선택한 이유
- STAR 준비 상태 (`star_ready`)
- STAR 공백이 있으면 짧은 코칭 메모

### 5. 선택적 STAR 승격

STAR 필드가 불완전한 상위 스토리에 대해:
- 간결한 STAR 골격을 작성합니다
- S/T/A/R이 각각 구체적이고 근거가 뒷받침될 때만 `star_ready: true`로 설정합니다
- 업데이트를 `StoryCorpus.json`에 다시 씁니다

### 6. interview-coach 핸드오프 계약

prep/mock 플로우에서 호출될 때는 간결한 핸드오프 페이로드를 제공합니다.

```json
{
  "retrieval_context": {
    "company": "...",
    "role": "...",
    "interview_stage": "..."
  },
  "selected_stories": [
    {
      "story_id": "...",
      "summary": "...",
      "competencies": ["..."],
      "themes": ["..."],
      "star_ready": true
    }
  ]
}
```

이 페이로드는 `interview-coach`가 우선적으로 사용하는 면접 근거 입력입니다.
