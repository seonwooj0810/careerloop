# CareerLoop 단계별 테스트 계획

이 문서는 각 제공 단계(phase)별 실용적인 검증 항목을 정의합니다.
단계 완료로 태깅하기 전의 릴리스 게이트로 사용합니다.

## 규칙: 예시 프롬프트 (복사/붙여넣기)

**기능이 출시되거나 변경될 때마다** 해당 단계(또는 기능을 소유한 가장 가까운 단계) 아래에 **`### 예시 프롬프트 (복사/붙여넣기)`** 하위 섹션을 이 파일에 추가합니다. 각 하위 섹션에는 최소한 다음이 포함되어야 합니다.

- 해당되는 경우 **슬래시 명령** 형식의 프롬프트 1개 (`/careerloop:…`).
- 같은 스킬 의도를 트리거하는 **자연어** 변형 1개.
- 동작이 자명하지 않은 경우(경계 조건, Phase 2A 제한 등) **기대 결과** 메모.

프롬프트는 **`skills/*/`** 트리거 및 **`references/careerloop-spec.md`**와 일치하도록 유지합니다. Phase **1E**는 네트워킹 + **`writer`** 프롬프트가 있는 단계이며, 해당 에이전트나 오케스트레이션이 변경되면 갱신합니다.

## 테스트 데이터 사전 조건

- `CareerLoop/profile.md`가 있는 유효한 `{user_dir}`.
- `{user_dir}`에 원본 이력서/CV 1개 이상.
- `CareerLoop/tracker.json`: 진행 중인 지원과 종료된 지원이 섞여 있으며, [tracker-schema.md](tracker-schema.md)에 정의된 분리 레이아웃을 따름 — 요약 행만 포함하고, 각 행에 `application`, `detail_file`, `notes_count`, `stage_count`, `latest_stage`, `latest_stage_date` 포함.
- `CareerLoop/applications/<application_id>.json`: 모든 요약 행마다 하나씩 존재하며, 해당 지원의 `stage_history[]`와 `notes[]` 보관.
- 최소 1개 회사에 대한 `CareerLoop/contacts/<company-slug>.json`, 각 연락처는 `"<company> — <role>"` 형식의 `application` 레이블 보유.
- `CareerLoop/artifacts-index.json`: 이력서 1개 이상과 자기소개서 1개 이상 등록.

---

## Phase 1A — 핵심 플랫폼

### 범위
- 런치 마법사(`/careerloop:launch`), 프로필 생성, ExperienceLibrary 초기화, focus-career 동작, 실시간 채용 검색.

### 테스트
- `/careerloop:launch` 실행, `CareerLoop/`에 모든 핵심 파일 생성 확인.
- 런치 마법사가 기존 문서를 처리하고 ExperienceLibrary 유닛을 구축하는지 확인.
- 새 세션 시작 후 `focus-career` 동작 확인 (최초 실행 온보딩 vs 중요 알림 전용).
- `/careerloop:search-jobs` 실행, Indeed에서 결과가 반환되고 지원 링크가 포함되는지 확인.

### 통과 기준
- 핵심 파일이 유효하고 읽을 수 있음.
- 프로필 기반 기본값으로 채용 검색이 동작함.
- 최초 실행 상태와 재방문 사용자 상태 모두에서 세션 동작이 올바름.

### 예시 프롬프트 (복사/붙여넣기)

```text
/careerloop:launch
```

```text
Set up CareerLoop using my job search folder. Build profile and ExperienceLibrary from the resumes already in this directory.
```

```text
Search for jobs matching my profile—top 5 with apply links.
```

```text
/careerloop:search-jobs
```

```text
Session just started—run focus-career for critical-only alerts using my CareerLoop data.
```

---

## Phase 1B — 스킬 계층 및 인텔리전스

### 범위
- 워크플로 스킬, 트래커 수명주기, ATS 점수화, 분석가 피드백 루프, `job-scout` 기준선.

### 테스트
- `tailor-resume`와 `cover-letter` 실행, 아티팩트가 기록되고 색인되는지 확인.
- `resume-score`와 `ats-optimization` 실행, ATS 출력과 수정 가이드 확인.
- 단계 전환 전반(applied -> interview -> offer/rejected)에 걸쳐 `track-application` 실행; 전환마다 `applications/<application_id>.json` → `stage_history[]`에 추가가 반영되었는지, 그리고 `tracker.json` 요약 행의 `status`, `stage_count`, `latest_stage`, `latest_stage_date`가 같은 쓰기에서 갱신되었는지 확인.
- `pattern-analysis` 실행, 각 행의 `detail_file`을 로드하는지(단계 이력은 다른 어디에도 없음 — `tracker.json`만으로 계산하면 0이 나옴) 그리고 `search_performance`와 ExperienceLibrary 가중치 갱신이 기록되는지 확인.
- `search-jobs` 실행, pattern-analysis 갱신 후 순위가 바뀌는지 확인.

### 통과 기준
- 아티팩트와 지원 레코드 갱신이 스키마와 일관되게 유지됨: `tracker.json` 요약 행 안에 `notes`, `stage_history`, `contacts` 배열이 다시 나타나지 않음; 모든 `detail_file`이 해석됨; `notes_count` / `stage_count` / `contact_count`가 집계 대상 배열과 일치; 지원 id는 서술형 슬러그(`app-hex-senior-pm`)를 유지하며 UUID나 `app-NNN` 형식은 사용하지 않음.
- 분석가 출력이 하위 순위 입력으로 전달됨.

### 예시 프롬프트 (복사/붙여넣기)

```text
/careerloop:add-source
```
```text
Ingest my latest resume PDF in this folder into the ExperienceLibrary.
```

```text
Here's the job description [paste JD]. Tailor my resume for this role.
```

```text
/careerloop:tailor-resume
```

