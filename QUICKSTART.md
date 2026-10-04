# ⚡ SafeSpeak Setup & Troubleshooting Guide

This guide walks you through setting up SafeSpeak locally on your laptop or desktop.

---

## 📋 Minimum Requirements

- **OS:** Windows 10/11, macOS (Intel or Apple Silicon), or Linux (Ubuntu 20.04+)
- **Python:** Version 3.10, 3.11, or 3.12
- **RAM:** 4GB minimum (8GB recommended)
- **Disk:** ~2GB free space (for Ollama model and Whisper weights)
- **Microphone & Speakers:** Built-in laptop mic/speakers work great

---

## 🛠️ Step-by-Step Installation

### Step 1: Install Ollama & Pull the Model

SafeSpeak uses Ollama to run Google's lightweight `gemma3:1b` model locally.

1. Download Ollama from [https://ollama.com/download](https://ollama.com/download).
2. Install it and open a terminal.
3. Pull the model (downloads ~815MB):
   ```bash
   ollama pull gemma3:1b
   ```
4. Verify the model responds:
   ```bash
   ollama run gemma3:1b "Say hello in one word"
   ```

> **Tip:** Make sure Ollama is running in your background or tray. You can run `ollama serve` in a terminal if it isn't running automatically.

---

### Step 2: Clone SafeSpeak & Create Virtual Environment

```bash
git clone https://github.com/geeknishantkyeus/safespeak.git
cd safespeak
```

Create and activate a clean Python virtual environment:

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
*(If you see an execution policy error in PowerShell, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `streamlit` (interactive web UI)
- `ollama` (local LLM client)
- `openai-whisper` (offline speech recognition)
- `piper-tts` (offline neural voice engine)
- `emoji` (emoji stripping for clean speech)
- `imageio-ffmpeg` (bundled ffmpeg binary for audio processing)

---

### Step 4: Verify Voice Model

SafeSpeak comes bundled with the Piper ONNX voice model inside the `models/` directory:
- `models/en_US-lessac-medium.onnx`
- `models/en_US-lessac-medium.onnx.json`

If these files are present, you are good to go!

---

### Step 5: Start SafeSpeak

```bash
streamlit run app.py
```

Your default browser will open automatically at:
```
http://localhost:8501
```

---

## 🔍 Verifying 100% Offline Mode

SafeSpeak requires zero internet connectivity once models and packages are downloaded.

To test offline capability:
1. Turn off your Wi-Fi or disconnect your ethernet cable.
2. Confirm you have no internet:
   - Windows: `ping 8.8.8.8` (should timeout or fail)
   - Mac/Linux: `ping -c 1 8.8.8.8`
3. In the browser, start speaking or typing to Ava.
4. Voice transcription, LLM generation, and speech synthesis will continue working smoothly.

---

## 🧰 Troubleshooting Common Issues

### 1. `Local AI error: Connection refused` or `Ollama not running`
- **Cause:** The Ollama background daemon is stopped.
- **Fix:** Open a terminal and run `ollama serve`, or start the Ollama desktop app.

### 2. Whisper says `ffmpeg not found`
- **Cause:** Whisper requires `ffmpeg` to decode audio formats.
- **Fix:** SafeSpeak includes `imageio-ffmpeg`, but if your system cannot locate it, you can install ffmpeg directly:
  - **Windows:** `winget install Gyan.FFmpeg` or `choco install ffmpeg`
  - **macOS:** `brew install ffmpeg`
  - **Linux:** `sudo apt install ffmpeg`

### 3. Voice is too quiet or not playing
- **Cause:** Browser audio autoplay policy.
- **Fix:** Most modern browsers block audio autoplay on first click. Simply click the play button on the audio player widget once; subsequent messages will play smoothly.

### 4. Text input looks strange in dark mode
- SafeSpeak has an embedded theme in `styles.css` that provides high-contrast, accessible styling. If your browser forces a third-party dark mode extension (like Dark Reader), try disabling it on `localhost:8501`.

---

## ⌨️ Useful Commands Cheat Sheet

| Action | Command |
|---|---|
| Start App | `streamlit run app.py` |
| Pull Model | `ollama pull gemma3:1b` |
| List Models | `ollama list` |
| Run Ollama Service | `ollama serve` |
| Run Offline Check | `python -c "from tts import synthesize_speech; print(len(synthesize_speech('Hello world')))"` |
