---
name: daily-schedule
description: "일일 스케줄러에서 실행됩니다. 정기 운영 브리프(파이프라인 다이제스트, 기한이 지난 후속 조치, 면접 컨텍스트, 오늘 해당 시 조건부 면접 전 브리프, 시장 요약, 액션 프롬프트)를 전달합니다. “오늘 면접 브리프” 같은 요청은 당일 면접 준비 부분만 집중 실행합니다. Runs on the daily scheduler. Delivers the routine operating brief (pipeline digest, overdue follow-ups, interview context, conditional pre-interview brief for today, market summary, and action prompts). A day-of-interview request triggers a focused prep slice only. 트리거 예시(Trigger phrases): \"daily job search brief\", \"careerloop daily digest\", \"pipeline summary for my applications\", \"morning job search summary\", \"run my daily career brief\", \"morning brief before my interview\", \"interviews today brief\", \"what do I need for my interviews today\", \"day of interview brief\", \"일일 구직 브리프\", \"오늘의 파이프라인 요약\", \"오늘 면접 브리프\", \"오늘 면접에 필요한 것\", \"면접 당일 브리프\"."
triggers:
  - "daily job search brief"
  - "careerloop daily digest"
  - "pipeline summary for my applications"
  - "morning job search summary"
  - "run my daily career brief"
  - "/daily-schedule"
  - "/careerloop:daily-schedule"
  - "morning brief before my interview"
  - "interviews today brief"
  - "what do I need for my interviews today"
  - "day of interview brief"
  - "오늘의 구직 브리프"
  - "데일리 브리프"
  - "파이프라인 요약해줘"
  - "아침 구직 요약"
  - "오늘 면접 브리프"
  - "오늘 면접 준비할 것 알려줘"
  - "면접 당일 브리프"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

### 스케줄링 (Claude Cowork)

이 스킬은 Cowork의 **`/schedule`**(또는 동등한 기능)을 사용하는 **일일 예약 작업**으로 실행되도록 설계되었습니다. 사용자가 예약할 수 있는 페이로드 예시는 다음과 같습니다.

> Run the CareerLoop `daily-schedule` skill for my job search folder. Deliver the daily brief per `skills/daily-schedule/SKILL.md`.

첫 실행이 성공한 뒤에는 Cowork가 보통 학습한 경로, 커넥터, 컨텍스트로 예약된 프롬프트를 다듬습니다.

## 워크플로

### 1. `{user_dir}` 확인 및 데이터 파일 검증

다음을 확인합니다.
- `{user_dir}/CareerLoop/profile.md`
- `{user_dir}/CareerLoop/ExperienceLibrary.json`
- `{user_dir}/CareerLoop/tracker.json`
- `{user_dir}/CareerLoop/artifacts-index.json`
- `{user_dir}/CareerLoop/StoryCorpus.json` (`mine-stories`를 통한 필요 시 생성 허용)

없으면 다음을 출력합니다.
> 일일 브리프를 건너뜁니다. `/careerloop:launch`를 실행하여 CareerLoop를 초기화하세요.

### 2. 요약 전에 아티팩트 정합성 맞추기

브리프를 계산하기 전에 `{user_dir}`에서 PDF/DOCX 아티팩트를 스캔합니다.

아티팩트 파일이 하나 이상 있으면 개수를 계산하기 전에 `artifacts-index.json`이 동기화되도록
`artifact-saved`를 먼저 실행합니다.

아티팩트가 없으면 `artifact-saved`를 실행하지 않고 계속 진행합니다.

### 2.5 새 소스 문서 자동 수집

브리프를 확정하기 전에, 새로 발견된 이력서/CV 형태의 파일이 `{user_dir}`에 있으나 `ExperienceLibrary`에 소스 항목으로 아직 반영되지 않았는지 감지합니다.

