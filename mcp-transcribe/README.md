# mcp-transcribe

**디스크에 이미 있는 오디오 파일**을 전사하는 로컬 MCP 서버입니다.

마이크 없음. 음성 합성(TTS) 없음. 스트리밍 없음. 음성 구간 감지(VAD) 없음.
이렇게 좁게 만든 것이 핵심입니다. 아래 "mcp-voice를 대체한 이유"를 참고하세요.

## 도구

| 도구 | 용도 |
|---|---|
| `transcribe_file(path, initial_prompt, vocabulary_group, language, model, out_dir, write_files)` | 녹음 파일을 전사합니다. 텍스트와 시간 정보가 있는 세그먼트를 반환하며, `<name>.transcript.txt`와 `<name>.segments.json`도 함께 씁니다. |
| `backend_info()` | 사용 중인 백엔드와 ffmpeg 유무를 보고합니다. 문제가 생기면 가장 먼저 호출하세요. |

## 백엔드

처음 사용할 때 자동으로 선택됩니다.

1. **mlx-whisper** — Apple Silicon 전용, Metal 가속. 기본 모델은 `mlx-community/whisper-large-v3-turbo`입니다. 실시간보다 몇 배나 빠릅니다.
2. **faster-whisper** — Intel Mac, Windows, Linux용 CPU 대체 백엔드. 기본 모델은 `medium.en`입니다.

## 설치

```bash
brew install uv ffmpeg          # 없다면 설치
python3 install_transcribe_mcp.py
# Claude Desktop 재시작
```

설치 프로그램은 uv, 서버 파일, ffmpeg, Claude Desktop 설정 디렉터리를 확인하고, 의존성을 설치한 뒤,
설정에 아무것도 쓰기 전에 **서버의 import를 스모크 테스트**합니다. 확인 중 하나라도 실패하면 중단하고 아무것도 변경하지 않습니다.

## 독립 실행 CLI(MCP 불필요)

전사가 데몬 기동 여부에 좌우되어서는 안 됩니다. 같은 엔진을 서버 없이 쓸 수 있습니다.

```bash
uv run cli/transcribe.py ~/path/recording.mp3 --prompt "AcmeCorp, Widgetron, J. Doe"
uv run cli/transcribe.py ~/path/recording.mp3 --vocab-group example-employer
```

## 중요한 두 가지 설정

**`initial_prompt`는 실제로는 선택 사항이 아닙니다.** Whisper는 흔치 않은 고유명사를 심하게 망가뜨립니다.
실제 녹음에서 네 글자짜리 벤더 이름이 흔한 영어 단어로, 성(姓)이 다른 성으로, 회사 이름이 비슷하게 들리는 다른 말로 바뀐 적이 있습니다.
말하게 될 것을 이미 아는 이름으로 프롬프트를 채워 두면 대부분 공짜로 해결되고, 비용도 들지 않습니다.

**VAD는 꺼져 있으며 계속 꺼 둡니다.** 음성 구간 필터링은 무음을 잘라 내지만, 무음 경계에서 발화까지 떨어뜨립니다.
23분짜리 리크루터 스크리닝에서 약 28초가 조용히 사라졌고, 거기에는 면접 절차에 대한 면접관의 답변 전체가 포함돼 있었습니다.
통화에서 가장 실행에 도움이 되는 내용이었습니다. 아낀 시간은 빠졌다는 사실조차 알 수 없는 내용을 잃는 것과 맞바꿀 만한 가치가 없습니다.

## 저장소에 이름을 남기지 않기

이 저장소는 공개 저장소입니다. 고용주 이름, 사람 이름, 프로젝트 이름은
**`vocabulary.local.json`**에 둡니다. 이 파일은 gitignore 대상이라 커밋되지 않습니다.
`vocabulary.example.json`을 `vocabulary.local.json`으로 복사한 뒤(설치 프로그램이 대신 해 줍니다) 실제 용어를 채우세요.

```json
{
  "always": ["MyProject", "MyCompany"],
  "groups": {
    "some-employer": ["Their Product", "A. Person", "THEIRACRONYM"]
  }
}
```

`transcribe_file`은 `always`와 요청된 `vocabulary_group`을 Whisper 프롬프트에 자동으로 합치고,
CLI는 `--vocab-group`을 받습니다. 도구와 로그 어느 쪽도 용어를 되돌려 출력하지 않습니다.
`backend_info`와 전사 결과는 **개수**만 보고하므로, 비공개 이름이 전사 헤더, 도구 결과, 커밋으로 새어 나갈 수 없습니다.

면접 작업에서는 트래커 자체가 더 풍부한 출처입니다
(`career/CareerLoop/`, 이미 gitignore 대상). `interview-capture` 스킬이 매칭된 지원 건의
회사, 직무, 담당자 이름으로 프롬프트를 만듭니다. 트래커에 없는 공통 용어(예: 본인 프로젝트 이름)에는
`vocabulary.local.json`을 사용하세요.

합쳐진 프롬프트는 대략 200토큰 이내로 유지하세요. Whisper는 더 긴 프롬프트를 잘라 냅니다.

## mcp-voice를 대체한 이유

`mcp-voice`는 마이크 캡처, Kokoro TTS, STT를 하나의 stdio 데몬에 묶어 놓았습니다.
다음 문제들 때문에 기동이 되지 않습니다.

- `requires-python = ">=3.14"`. 여러 의존성에 cp314 휠이 아직 없어서, 서버가 실행되기도 전에 의존성 해석이 실패합니다.
- `webrtcvad`가 모듈 최상단에서 import되고 인라인 스크립트 메타데이터에도 적혀 있지만,
  `pyproject.toml` 의존성에는 **빠져 있습니다**. 사실상 유지보수도 되지 않고, 최신 Python에서는 C 빌드가 필요합니다.
- `sounddevice`가 모듈 최상단에서 import되어 import 시점에 PortAudio를 로드합니다.
  PortAudio가 없으면 서버도 없고, 그 실패는 어떤 도구가 등록되기도 전에 일어납니다.
- 기동이 되더라도 `listen`은 Claude Desktop이 띄운 프로세스에 대한 TCC 마이크 권한이 필요합니다.

결정적인 점은 **mcp-voice에 파일 전사 도구가 아예 없다**는 것입니다. 도구는 `speak`와 `listen`(실시간 마이크)뿐입니다.
완벽히 동작하더라도 녹음된 면접을 전사할 수는 없었을 것입니다. 정작 필요했던 기능이 처음부터 없었습니다.

`mock-interview`용 실시간 TTS/STT는 별개의 문제이며 별도 서버에 속합니다.
그래야 마이크 권한 문제가 전사 기능을 멈추게 하는 일이 없습니다.
