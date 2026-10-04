from pathlib import Path
import streamlit as st
from ollama_chat import chat
from prompts import SCENARIO_STARTERS
from transcribe import transcribe_audio
from tts import clean_for_tts, synthesize_speech

st.set_page_config(page_title="SafeSpeak", page_icon="🎙️", layout="centered", initial_sidebar_state="expanded")

# Load CSS theme
css_path = Path(__file__).parent / "styles.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header & Badges
st.markdown(
    '<span class="eyebrow">BUILT FOR HACKTOBERFEST 2026</span>'
    '<span class="hero-squares">'
    '<span class="hero-sq" style="background:#1F4D2E"></span>'
    '<span class="hero-sq" style="background:#FFB800"></span>'
    '<span class="hero-sq" style="background:#E73427"></span>'
    '<span class="hero-sq" style="background:#0D2B1A"></span>'
    '</span>',
    unsafe_allow_html=True
)
st.title("SafeSpeak")
st.markdown('<p class="tagline">Your private English practice partner</p>', unsafe_allow_html=True)
st.markdown('<span class="privacy-badge">🔒 Privacy: Everything local — 100% offline</span>', unsafe_allow_html=True)

# Sidebar controls
with st.sidebar:
    st.markdown('<h2 style="color:#FFFFFF; margin-bottom:8px;">Settings</h2>', unsafe_allow_html=True)
    voice_enabled = st.toggle("Voice Output (Piper TTS)", value=True)
    st.markdown("<hr style='border-color: rgba(255,255,255,0.25); margin: 16px 0;'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.85rem; color:#F5F2EB;'>SafeSpeak runs 100% locally on your machine. No cloud APIs, no tracking, and no external calls.</p>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# Scenario quick buttons
st.markdown('<p style="font-weight:700; color:#1F4D2E; margin-top:12px; margin-bottom:6px;">Practice Scenarios:</p>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

if col1.button("🍔 Order Food"):
    st.session_state.messages = [{"role": "assistant", "content": SCENARIO_STARTERS["food"], "audio": None}]
    st.rerun()
elif col2.button("📞 Phone Call"):
    st.session_state.messages = [{"role": "assistant", "content": SCENARIO_STARTERS["phone"], "audio": None}]
    st.rerun()
elif col3.button("👋 Greeting"):
    st.session_state.messages = [{"role": "assistant", "content": SCENARIO_STARTERS["greeting"], "audio": None}]
    st.rerun()
elif col4.button("🗺️ Directions"):
    st.session_state.messages = [{"role": "assistant", "content": SCENARIO_STARTERS["directions"], "audio": None}]
    st.rerun()

# Initialize conversation history with an easy beginner greeting
if "messages" not in st.session_state or not st.session_state.messages:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm Ava. What is your name?", "audio": None}
    ]

# Display previous conversation
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "🎙️"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])
        if msg.get("audio"):
            st.audio(msg["audio"], format="audio/wav")

# Audio input widget for voice recording
audio_record = st.audio_input("Record voice practice (Whisper)")

user_input = None

if audio_record is not None:
    audio_bytes = audio_record.read()
    if audio_bytes and st.session_state.get("last_audio") != len(audio_bytes):
        st.session_state["last_audio"] = len(audio_bytes)
        with st.spinner("Transcribing with Whisper..."):
            transcribed = transcribe_audio(audio_bytes)
        if transcribed and not transcribed.startswith("Audio transcription error:"):
            user_input = transcribed
        elif transcribed:
            st.warning(transcribed)

# Text chat input
text_input = st.chat_input("Type in English, Hindi, or Hinglish...")
if text_input:
    user_input = text_input

# Process user turn
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.write(user_input)

    with st.spinner("Thinking..."):
        ai_reply = chat(st.session_state.messages)

    audio_bytes = None
    if voice_enabled:
        cleaned = clean_for_tts(ai_reply)
        if cleaned:
            audio_bytes = synthesize_speech(cleaned)

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply,
        "audio": audio_bytes
    })

    with st.chat_message("assistant", avatar="🎙️"):
        st.write(ai_reply)
        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav", autoplay=True)