```text
/careerloop:cover-letter
```
```text
Write the cover letter for the role whose JD I just used—use my tailored resume artifact if it exists.
```

```text
Score my resume against this JD and tell me ATS gaps: [paste resume + JD].
```

```text
/careerloop:resume-score
```

```text
I just applied to [Company] for [Role] on [date]. Log it in the tracker.
```

```text
/careerloop:track-application
```

```text
What's converting in my pipeline? Run pattern-analysis and update weights.
```

```text
/careerloop:pattern-analysis
```

```text
/careerloop:list-artifacts
```

```text
List my generated resumes and cover letters with dates and linked applications.
```

```text
This resume has bad ATS structure—run ats-optimization and give me prioritized fixes.
```

```text
Run the full analyst report and point me to the dashboard for charts I shouldn't miss.
```

```text
Run full career analysis / pipeline dashboard generation so I can open the HTML dashboard.
```

---

## Phase 1C — 어드바이저 계층

### 범위
- 솔직한 평가, 시장 인텔리전스, 교육 ROI, 역할 전략 신호.

### 테스트
- `/careerloop:assessment` 실행, norm/exception/strategy 출력과 신뢰도 등급 확인.
- `/careerloop:training-roi` 실행, 옵션 매트릭스 + 주 권장안/대안 권장안 확인.
- `/careerloop:market-brief` 실행, demand/displacement/geography 섹션 확인.
- `/careerloop:suggest-roles` 실행, `strategy_signals`가 `tracker.json`의 최상위 키로 기록되는지 확인 (상세 파일에는 기록되지 않음).
- `search-jobs` 재실행, 근거/점수 동작에 전략 신호 차원이 나타나는지 확인.

### 통과 기준
- 어드바이저 출력이 근거에 기반하고 순위 전략과 연결됨.
- `strategy_signals`가 존재하며 `job-scout`가 사용할 수 있음.

### 예시 프롬프트 (복사/붙여넣기)

```text
/careerloop:assessment
```
```text
Give me an honest assessment vs my target role using my tracker and ExperienceLibrary—norm, exceptions, and strategy.
```

```text
/careerloop:training-roi
```
```text
Is a part-time MBA worth it for my target role in the next 18 months? Compare to self-study and a certificate.
```

```text
/careerloop:market-brief
```
```text
Market brief for my primary target role and location—demand, AI displacement, geography.
```

```text
/careerloop:suggest-roles
```
```text
What non-obvious roles should I apply to based on transferable skills? Update job-scout signals if you can.
```

---

## Phase 1D — 선제적 발굴

### 범위
- 튜닝된 `job-scout` 점수화, 신뢰도 인식 가중치, 선제적 추천 등급, 스케줄 실행 준비 운영.

### 테스트
- 결과 이력 데이터셋이 적은 경우와 많은 경우로 `search-jobs` 실행, 신뢰도 등급과 적응형 동작 확인.
- 추천 등급(`critical`, `high`, `watch`, `none`)과 우선순위 요약 출력 검증.
- `daily-schedule` 실행, 아티팩트 정합(reconciliation)과 다이제스트 출력 확인.
- 새 PDF/DOCX 원본 파일 추가 후 `daily-schedule` 실행; 자동 수집 경로(`add-source`)와 색인 일관성 확인.
- `suggest-roles`와 `market-brief` 실행, 정확한 에이전트 이름으로 에이전트 호출이 성공하는지 확인.

### 통과 기준
- 순위가 안정적이고 설명 가능하며 신뢰도를 반영함.
- 일일 워크플로가 새 원본 파일을 자동으로 처리함.
- 에이전트 호출 실패가 정의된 대로 재시도/대체 처리됨.

### 예시 프롬프트 (복사/붙여넣기)

```text
Find jobs for my target role and rank them—call out critical and high alerts if any.
```

```text
/careerloop:search-jobs
```

```text
Run my daily brief: reconcile artifacts if needed, pipeline summary, follow-ups due.
```

```text
/careerloop:daily-schedule
```

```text
I added a new resume PDF to my job search folder—run daily-schedule and confirm add-source ran if a new source appeared.
```

```text
/careerloop:market-brief
```
```text
/careerloop:suggest-roles
```
**기대 결과:** 정확한 에이전트 이름 **`market-researcher`**와 **`honest-advisor`** 사용 (스킬 규정에 따른 1회 재시도 동작).

---

## Phase 1E — 전문가로서의 존재감

### 범위
- 스킬 **`networking-strategy`**, **`network-map`**, **`event-intelligence`**, **`event-radar`**가 호출하는 **`networking-strategist`** 에이전트.
- **`draft-outreach`**, **`content-suggest`**, **`evaluate-post`**가 호출하고 **`cover-letter`**, **`follow-up`**, 선택적 **`tailor-resume`** Summary 다듬기에서 오케스트레이션되는 **`writer`** 에이전트; **`networking-strategist`**의 핸드오프와 **`voice-profile.md`**(사용자가 제공한 게시물)를 입력으로 사용.

### 테스트 데이터 (권장)
- **Target Roles**, **Target Companies**(또는 `tracker.json`에서 추론), **Location**(로컬 한정 vs 원격/출장 가능 여부가 event-radar 범위에 영향)이 있는 `CareerLoop/profile.md`.
- 요약 행에 **`contacts_file`**과 일치하는 **`contact_count`**가 있는 지원 1건 이상, 그리고 해당 `contacts/<company-slug>.json` 파일(항목은 비어 있어도 됨) — 격차/경로 로직 검증용. 연락처는 더 이상 `tracker.json` → `applications[]` 안에 두지 않음.
- 선택: 생성 vs 갱신 동작 검증을 위한 오래되었거나 없는 `CareerLoop/network-map.md`.

### 예시 프롬프트 (복사/붙여넣기)