그런 파일이 발견되면 다음과 같이 합니다.
- 새로 발견된 각 소스 문서에 대해 `add-source`를 자동으로 실행합니다(수동 프롬프트 불필요).
- 각 수집이 성공할 때마다 `artifacts-index.json`의 일관성을 유지하기 위해 `artifact-saved`를 한 번 다시 실행합니다.
- 최종 브리프에 자동 수집된 파일 수를 나열하는 한 줄 메모를 포함합니다.

어떤 파일이든 수집에 실패하면 다음과 같이 합니다.
- 일일 브리프는 계속 진행합니다.
- 실패한 파일명을 짧은 "확인 필요" 줄에 나열합니다.
- 해당 파일들에 대해 `/careerloop:add-source`를 다시 실행하도록 권장합니다.

### 2.6 스토리 코퍼스 증분 갱신

브리프를 확정하기 전에, 마지막 스토리 마이닝 실행 이후 스토리가 담긴 소스 파일이
변경되었는지 감지합니다.

- 저널 / 로그
- PKM 노트/내보내기
- 면접 디브리프 노트
- 면접 근거를 더할 수 있는 이력서/CV/자기소개서 본문

가능한 경우 `CareerLoop/StoryCorpus.json`의 `source_index` 항목(경로 + mtime)을
기준선으로 사용합니다.

적격한 소스 파일이 하나 이상 새로 생겼거나 변경된 것이 감지되면 다음과 같이 합니다.
- `mine-stories`를 증분 모드로 자동 실행합니다(수동 프롬프트 불필요).
- `StoryCorpus.json`과 그 `meta.updated` + `source_index`를 갱신합니다.
- 최종 브리프에 짧은 한 줄을 추가합니다.
  - `스토리 코퍼스 갱신됨: 소스 파일 {n_files}개 스캔, 스토리 {n_stories}개 추가/갱신.`

갱신에 실패하면 다음과 같이 합니다.
- 일일 브리프는 계속 진행합니다.
- 간결한 "확인 필요" 줄을 추가합니다.
  - `스토리 코퍼스 갱신에 실패했습니다. "mine-stories"를 실행하여 다시 시도하세요.`

### 2.7 월간 커리어 플랜 점검
`{user_dir}/CareerLoop/career-trajectory-data.json` 또는
`{user_dir}/CareerLoop/career-trajectory.md`가 존재하면 플랜이 오래되었는지
판단합니다.
- `career-trajectory-data.json`의 `as_of` 필드를 우선합니다.
- JSON 파일이 없으면 `career-trajectory.md`의
  `## Career trajectory analysis ({YYYY-MM-DD})` 같은 제목으로 대체합니다.
- 다음 중 하나에 해당하면 파일이 "오래된(stale)" 것으로 간주합니다.
  - 파일이 없음(첫 실행), 또는
  - 생성된 지 30일을 초과, 또는
  - 파일의 `as_of` 이후 트래커에 새 결과(outcome) 이벤트가 5건 이상
    (거절, 오퍼, 수락 완료. `pending`은 세지 않음).

오래되었다면 `career_plan_refresh_due = true`로 설정합니다.

### 2.8 오퍼 평가 알림
트래커에서 다음을 만족하는 활성 지원 건이 있는지 확인합니다.
- `status`가 `"offer"`이고
- `{user_dir}/CareerLoop/offer-context-{application_id}.json`이
  존재하지 않음(오퍼 평가가 아직 실행되지 않음)

하나라도 있으면 `offer_evaluation_due = true`로 설정하고 회사, 직무, 마감일(있는 경우)과 함께
최대 3개 항목을 기록합니다.

### 3. 일일 운영 브리프 작성

지원 데이터는 [references/tracker-schema.md](../../references/tracker-schema.md)에 정의된 분할 레이아웃을 사용합니다. 읽기나 쓰기 전에 반드시 해당 문서를 읽습니다.

`{user_dir}/CareerLoop/tracker.json`과 `{user_dir}/CareerLoop/artifacts-index.json`을 읽습니다.

