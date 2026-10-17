---
name: salary-research
description: >
  Apify best-job-search 액터를 사용해 특정 직무와 지역의 실시간 보상 데이터를 가져옵니다. 연봉 정보가 있는 공고를
  최대 연봉 순으로 정렬한 마크다운 표와 보상 범위 요약(최소, 최대, 중앙값)을 반환합니다. 오퍼 평가, 직무 타기팅,
  명시적 요청 등 어떤 맥락에서든 보상이 언급되면 실행됩니다. 다음과 같은 요청에 사용합니다: "what's the salary for",
  "what does a [role] make", "salary range for", "benchmark my salary", "is this offer competitive",
  "이 직무 연봉이 얼마야?", "연봉 시세 알려줘", "이 오퍼 경쟁력 있어?".
  (Pulls live compensation data for a role and location using the Apify
  best-job-search actor. Returns a markdown table of salary-bearing listings
  sorted by maximum salary, plus a compensation range summary (min, max,
  median). Fires when compensation is mentioned in any context — offer
  evaluation, role targeting, or explicit request.)
triggers:
  - "what's the salary for"
  - "what does a [role] make"
  - "salary range for"
  - "how much do [role]s earn"
  - "compensation for"
  - "benchmark my salary"
  - "what should I be making"
  - "market rate for"
  - "salary data"
  - "pay range for"
  - "is this offer competitive"
  - "what are [role]s paid"
  - "이 직무 연봉이 얼마야"
  - "연봉 범위 알려줘"
  - "연봉 조사"
  - "보수 수준 알려줘"
  - "내 연봉 벤치마크해줘"
  - "얼마를 받아야 할까"
  - "시장 연봉 시세"
  - "이 오퍼 연봉 경쟁력 있어"
---

Apify MCP 서버를 통해 특정 직무와 지역의 실시간 연봉 데이터를 가져와 구조화된 보상 요약을 반환합니다.

## 사전 점검

다른 작업보다 먼저, 이 세션에서 Apify MCP 도구(예: **Call Actor**, **Get Actor run**, **Get dataset items**)를 쓸 수 있는지 확인합니다. 이 도구들은 사용자가 Claude **Customize → Connectors**에서 **Apify** **Desktop** 커넥터를 추가하고, 채팅이 아닌 커넥터 UI에 토큰을 붙여넣고, **Enabled tools**를 다음과 같이 설정하면 나타납니다.

`call-actor,get-actor-run,get-dataset-items,cheapget/best-job-search`

해당 도구를 쓸 수 **없다면**:
> "연봉 벤치마킹에는 Apify Desktop 커넥터가 필요합니다. Claude Desktop에서 **Customize → Connectors → Desktop → Apify → Configure**로 이동해 Apify 토큰을 추가하고, **Enabled tools**를 `call-actor,get-actor-run,get-dataset-items,cheapget/best-job-search`로 설정한 뒤 저장하고 커넥터를 활성화하세요. 그런 다음 **새 채팅**을 열어 다시 시도하세요. 자세한 안내는 `/careerloop:launch`의 Step 4를 실행하면 볼 수 있습니다."

여기서 중단합니다. MCP 연결 없이는 진행하지 않습니다.

## 워크플로

### 1. 입력 수집

대화에서 다음 항목을 추출합니다. 이미 말한 내용은 다시 묻지 않습니다.

| 입력 | 출처 | 필수 여부 |
|---|---|---|
| `keyword` | 대화 속 직무명 또는 `profile.md`의 `## Target Roles` | 필수 |
| `location` | 대화 속 지역 또는 `profile.md`의 `## Location` | 필수 |
| `remoteOnly` | 사용자가 언급한 경우("remote only", "fully remote", "재택만") | 선택 |
| `minSalary` | 사용자가 언급한 경우("above $120k", "minimum $150k", "1억 이상") | 선택 |

맥락이나 프로필에서 `keyword` 또는 `location`을 알 수 없으면 한 번의 질문으로 함께 묻습니다.
> "어떤 직무와 지역의 연봉 데이터를 가져올까요? (예: '시카고의 Senior Product Manager')"

### 2. Apify 액터 호출

Apify MCP `call-actor` 도구를 다음 파라미터로 사용합니다.

- **Actor ID:** `cheapget/best-job-search`
- **Input:**
```json
{
  "keyword": "<role title>",
  "location": "<city, state or country>",
  "maxResults": 25,
  "remoteOnly": <true if specified, omit otherwise>,
  "minSalary": <integer if specified, omit otherwise>
}
```

### 3. 응답 파싱

각 결과 레코드에서 다음 필드를 추출합니다.

| 필드 | 소스 키 |
|---|---|
| Title | `title` |
| Company | `company_name` |
| Location | `location` |
| Remote | `is_remote` |
| Salary min | `salary_minimum` |
| Salary max | `salary_maximum` |
| Currency | `salary_currency` |
| Platform | `platform` |
| URL | `platform_url` |
| Posted | `posted_date` |

### 4. 중복 제거