자연어 또는 이에 해당하는 **`/careerloop:…`** 명령을 사용합니다. 회사명, 역할, 행사는 본인의 **`CareerLoop`** 데이터에 맞게 바꿔 사용합니다.

#### **`networking-strategy`** — 기본 계획

```text
I need a networking strategy for my job search. Use my CareerLoop profile and tracker—prioritize the next 90 days and the top 5 relationship moves I should make.
```

```text
/careerloop:networking-strategy
```

#### **`networking-strategy`** — 아웃리치 경계 (전략가는 즉시 발송 가능한 문안을 작성하면 안 됨)

```text
Run my networking strategy using profile + tracker, and in the same answer write the exact LinkedIn DM I should send to a hiring manager at my top target company—ready to paste.
```

**기대 결과:** 핸드오프 브리프 + **`writer`** 또는 **`/careerloop:draft-outreach`**로의 안내이며, **`networking-strategist`**가 완성된 DM을 작성하지 않음.

#### **`network-map`** — 경로, 격차, JSON

```text
Map my network toward my dream roles and target companies. Label confirmed vs hypothetical paths, call out gaps, and include the network_map_v1 JSON block for later visualization.
```

```text
/careerloop:network-map
```

#### **`network-map`** — 저장 제안

```text
After you produce the network map, save the narrative and the network_map_v1 JSON to CareerLoop/network-map.md in my job search folder.
```

#### **`event-intelligence`** — 지정 행사 (ROI + 발표 플래그)

```text
Should I attend [name a real conference or meetup you are considering] for my job search? Assess ROI, audience quality, whether it's worth travel/time/money, and flag if there's a realistic speaking or visibility opportunity. If you don't have verified dates or prices, tell me exactly what to look up instead of guessing.
```

```text
/careerloop:event-intelligence
```
*(그런 다음 같은 스레드에 행사 이름과 제약 조건을 붙여넣습니다.)*

#### **`event-radar`** — 다중 범위 탐색

```text
Run an event radar for my interests and target roles: local and regional events first, then national, then international if my profile supports travel. Give ROI tiers, presentation flags, and real links—or search queries if links aren't available.
```

```text
I'm only looking locally—no travel. Scan my metro area for the next 3 months for meetups and conferences relevant to my target role. Skip national/international unless virtual.
```

```text
/careerloop:event-radar
```

#### **Phase 2A 정직성** (연결되지 않으면 받은편지함 접근 불가)

```text
Before we draft any outreach, summarize what I last emailed anyone at [Company X] and pull thread context from my inbox.
```

**기대 결과:** 이메일/캘린더 접근이 불가능하다는 (또는 Phase 2A + 사용자 승인이 필요하다는) 명확한 안내 — 스레드 요약을 지어내지 **않음**.

#### **`cover-letter`** (**`writer`** 오케스트레이션)

```text
/careerloop:cover-letter
```
```text
Write a cover letter for this role. [paste job description]. Use my tailored resume from artifacts if available.
```

#### **`follow-up`** (**`writer`** 오케스트레이션)

```text
What needs a follow-up? Show the queue and draft messages for anything overdue or critical.
```
```text
/careerloop:follow-up
```

#### **`writer`** — 직접 호출 스킬

**아웃리치 초안 작성**

```text
/careerloop:draft-outreach
```
```text
Draft a short LinkedIn note to a [peer IC | recruiter | hiring manager] at [Company]. Goal: informational conversation, not asking for a job in the first message. Tone: direct and respectful. Here's the handoff from my networking strategy: [paste handoff bullets].
```

**주제 아이디어**

```text
/careerloop:content-suggest
```
```text
Suggest three LinkedIn post ideas for the next month that support my target roles without sounding desperate. Flag any that might clash with employers I'm targeting.
```

**게시물 검토**

```text
/careerloop:evaluate-post
```
```text
Evaluate this draft post for audience fit and cultural risk relative to my target companies: [paste draft].
```

```text
Review this draft for political or reputational risk against my target employers in profile.md—risk tier and safer paraphrases only, don't tell me what to believe: [paste draft].
```

```text
/careerloop:evaluate-post
```

#### **`writer`** — 보이스 프로필 (시드 + 갱신)

```text
I'm going to use you for outreach and posts. Here are 3 LinkedIn posts I've written—capture my voice in CareerLoop/voice-profile.md and give me a voice_profile_v1 JSON block.

[paste posts]
```

```text
Before drafting anything else, read my voice-profile.md and tell me your confidence in matching my tone (high/medium/low).
```

#### **`tailor-resume`** — 선택적 보이스 정렬 Summary (**`writer`** 오케스트레이션)

```text
Tailor my resume for this JD, and for the Summary section only, match the voice in my voice-profile.md / pasted LinkedIn samples—use resume-coach ResumeSummaryBrief then writer resume-summary.

[paste JD]
```

#### **엔드투엔드: 전략가 핸드오프 → 아웃리치**

```text
Run networking-strategy from my profile and tracker, then I'll paste your handoff bullets into draft-outreach—don't draft my DM in the strategist step.
```
*(이어지는 후속 턴에서:)*
```text
/careerloop:draft-outreach — use this StrategistHandoff: [paste bullets from prior turn]
```

#### **감사 메일 후속 조치** (**`follow-up`** + **`writer`** 검증)

```text
I had a phone screen for [Role] at [Company] three days ago—what's my follow-up status and draft a thank-you if I'm due.
```

#### **에이전트 호출 / 재시도** (호스트 의존)

재시도 동작은 단일 사용자 프롬프트가 아니라 로그 또는 호스트의 에이전트 도구를 관찰하여 검증합니다. 일시적 실패 후 같은 **`network-map`** 또는 **`event-radar`** 프롬프트를 두 번 실행하여 스킬 규정에 따라 1회 재시도 후 복구되는지 선택적으로 확인합니다.

