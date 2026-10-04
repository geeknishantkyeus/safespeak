import io
import re
import wave
from pathlib import Path
import emoji
import piper
from piper.config import SynthesisConfig

MODEL_PATH = Path(__file__).parent / "models" / "en_US-lessac-medium.onnx"

_voice = None

def get_piper_voice():
    """Load and cache the Piper voice model in memory for fast synthesis."""
    global _voice
    if _voice is None and MODEL_PATH.exists():
        _voice = piper.PiperVoice.load(str(MODEL_PATH))
    return _voice

def clean_for_tts(text: str):
    """Clean text before speech synthesis so it sounds natural:
    - Strips emojis and markdown formatting
    - Converts symbols to spoken words (& -> and, ₹ -> rupees, % -> percent, etc.)
    - Removes punctuation that TTS trips over (asterisks, hashtags, backticks)
    """
    if not text or not isinstance(text, str):
        return None

    # 1. Remove all emojis using official emoji package
    text = emoji.replace_emoji(text, replace="")

    # Unicode emoji & pictograph regex fallback
    emoji_pattern = re.compile(
        "[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF"
        "\U0001F900-\U0001F9FF\U00002600-\U000026FF\U00002700-\U000027BF"
        "\U0001F1E6-\U0001F1FF\U0001FA70-\U0001FAFF]+",
        flags=re.UNICODE
    )
    text = emoji_pattern.sub("", text)

    # 3. Replace symbols with natural spoken equivalents
    text = re.sub(r'\s*&\s*', ' and ', text)
    text = re.sub(r'\s*@\s*', ' at ', text)
    text = re.sub(r'(\d+)\s*%', r'\1 percent', text)
    text = text.replace('%', ' percent ')
    text = re.sub(r'₹\s*(\d+)', r'\1 rupees', text)
    text = text.replace('₹', ' rupees ')
    text = re.sub(r'\$\s*(\d+(?:\.\d+)?)', r'\1 dollars', text)
    text = text.replace('$', ' dollars ')
    text = re.sub(r'\.{3,}', '.', text)

    # 4. Remove markdown formatting
    # Headers # Header -> Header
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    # **bold** and *italic*
    text = re.sub(r'\*+(.*?)\*+', r'\1', text)
    # `code` -> code
    text = re.sub(r'`+(.*?)`+', r'\1', text)

    # 2. Remove special characters and brackets
    text = re.sub(r'[{}\[\]\(\)]', '', text)
    text = re.sub(r'[_#~|><^=/\\+]', ' ', text)
    text = text.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
    text = re.sub(r'[—–]', ', ', text)
    # Hyphen in lists (- item) -> remove; hyphen in words -> keep
    text = re.sub(r'(?:^|\s)-\s+', ' ', text)

    # 5. Collapse multiple spaces & 6. Strip leading/trailing whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Empty after cleaning -> return None gracefully
    if not text or not re.search(r'[a-zA-Z0-9]', text):
        return None

    return text

# Backward compatibility alias
clean_text_for_speech = clean_for_tts

def synthesize_speech(text):
    """Synthesize text to speech audio bytes in-memory using clean_for_tts."""
    if not text:
        return None
    try:
        voice = get_piper_voice()
        if voice is None:
            return None

        # Clean text before synthesis
        cleaned = clean_for_tts(text)
        if not cleaned:
            return None

        # Human-like cadence: length_scale=1.06 gives relaxed, friendly, natural pacing
        syn_config = SynthesisConfig(length_scale=1.06)

        buf = io.BytesIO()
        with wave.open(buf, "wb") as wav_file:
            voice.synthesize_wav(cleaned, wav_file, syn_config=syn_config, set_wav_format=True)

        return buf.getvalue()
    except Exception:
        return None

# Pre-warm voice model on module load so the first request is instant (<200ms)
try:
    get_piper_voice()
except Exception:
    pass
