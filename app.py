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
st.markdown("📝 *Note: If the app doesn’t respond immediately, please wait a few seconds and try again. I may be handling multiple requests.*")

# Securely get API key
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Personality / system prompt
system_prompt = """
You are Sathwika, an AI enthusiast applying for an AI Agent role at a forward-thinking startup.
Respond in a friendly, thoughtful, and passionate tone. Reflect your real personality and answer as you would in an interview.
"""

# Input field
user_input = st.text_input("Ask me a question (e.g., What's your #1 superpower?)", "")

if user_input:
    with st.spinner("Thinking..."):
        try:
            # Call ChatGPT API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ]
            )
            answer = response.choices[0].message.content

        except openai.RateLimitError:
            answer = "⚠️ Sorry, too many requests right now. Please wait a few seconds and try again."

        except Exception as e:
            answer = f"❌ Oops! Something went wrong. Please try again. \n\n_Error: {str(e)}_"

        # Show answer
        st.write("🗣️", answer)

        # Convert text to speech
        tts = gTTS(answer)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            st.audio(fp.name, format='audio/mp3')
