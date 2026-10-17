"""
mcp-transcribe — 오디오 파일 일괄 전사용 로컬 MCP 서버.

한 가지 일을 확실하게 한다. 디스크에 이미 있는 오디오 파일을 받아 전사본을
돌려준다. 마이크, 스피커, 스트리밍, VAD는 없다. 음성 MCP 서버가 기동에
실패하는 원인이 바로 이 부분들이고, 녹음된 면접을 전사하는 데는 어느 것도
필요하지 않다.

도구:
  transcribe_file(path, ...)  — 오디오 파일 -> 전사 텍스트 + 디스크의 세그먼트
  backend_info()              — 활성 STT 백엔드 확인(진단용)

백엔드(자동 선택):
  1. mlx-whisper      (Apple Silicon, Metal 가속 — 압도적으로 빠름)
  2. faster-whisper   (CPU, 크로스 플랫폼 대체)

Claude Desktop MCP(stdio 전송)로 실행한다. 모델은 처음 쓸 때 지연 로드된다.
"""

import json
import os
import platform
import shutil
import subprocess
import time
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp-transcribe")

# Apple Silicon 기본값. large-v3-turbo는 large에 가까운 정확도를 훨씬 적은
# 비용으로 내고, M 시리즈 칩에서는 실시간보다 몇 배 빠르게 돈다.
MLX_DEFAULT_MODEL = "mlx-community/whisper-large-v3-turbo"
# CPU 대체 기본값. medium.en은 면접 오디오에서 small.en이 내는 고유명사·
# 완곡 표현 오류를 피할 수 있는 최소 정확도선이다.
FW_DEFAULT_MODEL = "medium.en"

AUDIO_SUFFIXES = {
    ".mp3", ".m4a", ".mp4", ".wav", ".flac", ".ogg", ".opus",
    ".aac", ".webm", ".mov", ".aiff", ".aif", ".wma",
}

_backend = None          # "mlx" | "faster-whisper"
_fw_model_cache = {}


# ── 백엔드 선택 ──────────────────────────────────────────────────────────────

def _detect_backend() -> str:
    global _backend
    if _backend:
        return _backend
    if platform.system() == "Darwin" and platform.machine() == "arm64":
        try:
            import mlx_whisper  # noqa: F401
            _backend = "mlx"
            return _backend
        except Exception:
            pass
    import faster_whisper  # noqa: F401  (정말 쓸 수 없으면 예외 발생)
    _backend = "faster-whisper"
    return _backend


def _probe_duration(path: Path):
    """가능한 범위에서 미디어 길이(초)를 구한다. ffprobe가 없으면 None."""
    if not shutil.which("ffprobe"):
        return None
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            capture_output=True, text=True, timeout=30,
        )
        return round(float(out.stdout.strip()), 2)
    except Exception:
        return None


# ── 로컬 어휘(gitignore 대상, 커밋하지 않음) ─────────────────────────────────

VOCAB_PATH = Path(__file__).resolve().parent.parent / "vocabulary.local.json"


