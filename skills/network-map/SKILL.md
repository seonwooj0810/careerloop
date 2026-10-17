---
name: network-map
description: "사용자에서 목표 고용주까지 이어지는 그럴듯한 경로와 공백(브리지, 가설, 드림 잡 레버리지 지점)을 매핑합니다. 서술형 텍스트와 향후 시각화 레이어용 network_map_v1 JSON을 출력합니다. networking-strategist를 호출합니다. Maps plausible paths and gaps from the user to target employers—bridges, hypotheses, and dream-job leverage points. Outputs prose plus network_map_v1 JSON for a future visualization layer. Invokes networking-strategist. 트리거 예시(Trigger phrases): \"network map\", \"map my network\", \"who can introduce me\", \"dream job connections\", \"path to company\", \"introduction strategy\", \"네트워크 맵\", \"내 인맥 지도\", \"누가 소개해 줄 수 있을까\", \"드림 잡 인맥\", \"회사까지의 경로\", \"소개 전략\"."
triggers:
  - "network map"
  - "map my network"
  - "who can introduce me"
  - "dream job connections"
  - "path to company"
  - "introduction strategy"
  - "/careerloop:network-map"
  - "네트워크 지도"
  - "내 네트워크 지도 그려줘"
  - "누가 소개해 줄 수 있어"
  - "드림 잡 연결고리"
  - "이 회사로 가는 경로"
  - "소개 전략"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

**`networking-strategist`**를 **`network-map`** 모드로 호출합니다.

## 호출

- 정확한 에이전트 이름 **`networking-strategist`**를 사용합니다. 호출에 실패하면 한 번 재시도합니다.

## 워크플로

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분할 레이아웃을 사용합니다. 읽기나 쓰기 전에 반드시 해당 문서를 읽습니다.

1. `{user_dir}/CareerLoop/profile.md`, `tracker.json`(요약 행), `ExperienceLibrary.json`을 읽습니다.
   - **알려진 연락처(맵의 확정 노드):** 연락처는 더 이상 `applications[]`에 있지 않습니다. 대상 지원 건마다 요약 행의 `contacts_file`을 가져와 `{user_dir}/CareerLoop/` + 해당 경로(`contacts/<company-slug>.json`)를 로드하고, `contacts[]` 중 `application`이 해당 행의 `application` 레이블과 같은 항목만 필터링합니다. slug를 직접 만들어 내지 않으며, `contacts_file`이 없는 행은 등록된 연락처가 없는 것입니다. 회사 파일 하나가 그 회사의 모든 지원 건을 담당하므로 같은 사람이 여러 번 나타날 수 있습니다. **`name` 기준으로 중복을 제거**하여 한 사람이 여러 노드가 아닌 하나의 노드가 되게 합니다.
   - **관계 근거:** 일치한 각 연락처의 `relationship`, `title`, `notes`, `interactions[]`가 확정된 엣지입니다. `notes[]` / `stage_history[]`가 필요할 때는 실제로 진행 중인 지원 건에 한해서만 행의 `detail_file`(`applications/<application_id>.json`)을 엽니다. 행의 `latest_stage`, `latest_stage_date`, `notes_count`, `stage_count`, `contact_count`만으로 대개 답이 나오므로 아무것도 열지 않아도 되는 경우가 많습니다.
2. 사용자가 특정 회사나 연락처를 지목하면 **confirmed**(확정)로 포함하고, 나머지는 모두 신뢰도 레이블을 붙인 **hypothesis**(가설)로 처리합니다.
3. 에이전트에게 다음을 요구합니다.
   - **목표 → 경로 → 공백**을 읽기 쉬운 형태로 요약합니다.
   - `agents/networking-strategist/AGENT.md`에 따라 **`network_map_v1`** JSON 블록을 출력합니다.
   - **그래프 시각화는 이후 제품 반복으로 미뤄졌음**(JSON이 교환 포맷)을 명시적으로 밝힙니다.
4. 사용자가 동의하면 `{user_dir}/CareerLoop/network-map.md`에 서술 내용과 펜스 처리된 JSON을 작성하거나 갱신합니다(기본값: 출력 후 저장 여부를 제안).

## 향후 시각화

이 스킬에서는 그래프를 렌더링하지 않습니다. 이후 시각화 레이어가 맵을 다시 추론하지 않고도 노드/엣지를 렌더링할 수 있도록 **`network_map_v1`**을 그대로 유지합니다.