아래 모든 수치는 `tracker.json` **요약 행만으로** 계산합니다. `status`, `outcome`, `follow_up_date`, `latest_stage`, `latest_stage_date`, `notes_count`, `stage_count`, `contact_count`가 모두 행에 있습니다. 다이제스트를 계산하는 동안 `applications/<application_id>.json`이나 `contacts/<company-slug>.json`을 열지 **않습니다**. 이 파일들은 **§3.2**의 면접 전 브리프 대상이 되는 소수의 지원 건에 한해서만 엽니다.

계산 항목:
- `tracker.json` 요약 행의 status별 파이프라인 건수(`applied`, `phone_screen`, `interview`, `offer`, `accepted`, `rejected`, `withdrew`, `ghosted`). 여기에 `recommendations.json`의 `considering` 레코드 수를 더하며, 이는 별도로 "검토 중인 직무 X개"로 보고합니다
- 기한이 지난 후속 조치 건수(`follow_up_date`가 있으면 사용)
- **오늘의 미팅** — **`latest_stage_date`가 오늘**(로컬)이고 **`latest_stage`**가 아래 허용 목록과 일치하는 요약 행의 수(`latest_stage` 문자열에 대한 대소문자 무시 부분 문자열 일치)
- 유형별 아티팩트 건수(`resume`, `cover_letter`)

#### 3.1 단계 허용 목록 — 오늘의 면접 / 리크루터 / 스크리닝

`latest_stage_date`가 **오늘**이고 `latest_stage`가 다음 부분 문자열 중 하나와 일치하면 요약 행을 **“오늘 미팅”**으로 간주합니다.

`interview`, `recruiter`, `phone screen`, `phone_screen`, `hiring manager`, `hm `, `hm interview`, `technical`, `panel`, `onsite`, `executive`, `final round`, `final interview`

이 간단한 1차 필터에 두 가지 보완이 있습니다.
- `stage_count: 0`인 행은 건너뜁니다. 단계 이력이 전혀 없습니다.
- `latest_stage_date`가 **오늘보다 이후**인 행에도 오늘 날짜의 단계가 숨어 있을 수 있습니다. 예정된 면접은 미래 날짜로 기록되기 때문입니다. **그런 행에 한해서만** `{user_dir}/CareerLoop/` + 해당 행의 `detail_file`을 읽고 `stage_history[]`에서 오늘 날짜의 허용 목록 일치 항목을 스캔합니다.

이 질문에 답하기 위해 모든 상세 파일을 로드하지 않습니다. 거의 모든 지원 건은 요약 행만으로 답이 나옵니다.

오늘 해당되는 **지원 건** 목록을 만듭니다(요약 행의 `id`로 중복 제거).

#### 3.2 면접 전 브리프 하위 섹션

- **오늘 미팅에 해당하는 지원 건이 없으면:** 출력에서 **Pre-interview brief** 하위 섹션 전체를 **생략**합니다(플레이스홀더 없음).
- **하나 이상 해당하면:** 파이프라인 블록 **뒤에**(§5 참조) **`Pre-interview brief (today)`**라는 제목의 하위 섹션을 추가합니다. 해당하는 **각** 지원 건에 대해서만 `{user_dir}/CareerLoop/` + 해당 `detail_file`을 읽습니다. 이 파일에는 `stage_history[]`(`interviewers` 포함)와 `notes[]`가 있으며, 이 중 어느 것도 더 이상 `tracker.json`에는 없습니다. 그런 다음 **짧은** 불릿만 작성합니다(엄격한 간결성 — 전체 준비 문서가 아닙니다).
  - **뉴스 또는 회사 훅** 하나(트래커/아티팩트 또는 검증 가능한 웹으로 근거가 확인된 경우에만. 아니면 “확인된 헤드라인 없음 — 자세한 내용은 `/careerloop:prep-interview` 실행”이라고 말함)
  - `ExperienceLibrary` + 직무 적합성에서 뽑은 **토킹 포인트 2–3개**
  - 상세 파일의 오늘자 `stage_history` 항목에 `interviewers`가 나열되어 있거나 지원 건에 연락처가 있는 경우 **면접관** 리마인더: 행의 `contact_count`가 0보다 크면 `{user_dir}/CareerLoop/` + 해당 `contacts_file`을 읽고, **`application`**이 행의 **`application`** 레이블(`"<company> — <role>"`)과 같은 항목만 남기며, 누구든 이름을 언급하기 전에 **`name` 기준으로 중복을 제거**합니다
  - **주의(watch)** 한 줄(리스크, 공백, 또는 확인할 후속 조치)

