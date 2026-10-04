import os
import sys
import tempfile
from pathlib import Path
import whisper

# Ensure local venv/Scripts is in PATH so whisper finds ffmpeg
scripts_dir = str(Path(sys.executable).parent)
if scripts_dir not in os.environ.get("PATH", ""):
    os.environ["PATH"] = scripts_dir + os.pathsep + os.environ.get("PATH", "")

_model = None

def get_whisper_model():
    """Load and cache the base whisper model locally."""
    global _model
    if _model is None:
        _model = whisper.load_model("base")
    return _model

def transcribe_audio(audio_bytes):
    """Transcribe audio bytes using local Whisper with fast single-pass decoding."""
    if not audio_bytes:
        return ""
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        model = get_whisper_model()
        # Greedy decoding (beam_size=1) keeps transcription snappy on CPU
        result = model.transcribe(
            tmp_path,
            fp16=False,
            beam_size=1,
            best_of=1,
            temperature=0.0
        )
        Path(tmp_path).unlink(missing_ok=True)
        return result.get("text", "").strip()
    except Exception as e:
        return f"Audio transcription error: {e}"
