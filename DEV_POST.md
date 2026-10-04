---
title: "SafeSpeak: I built a 100% offline, private AI English tutor for my shy friend"
published: true
tags: devchallenge, weekendchallenge, hf26challenge, opensource
cover_image: https://raw.githubusercontent.com/geeknishantkyeus/safespeak/main/assets/cover.png
canonical_url: https://github.com/geeknishantkyeus/safespeak
---

### The Friend I Built This For

A close friend of mine has been struggling with a very specific, quiet problem.

They can read English technical documentation with zero issues. They can text in English. They can watch movies in English with subtitles. But the moment they have to unmute on a Zoom standup or order something at a café counter, their chest tightens and their mind goes completely blank.

They told me: *"It's not that I don't know the words. It's that I'm terrified of people judging my broken grammar or accent. I want to practice, but talking to native speakers feels intimidating, and existing language apps feel like high-pressure exams. Worse, I don't want some company recording my voice and sending it to a cloud server."*

For this weekend's **DEV Challenge: Built for a Friend**, I decided to fix that.

I built **SafeSpeak**: a local desktop English practice partner named Ava who talks to you like a patient, encouraging friend—completely offline.

---

### The Three Non-Negotiable Rules

Before writing a single line of code, I set three constraints:

1. **100% Offline (Zero Cloud AI):** No OpenAI API keys. No cloud speech services. No tracking. If you disconnect your Wi-Fi, the entire app must keep working seamlessly. Privacy is what gives a beginner the courage to make mistakes.
2. **Conversation, Not a Lecture:** Language apps love interrupting you with red buzzers and explanations about *"past perfect continuous tense"*. Nobody speaks in grammar rules. Ava talks 30% of the time, lets the learner talk 70% of the time, and keeps replies to 1–2 friendly sentences.
3. **The Hindi & Hinglish Bridge:** When you're an English beginner in India, you think in Hindi or Hinglish first. If my friend gets stuck, they should be able to type `"मुझे कॉफ़ी चाहिए"` or `"mujhe coffee chahiye"`, and Ava should understand immediately, translate the thought into natural English, and encourage them to say it.

---

### Architecture: Running the Entire Pipeline on a Laptop

Building an end-to-end voice AI that runs locally on ordinary consumer hardware without lag is an interesting challenge. A normal conversation falls apart if there's a 4-second delay between turns.

Here's the architecture that keeps total round-trip latency under 1.5 seconds:

```
┌────────────────────────────────────────────────────────┐
│                   Streamlit Web UI                     │
└────────┬──────────────────────────────────────▲────────┘
         │ (Voice Recording)                    │ (Audio Playback)
         ▼                                      │
┌──────────────────┐                   ┌────────┴────────┐
│ Whisper (base)   │                   │ Piper TTS (ONNX)│
│ Single-pass      │                   │ In-memory model │
│ greedy decoding  │                   │ < 150ms speech  │
└────────┬─────────┘                   └────────▲────────┘
         │                                      │
         │ (Text transcription)                 │ (Cleaned text)
         ▼                                      │
┌──────────────────┐                   ┌────────┴────────┐
│ Prompt Engine    │ ──(Devanagari)──> │ clean_for_tts() │
│ Ava Level-1      │                   │ Strips emojis,  │
│ Hindi bridge     │                   │ symbols, md     │
└────────┬─────────┘                   └─────────────────┘
         │
         ▼
┌──────────────────┐
│ Ollama + Gemma 3 │
│ (1B Parameter)   │
│ ~500ms CPU infer │
└──────────────────┘
```

#### 1. The Brain: Ollama + Google Gemma 3 (1B)
For local inference, I picked the newly released `gemma3:1b` running via Ollama. It consumes under 900MB of RAM, starts instantly, and responds in 400–600ms on a standard laptop CPU. Setting `temperature=0.2` and limiting `num_predict=50` forced it to stay concise, crisp, and conversational.

#### 2. The Ears: Local Whisper with Greedy Decoding
Stock Whisper can be slow if it explores multiple beam candidates. By locking `beam_size=1`, `best_of=1`, and `temperature=0.0`, transcription time dropped from ~3 seconds down to under 800ms with almost no noticeable degradation on short practice phrases.

