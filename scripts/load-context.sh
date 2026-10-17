#!/usr/bin/env bash
set -euo pipefail

CONTENT_PATH="${CLAUDE_PLUGIN_ROOT}/hooks/context/session-start.md"
CONTENT="$(cat "$CONTENT_PATH")"
export CONTENT

# jq 같은 외부 의존성은 피하고 Python(macOS/Linux에 기본 설치)으로 JSON 이스케이프한다.
python3 - <<'PY'
import json, os, sys
sys.stdout.write(json.dumps({"systemMessage": os.environ.get("CONTENT", "")}))
PY