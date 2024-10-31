from gtts import gTTS
import tempfile
import base64
import streamlit as st
from pydub import AudioSegment


def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

def play_message(message):
    # Generate audio from the message
    tts = gTTS(text=message, lang='en')

    # Use a temporary file to store the audio
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
        tts.save(tmp_file.name)
        # Use Streamlit's audio component to play the audio file
        autoplay_audio(tmp_file.name)
        # Load the audio file to calculate duration
        audio = AudioSegment.from_file(tmp_file.name)
        duration_in_seconds = len(audio) / 1000.0  # Convert milliseconds to seconds
        return duration_in_seconds