### 에이전트: **`networking-strategist`**

#### 호출 및 오케스트레이션
- 각 스킬 본문에서 모델이 **정확한** 에이전트 이름 **`networking-strategist`**를 사용하는지 확인 (“network”나 “strategy agent” 같은 별칭 불가).
- 하위 에이전트 호출 실패를 모사하거나 관찰하여, 오류를 노출하기 전에 같은 이름으로 **1회 재시도**하는지 확인 (스킬 지침 기준).

#### 역할 경계 (아웃리치 vs 전략)
- 같은 턴에서 “write my LinkedIn message”라는 명시적 요청과 함께 **`networking-strategy`** 실행.
  - **기대 결과:** **`networking-strategist`**가 즉시 발송 가능한 DM/이메일 본문을 작성하지 않고, **핸드오프 브리프**(목표, 대상 아키타입, 근거 기반 훅, 톤, 피해야 할 목록)와 최종 문안을 위한 **`writer`** 또는 **`/careerloop:draft-outreach`** 안내를 제시.
- **`network-map`** 실행; 출력에 전체 아웃리치 초안이 포함되지 않고 전략, 경로 레이블, 격차, JSON, 선택적 핸드오프 요점만 포함되는지 확인.

#### Phase 2A 정직성
- 이메일/캘린더 커넥터가 없을 때 에이전트가 받은편지함이나 이전 스레드에 접근할 수 있다고 주장하지 **않는지** 확인; Phase 2A를 언급하는 경우 서신을 지어내지 않고 필요한 조건을 설명해야 함.

### 스킬

#### **`networking-strategy`**
- 계획에 **기간이 정해진** 흐름(예: 90일 프레이밍), **우선순위화된 행동**, **피해야 할 사항**이 포함되는지 확인.
- 사용자가 출력을 저장하는 경우, `CareerLoop/networking-strategy.md`(또는 날짜가 붙은 동등한 섹션)에 대한 선택적 저장이 다른 `CareerLoop` 파일을 손상시키지 않는지 확인.

#### **`network-map`**
- **confirmed** 경로와 **hypothesis** 경로가 레이블링됨; 브리지 **페르소나**는 사용자가 실제 이름을 제공하지 않는 한 아키타입임.
- 펜스 처리된 **`network_map_v1`** JSON 블록이 존재하며 `schema`, `as_of`, `nodes`, `edges`, `gaps`, **`viz_note`**(그래프 시각화는 보류) 포함.
- 사용자가 동의하면 **`CareerLoop/network-map.md`** 작성/갱신을 제안; 파일을 다시 읽어 서술과 JSON이 함께 존재하는지 확인.

#### **`event-intelligence`**
- **지정된** 행사의 경우: ROI 평가, 청중/준비도 신호, **발표 기회**(`yes` / `maybe` / `no`), **위험**(pay-to-play, 낮은 신호).
- 날짜, 가격, CFP 마감일을 **지어내지 않음** — 검증 가능한 출처를 인용하거나 확인할 **검색어/URL**을 제시.

#### **`event-radar`**
- 결과가 프로필에 맞게 **local → regional → national → international** 순으로 그룹화 또는 레이블링됨(프로필이 엄격히 로컬이고 사용자가 출장 없음을 확인하면 international 생략).
- 각 후보에 **ROI 등급**(예: A/B/C), **발표 플래그**, **링크 또는 명시적 확인 단계** 포함; 지어낸 컨퍼런스 없음.

### **`writer`**

#### 보이스 및 저장
- 최초 실행: 에이전트가 **샘플 게시물 2~5개**(또는 유사한 업무 글)를 요청하고 선택적 **`voice_profile_v1`** JSON과 함께 **`CareerLoop/voice-profile.md`**에 추가할지 제안하는지 확인.
- 샘플 추가 후 **`evaluate-post`** 재실행; **voice match** 신뢰도 레이블이 갱신되거나 근거가 샘플을 참조하는지 확인.

#### 스킬
- **`draft-outreach`:** 즉시 발송 가능한 문안; 지어낸 공통 이력 **없음**; 사용자가 붙여넣으면 **StrategistHandoff** 수용; 받은편지함 맥락이 없을 때 **Phase 2A** 안내.
- **`content-suggest`:** 프로필/ExperienceLibrary에 연결된 주제; 선택적 전체 초안 경로 + **`evaluate-post`** 권유.
- **`evaluate-post`:** 프로필의 **대상 회사** 대비 **위험 등급** + 근거; 선택적 더 안전한 표현 대안; “무엇을 믿어야 하는지”에 대한 지시 없음.
- **`cover-letter`:** 먼저 **CoverLetterBrief**가 구축되는지 확인한 뒤 **`writer`**(`cover-letter` 모드)가 최종 편지를 생성; 아티팩트 저장은 변경 없음.
- **`follow-up`:** 스킬 안에는 **FollowUpBrief** 객체만 있는지 확인; 메시지 본문은 **`writer`**(`follow-up` 모드)에서 생성.
- **`tailor-resume`**(선택): “match my LinkedIn voice for the Summary only”를 요청; 저장 전에 **`ResumeSummaryBrief`** → **`writer`**(`resume-summary`) → 병합된 Summary 순서로 진행되는지 확인.

### 통과 기준
- **`networking-strategist`** 출력이 근거에 기반하고 신뢰도 레이블이 있으며, 아웃리치 문안에서 **`writer`**를 **대체하지 않음**.
- 행사 출력이 환각된 운영 정보를 피하고 불확실성을 명시적으로 밝힘.
- **`writer`**가 사용자 대면 문장(아웃리치, 자기소개서, 후속 조치, 선택적 Summary 다듬기)을 담당; 브리프는 오케스트레이션 스킬 안에 유지; **`voice-profile.md`** 갱신은 명시적이며 옵트인.