어조와 한도는 **`morning_section`** 모드의 **`agents/interview-coach/AGENT.md`**를 따릅니다. 이 스킬 안에서 해당 모드를 **인라인**으로 구현하는 것입니다(별도의 스킬 파일 없음).

### 3.3 집중 실행 — 당일 면접 브리프

사용자의 메시지가 **주로** 당일 면접 요청인 경우(트리거에는 “morning brief before my interview”, “오늘 면접 브리프” 등이 포함됩니다):

1. **§1** 검증은 그대로 수행하고, 적절한 경우 **§2** 아티팩트 정합성 맞추기(경량)도 수행합니다.
2. 사용자가 전체 다이제스트도 요청하지 않았다면 전체 파이프라인 표와 아티팩트 건수는 **건너뜁니다**.
3. **다음만** 출력합니다.
   - 한 줄 헤더: **`CareerLoop — Pre-interview brief`** [{today}]
   - **§3.2**에 따른 **Pre-interview brief (today)** 내용, 또는 오늘 `tracker.json`에 해당하는 미팅이 **없다**는 명확한 한 줄 — 그런 다음 예정된 스크리닝을 기록하려면 `/careerloop:track-application`을, 심층 준비는 `/careerloop:prep-interview`를 제안합니다.

사용자가 **일반 일일** 트리거를 실행하면 **§3.2**가 해당될 때 **Pre-interview brief**를 포함하여 **§5**의 **전체** 템플릿을 출력합니다.

### 4. 시장 및 전략 프롬프트 추가

사용자가 최근 시장 워크플로를 실행했다면 최상위 신호를 한 줄로 요약합니다.
트래커 데이터에 최근 전략 신호가 없으면 다음을 추가합니다.
> job-scout 랭킹을 위한 전략 신호를 갱신하려면 `/careerloop:suggest-roles`를 실행하세요.

최근 생성된 시장 브리프가 없으면 다음을 추가합니다.
> 주간 수요 및 대체(displacement) 업데이트를 보려면 `/careerloop:market-brief`를 실행하세요.

### 5. 출력 형식

```
**CareerLoop — Daily Brief** [{today}]

파이프라인
  검토 중          {n}
  지원 완료        {n}
  전화 스크리닝    {n}
  면접             {n}
  오퍼             {n}

후속 조치 기한     {n}
오늘의 미팅        {n from §3.1 또는 "예정 없음"}

아티팩트
  이력서           {n}
  자기소개서       {n}
```

**§3.2**가 해당되면 다음을 추가합니다.

```
Pre-interview brief (today)
  {지원 건별 간결한 불릿 — §3.2 참조}
```

그런 다음 긴급도가 높은 순으로 최대 3개의 간결한 액션 불릿을 추가합니다. 다음을 포함합니다.
- `offer_evaluation_due`인 경우: 상위 항목과 `/careerloop:evaluate-offer` 실행 안내를 담은
  "Offer evaluation due" 불릿.
- `career_plan_refresh_due`인 경우: 사용자에게 `/careerloop:career-plan` 실행을 안내하는
  "Career plan refresh due" 불릿.

## 가드레일

- 정기 요약의 기본 위치는 이 스킬입니다. `focus-career`에서 중복하지 않습니다
- 데이터가 부족하면 명시적으로 밝히고 권장 사항은 가볍게 유지합니다
- 시장 뉴스, 날짜, 마감일을 지어내지 않습니다
