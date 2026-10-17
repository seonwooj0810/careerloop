---
name: content-suggest
description: "프로필과 ExperienceLibrary에 맞춰 LinkedIn 및 전문가 게시글의 주제, 관점, 게시 주기를 추천합니다. writer를 호출합니다. 트리거 예: \"linkedin post ideas\", \"what should i post\", \"content suggestions\", \"topics for linkedin\" (링크드인 게시글 아이디어, 뭐 올릴까, 콘텐츠 추천, 링크드인 주제)."
triggers:
  - "linkedin post ideas"
  - "what should i post"
  - "content suggestions"
  - "topics for linkedin"
  - "/careerloop:content-suggest"
  - "링크드인 게시물 아이디어"
  - "뭘 올리면 좋을까"
  - "콘텐츠 추천해줘"
  - "링크드인 주제 추천해줘"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

**`writer`**를 **`content-suggest`** 모드로 호출합니다.

## 호출

- 에이전트 이름은 정확히 **`writer`**를 사용합니다. 호출에 실패하면 한 번 재시도합니다.

## 워크플로

1. `{user_dir}/CareerLoop/profile.md`, `{user_dir}/CareerLoop/ExperienceLibrary.json`, 그리고 있으면 **`voice-profile.md`**를 읽습니다.
2. **`writer`**에게 **5~8개의 주제 아이디어**를 요청합니다. 각 아이디어에는 적합한 이유, 리스크 수준(논란 적음 vs 자극적), 권장 형식(짧은 게시글 vs 스레드 vs 링크 + 댓글)을 포함합니다.
3. 사용자가 한 주제의 **전체 초안**을 원하면, **`writer`**의 보이스 사전 점검이 충족되었는지 확인합니다(`voice-profile.md`에 **`## User writing samples`** 또는 **`## User writing samples (launch)`**가 있거나, 게시글을 요청하거나 **skip**을 한 번 묻습니다. **`draft-outreach`**와 같은 패턴입니다). 그다음 **`writer`**를 호출해 게시글 하나를 작성합니다. **`writer`**는 초안을 **`{user_dir}/LinkedIn Posts/`** 아래에 **`.md`**로 **저장**하고(폴더가 없으면 생성), **`artifacts-index.json`**에 `"type": "linkedin_post"`로 **추가**하며, 사용자가 열어 편집할 파일 경로를 알려야 합니다. 게시 전에 **`evaluate-post`**를 제안합니다.
