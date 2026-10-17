---
name: event-intelligence
description: "특정 컨퍼런스·밋업의 네트워킹 ROI, 참석자 적합도, 비용·시간 트레이드오프, 발표·연사 기회를 평가합니다. networking-strategist를 호출합니다. (Evaluates specific conferences and meetups for networking ROI, audience fit, cost-time tradeoffs, and presentation or speaking opportunities. Invokes networking-strategist.)"
triggers:
  - "event intelligence"
  - "should I go to this conference"
  - "conference ROI"
  - "speaking opportunity"
  - "CFP worth submitting"
  - "which event should I attend"
  - "/careerloop:event-intelligence"
  - "이벤트 분석"
  - "이 컨퍼런스 가야 할까"
  - "컨퍼런스 ROI"
  - "발표 기회"
  - "CFP 낼 만한가"
  - "어떤 행사에 참석해야 할까"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

**`networking-strategist`**를 **`event-intelligence`** 모드로 호출합니다.

## 호출

- 에이전트 이름은 정확히 **`networking-strategist`**를 사용합니다. 호출에 실패하면 한 번 재시도합니다.

## 워크플로

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분리(split) 레이아웃을 사용합니다. 읽기·쓰기 전에 반드시 해당 문서를 먼저 읽습니다.

1. `{user_dir}/CareerLoop/profile.md`를 읽고 `tracker.json`을 훑어봅니다. 요약 행만으로 목표 회사, 직무, `status`, `latest_stage`를 알 수 있으며, 이 스킬에는 보통 이것으로 충분합니다. 특정 지원 건의 메모나 단계 이력이 이벤트 결정에 영향을 줄 때가 아니면 `detail_file`을 열지 않습니다.
   - **사용자가 특정 회사에서 이미 아는 사람이 누구인지 알아야 하는 경우**(예: 이벤트가 인맥 확장에 도움이 되는지 판단할 때), 해당 회사 요약 행의 `contacts_file`을 가져와 `{user_dir}/CareerLoop/` + 해당 경로(`contacts/<company-slug>.json`)를 로드하고, `contacts[]`에서 `application`이 해당 행의 `application` 레이블과 같은 항목만 걸러냅니다. 회사 파일 하나가 그 회사의 모든 지원 건을 담고 있으므로, 사용자의 네트워크에 이미 있는 사람을 나열할 때는 **`name` 기준으로 중복을 제거**합니다.
2. 대화에서 **이벤트 이름** 또는 **카테고리**(예: “ML product conferences Q3”)와 **사용자 제약 조건**(예산, 출장, 휴가)을 추출합니다.
3. 사용 가능한 웹/검색 또는 이벤트 도구로 날짜, 장소, 공식 URL을 검증합니다. 날짜나 가격을 지어내지 않습니다.
4. 에이전트에게 다음을 요청합니다: **ROI 등급(tier)**, **참석자 평가**, 근거를 포함한 **발표 기회 플래그**(`yes` / `maybe` / `no`), **리스크**(pay-to-play, 낮은 시그널), **go/no-go** 권고.
5. 필요하면 에이전트 가이드라인에 따라 **`event_radar_v1`** JSON 부분집합(단일 이벤트 또는 소규모 목록)을 `{user_dir}/CareerLoop/event-radar.md` 또는 `network-map.md`에 추가합니다.

## 스케줄링 (Claude Cowork)

사용자가 이벤트 채용 채널이 강한 직무 유형을 목표로 한다면, 컨퍼런스 성수기 전에 선택적으로 **분기별** `/schedule`을 실행합니다.
