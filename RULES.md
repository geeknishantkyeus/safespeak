# SafeSpeak — Rules for Antigravity

You are building SafeSpeak. Read `PHASES.md` for the full plan.
These rules are NON-NEGOTIABLE. Follow them at every step.

---

## 1. Build One Phase at a Time

- Complete Phase 0 before starting Phase 1.
- Complete Phase 1 before starting Phase 2.
- And so on, until Phase 7.
- After each phase: run the verification step, report briefly, 
  then continue to the next phase without waiting.
- Do NOT jump ahead. Do NOT build multiple phases together.
- Do NOT touch files from a later phase until its turn.

**After every phase, report in this exact format:**
```
PHASE X — DONE
- Built: [one line]
- Worked: [one line]
- Issue: [one line or "none"]
- Next: Phase Y — [name]
- Need from you: [nothing / approval / info]
```

---

## 2. Do Everything Yourself — Don't Ask Me

If something needs to be done, DO IT. Don't ask me to do it manually.

- Need an account? Create it yourself (use temp/throwaway if needed).
- Need a file? Create it.
- Need a folder? Create it.
- Need a package installed? Install it (system-level → ask first, see Rule 5).
- Need a model downloaded? Download it.
- Need a config written? Write it.
- Need a test run? Run it.
- Need a fix? Fix it.

Only ask me when:
- System-level install needs sudo/admin (Rule 5)
- You're stuck > 10 minutes (Rule 8)
- A decision affects the whole project direction
- You need my personal info (name, friend's name, etc.)

---

## 3. Short Code — No Long Hand-Written Logic

Prefer libraries, built-ins, and short helpers over long custom code.

**Rules:**
- If a library does it, USE THE LIBRARY. Don't rewrite it.
- If a built-in does it, USE THE BUILT-IN.
- Keep functions under ~20 lines. If longer, split or use a library.
- Keep files under ~150 lines. If longer, split into modules.
- No copy-paste blocks. Make a helper instead.
- No 50-line `if/else` chains. Use dicts, match, or libraries.

**Examples of what to do:**
```python
# BAD — long hand-written code
def get_greeting(hour):
    if hour < 12:
        return "Good morning"
    elif hour < 17:
        return "Good afternoon"
    else:
        return "Good evening"

# GOOD — use a library or short form
from datetime import datetime
greeting = "Good morning" if datetime.now().hour < 12 else "Good evening"

# BAD — rewriting HTTP
import socket
s = socket.socket()
...

# GOOD — use requests
import requests
r = requests.get(url)
```

**Examples of libraries to prefer:**
- Ollama calls → `ollama` python package (not raw HTTP)
- Audio → `whisper-python`, `piper-tts` (not raw processing)
- UI → Streamlit (not hand-built HTML/JS)
- HTTP → `requests` (not `urllib` or raw sockets)
- Paths → `pathlib` (not `os.path` string juggling)
- Data → `pydantic` models if needed

**If you catch yourself writing more than 20 lines for one task — STOP. Find a library.**

---

## 4. Write Human-Style Code

Code should look like a person wrote it, not a code generator.

**Do:**
- Use clear, normal variable names: `user_message`, `ai_reply`, `history`
- Add a short comment only where it helps: `# keep last 10 messages`
- Use blank lines between logical blocks
- Use f-strings for formatting
- Keep indentation clean and consistent (4 spaces)
- Write simple functions with obvious names: `send_to_ai()`, `play_audio()`
- Handle errors simply: `try/except` with a useful message

**Don't:**
- Don't use cryptic names: `x`, `tmp1`, `obj_a`, `_res`
- Don't over-comment obvious lines: `# increment i by 1`
- Don't write "AI-style" walls of code with no blank lines
- Don't use fancy tricks nobody understands
- Don't add type hints everywhere unless it helps readability
- Don't write docstrings for every tiny function — only where useful
- Don't use `lambda` chains or one-liners that hurt readability

**Example — good human style:**
```python
import ollama

MODEL = "gemma3:1b"

def ask_ai(messages):
    """Send conversation to local Gemma and get a reply."""
    try:
        response = ollama.chat(model=MODEL, messages=messages)
        return response["message"]["content"]
    except Exception as e:
        return f"Sorry, something went wrong: {e}"
```

**Example — bad AI style:**
```python
import ollama
from typing import List, Dict, Any, Optional

MODEL: str = "gemma3:1b"

def ask_ai(messages: List[Dict[str, Any]]) -> Optional[str]:
    """
    Sends a list of message dictionaries to the Ollama chat API
    and returns the assistant's response content as a string,
    or None if an error occurs during processing.
    """
    try:
        response: Dict[str, Any] = ollama.chat(
            model=MODEL, messages=messages
        )
        return response["message"]["content"]
    except Exception as e:
        print(f"Error: {e}")
        return None
```

The first one is what we want.

---

## 5. Installing Things

- Python packages (`pip install ...`) → install directly, no need to ask.
- Ollama models (`ollama pull ...`) → pull directly, no need to ask.
- System-level installs (`apt`, `brew`, `sudo`, `.exe`, drivers) → ASK ME FIRST.
- Anything that asks for admin/sudo password → ASK ME FIRST.
- Anything that changes system settings → ASK ME FIRST.
- Anything that costs money → ASK ME FIRST.

**No cloud AI APIs. Ever.**
- No OpenAI, no Gemini API, no Anthropic, no cloud LLMs.
- Everything AI-related runs locally via Ollama.
- If a library tries to phone home, block it or replace it.

---

## 6. File & Folder Rules

- Keep the structure exactly as shown in `PHASES.md`.
- Don't create random extra files. If you need a new file, name it clearly.
- Don't create backup files like `app_backup.py`, `app_old.py`.
- Use `pathlib` for all file paths.
- Read config from a single place (`config.py` or `.env`), don't scatter it.

**Expected structure:**
```
safespeak/
├── PHASES.md
├── RULES.md
├── app.py
├── ollama_chat.py
├── prompts.py
├── styles.css
├── requirements.txt
└── README.md
```

---

## 7. Testing After Every Change

- After writing code, run it. Don't assume it works.
- If it fails, fix it before moving on.
- If a test needs input, make a simple test case and run it.
- Keep a short `notes.md` if you discover something useful.
- Don't move to the next phase until the current one actually runs.

---

## 8. When Stuck

- Try 2-3 quick fixes yourself first.
- If still stuck after ~10 minutes, STOP and ask me.
- When asking, tell me:
  - What you tried
  - What error you saw (exact text)
  - What you think is wrong
  - What options you see

Don't silently struggle. Don't guess wildly. Ask.

---

## 9. Keep It Local, Keep It Private

This is the whole point of the project.

- No network calls for AI (Rule 5).
- No telemetry, no analytics, no logging to external services.
- No user accounts, no sign-in, no email collection.
- No saving transcripts to disk unless the user asks.
- Everything runs on `localhost`.

If a feature breaks this, DON'T add it.

---

## 10. Communication

- Be brief in your reports. One line per item (see Rule 1 format).
- Don't explain obvious things.
- Don't apologize repeatedly. Just fix and move on.
- If you make a mistake, say so in one line and correct it.
- Use plain English, no jargon.

---

## Quick Self-Check (before every report)

- [ ] Am I on the correct phase?
- [ ] Did I run the verification?
- [ ] Is the code under 20 lines per function?
- [ ] Did I use a library instead of writing it myself?
- [ ] Does the code look human-written?
- [ ] Is everything still 100% local?
- [ ] Am I reporting in the exact format?

If any box is unchecked, fix it before reporting.