---

## Phase 1F — 커리어 계획, 오퍼 평가 및 연봉 협상

### 범위
- 신규 스킬: `career-plan`, `evaluate-offer`, `negotiate-offer`, `compare-offers`
- 아티팩트 출력:
  - `{user_dir}/CareerLoop/career-trajectory.md` (보고서)
  - `{user_dir}/CareerLoop/career-trajectory-data.json` (`career_trajectory_v1`)
  - `{user_dir}/CareerLoop/offer-context-{application_id}.json`
- 연동:
  - `job-scout`가 `career_trajectory_v1`을 읽어 경로 정렬 가산점 적용
  - `daily-schedule` 월간 커리어 계획 갱신 알림
  - `daily-schedule` 오퍼 평가 기한 알림
  - `focus-career`: 마감이 임박했을 때 오퍼 평가 기한을 critical 전용 알림으로 표시

### 테스트 데이터 사전 조건
- 목표 역할 + 목표 지역이 채워진 `CareerLoop/profile.md`.
- 비어 있지 않은 `units`가 몇 개 이상 있는 `CareerLoop/ExperienceLibrary.json`.
- 다음을 포함하는 `CareerLoop/tracker.json`:
  - `status: "offer"`인 지원 1건 이상(가능하면 `offer.deadline` 포함).
  - `honest-advisor`가 신뢰도 등급을 표기할 수 있도록 다양한 결과 혼합.

### 테스트
- `/careerloop:career-plan` 실행
  - `career-trajectory.md`(사람이 읽을 수 있는 보고서) 생성 확인.
  - 유효한 `career_trajectory_v1` 스키마로 `career-trajectory-data.json` 생성 확인.
- `/careerloop:evaluate-offer` 실행
  - 올바른 오퍼 지원 건에 대해 `offer-context-{application_id}.json` 생성 확인.
  - 오퍼 평가에 시나리오 분류와 직접적인 권고가 포함되는지 확인.
- `/careerloop:negotiate-offer` 실행
  - OfferContext를 로드하고(중복 재수집 없음) `writer`를 통해 초안을 생성하는지 확인.
- 오퍼가 여러 개일 때 `/careerloop:compare-offers` 실행
  - 나란히 비교하고 협상 핸드오프를 안내하는지 확인.
- `/careerloop:search-jobs` 실행
  - `job-scout` 출력에 경로 정렬이 포함되고 점수에 반영되는지 확인.
  - 경로 근거가 명시적인지 확인: `trajectory_context_status`와 `trajectory_as_of`가 반환되고 사용자 대면 출력에 경로 맥락 줄이 포함됨.
- `/careerloop:daily-schedule` 실행
  - `career-trajectory-data.json`이 없거나 오래된 경우 월간 커리어 계획 갱신을 안내하는지 확인.
  - 활성 오퍼가 있는데 OfferContext가 없는 경우 오퍼 평가 기한을 안내하는지 확인.
- 마감 경계 사례로 `focus-career` 실행
  - 24시간 이내 마감이면서 OfferContext가 없는 트래커 오퍼를 생성/준비.
  - `focus-career`가 "Offer evaluation due" critical 알림을 포함하는지 확인.

### 통과 기준
- 모든 신규 슬래시 명령이 올바른 트리거와 함께 존재함.
- 필수 아티팩트가 지정된 `{user_dir}` 경로에 기록됨 (또는 수동 저장 대체 안내가 표시됨).
- `career-trajectory-data.json`이 있으면 `job-scout` 경로 가산점이 존재하고, 없으면 명시적으로 부재함.
- 알림이 `daily-schedule`에 나타나며 (마감 임박 시) `focus-career`에도 나타남.

### 예시 프롬프트 (복사/붙여넣기)

#### `career-plan` (기본)
```text
/careerloop:career-plan
```

#### `career-plan` (목표 이상적 역할)
```text
/careerloop:career-plan
Ideal role: Senior Product Manager
```

#### `evaluate-offer` (단일 오퍼)
```text
/careerloop:evaluate-offer
I received an offer from Acme for a Senior PM role. Deadline is 2026-04-02.
Base: $150k, bonus: $20k, equity: $60k. Location: Chicago.
```

#### `negotiate-offer`
```text
/careerloop:negotiate-offer
Use my last OfferEvaluation to draft a counter. Keep it assertive but respectful.
```

#### `compare-offers` (복수 오퍼)
```text
/careerloop:compare-offers
Compare these two offers and tell me which one best matches my near-term trajectory.
```

#### 일일 알림
```text
/careerloop:daily-schedule
```

### 1차 수정 — 리패키징 회귀 점검

리패키징 후 최근의 명칭, 오케스트레이션, 시작 동작 수정 사항을
확인하기 위한 집중 점검에 사용합니다.

#### 범위 점검
- `focus-career` 명칭으로 시작 동작이 동작.
- 자동 훅이 실행되지 않을 때 세션 시작 훅 대체 안내가 명확.
- `search-jobs`가 **Recommendation** 레이블 사용 (Alert 아님).
- `search-jobs`/`job-scout`의 경로(trajectory) 반영이 출력에 명시적으로 드러남.

#### 테스트
- 새 명령으로 시작 동작을 수동 실행:
  - 호출된 스킬이 `focus-career`인지 확인.
  - critical 전용 출력 형식이 변경되지 않았는지 확인.
- 유효한 `career-trajectory-data.json`이 있는 상태에서 `search-jobs` 실행:
  - 출력에 경로 맥락 줄이 포함되는지 확인:
    - `Trajectory context: used (as_of YYYY-MM-DD)` (또는 사용 불가 사유)
  - 목록 줄이 `Recommendation: {critical|high|watch|none}` 형식을 사용하는지 확인.