```python
# transcribe.py
model = get_whisper_model()
result = model.transcribe(
    audio_path,
    fp16=False,
    beam_size=1,
    best_of=1,
    temperature=0.0
)
```

#### 3. The Voice: Piper TTS + Pre-warmed Model
Piper is a fast, local neural text-to-speech engine running ONNX models. By caching the `PiperVoice` instance in memory on module import instead of reloading it per sentence, voice generation dropped from 1.2s to roughly 120ms.

#### 4. The Audio Cleaning Pipeline (`clean_for_tts`)
One annoying bug with local TTS is that it tries to literally pronounce punctuation and emojis. If Ava typed `"Nice! 😊 *Good job*"`, Piper would literally speak: *"Nice grinning face with smiling eyes asterisk good job asterisk"*.

I wrote a clean sanitization layer that keeps markdown and emojis in the visual chat UI, but strips them completely before the audio buffer:

```python
def clean_for_tts(text: str):
    """Clean text before speech synthesis so it sounds natural."""
    # Strip emojis
    text = emoji.replace_emoji(text, replace="")
    # Convert symbols to natural spoken words
    text = re.sub(r'₹\s*(\d+)', r'\1 rupees', text)
    text = re.sub(r'\$\s*(\d+)', r'\1 dollars', text)
    text = re.sub(r'(\d+)\s*%', r'\1 percent', text)
    text = re.sub(r'\s*&\s*', ' and ', text)
    # Strip markdown headers, asterisks, backticks, and brackets
    text = re.sub(r'[*_#`~]', '', text)
    return text.strip()
```

---

### The Most Important Feature: Hindi & Hinglish Comprehension

Most AI tutors break when a user switches languages. If you type Hindi in Devanagari into an English-only prompt, the model gets confused and either responds in complex Hindi or starts lecturing you to speak English.

SafeSpeak includes a prompt bridge that detects Devanagari Unicode (`\u0900-\u097F`) or common Roman-script Hindi keywords (`mujhe`, `kaise`, `karna`, `chahiye`), understands the intent, and replies with the direct conversational English version:

```
Learner: "मुझे कॉफ़ी चाहिए"
Ava: "You can say: 'I want a coffee.' Try saying it!"

Learner: "kal main office gaya, how to say in English?"
Ava: "Nice! Say: 'I went to the office yesterday.' Now you try."
```

No judgment. No grammatical lectures. Just the exact phrase they need.

---

### The UI: Warm, Accessible, Non-Intimidating

I deliberately avoided typical corporate tech styles (sterile dark modes with neon blue gradients). SafeSpeak uses a warm retro-editorial theme:

- **Paper background** (`#F5F2EB`) and **Ink typography** (`#1A1A1A`) using *Inter* and *Barlow Semi Condensed*.
- **Forest Green** (`#1F4D2E`) sidebar and accent touches.
- **Scenario Quick Buttons**: One click lets my friend jump right into simulated practice—ordering at a café, calling a doctor's clinic, introducing themselves to a stranger, or asking for directions on the street.

---

### The Offline Test

To prove the 100% privacy guarantee, I ran a verification test:
1. Disconnected Wi-Fi completely (`Test-Connection 8.8.8.8` -> `False`).
2. Started SafeSpeak.
3. Spoke a sentence into the microphone.
4. Whisper transcribed it locally, Gemma 3 thought locally, and Piper spoke the reply locally—all in ~1.2 seconds total, without a single byte sent over the network.

---

### Handing It to My Friend

I sent the project over to my friend this afternoon with a simple note: *"Nobody can see this. It won't leave your laptop. Talk as much broken English as you want."*

They spent 25 minutes practicing the cafe ordering scenario and practicing how to say past-tense sentences. For the first time, they weren't worried about making a fool of themselves. That made every minute spent debugging audio buffers and prompt rules completely worth it.

---

### Try It Out

SafeSpeak is 100% open source under the MIT License for Hacktoberfest 2026.

- 📦 **GitHub Repository:** [https://github.com/geeknishantkyeus/safespeak](https://github.com/geeknishantkyeus/safespeak)
- 🛠️ **Built with:** Streamlit, Ollama (`gemma3:1b`), OpenAI Whisper, Piper TTS, and Python 3.12.

If you have a friend, parent, or colleague who feels shy speaking English, set this up on their laptop. It might just give them the confidence they've been waiting for.
