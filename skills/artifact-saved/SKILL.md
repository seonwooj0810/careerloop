---
name: artifact-saved
description: "아티팩트 저장 후 실행됩니다. 사용자 구직 폴더의 artifacts-index를 디스크의 실제 파일과 대조·정합화하고, 분석에 쓸 수 있는 아티팩트 이벤트 요약을 준비합니다. (Runs after artifact writes. Reconciles artifacts-index with files on disk in the user job search folder and prepares an analytics-ready artifact event summary.)"
triggers:
  - "reconcile artifacts index"
  - "sync artifacts index with files"
  - "fix artifacts-index.json"
  - "refresh artifact inventory from disk"
  - "/careerloop:artifact-saved"
  - "아티팩트 색인 맞춰줘"
  - "아티팩트 색인을 파일과 동기화해줘"
  - "artifacts-index.json 고쳐줘"
  - "디스크 기준으로 아티팩트 목록 갱신해줘"
---

> **구직 폴더(`{user_dir}`) 확인:** 먼저 현재 작업 디렉터리에서 `CareerLoop/` 폴더(또는 한 단계 위·아래)를 찾아 그 폴더가 들어 있는 디렉터리를 `{user_dir}`로 쓴다. 홈 디렉터리 전체를 검색하지 않는다. 작업 디렉터리에서 찾지 못하면 사용자에게 경로를 묻고, 그래도 없으면 `/careerloop:launch`를 안내한다.

새 이력서나 자기소개서가 디스크에 저장된 **후**(예: `tailor-resume` / `cover-letter`에서 저장한 직후), 그리고/또는 `{user_dir}`에 PDF/DOCX 아티팩트가 있을 때 `daily-schedule` 시작 시점에 실행합니다. 이 저장소에는 별도의 플러그인 훅 파일이 없습니다.

중요한 동작:
- 이 워크플로는 `ExperienceLibrary`에 아직 반영되지 않은, 새로 발견된 이력서/CV 소스 파일에 대해 `add-source`를 자동으로 트리거해야 합니다.
- 새로 반영되었거나 변경된 소스 파일이 면접 스토리 커버리지에 영향을 줄 수 있으면 증분 `mine-stories`를 트리거해야 합니다.
- 자동 반영(auto-ingest)이 가능한 경우 사용자에게 `add-source`를 직접 실행하라고 요청하지 않습니다.

## 워크플로

### 1. `{user_dir}` 확인 및 인덱스 파일 검증

`{user_dir}/CareerLoop/artifacts-index.json`을 확인합니다.

파일이 없으면 다음을 출력합니다.
> 아티팩트 동기화를 건너뜁니다. `/careerloop:launch`를 실행해 artifacts-index를 초기화하세요.

### 2. 아티팩트 인벤토리 정합화

`{user_dir}`에서 이 플러그인이 사용하는 아티팩트 파일(PDF 및 DOCX)을 스캔합니다.

파일 시스템 상태를 `{user_dir}/CareerLoop/artifacts-index.json`과 교차 검증합니다.
- 디스크에는 있으나 인덱스에 없는 파일은 레코드 추가
- 더 이상 존재하지 않는 파일의 오래된 인덱스 레코드는 제거
- 파일명/경로가 여전히 일치하면 기존 메타데이터 유지

새로 추가하는 레코드에는 다음을 설정합니다.
- 사용자 파일에서 추정한 경우 `source`는 `existing`
- 알 수 없으면 `date_created`는 오늘 날짜
- 가능하면 파일명에서 `type` 추정(`resume` 또는 `cover_letter`), 불가능하면 notes는 중립적으로 비워 둠

`meta`를 다음과 같이 갱신합니다.
- `updated_at`: `{today}`

### 2.5 소스 문서 자동 반영(auto-ingest)

발견한 PDF/DOCX 파일 중 소스 문서일 가능성이 높은 것(이력서/CV 변형본)을 식별합니다.

`ExperienceLibrary`에 아직 반영되지 않은 소스 문서마다 다음을 수행합니다.
- 해당 파일 경로로 `add-source`를 자동 실행
- ingest 성공 또는 실패 여부 기록

자동 반영 시도 후 다음을 다시 읽습니다.
- `{user_dir}/CareerLoop/ExperienceLibrary.json`
- `{user_dir}/CareerLoop/artifacts-index.json`

그런 다음 정합화 건수를 확정합니다.

### 2.6 증분 스토리 갱신 트리거

소스 자동 반영 후, 새로 발견되었거나 변경된 파일 중 스토리가 담긴 파일(이력서/CV 본문, 일지 형식 노트, 디브리프 노트, PKM 내보내기)이 있는지 확인합니다.

있는 경우:
- `mine-stories`를 증분 모드로 자동 실행
- `{user_dir}/CareerLoop/StoryCorpus.json`의 `meta.updated`와 `source_index` 갱신
- 출력용으로 갱신 상태 기록

없는 경우:
- 스토리 갱신은 조용히 건너뜀

### 3. 분석 이벤트 핸드오프 준비

이벤트 요약 페이로드를 생성합니다(현재의 로컬 로깅과 향후 커넥터 핸드오프용).
- `event_type`: `artifact_saved`
- `created_count`
- `removed_count`
- `unchanged_count`
- `as_of`

분석 커넥터가 구성되지 않았다면 다음을 명시적으로 알립니다.
> 분석 커넥터 핸드오프는 보류됩니다(이 단계에서는 구성된 커넥터가 없음).

### 4. 출력 형식

```
ArtifactSaved 처리 완료.
추가: {n}
제거: {n}
변경 없음: {n}
자동 반영한 소스 문서: {n}
반영 실패: {n}
스토리 코퍼스 갱신: {yes/no} (변경된 소스 파일 {n_files}개)
```

`추가` 또는 `제거`가 0보다 크면 짧은 한 줄을 덧붙입니다.
> 아티팩트 인덱스를 `{user_dir}`에 현재 존재하는 파일에 맞게 갱신했습니다.

## 가드레일

- 파일/인덱스 근거로 뒷받침되지 않는 파일 경로나 메타데이터를 지어내지 않습니다
- 디스크의 실제 파일은 삭제하지 않으며, 인덱스 레코드만 정합화합니다
- `ExperienceLibrary.json`을 취약한 줄 단위 문자열 치환으로 편집하지 않습니다. JSON은 구조화된 데이터로 다루고 안전하게 다시 씁니다.
- 출력은 간결하고 실무적으로 유지합니다
