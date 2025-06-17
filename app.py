import streamlit as st
from gtts import gTTS
import os
import tempfile
import requests

# Set page title
st.set_page_config(page_title="Voice Interview Bot", layout="centered")

# Title and instruction
st.title("🎙️ AI Voice Interview Bot")
st.markdown("Ask any interview question and hear my voice-based answer!")

# Info note to recruiter or user
st.info("📝 **Note:** If the app doesn’t respond immediately, it may be due to server load. Please wait a few seconds and try again. The app is working fine — this is just a server limit.")

# Together AI setup
TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]  # You must add this in your Streamlit secrets

# ✅ FINAL SYSTEM PROMPT
system_prompt = """
You are Sathwika Goud, an MSc Data Science student with a strong interest in AI and solving real-world problems.
Answer the following interview questions honestly, confidently, and naturally — as if you're in a real interview.

Do NOT say anything like “I am an AI assistant” or “I don't have feelings.”
Avoid robotic, generic, or overly formal responses.

Speak with clarity and passion. Show your eagerness to collaborate, your ability to adapt, and your drive to grow in the AI field.

Use your real background (MSc in Data Science), your hands-on project experiences, your collaborative mindset, and your strong motivation to contribute meaningfully to any team.
"""

# Input box
user_input = st.text_input("Ask me a question (e.g., What's your #1 superpower?)", "")

# If input exists
if user_input:
    try:
        with st.spinner("Thinking..."):
            headers = {
                "Authorization": f"Bearer {TOGETHER_API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "mistralai/Mistral-7B-Instruct-v0.2",

                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                "max_tokens": 512,
                "temperature": 0.7
            }

            response = requests.post("https://api.together.xyz/v1/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            answer = response.json()["choices"][0]["message"]["content"]
            st.write("🗣️", answer)

            # Voice output
            tts = gTTS(answer)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                st.audio(fp.name, format='audio/mp3')

    except requests.exceptions.HTTPError as errh:
        st.error("⚠️ HTTP Error: Please try again. If it continues, check your Together API key.")
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {e}")