def load_vocabulary(group: str = ""):
    """
    vocabulary.local.json에서 고유명사를 읽는다. 이 파일은 gitignore 대상이라
    고용주, 프로젝트, 사람 이름이 공개 저장소에 들어가지 않는다.

    형식:
        {"always": ["TermA", "TermB"],
         "groups": {"some-key": ["TermC", "TermD"]}}

    (terms, note)를 반환한다. 예외를 던지지 않는다. 파일이 없거나 형식이
    잘못됐으면 추가 어휘가 없는 것으로 취급한다.
    """
    if not VOCAB_PATH.exists():
        return [], "vocabulary.local.json 없음"
    try:
        data = json.loads(VOCAB_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        return [], f"vocabulary.local.json을 읽을 수 없음 ({type(e).__name__})"

    terms = [t for t in data.get("always", []) if isinstance(t, str)]
    if group:
        terms += [t for t in data.get("groups", {}).get(group, []) if isinstance(t, str)]

    seen, ordered = set(), []
    for t in terms:
        k = t.strip()
        if k and k.lower() not in seen:
            seen.add(k.lower())
            ordered.append(k)
    return ordered, f"용어 {len(ordered)}개 로드됨"


# ── 도구 ─────────────────────────────────────────────────────────────────────

@mcp.tool()
def backend_info() -> str:
    """
    활성 전사 백엔드와 ffmpeg 설치 여부를 보고한다.
    전사가 이상하게 동작할 때 가장 먼저 호출한다. "서버는 정상이고 파일이
    문제"인 경우와 "백엔드가 아예 로드되지 않은" 경우를 구분해 준다.
    """
    info = {
        "platform": f"{platform.system()}/{platform.machine()}",
        "ffmpeg": bool(shutil.which("ffmpeg")),
        "ffprobe": bool(shutil.which("ffprobe")),
    }
    _terms, vocab_note = load_vocabulary()
    info["vocabulary"] = vocab_note   # 개수만 — 용어는 비공개이며 절대 출력하지 않음
    try:
        info["backend"] = _detect_backend()
        info["default_model"] = (
            MLX_DEFAULT_MODEL if info["backend"] == "mlx" else FW_DEFAULT_MODEL
        )
        info["ok"] = True
    except Exception as e:
        info["backend"] = None
        info["ok"] = False
        info["error"] = f"{type(e).__name__}: {e}"
    return json.dumps(info, indent=2, ensure_ascii=False)


@mcp.tool()
def transcribe_file(
    path: str,
    initial_prompt: str = "",
    vocabulary_group: str = "",
    language: str = "en",
    model: str = "",
    out_dir: str = "",
    write_files: bool = True,
) -> str:
    """
    디스크에 이미 있는 오디오 파일을 전사한다.

    Args:
      path:           오디오 파일의 절대 경로.
      initial_prompt: 등장할 가능성이 높은 고유명사와 전문 용어 — 회사 이름,
                      면접관 이름, 제품 이름. 이것이 없으면 Whisper는 흔치 않은
                      이름을 심하게 망가뜨린다. 실제 녹음에서 네 글자짜리 벤더
                      이름이 흔한 영어 단어로, 성(姓)이 아예 다른 성으로 바뀐
                      적이 있다. 이 값을 채워 두는 것이 가장 싸게 정확도를 올리는
                      방법이다. vocabulary.local.json(gitignore 대상)의 용어는
                      자동으로 합쳐진다. load_vocabulary 참고.
      vocabulary_group: vocabulary.local.json의 "groups" 맵에 대한 선택적 키.
                      특정 고용주나 프로젝트에 한정된 용어용이다. "always"
                      용어는 항상 포함된다.
      language:       ISO 언어 코드. 기본값 "en".
      model:          백엔드 기본값을 덮어쓴다. 기본값을 쓰려면 비워 둔다.
      out_dir:        출력을 쓸 위치. 기본값은 오디오 파일이 있는 폴더.
      write_files:    <name>.transcript.txt와 <name>.segments.json을 쓴다.

    JSON을 반환한다: backend, model, duration, elapsed, speed, 세그먼트 수,
    출력 경로, 전체 전사 텍스트.

    참고:
      - 동기 방식으로 실행된다. Apple Silicon에서는 실시간보다 몇 배 빠르며,
        약 25분짜리 면접도 보통 1분이 채 걸리지 않는다.
      - 음성 구간 필터링(VAD)은 적용하지 않는다. VAD는 무음 경계 근처의 발화를
        조용히 떨어뜨려 실제 내용을 잃은 적이 있다. 항상 파일 전체를 처리한다.
    """
    src = Path(path).expanduser()
    if not src.exists():
        return json.dumps({"ok": False, "error": f"파일을 찾을 수 없습니다: {src}"}, ensure_ascii=False)
    if not src.is_file():
        return json.dumps({"ok": False, "error": f"파일이 아닙니다: {src}"}, ensure_ascii=False)
    if src.suffix.lower() not in AUDIO_SUFFIXES:
        return json.dumps({
            "ok": False,
            "error": f"인식할 수 없는 오디오 확장자입니다: '{src.suffix}'. "
                     f"지원 확장자: {sorted(AUDIO_SUFFIXES)}",
        }, ensure_ascii=False)
    if not shutil.which("ffmpeg"):
        return json.dumps({
            "ok": False,
            "error": "PATH에서 ffmpeg를 찾을 수 없습니다. 설치: brew install ffmpeg",
        }, ensure_ascii=False)

    try:
        backend = _detect_backend()
    except Exception as e:
        return json.dumps({
            "ok": False,
            "error": f"사용 가능한 전사 백엔드가 없습니다 ({type(e).__name__}: {e}). "
                     f"Apple Silicon: uv add mlx-whisper. 그 외: uv add faster-whisper.",
        }, ensure_ascii=False)

    # 호출자가 준 이름과 gitignore 대상 로컬 어휘를 합친다.
    vocab_terms, vocab_note = load_vocabulary(vocabulary_group)
    prompt_parts = [p for p in (initial_prompt.strip(), ", ".join(vocab_terms)) if p]
    effective_prompt = ". ".join(prompt_parts)

    duration = _probe_duration(src)
    t0 = time.time()
    segments = []

    try:
        if backend == "mlx":
            import mlx_whisper
            repo = model or MLX_DEFAULT_MODEL
            result = mlx_whisper.transcribe(
                str(src),
                path_or_hf_repo=repo,
                language=language or None,
                initial_prompt=effective_prompt or None,
                condition_on_previous_text=True,
                verbose=None,
            )
            text = (result.get("text") or "").strip()
            for s in result.get("segments", []):
                segments.append({
                    "start": round(float(s["start"]), 2),
                    "end": round(float(s["end"]), 2),
                    "text": (s.get("text") or "").strip(),
                })
        else:
            from faster_whisper import WhisperModel
            name = model or FW_DEFAULT_MODEL
            if name not in _fw_model_cache:
                _fw_model_cache[name] = WhisperModel(
                    name, device="cpu", compute_type="int8",
                    cpu_threads=max(1, (os.cpu_count() or 2)),
                )
            seg_iter, _info = _fw_model_cache[name].transcribe(
                str(src),
                beam_size=5,
                language=language or None,
                initial_prompt=effective_prompt or None,
                condition_on_previous_text=True,
                vad_filter=False,   # 의도적: docstring 참고
            )
            for s in seg_iter:
                segments.append({
                    "start": round(s.start, 2),
                    "end": round(s.end, 2),
                    "text": s.text.strip(),
                })
            text = " ".join(s["text"] for s in segments).strip()
    except Exception as e:
        return json.dumps({
            "ok": False,
            "backend": backend,
            "error": f"전사 실패: {type(e).__name__}: {e}",
        }, ensure_ascii=False)

    elapsed = round(time.time() - t0, 1)
    model_used = model or (MLX_DEFAULT_MODEL if backend == "mlx" else FW_DEFAULT_MODEL)

    payload = {
        "ok": True,
        "backend": backend,
        "model": model_used,
        "source": str(src),
        "duration_seconds": duration,
        "elapsed_seconds": elapsed,
        "speed_x_realtime": round(duration / elapsed, 1) if duration and elapsed else None,
        "segment_count": len(segments),
        "vocabulary": vocab_note,   # 개수만 — 용어는 비공개이며 절대 출력하지 않음
        "text": text,
    }

    if write_files:
        dest = Path(out_dir).expanduser() if out_dir else src.parent
        try:
            dest.mkdir(parents=True, exist_ok=True)
            txt_path = dest / f"{src.stem}.transcript.txt"
            json_path = dest / f"{src.stem}.segments.json"
            txt_path.write_text(text, encoding="utf-8")
            json_path.write_text(
                json.dumps(segments, indent=1, ensure_ascii=False), encoding="utf-8"
            )
            payload["transcript_path"] = str(txt_path)
            payload["segments_path"] = str(json_path)
        except Exception as e:
            payload["write_warning"] = f"{type(e).__name__}: {e}"

    return json.dumps(payload, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    mcp.run()
