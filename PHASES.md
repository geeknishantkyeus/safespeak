# SafeSpeak — Build Phases

## Project Overview
A fully local, anonymous English speaking practice app for my friend 
who is a beginner and feels shy practicing with people. Hinglish 
support included. 100% private — nothing leaves the laptop.

**Theme:** Hacktoberfest 2026 + MLH
**Challenge:** Build for a Friend (DEV Weekend Challenge #1)
**Deadline:** 5 Oct 2026, 12:29 PM IST

---

## Tech Stack (DO NOT CHANGE)
| Layer | Tool | Notes |
|-------|------|-------|
| AI Brain | Ollama + gemma3:1b | Local only, no cloud |
| Speech-to-Text | whisper (local) | Offline |
| Text-to-Speech | piper-tts (local) | Offline |
| UI | Streamlit | Browser-based |
| Language | Python 3.10+ | |
| Dev Tool | Antigravity | You are here |

**HARD RULE:** No cloud APIs. No OpenAI. No Gemini API. No external 
network calls for AI. Everything runs on localhost.

---


## Brand Theme (Hacktoberfest 2026 + MLH)

### Colors
```css
--forest: #1F4D2E /* Primary */
--deep-forest: #0D2B1A /* Dark */
--paper: #F5F2EB /* Light BG */
--ink: #1A1A1A /* Text */
--accent-red: #E73427 /* MLH red / loud accent */
--accent-warm: #FFB800 /* Buttons */
```

### Fonts (Google Fonts)
- Headings: **Barlow Semi Condensed** (700, 800)
- Body/UI: **Inter** (400, 700)
- Labels/Eyebrows: **Martian Mono** (uppercase, letter-spacing 0.05em)

### Design Rules
- Forest green bg → white text
- Paper bg → ink text
- Accents sparingly (badges, buttons only)
- Hero squares (4 accents together) only in ONE place
- Logo clear space: min "H" height around

---

## Phase 0 — Setup (15 min)

### Tasks
- [ ] Create project folder `safespeak/`
- [ ] Python venv: `python -m venv venv`
- [ ] Activate venv
- [ ] Install: `pip install streamlit ollama whisper-python piper-tts`
- [ ] Verify Ollama installed: `ollama --version`
- [ ] Pull model: `ollama pull gemma3:1b`
- [ ] Test model: `ollama run gemma3:1b "Hello"`

### Deliverable
Working Ollama + gemma3:1b responding via CLI.

### Verification
Run `ollama run gemma3:1b "Say hi in one word"` — should reply.

---

## Phase 1 — Core Chat UI (30 min)

### Tasks
- [ ] Create `app.py` with Streamlit
- [ ] Create `ollama_chat.py` — function to call Ollama
- [ ] Basic chat UI: `st.chat_message`, `st.chat_input`
- [ ] Maintain conversation history in `st.session_state`
- [ ] Display user + assistant messages

### Code Structure
```
safespeak/
├── app.py # Streamlit entry
├── ollama_chat.py # Ollama wrapper
├── prompts.py # System prompts
├── requirements.txt
└── styles.css # Theme (Phase 6)
```

### ollama_chat.py (reference)
```python
import ollama

def chat(messages, model="gemma3:1b"):
    response = ollama.chat(model=model, messages=messages)
    return response['message']['content']
```

### Deliverable
Working chat UI where user types, Gemma3 replies.

### Verification
Type "Hello" → get a response. Type "How are you?" → get a response.

---

## Phase 2 — Tutor Personality (20 min)

### Tasks
- [ ] Create prompts.py with system prompt
- [ ] Inject system prompt at conversation start
- [ ] Test corrections are gentle (1-line tip, not lecture)

### System Prompt (prompts.py)
```python
TUTOR_SYSTEM = """You are a patient English tutor for a beginner 
learner. Correct mistakes gently with ONE short tip, never a lecture. 
If the user writes in Hinglish (Hindi words in English letters), 
understand it and help them say it in English. Keep responses to 
1-3 sentences. Be encouraging. Never shame the learner.
"""
```

### Deliverable
Tutor behaves gently, corrects without lecturing.

### Verification
Send: "I goes to market yesterday" → should get gentle correction.

---

## Phase 3 — Hinglish Fallback (20 min)

### Tasks
- [ ] Detect Hinglish input (Roman-script Hindi words)
- [ ] System prompt handles Hinglish → English translation + help
- [ ] Add Hinglish examples to system prompt
- [ ] Test: "mujhe ye kaise bolna chahiye" → AI helps

### System Prompt Addition
```text
If the user writes in Hinglish like "mujhe ye kaise bolna chahiye", 
first understand their intent, then show them how to say it in 
English, and explain briefly.
```

### Deliverable
AI understands Hinglish and helps translate + teach.

### Verification
Type "mujhe coffee order karna hai" → AI teaches English version.

---

## Phase 4 — Voice Input (Whisper) (30 min)

### Tasks
- [ ] Install whisper-python (already in Phase 0)
- [ ] Use st.audio_input for recording
- [ ] Transcribe with Whisper locally
- [ ] Send transcribed text to chat
- [ ] Handle errors (empty audio, unclear speech)

### Code Hint
```python
import whisper
model = whisper.load_model("base")
result = model.transcribe("audio.wav")
text = result["text"]
```

### Deliverable
User records voice → text appears → AI responds.

### Verification
Record "Hello, my name is [name]" → correct transcription.

---

## Phase 5 — Voice Output (Piper) (20 min)

### Tasks
- [ ] Install piper-tts (already in Phase 0)
- [ ] Download a voice model
- [ ] Generate audio from AI response
- [ ] Play audio in Streamlit with st.audio
- [ ] Add toggle: voice on/off

### Code Hint
```python
import subprocess
subprocess.run(["piper", "--model", "en_US-voice.onnx", 
                "--output_file", "out.wav"], input=text.encode())
```

### Deliverable
AI response spoken aloud, fully local.

### Verification
AI replies → audio plays automatically.

---

## Phase 6 — Theme + Polish (30 min)

### Tasks
- [ ] Create styles.css with Hacktoberfest colors
- [ ] Inject CSS into Streamlit
- [ ] App title "SafeSpeak" in Barlow Semi Condensed Bold
- [ ] Tagline "Your private English practice partner" in Inter
- [ ] Badge "Built for Hacktoberfest 2026" in Martian Mono
- [ ] Add scenario buttons: Order food, Phone call, Greeting, Directions
- [ ] Add "Privacy: Everything local" notice

### styles.css (reference)
```css
:root {
    --forest: #1F4D2E;
    --deep-forest: #0D2B1A;
    --paper: #F5F2EB;
    --ink: #1A1A1A;
    --accent-red: #E73427;
    --accent-warm: #FFB800;
}
body, .stApp {
    background-color: var(--paper);
    color: var(--ink);
    font-family: 'Inter', sans-serif;
}
h1, h2, h3 {
    font-family: 'Barlow Semi Condensed', sans-serif;
    font-weight: 800;
    color: var(--forest);
}
.eyebrow {
    font-family: 'Martian Mono', monospace;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--accent-red);
}
```

### Inject in app.py
```python
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
```

### Deliverable
App looks like Hacktoberfest + MLH branded.

### Verification
Screenshot shows forest green, paper bg, proper fonts.

---

## Phase 7 — DEV Post + Submit (45 min)

### Tasks
- [ ] Record 60-sec demo (screen recording)
- [ ] Take screenshots
- [ ] Write DEV post (structure below)
- [ ] Tags: #devchallenge #weekendchallenge #hf26challenge
- [ ] Publish on DEV
- [ ] Submit via challenge page