같은 `title` + `company_name` 조합이 여러 지역 변형으로 나타나면, `salary_maximum`이 가장 높은 레코드만 남깁니다. 모든 변형에서 `salary_maximum`이 null이면 `salary_minimum`이 가장 높은 레코드를 남깁니다. 모든 변형에서 연봉 필드가 전부 null이면 처음 나온 것을 남깁니다.

### 5. 필터링

`salary_minimum`과 `salary_maximum`이 **둘 다** null인 레코드를 제거합니다. 단, 제거하면 결과가 5개 미만이 되는 경우는 예외입니다. 필터링 후 연봉 정보가 있는 레코드가 5개 미만이면, 표가 여전히 쓸모 있도록 중복 제거된 모든 레코드(연봉 정보 유무 무관)를 포함합니다.

### 6. 정렬

남은 레코드를 `salary_maximum` 내림차순으로 정렬합니다. `salary_maximum`이 없는 레코드는 맨 아래에 두고, `salary_minimum` 내림차순으로 정렬합니다.

### 7. 출력

#### 연봉 공고 표

```
## 연봉 벤치마크 — {keyword} · {location}
Apify 제공 데이터 · {오늘 날짜} · 공고 {n}건

| 직무명 | 회사 | 지역 | 리모트 | 최소 | 최대 | 플랫폼 |
|---|---|---|---|---|---|---|
| [title](platform_url) | company_name | location | ✓ / — | $salary_minimum | $salary_maximum | platform |
```

- 연봉 값은 `$XXXk`(예: `$145k`) 형식으로 쓰고, 원본이 정확한 값을 제공하면 `$XXX,XXX`를 사용합니다. `salary_currency` 필드를 사용하며, USD가 아니면 통화 코드를 표시합니다(예: `£85k`).
- 레코드의 `salary_minimum` 또는 `salary_maximum`이 null이면 `—`를 표시합니다.
- `is_remote`가 true이면 ✓, 아니면 —를 표시합니다.
- 직무명에 `platform_url`을 하이퍼링크로 삽입합니다.
- `posted_date`가 있으면 상대 표기(예: "3일 전")로 표시하고, 어떤 레코드에도 없으면 해당 열을 생략합니다.

#### 보상 범위 요약

표 아래에, 연봉 필드가 하나 이상 채워진 레코드**만** 대상으로 계산한 요약 블록을 추가합니다.

```
### 보상 범위
- **하한:** $XXXk  (결과 전체에서 가장 낮은 salary_minimum)
- **중앙값:** $XXXk  (salary_maximum 값의 중앙값, max가 null이면 salary_minimum 사용)
- **상한:** $XXXk  (결과 전체에서 가장 높은 salary_maximum)
- **통화:** USD (혼재 시 그 사실을 표기)
- **산정 기준:** 전체 {total}건 중 연봉 데이터가 있는 {n}건
```

연봉 정보가 있는 레코드가 3개 미만이면 주의 문구를 추가합니다.
> "⚠️ 연봉 데이터가 포함된 공고가 {n}건뿐이어서 이 범위는 대표성이 없을 수 있습니다."

#### 맥락 메모

사용자가 특정 오퍼나 본인의 보상 하한선에 대해 물었다면, 범위와 비교한 한 문장을 추가합니다.
> "제안받은 기본급 $135k는 이 직무와 시장의 공고 범위 중 60번째 백분위에 해당합니다."

또는 프로필의 보상 하한선과 비교하는 경우:
> "보상 하한선 $120k는 공고 범위의 중앙값보다 낮습니다. 협상 여지가 있습니다."

비교할 구체적인 수치가 있을 때만 포함합니다. 비교를 지어내지 않습니다.

### 8. 오류 처리

**액터가 결과를 반환하지 않은 경우:**
> "Apify가 '{location}'의 '{keyword}'에 대한 연봉 데이터를 반환하지 않았습니다. 더 넓은 직함(예: 'Senior AI Product Manager' 대신 'Product Manager')이나 더 큰 대도시권으로 시도해 보세요."

**모든 결과가 필터링된 경우 (어떤 레코드에도 연봉 데이터 없음):**
> "'{location}'의 '{keyword}' 공고 {n}건을 찾았지만 연봉 정보가 포함된 공고는 없었습니다. 보상이 'competitive'나 'DOE'로 표기된 직무에서 흔한 일입니다. `minSalary` 필터를 추가해 급여를 공개한 공고가 나오도록 시도해 보세요."

**MCP 호출이 실패하거나 시간 초과된 경우:**
> "Apify 요청이 완료되지 않았습니다. Claude Desktop에서 **Customize → Connectors → Apify**를 열어 토큰과 **Enabled tools**(`call-actor,get-actor-run,get-dataset-items,cheapget/best-job-search`)를 확인하고, 저장한 뒤 커넥터를 활성화하고 **새 채팅**에서 다시 시도하세요. 전체 안내가 필요하면 `/careerloop:launch`의 Step 4를 참고하세요."
