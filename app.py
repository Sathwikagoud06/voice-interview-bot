import openai
import streamlit as st
from gtts import gTTS
import os
import tempfile

# Set page title
st.set_page_config(page_title="Voice Interview Bot", layout="centered")

# Title and instruction
st.title("🎙️ AI Voice Interview Bot")
st.markdown("Ask any interview question and hear my voice-based answer!")

# Add important message for recruiter or user
st.info("📝 **Note:** If the app doesn’t respond immediately, it may be due to OpenAI's temporary rate limits. Please wait a few seconds and try again. The app is working fine — this is just a limit from the OpenAI server.")

# Load your OpenAI API key securely from Streamlit Secrets
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# System prompt to define the bot's personality
system_prompt = """
You are Sathwika, an AI enthusiast applying for an AI Agent role at a forward-thinking startup.
Respond in a friendly, thoughtful, and passionate tone. Reflect your real personality and answer as you would in an interview.
"""

# Input box for user questions
user_input = st.text_input("Ask me a question (e.g., What's your #1 superpower?)", "")

# If there's a question, process it
if user_input:
    try:
        with st.spinner("Thinking..."):
            # ChatGPT API call
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ]
            )
            answer = response.choices[0].message.content
            st.write("🗣️", answer)

            # Convert text to speech
            tts = gTTS(answer)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                st.audio(fp.name, format='audio/mp3')

    except openai.RateLimitError:
        st.error("⚠️ Sorry, too many requests right now (OpenAI rate limit). Please wait a moment and try again.")
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {e}")
