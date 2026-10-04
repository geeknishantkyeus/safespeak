import re
import ollama
from prompts import TUTOR_SYSTEM, get_system_prompt

MODEL = "gemma3:1b"

def chat(messages, system_prompt=None, model=MODEL):
    """Send conversation with system prompt directly to local Ollama and return assistant text."""
    try:
        if system_prompt is None:
            system_prompt = get_system_prompt(messages)

        full_messages = [{"role": "system", "content": system_prompt}] + messages

        response = ollama.chat(
            model=model,
            messages=full_messages,
            options={
                "temperature": 0.2,
                "num_predict": 50,
            }
        )
        content = response["message"]["content"].strip()

        # Clean persona prefixes if model echoed (e.g. "Ava:")
        content = re.sub(r'^(Ava|Tutor|Waiter|Receptionist):\s*', '', content, flags=re.IGNORECASE).strip()

        # Chat UI preserves markdown and emojis; only TTS cleans them
        return content
    except Exception as e:
        return f"Local AI error: {e}"
