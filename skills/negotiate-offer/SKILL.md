---
name: negotiate-offer
description: >
  협상 레버리지와, writer를 통한 바로 보낼 수 있는 협상 초안을 작성합니다. evaluate-offer가 저장한 OfferContext를
  불러와 이미 알고 있는 세부 정보를 다시 수집하지 않습니다. 다음과 같은 요청에 사용합니다: "negotiate my salary",
  "negotiate this offer", "salary counter offer", "help me negotiate", "연봉 협상 도와줘", "오퍼 협상 메시지 써줘".
  (Produces negotiation leverage and a send-ready negotiation draft via
  writer. Loads OfferContext persisted by evaluate-offer and
  avoids re-collecting already-known details.)
triggers:
  - "negotiate my salary"
  - "negotiate this offer"
  - "raise negotiation"
  - "promotion negotiation"
  - "salary counter offer"
  - "help me negotiate"
  - "/careerloop:negotiate-offer"
  - "연봉 협상해줘"
  - "이 오퍼 협상하고 싶어요"
  - "연봉 인상 협상"
  - "승진 협상"
  - "연봉 카운터 오퍼"
  - "협상 도와줘"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

> **경력 연수 인용 규칙:** 경력·도메인 연수를 말할 때는 ExperienceLibrary의 날짜로 직접 계산한 값을 쓴다. 이력서나 프로필의 표기가 계산값과 다르면 계산값을 쓰고 불일치를 한 줄로 알린다(예: 이력서 "5년" ↔ 날짜상 4년 7개월).

`negotiate-offer`를 실행해 다음 자료를 바탕으로 사용자의 어조로 바로 보낼 수 있는 협상 메시지를 작성합니다.
- 가능하면 `evaluate-offer`가 저장한 `OfferContext`
- 없으면 최소한의 정보 수집 + 새 시장 벤치마크

## 워크플로

### 디렉터리 공유 (호스트 연동)
이 스킬을 실행하는 동안 호스트 UI가 **에이전트와 공유할 디렉터리**를 요청하면, `{user_dir}` 구직 폴더(`CareerLoop/`를 포함한 폴더)만 공유합니다.

이 스킬이 읽는 파일:
- `{user_dir}/CareerLoop/profile.md`
- `{user_dir}/CareerLoop/ExperienceLibrary.json`
- `{user_dir}/CareerLoop/tracker.json` (요약 행)
- `{user_dir}/CareerLoop/applications/<application_id>.json` (협상 중인 오퍼 하나)
- `{user_dir}/CareerLoop/contacts/<company-slug>.json` (협상 메시지의 수신자)
- `{user_dir}/CareerLoop/offer-context-{application_id}.json` (있는 경우)

전체 워크스페이스나 관련 없는 폴더는 공유하지 않습니다.

### 1. 필수 데이터 존재 확인

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분리 레이아웃을 사용합니다. 읽거나 쓰기 전에 반드시 이 문서를 먼저 읽습니다.

읽을 파일:
- `{user_dir}/CareerLoop/profile.md`
- `{user_dir}/CareerLoop/ExperienceLibrary.json`
- `{user_dir}/CareerLoop/tracker.json`

필수 파일이 없으면 다음과 같이 출력합니다.
> 협상을 건너뜁니다: `/careerloop:launch`를 실행해 `CareerLoop/`를 초기화하세요.

### 2. 협상할 오퍼 식별
우선 경로:
- 사용자 메시지에 `company`와 `role`(또는 공고 링크 / 마감일)이 있으면, `status`가 `"offer"`인 `tracker.json` 요약 행과 매칭합니다.

트래커에 `"offer"` 행이 정확히 하나면 그것을 사용합니다.

오퍼 지원(건)이 여러 개이고 매칭이 모호하면:
- 명확화 질문을 딱 하나만 합니다: "어느 회사/직무의 오퍼를 협상할까요?"

행의 `id`로 `application_id`를 설정하고, 해당 행의 `application` 라벨, `detail_file`, `contacts_file`, `contact_count`, `latest_stage`, `latest_stage_date`를 유지합니다.

그런 다음 **이 지원(건)에 대해서만** 다음을 불러옵니다.
- `{user_dir}/CareerLoop/` + `detail_file` — `stage_history[]`와 `notes[]`에는 보상에 대해 이미 오간 이야기, 오퍼가 나온 단계, 이전 카운터 제안이 담겨 있습니다. 두 배열 모두 `tracker.json`에 없으며, 이를 보지 않고 초안을 쓰면 이미 다룬 내용을 반복하게 됩니다.
- 지명된 수신자가 있으면 `{user_dir}/CareerLoop/` + `contacts_file`. **`application`**이 행의 **`application`** 라벨과 같은 항목만 남기고, **`name` 기준으로 중복을 제거**한 뒤, 해당 항목의 `title`, `relationship`, 이전 `interactions[]`를 사용해 수신자와 채널을 정합니다. `contacts_file`이 없는 행은 등록된 연락처가 없다는 뜻이므로, slug나 이름을 지어내지 않습니다.