- 경로 파싱 실패를 일시적으로 유발(또는 `career-trajectory-data.json` 제거/이름 변경):
  - 검색은 계속 동작하며 경로를 사용 불가/파싱 불가로 보고하는지 확인.

#### 통과 기준
- `focus-career`가 컨텍스트/출력에서 기본 시작 스킬 이름임.
- 자동 SessionStart 훅이 실행되지 않는 세션에서도 수동 대체 경로가 동작함.
- 검색 결과에 사용자 대면 `Alert:` 레이블이 남아 있지 않음.
- 경로 사용 여부를 응답 텍스트와 점수 근거에서 감사(audit)할 수 있음.

#### 예시 프롬프트 (복사/붙여넣기)

```text
/careerloop:focus-career
```

```text
/careerloop:focus-career
```

```text
/careerloop:search-jobs
Use my current profile targets and show top 5.
```

```text
For each result, include the scoring header plus trajectory context status and recommendation tier.
```

```text
I got an offer from Stripe for Senior Product Manager, and the decision deadline is tomorrow at 10am. Please update my tracker.
Then run /careerloop:focus-career.
```

---

## Phase 2A — 이메일 및 캘린더 연동

### 범위
- 서신 및 캘린더 맥락을 위한 OAuth 커넥터.

### 테스트
- 커넥터 설정과 권한 요청 프롬프트 검증.
- 연락처 맥락 보강이 사용자가 승인한 경우에만 나타나는지 확인.
- 캘린더 데이터 기반의 아침/당일 맥락 검증.

### 통과 기준
- 읽기 전용 연동이 명시적 동의 경계 안에서 안정적으로 동작함.

### 예시 프롬프트 (복사/붙여넣기)

```text
Search my Gmail for prior threads with [Name] at [Company] and summarize only what you find—I approve access for this session.
```
**기대 결과:** Phase 2A 커넥터가 구성되고 사용자가 명시적으로 승인한 경우에만 동작하며, 그렇지 않으면 명확한 **접근 불가** 안내.

```text
Before /careerloop:draft-outreach to [recruiter], pull last email exchange from calendar/email context and fold into the brief.
```

---

## Phase 2B — 면접 인텔리전스

### 범위
- 면접 준비(`prep-interview`, **`interview-coach`**), 모의 면접 모드(모드/vibe 생략 시 **기본값**, 텍스트 전용), **`interview-capture`** **스킬**(에이전트 아님, **`mcp-transcribe`** 사용 — **`CONNECTORS.md`** 참조), **`daily-schedule`**의 일부인 **Pre-interview brief**(“morning brief before my interview” 같은 요청 = 집중형 실행). **`interview-debrief`**는 보류 상태일 수 있음.
- **폐기됨:** `mcp-voice` MCP와 아래의 TTS/STT 스모크 테스트(2B-A2, 2B-A3, 2B-V1)는 안정적으로 시작되지 않는 것으로 나중에 확인된 번들을 다루었으며(`mcp-transcribe/README.md`의 "Why this replaced mcp-voice" 참조) 더 이상 배포되지 않습니다. 이력 기록용으로만 남겨 두었으며, 현재 릴리스 검증에는 사용하지 않습니다.

### 테스트
- 여러 단계/vibe에 걸쳐 준비 + 모의 면접 실행.
- **모드/vibe 없는 `mock-interview`:** 첫 질문 전에 모델이 선택된 `mock_mode` + `vibe`(기본값은 §2.1 기준)를 **공지**.
- 요약 행의 **`latest_stage_date`**가 **오늘**이고 **`latest_stage`**가 허용 목록에 있을 때(또는 미래 날짜 행의 `detail_file`에 오늘 날짜의 `stage_history` 항목이 숨어 있을 때) **daily-schedule**에 **Pre-interview brief**가 포함되는지 검증; 해당 없으면 **생략**되는지 검증.
- “오늘 면접 브리프” 같은 요청으로 집중형 출력 검증 (해당하는 경우에만 면접 전 슬라이스).
- 준비 후 `applications/<application_id>.json` → `notes[]`에 **`[prep]`** 노트가 추가되고 요약 행의 `notes_count`가 증가하며, `CareerLoop/interview-prep/` 아래에 브리프 파일이 생성.
- **`mcp-voice` MCP(Claude Desktop Extension `mcp-voice.mcpb`):** **TTS** — 짧은 문자열로 **`speak`** 호출; 로컬 스피커로 오디오가 재생되고 `"Speech complete."` 응답이 오는 것을 기대. **STT** — **`listen`** 호출 후 짧은 문구를 말함; 말한 내용과 일치하는 전사 텍스트가 반환되는 것을 기대.
- **`interview-capture`:** 옵트인 흐름; 고용주 경고는 1회; 전사 처리 시 **`[capture]`** 또는 구조화된 노트가 해당 지원의 `detail_file`에 추가되고 같은 트랜잭션에서 요약 행의 카운터가 갱신.
- **출시 전까지 보류:** 아직 없는 경우 **`interview-debrief`** 전체 자동화.

### 통과 기준
- 면접 준비와 모의 면접 워크플로가 일관됨; 음성/STT는 **사용자 오디오 전용** 가정; 독립형 **`morning-brief`** 스킬 없음.

### 구조화된 테스트 케이스 (ID)

