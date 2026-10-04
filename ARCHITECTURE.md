# 🏛️ SafeSpeak Architecture & Technical Design

This document explains the technical architecture, latency optimizations, memory footprint, and privacy boundary of SafeSpeak.

---

## 🎯 Design Philosophy

SafeSpeak was engineered around three strict constraints:
1. **Zero Cloud Dependencies:** The entire pipeline must execute on local hardware (`localhost`) without network connectivity.
2. **Sub-1.5s Conversational Turnaround:** In conversational speech, pauses longer than 2 seconds feel awkward and induce anxiety for beginners.
3. **Low Hardware Barrier:** The app must run on ordinary student and office laptops (e.g. 8GB RAM, modern multi-core CPU) without requiring a dedicated high-end GPU.

---

## 🔄 End-to-End Pipeline

```
                     ┌───────────────────────────────┐
                     │          User Audio           │
                     └───────────────┬───────────────┘
                                     │ (WAV Bytes via WebRTC)
                                     ▼
                     ┌───────────────────────────────┐
                     │      Whisper Base (CPU)       │
                     │  - greedy decoding            │  ~700ms
                     │  - beam_size=1, best_of=1     │
                     └───────────────┬───────────────┘
                                     │
                             (User Text String)
                                     ▼
                     ┌───────────────────────────────┐
                     │    Prompt Engine & Router     │
                     │  - Devanagari Hindi check     │  < 1ms
                     │  - Hinglish keyword check     │
                     │  - Scenario context injection │
                     └───────────────┬───────────────┘
                                     │
                             (Contextual Prompt)
                                     ▼
                     ┌───────────────────────────────┐
                     │     Ollama + Gemma 3 (1B)     │
                     │  - temperature: 0.2           │  ~400ms
                     │  - num_predict: 50            │
                     └───────────────┬───────────────┘
                                     │
                              (AI Reply Text)
                                     │
              ┌──────────────────────┴──────────────────────┐
              ▼                                             ▼
┌───────────────────────────────┐             ┌───────────────────────────────┐
│     Streamlit Chat UI         │             │       clean_for_tts()         │
│  - Displays Markdown          │             │  - Strips emojis & markdown   │
│  - Displays Emojis            │             │  - Converts symbols to speech │
└───────────────────────────────┘             └──────────────┬────────────────┘
                                                             │
                                                      (Sanitized Text)
                                                             ▼
                                              ┌───────────────────────────────┐
                                              │      Piper TTS (ONNX)         │
                                              │  - In-memory cached model     │  ~120ms
                                              │  - length_scale: 1.06 (cadence│
                                              └──────────────┬────────────────┘
                                                             │
                                                        (WAV Audio)
                                                             ▼
                                              ┌───────────────────────────────┐
                                              │       Audio Playback          │
                                              └───────────────────────────────┘
```

**Total End-to-End Latency:** ~1.2s to 1.4s on standard 8-core CPU.

---

## ⚡ Latency Optimizations

### 1. Whisper Greedy Decoding
Standard Whisper beam search explores multiple acoustic branches (`beam_size=5`), which is computationally expensive on CPUs (~3.5s per turn).
In `transcribe.py`:
- We set `beam_size=1`, `best_of=1`, and `temperature=0.0`.
- This greedy single-pass search drops transcription time to ~700ms on CPU with virtually zero accuracy loss on short beginner phrases.

### 2. Piper TTS In-Memory Model Caching
Reloading ONNX voice models from disk takes ~1.2 seconds per sentence.
In `tts.py`:
- The `PiperVoice` instance is loaded and pre-warmed into memory once on application startup.
- Subsequent speech synthesis runs in under 150ms directly into an in-memory `io.BytesIO()` WAV buffer.

### 3. Gemma 3 1B with Strict Generation Limits
By using Google's lightweight `gemma3:1b` model:
- RAM footprint is under 900MB.
- `num_predict` is capped at 50 tokens. Because Ava's persona rule is to respond in 1–2 friendly sentences, generation finishes in ~400ms without dragging out into essays.
- `temperature=0.2` keeps responses predictable, consistent, and fast.

---

## 🇮🇳 The Hindi & Hinglish Comprehension Bridge

Most LLMs fine-tuned on English struggle when a beginner enters Devanagari Hindi (e.g. `"मुझे कॉफ़ी चाहिए"`) or Hinglish (e.g. `"mujhe pani chahiye"`). The models often hallucinate or start replying in Hindi poetry.

SafeSpeak solves this in `prompts.py`:
1. **Detection:** Checks Unicode range `\u0900-\u097F` for Devanagari and a curated hashset of common Roman-script Hindi keywords.
2. **Intent Comprehension:** Instead of running a heavy transliteration pipeline, the prompt directly instructs Gemma 3 to extract the intended meaning and provide the exact English equivalent the learner needs.
3. **Response Formulation:** Replies in simple, clear English:
   > *"You can say: 'I want a coffee.' Try saying it!"*

---

## 🔒 Privacy & Security Boundary

| Threat Vector | Cloud-Based Tutors | SafeSpeak |
|---|---|---|
| Voice Recording Uploads | Uploaded to vendor S3 / CDN | Stored in RAM, discarded after session |
| User Telemetry | Tracked via Mixpanel / PostHog | Zero tracking, telemetry disabled |
| Data Retention for Training | Conversation logged to cloud DB | Zero network calls, 100% ephemeral |
| Offline Resilience | Breaks if connection drops | Works seamlessly without internet |

All interactions remain strictly bounded within `localhost:8501` and `localhost:11434`.