### 3. 저장된 OfferContext 불러오기 (있으면 재수집 생략)
다음 파일이 있는지 확인합니다.
`{user_dir}/CareerLoop/offer-context-{application_id}.json`
(없으면 행의 `previous_ids`를 확인해 이전 id로 저장된 컨텍스트 파일을 찾음)

찾았다면:
- 불러옵니다
- 파일에 이미 있는 오퍼 세부 정보와 시장 벤치마크는 재수집하지 않습니다

찾지 못했다면:
- 빠진 오퍼 기본 정보(보상 + 마감일 + 주요 조건)를 요청합니다
- 이후 프로필 + ExperienceLibrary를 바탕으로 벤치마크/레버리지를 진행합니다

### 4. 협상 레버리지 + 요구 전략 구성
`honest-advisor`(주) + `market-researcher`(입력)를 사용해 다음을 포함한 **NegotiationBrief**를 작성합니다.
- 시장 내 위치 (현재 오퍼가 벤치마크 대비 어디에 있는지)
- 레버리지 목록 (중앙값을 웃도는 요구를 뒷받침하는 자격/성과/ExperienceLibrary 단위를 순위별로 정리)
- 요구 전략 (권장 기본급/지분/사이닝 보너스 목표와 제시 순서)
- 리스크 보정 (이 시나리오에서의 하방 리스크, 가능하면 협상 결렬 하한선)

### 5. `writer`에 `NegotiationHandoffBrief` 전달
다음을 포함하는 구조화된 **NegotiationHandoffBrief** 객체를 만듭니다.
- 요구 금액/범위
- 핵심 레버리지 포인트
- 어조 가이드 (단호함 vs 협력적)
- 권장 채널 (이메일 vs 구두)
- 제안 문구 (짧은 불릿 목록)

그런 다음 다음 모드로 **`writer`**를 호출합니다.
- `negotiate-offer`

그러면 `writer`가 사용자의 어조로 바로 보낼 수 있는 협상 메시지를 작성합니다.

### 6. 초안 제시 + 명시적 승인 요청
`writer`의 초안을 전문 그대로 보여주고 다음과 같이 묻습니다.
> "보내도 될까요? 수정을 원하시면 무엇을 조정할지 알려주세요(요구 금액 수준, 어조, 채널)."

어떤 것도 자동으로 전송하지 않습니다.

### 7. 사용자가 확인하면 전송 기록
사용자가 보냈다고 말한 뒤에만, [references/tracker-schema.md](../../references/tracker-schema.md)의 **다중 파일 트랜잭션**을 씁니다. 한 파일만 업데이트하고 나머지를 건너뛰어서는 안 됩니다.

- `{user_dir}/CareerLoop/` + `detail_file`의 `notes[]`에 다음을 추가합니다.
  `{ "date": "YYYY-MM-DD", "text": "[negotiation] {ask} sent via {channel}" }` 그런 다음 요약 행의 `notes_count`를 새 배열 길이로 설정합니다.
- 수신한 연락처가 있으면 `contacts_file`에서 해당 연락처의 `interactions[]`에 추가합니다. `name`이 일치하고 **동시에** `application`이 행의 `application` 라벨과 같은 항목이어야 합니다.
  `{ "date": "YYYY-MM-DD", "type": "email | call", "notes": "Negotiation ask sent" }`
  지명된 연락처가 없으면 지어내지 말고 이 단계를 건너뜁니다.
- 요약 행에서 `next_step`을 "Await negotiation response"로 설정하고 `follow_up_date`를 합의한 확인 일자로 옮깁니다.

각 파일을 프로그램으로 불러와 다시 덤프하고(`json.load` / `json.dump`, `indent=2`, `ensure_ascii=False`) 다시 읽어 카운터가 여전히 배열과 일치하는지 검증합니다.

*** 마무리 참고 (호스트 도구 안전) ***
- 오류 텍스트를 파일명이나 경로로 사용하지 않습니다.
- 호스트 쓰기가 하나라도 실패하면 저장된 것처럼 꾸미지 말고, 어떤 파일이 쓰이지 않았는지 알려준 뒤 채팅에서 계속 진행합니다. §7 트랜잭션이 일부만 적용된 상태는 아예 적용하지 않은 것보다 나쁩니다. 상세 파일은 쓰였는데 요약 행이 쓰이지 않았다면, 복구할 수 있도록 불일치를 보고합니다.

