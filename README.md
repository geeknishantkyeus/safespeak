# 🎙️ SafeSpeak

> **A 100% offline, judgment-free English practice partner for shy beginners.**  
> *Built for a Friend (DEV Weekend Challenge #1) · Hacktoberfest 2026*

---

## The Story: Why I Built This

A close friend of mine has wanted to practice spoken English for a long time. They read English well and understand videos fine, but the moment they have to speak to someone in public, they freeze up. 

When I suggested popular language apps, they told me two things:
1. *"Those apps feel like quizzes. One mistake and it buzzes at you with red text."*
2. *"I don't want my broken voice recordings being uploaded to someone's cloud server."*

I built **SafeSpeak** to give them a safe place to practice. No judgment, no grammar quizzes, no cloud servers, and no subscription fees. Just a friendly conversation partner who understands what you mean (even if you type in Hindi or Hinglish) and helps you say it naturally in English.

Everything runs **100% locally on your machine**. You can literally turn off your Wi-Fi, pull out the ethernet cable, and have a full spoken conversation.

---

## ✨ What Makes SafeSpeak Different

- 🔒 **Zero Cloud, Total Privacy:** Powered by local Ollama (`gemma3:1b`), local Whisper (`base`), and local Piper TTS. Nothing leaves `localhost`.
- 🤝 **Tutor Persona (Ava):** Ava acts like a patient friend, not a schoolteacher. She follows the 70/30 rule (you talk 70% of the time, she talks 30%), keeps answers to 1–2 short sentences, and never lectures with grammar jargon.
- 🇮🇳 **Devanagari Hindi & Hinglish Support:** When a beginner is stuck, forcing them to think in English causes a mental block. In SafeSpeak, you can type `"मुझे कॉफ़ी चाहिए"` or `"mujhe coffee chahiye"`, and Ava immediately understands and teaches you how to say it in natural English.
- ⚡ **Snappy Local Latency:** 
  - Gemma 3 1B generates replies in ~400–600ms on CPU.
  - Whisper uses single-pass greedy decoding to transcribe speech in <1s.
  - Piper ONNX generates warm voice audio in under 150ms.
- 🗣️ **Clean Voice Output:** Emojis and markdown formatting are kept in the chat text for readability, but stripped cleanly from the audio output so the TTS never tries to read out asterisks or emoji names.
- 🎭 **Real-Life Scenarios:** Quick-start buttons to roleplay everyday situations: ordering at a café, making a clinic appointment, meeting someone new, or asking for street directions.

---

## 🛠️ The Local Stack

| Component | Tool / Model | Why it's here |
|---|---|---|
| **LLM Engine** | [Ollama](https://ollama.com/) + `gemma3:1b` | Lightweight (~800MB VRAM/RAM), sub-second generation, runs on modest hardware |
| **Speech-to-Text** | [OpenAI Whisper](https://github.com/openai/whisper) (`base`) | Offline voice input with greedy decoding for instant turnaround |
| **Text-to-Speech** | [Piper TTS](https://github.com/rhasspy/piper) (`en_US-lessac`) | Fast neural ONNX speech synthesis with a natural conversational cadence |
| **Frontend** | Streamlit + Custom CSS | Warm, accessible retro-editorial theme (Paper & Forest Green) |
| **Language** | Python 3.12 | Simple, hackable codebase with minimal dependencies |

---

## 🚀 Quickstart Guide

### 1. Prerequisites

- **Python 3.10+** (Tested on Python 3.12)
- **Ollama**: Download and install from [ollama.com](https://ollama.com)

Pull the Gemma 3 1B model:
```bash
ollama pull gemma3:1b
```

Make sure Ollama is running in the background:
```bash
ollama serve
```

### 2. Clone & Setup

```bash
git clone https://github.com/geeknishantkyeus/safespeak.git
cd safespeak

# Create and activate a virtual environment
python -m venv venv

# Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Linux / macOS:
source venv/bin/activate

# Install dependencies:
pip install -r requirements.txt
```

### 3. Run SafeSpeak

```bash
streamlit run app.py
```

Your browser should automatically open to `http://localhost:8501`.

---

## 🧪 Testing 100% Offline Mode

Want to verify that nothing touches the internet?

1. Disconnect your Wi-Fi or unplug your ethernet cable.
2. Verify you have no internet access:
   ```bash
   ping 8.8.8.8
   ```
3. Run `streamlit run app.py`.
4. Talk or type to Ava. Notice that transcription, AI thinking, and voice output all work completely without internet.

---

## 💡 How It Works (Under the Hood)

```
[ User Voice ] ──> [ Streamlit Audio Input ]
                           │
                           ▼
                 [ Whisper (base) ] ──> (Local speech-to-text)
                           │
                           ▼
             [ Prompt Engine (Ava) ] ──> (Devanagari / Hinglish bridge)
                           │
                           ▼
              [ Ollama (gemma3:1b) ] ──> (Local LLM response)
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
      [ Chat UI ]               [ clean_for_tts() ]
   (Markdown + Emojis)                   │
                                         ▼
                               [ Piper Voice (ONNX) ]
                                         │
                                         ▼
                                 [ Spoken Audio ]
```

---

## 📁 Project Structure

```
safespeak/
├── app.py              # Main Streamlit app and interaction loop
├── ollama_chat.py      # Ollama client connection and inference parameters
├── prompts.py          # Ava tutor persona, Hindi understanding, and scenarios
├── transcribe.py       # Whisper speech-to-text loader and greedy inference
├── tts.py              # Piper TTS synthesis and clean_for_tts text sanitizer
├── styles.css          # Editorial theme (forest green, warm paper, readable text)
├── requirements.txt    # Project dependencies
├── models/             # Local Piper voice model (.onnx + .json)
├── README.md           # You are here
├── DEV_POST.md         # DEV Community submission writeup
├── ARCHITECTURE.md     # Deep dive into latency, memory, and design
└── QUICKSTART.md       # Step-by-step setup and troubleshooting
```

---

## 🤝 Contributing

Contributions are welcome! Whether it's adding another local language bridge (like Tamil, Telugu, Spanish, or Arabic), testing smaller/larger models, or improving voice styling, feel free to open an issue or PR for Hacktoberfest.

---

## 📜 License

MIT License. Free to use, modify, and build upon.
