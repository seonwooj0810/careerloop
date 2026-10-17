---
name: networking-strategy
description: "목표 직무를 위한 근거 기반 네트워킹 계획(우선순위, 순서, 웜 패스, 공백 보완)을 수립합니다. 아웃리치 문안은 writer가 담당합니다. networking-strategist를 호출합니다. Builds an evidence-based networking plan for target roles—priorities, sequencing, warm paths, and gap fixes. Outreach copy is handled by writer. Invokes networking-strategist. 트리거 예시(Trigger phrases): \"networking strategy\", \"who should I network with\", \"how should I network\", \"job search networking plan\", \"warm intros\", \"informational interviews\", \"네트워킹 전략\", \"누구와 네트워킹해야 할까\", \"네트워킹은 어떻게 해야 할까\", \"구직 네트워킹 계획\", \"웜 인트로\", \"정보 인터뷰\"."
triggers:
  - "networking strategy"
  - "who should I network with"
  - "how should I network"
  - "job search networking plan"
  - "warm intros"
  - "informational interviews"
  - "/careerloop:networking-strategy"
  - "네트워킹 전략"
  - "누구와 네트워킹해야 할까"
  - "어떻게 네트워킹해야 할까"
  - "구직 네트워킹 계획"
  - "웜 인트로"
  - "정보 인터뷰"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

**`networking-strategist`**를 **`networking-strategy`** 모드로 호출합니다.

## 호출

- 정확한 에이전트 이름 **`networking-strategist`**를 사용합니다. 호출에 실패하면 오류를 보고하기 전에 같은 이름으로 한 번 재시도합니다.

## 워크플로

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분할 레이아웃을 사용합니다. 읽기나 쓰기 전에 반드시 해당 문서를 읽습니다.

1. `{user_dir}/CareerLoop/profile.md`, `tracker.json`(요약 행), `ExperienceLibrary.json`을 읽습니다.
   - **기존 관계:** 연락처는 더 이상 `applications[]` 안에 있지 않습니다. 계획의 기준이 되는 지원 건마다 요약 행의 `contacts_file`을 가져와 `{user_dir}/CareerLoop/` + 해당 경로(`contacts/<company-slug>.json`)를 로드하고, `contacts[]` 중 `application`이 해당 행의 `application` 레이블과 같은 항목만 필터링합니다. slug를 직접 만들어 내지 않으며, `contacts_file`이 없는 행은 연락처가 없는 것입니다. 회사 파일 하나가 그 회사의 모든 지원 건을 담당하므로, 사용자에게 관계 맵이나 웜 패스 목록을 보여주기 전에 **`name` 기준으로 중복을 제거**합니다.
   - **파이프라인 맥락:** 요약 행의 `status`, `latest_stage`, `latest_stage_date`, `notes_count`, `stage_count`, `contact_count`만으로도 대개 우선순위를 정하기에 충분합니다. `notes[]` / `stage_history[]`가 필요할 때는 실제로 진행 중인 지원 건에 한해서만 행의 `detail_file`(`applications/<application_id>.json`)을 엽니다.
2. 사용자가 밝힌 목표(있는 경우)를 전달합니다. 목표 직무, 드림 컴퍼니, 일정 등입니다.
3. 에이전트에게 **90일 계획**, **상위 5개 관계 액션**, **하지 말아야 할 것**을 요청하고, 메시지가 필요한 경우에는 `agents/networking-strategist/AGENT.md`에 따라 **`writer`용 핸드오프 브리프**(목적, 대상, 훅, 톤, 피해야 할 것 목록)도 요청합니다. 실제 LinkedIn/이메일 문안은 **`writer`** 또는 **`/careerloop:draft-outreach`**로 안내합니다.
4. 사용자가 지속적으로 참고할 자료를 원하면 요약을 `{user_dir}/CareerLoop/networking-strategy.md`에 저장하도록 제안합니다(생성하거나 날짜가 붙은 섹션으로 추가).

## 스케줄링 (Claude Cowork)

`networking-strategy`는 트래커나 목표가 크게 바뀐 뒤 **매월** `/schedule`로 갱신하면 효과적입니다.
