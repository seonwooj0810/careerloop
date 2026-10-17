---
name: mine-stories
description: >
  원본 소스(일지, PKM 노트, 디브리프, 이력서 및 관련 문서)에서 면접 스토리 후보를
  추출해 CareerLoop/StoryCorpus.json을 구축하고 갱신합니다. 일회성/오프라인
  전처리로 실행되며, {user_dir}에서 새 소스 파일이 감지되면 증분 갱신으로도 실행됩니다.
  (Builds and refreshes CareerLoop/StoryCorpus.json by extracting interview
  story candidates from raw sources (journals, PKM notes, debriefs, resumes,
  and related documents). Runs as a one-time/offline preprocessing pass and as
  an incremental refresh when new source files are detected in {user_dir}.)
triggers:
  - "mine stories"
  - "extract interview stories"
  - "build story corpus"
  - "refresh story corpus"
  - "index my journal for interview stories"
  - "update story corpus"
  - "스토리 마이닝"
  - "면접 스토리 추출해줘"
  - "스토리 코퍼스 만들어줘"
  - "스토리 코퍼스 갱신해줘"
  - "일지에서 면접 스토리 색인해줘"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

하위 면접 스킬이 원본 일지를 매번 통째로 다시 읽지 않아도 되도록, 지속적으로 유지되는 면접 스토리 코퍼스를 만들고 관리합니다.

## 워크플로

### 1. `{user_dir}` 및 필수 경로 확인

다음을 사용합니다.
- `{user_dir}/CareerLoop/StoryCorpus.json` (대상 코퍼스)
- `{user_dir}` (원본 소스 탐색 루트)

`StoryCorpus.json`이 없으면 5단계의 스키마로 생성합니다.

### 2. 소스 후보 탐색

`{user_dir}`를 재귀적으로 스캔해 스토리가 담겼을 가능성이 높은 파일을 찾으며, 다음을 우선합니다.
- 일지 및 주간 로그
- 면접 디브리프 노트
- PKM 내보내기/노트(커넥터/MCP 또는 로컬 내보내기로 가능한 경우 Notion 및 Capacities 콘텐츠 포함)
- 이력서/CV/자기소개서 본문
- 날짜별 항목이 있는 일반 텍스트/마크다운 노트

제외 대상:
- `{user_dir}/CareerLoop/*.json`
- 사용자가 직접 작성한 소스 근거가 아닌 생성된 아티팩트
- 파싱할 수 없는 바이너리/미디어 파일

### 3. 증분 작업과 전체 빌드 판별

`StoryCorpus.json`이 이미 있는 경우:
- 소스 경로 + 수정 시각으로 파일 지문(fingerprint) 맵을 만듭니다.
- 이미 처리했고 수정 시각이 변하지 않은 파일은 건너뜁니다.
- 새 파일/변경된 파일만 처리합니다.

이전 코퍼스 메타데이터가 없으면 전체 빌드를 한 번 실행합니다.

### 4. 스토리 후보 추출 (Layer 1)

새로 생겼거나 변경된 소스마다:
1. 자연스러운 항목 경계(날짜, 제목, 섹션, 문단 블록)로 청크를 나눕니다.
2. 다음 의도로 저비용 추출 패스를 실행합니다.
   > "Extract any anecdote, decision, challenge, outcome, or project detail from this entry. Output structured JSON."
3. 원본 소스 청크가 아니라 추출한 후보를 보관합니다.

각 후보에는 다음을 포함해야 합니다.
- 짧은 서술 요약
- 날짜(명시적이거나, 강하게 뒷받침될 때 추론)
- 역량/주제 태그
- 주도성/성과 신호
- 추출 품질에 대한 신뢰도 점수

### 5. `StoryCorpus.json` 작성 / 병합 (Layer 2)

다음 최상위 구조를 사용합니다.

```json
{
  "meta": {
    "created": "YYYY-MM-DD",
    "updated": "YYYY-MM-DD",
    "version": "1.0",
    "description": "Interview story corpus extracted from user-owned sources for prep and mock interview retrieval."
  },
  "stories": [
    {
      "story_id": "story-uuid",
      "source": "journal | pkm | debrief | resume | other",
      "source_path": "relative/path/to/file",
      "source_entry_ref": "date heading or chunk id",
      "date": "YYYY-MM-DD",
      "raw_summary": "Concise evidence summary from extraction.",
      "themes": ["technical_leadership", "crisis_management"],
      "competencies": ["problem_solving", "ownership", "cross_functional"],
      "result_signal": true,
      "ownership_signal": true,
      "star_ready": false,
      "star": {
        "situation": "",
        "task": "",
        "action": "",
        "result": ""
      },
      "quality": {
        "clarity": "low | medium | high",
        "specificity": "low | medium | high",
        "credibility": "low | medium | high"
      },
      "embedding": [],
      "score_hint": 0.0,
      "last_refreshed": "YYYY-MM-DD"
    }
  ],
  "source_index": [
    {
      "path": "relative/path",
      "mtime": "ISO-8601",
      "status": "processed | skipped",
      "last_processed": "ISO-8601"
    }
  ]
}
```

병합 동작:
- 같은 소스 항목을 다시 처리하는 경우 기존 `story_id`를 유지합니다.
- 추출 결과가 개선되었으면 필드를 갱신합니다.
- 새 소스 항목은 새 스토리로 추가합니다.
- 사용자가 명시적으로 삭제를 요청하지 않는 한 아무것도 제거하지 않습니다.

### 6. 압축 및 중복 제거

병합 후:
- 거의 동일한 스토리(같은 사건/결과를 다르게 표현한 것)는 중복 제거합니다.
- 가장 강한 버전(명확성/구체성/신뢰성이 가장 높은 것)을 유지합니다.
- 두 버전이 서로 다른 역량에 유용하다면 관련 스토리 변형으로 표시합니다.

### 7. 출력 + 다음 행동

다음을 보고합니다.
- 스캔한 파일 수
- 새로 처리한 파일 수
- 추가/갱신한 스토리 수
- `star_ready`로 표시한 스토리 수
- 주요 역량 커버리지 공백

launch/setup 중에 실행되는 경우, 다시 마이닝하기보다 prep 워크플로 안에서 `story-retrieval`을 실행하도록 제안합니다.
