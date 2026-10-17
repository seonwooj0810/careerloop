---
name: event-radar
description: "지역·광역·전국·해외 범위의 네트워킹 이벤트를 ROI 등급과 발표 기회 표시와 함께 찾아줍니다. networking-strategist를 호출합니다. 트리거 예: \"event radar\", \"upcoming conferences\", \"networking events near me\", \"meetups for my role\", \"events this quarter\" (이벤트 레이더, 다가오는 컨퍼런스, 근처 네트워킹 행사, 내 직무 밋업, 이번 분기 이벤트)."
triggers:
  - "event radar"
  - "upcoming conferences"
  - "networking events near me"
  - "meetups for my role"
  - "events this quarter"
  - "/careerloop:event-radar"
  - "이벤트 레이더"
  - "예정된 컨퍼런스"
  - "내 근처 네트워킹 행사"
  - "내 직무 밋업"
  - "이번 분기 행사"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

**`networking-strategist`**를 **`event-radar`** 모드로 호출합니다.

## 호출

- 에이전트 이름은 정확히 **`networking-strategist`**를 사용합니다. 호출에 실패하면 한 번 재시도합니다.

## 워크플로

1. `{user_dir}/CareerLoop/profile.md`에서 위치, 원격 근무 선호, 목표 직무, 산업을 읽습니다.
2. 에이전트에게 **지역 → 광역 → 전국 → 해외** 순으로 상황에 맞게 탐색하도록 지시합니다(프로필이 지역 한정이면 해외는 건너뜁니다).
3. **공식 사이트**와 **검증 가능한 목록**을 우선하며, 도구가 없으면 이벤트를 지어내지 말고 **검색 쿼리**와 **확인할 사항**을 대신 출력합니다.
4. 범위별로 묶은 결과를 **ROI 등급 A/B/C**, **발표 기회** 표시, 링크와 함께 제공합니다.
5. 후속 활용을 위해 **`event_radar_v1`** JSON 블록을 포함한 `{user_dir}/CareerLoop/event-radar.md` 파일 작성을 제안합니다.

## 스케줄링 (Claude Cowork)

이벤트에 적극 참석하는 구직자라면 **월 단위** `/schedule`이 적절하며, 소극적 구직이면 주기를 줄입니다.