| ID | 시나리오 | 통과 힌트 |
| --- | --- | --- |
| 2B-P1 | 트래커에 있는 HM + 회사에 대한 `/careerloop:prep-interview` | 브리프 파일 + `applications/<application_id>.json`의 `[prep]` 노트, 행의 `notes_count` 증가; ExperienceLibrary 인용 |
| 2B-P2 | **리크루터 스크리닝** 준비 | 프로세스, 보상, 일정, 직무 적합성 강조 |
| 2B-D1 | §3.1 허용 목록 기준 오늘 미팅이 **없는** 상태의 `/careerloop:daily-schedule` | 출력에 **Pre-interview brief** 하위 섹션 **없음** |
| 2B-D2 | 요약 행의 `latest_stage_date`가 **오늘**이고 `latest_stage`가 interview/recruiter인 `daily-schedule` | **Pre-interview brief (today)** 표시; 1개 이상 회사 포함; 조건에 맞는 지원에 대해서만 상세 파일 열람 |
| 2B-D3 | “오늘 면접 브리프 보여줘” | 해당 시 2B-D2와 동일한 면접 전 동작; 사용자가 요청하지 않으면 전체 파이프라인 표 없음 |
| 2B-M1 | `mock-interview` adaptive, neutral, **recruiter** | 오디오를 요구하지 **않고** 세션 진행 |
| 2B-M2 | `mock-interview` challenging vibe, **hiring_manager** | 더 강한 어조/압박이 관찰됨 |
| 2B-M3 | 모드/vibe를 **지정하지 않은** `mock-interview` | 첫 질문 전에 선택된 모드 + vibe를 **공지** (예: adaptive + neutral) |
| 2B-A1 | **오디오 사용 불가** 상태의 준비 | 텍스트 전용으로 완료; 제한 사항을 1회 안내 |
| 2B-A2 | **STT**(`listen`)를 사용한 준비/모의 면접 | 마이크 녹음 → 전사 텍스트가 말한 내용과 일치 |
| 2B-A3 | **TTS**(`speak`) | 로컬 스피커로 오디오 재생; `"Speech complete."` 반환 |
| 2B-V1 | **엔드투엔드 음성**(선택) | `speak`가 질문을 음성으로 전달; `listen`이 음성 답변을 캡처; 전사가 다음 모의 면접 턴에 사용됨 |
| 2B-C1 | 옵트인 상태의 `/careerloop:interview-capture` | 경고 1회; `interview-capture-settings.json`; STT 후 상세 파일 노트 + 요약 행 카운터 갱신 |

### 예시 프롬프트 (복사/붙여넣기)

```text
/careerloop:prep-interview
```
```text
Prep me for my upcoming HM interview at [Company] for [Role]—questions, stories, company angles.
```
```text
Prep me for a recruiter phone screen at [Company] for [Role].
```

```text
/careerloop:mock-interview
```
```text
Mock interview: recruiter stage, neutral vibe, adaptive difficulty. Company: [Company], role: [Role].
```
```text
/careerloop:mock-interview
```
```text
Mock interview for my Acme PM application — no other preferences.
```
**기대 결과:** 첫 질문 전에 선택된 **mode** + **vibe**(기본값)를 공지.

```text
/careerloop:interview-capture
```
```text
I want to log my interview from this WAV file: [path under job search folder]. I opt in for this session.
```

```text
오늘 면접 브리프 보여줘
```
```text
I have interviews today—give me the morning brief with news and talking points.
```

```text
/careerloop:daily-schedule
```
```text
Run my full daily brief (expect Pre-interview section only if something is scheduled today in the tracker).
```

#### `mcp-voice` MCP — TTS 스모크 테스트 (2B-A3)

```text
Say this aloud: "Your mock interview for Acme will begin in 10 seconds. Take a breath and get ready."
```
**기대 결과:** 로컬 스피커로 즉시 오디오가 재생되고, 응답은 `"Speech complete."`; 링크도 파일도 없이 소리만 출력.

#### `mcp-voice` MCP — STT 스모크 테스트 (2B-A2)

```text
Listen for 10 seconds. I'll say my name and target role — then confirm you heard me correctly.
```
**기대 결과:** `listen` 도구가 `duration_seconds=10`으로 호출됨; 반환된 전사가 발화 내용과 일치; 모델이 확인을 위해 이를 되풀이함.

#### `mcp-voice` MCP — 엔드투엔드 음성 턴 (2B-V1)

```text
Ask me the first behavioral question for my [Company] HM interview using voice, then listen for my answer and give feedback.
```
**기대 결과:** 모델이 `speak`를 호출해 질문을 음성으로 전달한 뒤 `listen`을 호출해 응답을 캡처하고, 텍스트로 코칭 피드백을 제공.

```text
면접 후 Q&A 디브리프 해줘
```
```text
Interview debrief: I just finished a panel at [Company]. [paste notes].
```
**기대 결과:** **`interview-debrief`** 스킬이 출시되기 전에는 미구현; 현재는 아무 동작도 하지 않거나 **`track-application`** 노트를 사용하도록 안내할 수 있음.

---

## Phase 2C — 확장 연동

### 범위
- 클라우드 스토리지 및 ATS/채용 사이트 커넥터.

### 테스트
- **2C-S1 (앱 동기화/수동 백업을 통한 Google Drive, OneDrive, Dropbox 이식성):** 데스크톱 앱으로 로컬 `{user_dir}` 구직 폴더를 동기화(또는 폴더를 수동 백업/복원)해 폴더 내용을 로컬에서 사용 가능하게 한 뒤 `/careerloop:launch`를 실행하고, 어시스턴트가 구직 파일용 커넥터 연결을 요청하지 않으며 스토리지 동작이 로컬 우선으로 유지되는지 확인.
- **2C-F1 (커넥터/동기화 없음 대체):** 클라우드 스토리지 동기화/커넥터가 구성되지 않은 상태에서 launch를 실행하고, 지어낸 클라우드 상태 없이 스토리지 동작이 로컬 우선으로 유지되는지 확인.
- **2C-F2 (연결 해제 시 기능 저하):** 앱 동기화를 끈 뒤 launch/list 흐름을 다시 실행하고 로컬 동작으로 정상 대체되는지 확인.
- **2C-R1 (아티팩트 목록 동등성):** 스토리지 옵션을 선택한 뒤 `/careerloop:list-artifacts`를 실행하고 목록이 로컬 색인 의미와 일관되게 유지되는지 확인.
- ATS 읽기 커넥터가 쓰기 부작용 없이 상태를 반환하는지 검증.
- 추가 채용 사이트 소스 수집 및 중복 제거 동작 검증.

