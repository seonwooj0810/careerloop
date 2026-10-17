---
name: evaluate-post
description: "전문가 게시글이나 아웃리치 초안을 평가해, 대상 기업 프로필 대비 독자 적합성과 문화적·정치적·평판 리스크를 판단합니다. writer를 호출합니다. 트리거 예: \"evaluate this post\", \"cultural risk\", \"is this safe to post\", \"review my linkedin draft\", \"employer risk\" (이 게시글 평가해줘, 문화적 리스크 확인, 올려도 안전한지 봐줘, 링크드인 초안 검토)."
triggers:
  - "evaluate this post"
  - "cultural risk"
  - "is this safe to post"
  - "review my linkedin draft"
  - "employer risk"
  - "/careerloop:evaluate-post"
  - "이 게시물 평가해줘"
  - "올려도 안전한 글인가"
  - "내 링크드인 초안 검토해줘"
  - "고용주 리스크 확인해줘"
  - "문화적 리스크 확인해줘"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

**`writer`**를 **`evaluate-post`** 모드로 호출합니다.

## 호출

- 에이전트 이름은 정확히 **`writer`**를 사용합니다. 호출에 실패하면 한 번 재시도합니다.

## 워크플로

1. `{user_dir}/CareerLoop/profile.md`(**Target Companies**, **Target Roles**, 산업)를 읽습니다. 대상이 비어 있으면 **직무 수준** 기준으로만 평가할지 한 번 묻습니다.
2. 사용자로부터(또는 현재 턴에서) **초안 텍스트**를 수집합니다.
3. **`writer`**에게 **evaluate-post** 작업을 실행하도록 지시합니다: **리스크 등급**, 언급된 각 대상 고용주 유형별 근거, 선택 사항인 **더 안전한 대체 표현**을 제공하며, 수정 여부는 사용자가 결정합니다.
4. 리스크가 **높음**이면, 사용자가 초안을 조정하거나 대안 관점을 얻기 위해 **`content-suggest`**를 실행할 때까지 게시를 보류하도록 제안합니다.

## cultural-risk-flag와의 관계

다른 흐름에서 초안을 작성하다가 리스크 점검이 필요해지면 이 스킬의 규칙을 우선 적용해, 공개용 문구의 평가자는 항상 **`writer`** 하나로 유지합니다.
