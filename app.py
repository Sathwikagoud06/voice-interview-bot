import openai
import streamlit as st
from gtts import gTTS
import os
import tempfile

# Set page title
st.set_page_config(page_title="Voice Interview Bot", layout="centered")

# Title
st.title("🎙️ AI Voice Interview Bot")
st.markdown("Ask any interview question and hear my voice-based answer!")

# Get API key securely
openai.api_key = st.secrets["OPENAI_API_KEY"]

# System prompt to reflect YOUR personality
system_prompt = """
You are Sathwika, an AI enthusiast applying for Home.LLC’s AI Agent Team role.
Respond in a friendly, thoughtful, and passionate tone. Reflect your real personality and answer as you would in an interview.
"""

# User input
user_input = st.text_input("Ask me a question (e.g., What's your #1 superpower?)", "")

if user_input:
    # Call ChatGPT API
    with st.spinner("Thinking..."):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        answer = response['choices'][0]['message']['content']
        st.write("🗣️", answer)

        # Generate voice using gTTS
        tts = gTTS(answer)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            st.audio(fp.name, format='audio/mp3')