### 통과 기준
- 스토리지 온보딩이 안정적이며 제공자별로 범위가 구분됨:
  - Google Drive는 Drive 앱 동기화 또는 수동 백업/복원을 사용 (일반적인 구직 파일에 Drive 커넥터 의존 없음).
  - OneDrive는 OneDrive 앱 동기화 또는 수동 백업/복원을 사용 (플러그인 JSON 아티팩트에 Claude의 Microsoft 365/OneDrive 파일 접근 커넥터 의존 없음).
  - Dropbox는 Dropbox 앱 동기화 또는 수동 백업/복원을 사용.
- 클라우드 스토리지 동기화/커넥터가 없거나 연결 해제되어도 로컬 우선 동작이 유지됨.
- Google Drive/OneDrive/Dropbox 설정을 `.mcp.json`으로 안내하는 문서나 launch 프롬프트가 없음.

### 예시 프롬프트 (복사/붙여넣기)

```text
/careerloop:launch
```

```text
Use Google Drive for portability for this workspace via Drive app sync (sync the local job-search folder to Google Drive). Do not rely on connecting a Drive connector for job files.
```
**기대 결과:** 어시스턴트가 Drive 앱 동기화 또는 수동 백업/복원 절차를 권장하고 로컬 우선 동작을 계속함.

```text
/careerloop:launch
```
```text
Use OneDrive for portability for this workspace via OneDrive application sync (sync the local job-search folder to OneDrive) or manual backup/restore. Do not rely on connecting a OneDrive connector for job files.
```
**기대 결과:** 어시스턴트가 OneDrive 앱 동기화/수동 백업/복원 절차를 권장하고 로컬 우선 동작을 계속함.

```text
/careerloop:launch
```
```text
Set up cloud storage with Dropbox for this workspace. If it's already connected in this chat, acknowledge and skip setup steps.
```
**기대 결과:** 어시스턴트가 Dropbox 앱 동기화/수동 백업/복원 절차를 권장하고 로컬 우선 동작을 계속함.

```text
Run launch with local-only storage. Do not configure any cloud connector right now.
```
**기대 결과:** 어시스턴트가 로컬 `{user_dir}` 스토리지를 유지하며 클라우드 동기화를 주장하지 않음.

```text
I turned off Drive app sync (for Google Drive), paused OneDrive application sync (for OneDrive), or paused Dropbox application sync (for Dropbox). Re-run launch and confirm fallback behavior.
```
**기대 결과:** 연결 해제/비활성화 상태를 알리는 명확한 메시지와 로컬 우선 동작 지속.

```text
/careerloop:list-artifacts
```
```text
List artifacts after connector selection and confirm index consistency.
```
**기대 결과:** 스토리지 선택과 관계없이 아티팩트 목록이 일관되고 사용 가능한 상태로 유지됨.

```text
Show me how to set up Google Drive (Drive app sync or manual backup/restore), OneDrive (OneDrive app sync or manual backup/restore), and Dropbox (Dropbox app sync or manual backup/restore) for storage in Claude Desktop. Do not use `.mcp.json`.
```
**기대 결과:** Google Drive, OneDrive, Dropbox 안내가 모두 앱 동기화 또는 수동 백업/복원을 가리킴.

```text
Sync application status from Greenhouse for applications I logged—read-only, no writes to employer ATS.
```

---

## Phase 2D — 고급 분석 및 자동화

### 범위
- BI 커넥터 내보내기, 고급 분석, LinkedIn 자동화 표면.

### 테스트
- 구성된 BI 대상에 대한 내보내기 페이로드 검증.
- 로컬 데이터셋과 내보낸 데이터셋 간 대시보드/보고서 일치 검증.
- LinkedIn 관련 워크플로가 정책/위험 가드레일을 준수하는지 검증.

### 통과 기준
- 분석 출력이 일관되고 자동화 기능이 정책상 안전하게 유지됨.

### 예시 프롬프트 (복사/붙여넣기)

```text
Export my pipeline and analyst graph data in the format expected by our BI connector and show me the payload shape.
```

```text
/careerloop:pipeline-status
```
```text
Open the dashboard and confirm exported metrics match the local tracker counts for applied vs interview stages.
```

```text
Run a LinkedIn-automation workflow only if it complies with policy—show guardrails before executing.
```

---

## 회귀 체크리스트 (모든 단계에서 실행)

- 변경된 모든 스킬(**`draft-outreach`**, **`content-suggest`**, **`evaluate-post`** 포함)의 SKILL frontmatter(`name`, `description`, `triggers`)가 파싱되는지 검증.
- 핵심 JSON 파일(`tracker.json`, 모든 `applications/<application_id>.json`, 모든 `contacts/<company-slug>.json`, `ExperienceLibrary.json`, `artifacts-index.json`)이 유효하게 유지되고, 분리 레이아웃이 [tracker-schema.md](tracker-schema.md)에 따라 내부적으로 일관되는지 검증: 각 `detail_file`이 해석되고, 카운터가 해당 배열과 일치하며, `latest_stage`가 마지막 `stage_history` 항목과 일치.
- `search-jobs`, `track-application`, `tailor-resume`, `daily-schedule`를 스모크 테스트로 재실행.
- 문서가 실제 동작과 일치하는지 확인 (README + 스펙).
- **사용자 대면 동작을 출시하거나 변경한 경우**, 해당 단계 아래에 **`### 예시 프롬프트 (복사/붙여넣기)`**를 추가하거나 갱신 (이 파일 상단의 규칙 참조).
