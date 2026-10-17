---
name: setup-transcribe
description: >
  /careerloop:interview-capture가 녹음된 면접 오디오 파일을 텍스트로 변환할 수 있도록, 로컬 mcp-transcribe MCP 서버를 설치하고 Claude Desktop에 등록합니다. 사전 점검과 설치 명령을 사용자 대신 실행하므로 터미널을 직접 쓸 필요가 없습니다. /careerloop:setup-transcribe로도 호출할 수 있습니다.
  Installs and registers the local mcp-transcribe MCP server with Claude
  Desktop so /careerloop:interview-capture can transcribe recorded
  interview audio files. Runs the prerequisite checks and installer commands
  on the user's behalf so they don't need to use a terminal themselves.
  Also invocable via /careerloop:setup-transcribe.
triggers:
  - "set up interview transcription"
  - "install mcp-transcribe"
  - "enable interview capture"
  - "set up audio transcription"
  - "set up mcp-transcribe"
  - "/careerloop:setup-transcribe"
  - "/setup-transcribe"
  - "면접 전사 설정"
  - "mcp-transcribe 설치해줘"
  - "면접 기록 기능 켜줘"
  - "오디오 전사 설정"
  - "녹음 전사 환경 설정"
---

`/careerloop:interview-capture`가 녹음된 면접 오디오 파일을 텍스트로 변환할 수 있도록 로컬 `mcp-transcribe` MCP 서버를 설치합니다. `mcp-transcribe/README.md`에 명령줄 기준으로 문서화된 것과 같은 단계를 비전문가 사용자에게 안내하되, 실제 실행은 Claude가 하며 설치나 변경 전에 반드시 확인을 받습니다.

이 작업은 선택 사항입니다. 사용자가 `interview-capture`를 쓸 계획이 없으면 통째로 건너뜁니다.

---

## 1. 이미 설치되어 있는지 확인

이 세션에서 `backend_info`라는 이름의 도구(`mcp-transcribe` 제공)를 이미 사용할 수 있는지 확인합니다. 사용할 수 있으면 해당 도구를 호출하여 활성 백엔드를 보고하고 멈춥니다. 설치할 것이 없습니다.

그렇지 않으면 계속 진행합니다.

---

## 2. 플러그인 디렉터리 찾기

이 플러그인의 `mcp-transcribe/` 디렉터리 절대 경로를 확인합니다(`skills/setup-transcribe/SKILL.md`가 있는 같은 레포). 찾을 수 없으면(예: 이 선택적 디렉터리 없이 플러그인이 zip으로 설치된 경우) 사용자에게 다음과 같이 안내합니다.

> 이 설치본에서는 면접 전사 설정을 사용할 수 없습니다. CareerLoop GitHub 레포의 `mcp-transcribe/` 폴더가 필요합니다. https://github.com/seonwooj0810/careerloop 에서 레포를 클론하거나 다운로드한 뒤, 그 안에서 이 작업을 다시 실행해 주세요.

그런 다음 멈춥니다.

---

## 3. 사전 요구 사항 확인

Bash로 실행합니다(읽기 전용 점검이므로 확인 불필요).

```bash
command -v uv; command -v ffmpeg; command -v brew
```

어떤 것이 있는지 보고합니다. 두 가지 경우가 있습니다.

**Homebrew 없음(uv 및/또는 ffmpeg도 없음):** 이 흐름은 Homebrew 경로(macOS/Linuxbrew)만 자동화합니다. 사용자에게 `uv`와 `ffmpeg`를 직접 설치하도록 안내하고(https://docs.astral.sh/uv/getting-started/installation/ 와 https://ffmpeg.org/download.html 참조) 설치 후 이 스킬을 다시 실행하게 합니다. 멈춥니다.

**Homebrew 있음, uv 및/또는 ffmpeg 없음:** 무엇을 왜 실행할지 정확히 알려준 뒤, 실행 전에 명시적 확인을 요청합니다.

> Homebrew로 `uv`와 `ffmpeg`를 설치해야 합니다. `brew install uv ffmpeg`를 실행하겠습니다. 진행해도 될까요?

분명한 승낙을 받은 뒤에만 Bash로 실행합니다. 실패하면 오류를 보여주고 멈춥니다. 조용히 재시도하지 않습니다.

---

## 4. 설치 프로그램 실행

실행하기 전에 무슨 일이 일어날지 설명합니다.

> 플러그인의 설치 프로그램을 실행합니다. 설정을 점검하고, `mcp-transcribe`의 Python 의존성을 전용 격리 환경에 설치하며, Claude Desktop 설정(`~/Library/Application Support/Claude/claude_desktop_config.json`)에 등록합니다. 먼저 해당 설정 파일을 백업하고, 점검에서 하나라도 실패하면 건드리지 않습니다.

그런 다음 실행합니다.

```bash
python3 {resolved_path}/mcp-transcribe/install_transcribe_mcp.py
```

출력은 그대로 전달합니다. 이미 사전 요구 사항별로 OK/FAIL 줄을 명확하게 출력하며, 문제가 있으면 설정을 건드리지 않고 깔끔하게 멈춥니다. 실패하면 근본 원인을 직접 고치려 하지 않습니다(예: 우회해서 `pip install`을 수동으로 하지 않습니다). 출력된 내용을 그대로 보고하고 사용자가 진행 방법을 결정하게 합니다. 이 스크립트는 잘못된 설정을 쓰지 않도록 의도적으로 보수적으로 설계되어 있기 때문입니다.

---

## 5. 확인 및 인계

성공하면:

```
✅ mcp-transcribe가 설치되고 등록되었습니다.

도구가 로드되도록 Claude Desktop을 재시작(또는 새 채팅 시작)한 뒤,
녹음된 면접 오디오 파일 경로와 함께
/careerloop:interview-capture를 실행하세요.
```

같은 세션에서 `backend_info`를 호출하려 하지 않습니다. 설정 변경은 새 세션에서만 적용됩니다.

---

## 가드레일

- 이 작업이 무엇을 하는지 먼저 사용자에게 알리고 명시적인 승낙을 받기 전에는 `brew install`이나 Python 설치 프로그램을 절대 실행하지 않습니다. 사용자의 로컬 Homebrew 패키지와 Claude Desktop 설정을 수정하기 때문입니다.
- `claude_desktop_config.json`을 직접 수동 편집하지 않습니다. 쓰기 전에 검증하고 백업하는 `install_transcribe_mcp.py`를 항상 거칩니다.
- `vocabulary.local.json`의 내용을 붙여넣거나 로그에 남기거나 에코하지 않습니다. 설치 프로그램이 첫 실행 시 `vocabulary.example.json`에서 이 파일을 생성하며, 실제 값은 사용자의 개인 데이터입니다.
- 이 흐름은 macOS/Homebrew 전용입니다(`install_transcribe_mcp.py`는 Claude Desktop의 macOS 설정 경로를 대상으로 함). Windows/Linux이거나 Claude Desktop이 설치되어 있지 않다면, 3단계 이후 멈추고 대신 `mcp-transcribe/README.md`의 수동 설치 절차를 안내합니다.
