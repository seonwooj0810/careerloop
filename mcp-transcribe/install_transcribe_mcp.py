#!/usr/bin/env python3
"""
mcp-transcribe를 Claude Desktop에 등록한다.

터미널에서 한 번 실행한다:
    python3 <repo>/mcp-transcribe/install_transcribe_mcp.py

예전 setup_career_voice.py와 달리, 설정을 건드리기 전에 모든 사전 요건을 확인하고
빠진 것이 있으면 정확히 무엇이 빠졌는지 알려 준다.
"""
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
SERVER = SCRIPT_DIR / "server" / "main.py"
CONFIG = Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"

fail = []

# 1. uv
uv = shutil.which("uv")
if not uv:
    for c in ["/opt/homebrew/bin/uv", "/usr/local/bin/uv", str(Path.home() / ".local/bin/uv")]:
        if Path(c).exists():
            uv = c
            break
print(f"{'OK  ' if uv else 'FAIL'}  uv: {uv or '찾을 수 없음 — brew install uv'}")
if not uv:
    fail.append("uv")

# 2. 서버 파일
print(f"{'OK  ' if SERVER.exists() else 'FAIL'}  server: {SERVER}")
if not SERVER.exists():
    fail.append("server/main.py")

# 3. ffmpeg (whisper가 이것을 통해 디코딩함)
ff = shutil.which("ffmpeg")
print(f"{'OK  ' if ff else 'FAIL'}  ffmpeg: {ff or '찾을 수 없음 — brew install ffmpeg'}")
if not ff:
    fail.append("ffmpeg")

# 4. 설정 디렉터리
print(f"{'OK  ' if CONFIG.parent.exists() else 'FAIL'}  Claude Desktop config dir: {CONFIG.parent}")
if not CONFIG.parent.exists():
    fail.append("Claude Desktop 설정 디렉터리(Claude Desktop이 설치돼 있나요?)")

if fail:
    print("\n누락: " + ", ".join(fail))
    print("해결한 뒤 다시 실행하세요. 아무것도 변경하지 않았습니다.")
    sys.exit(1)

# 4b. 커밋된 예시 파일로 gitignore 대상 로컬 어휘 파일을 만든다.
VOCAB = SCRIPT_DIR / "vocabulary.local.json"
EXAMPLE = SCRIPT_DIR / "vocabulary.example.json"
if not VOCAB.exists() and EXAMPLE.exists():
    shutil.copy(EXAMPLE, VOCAB)
    print(f"OK    {VOCAB.name} 생성됨(gitignore 대상) — 실제 고유명사를 여기에 추가하세요")
elif VOCAB.exists():
    print(f"OK    {VOCAB.name} 이미 있음")

# 5. Apple Silicon 가속 — 선택 사항이지만 속도가 크게 빨라짐
if platform.system() == "Darwin" and platform.machine() == "arm64":
    print("\nApple Silicon 감지. Metal 가속을 위해 mlx-whisper를 설치합니다...")
    r = subprocess.run([uv, "sync", "--extra", "mlx"], cwd=SCRIPT_DIR)
    if r.returncode != 0:
        print("WARN  mlx-whisper 설치에 실패했습니다. 서버는 faster-whisper로 CPU에서 "
              "계속 동작하지만 더 느립니다.")
else:
    subprocess.run([uv, "sync"], cwd=SCRIPT_DIR)

# 6. 스모크 테스트 — 설정에 연결하기 전에 서버의 import를 먼저 실행해,
#    환경 문제가 Claude Desktop의 조용한 실패가 아니라 여기서 드러나게 한다.
print("\n스모크 테스트: 서버 모듈을 로드하는 중...")
probe = subprocess.run(
    [uv, "run", "--project", str(SCRIPT_DIR), "python", "-c",
     "import importlib.util,sys;"
     f"spec=importlib.util.spec_from_file_location('m',r'{SERVER}');"
     "m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);"
     "print(m.backend_info())"],
    capture_output=True, text=True, cwd=SCRIPT_DIR)
print(probe.stdout.strip() or probe.stderr.strip()[-1500:])
if probe.returncode != 0:
    print("\nFAIL  서버를 정상적으로 import하지 못했습니다. 설정을 수정하지 않습니다.")
    sys.exit(1)

# 7. 설정 쓰기
config = json.loads(CONFIG.read_text()) if CONFIG.exists() else {}
config.setdefault("mcpServers", {})
config["mcpServers"]["mcp-transcribe"] = {
    "type": "stdio",
    "command": uv,
    "args": ["run", "--project", str(SCRIPT_DIR), str(SERVER)],
    # 고정해 둔 값: ~/.zshrc에서 Interlock용 UV_PROJECT_ENVIRONMENT가 전역으로
    # export되어 있어도 이 서버는 항상 자체 venv를 쓰게 한다.
    # 이것이 없으면 mcp-transcribe가 조용히 ~/.venvs/interlock에 동기화되어
    # 그 프로젝트에 필요한 것을 덮어쓴다.
    "env": {"UV_PROJECT_ENVIRONMENT": str(SCRIPT_DIR / ".venv")},
}

if CONFIG.exists():
    backup = CONFIG.with_suffix(".json.transcribe_backup")
    shutil.copy(CONFIG, backup)
    print(f"\nOK    백업: {backup}")

CONFIG.write_text(json.dumps(config, indent=2))
print(f"OK    {CONFIG.name}에 'mcp-transcribe'를 등록했습니다")
print("\nClaude Desktop을 재시작하세요. 그런 다음 Claude에게 backend_info를 실행해 로드됐는지 확인해 달라고 하세요.")
