import os
import streamlit as st
import pyttsx3
import openai

# Load secret key from environment variable
openai.api_key = os.environ['OPENAI_API_KEY']

# Text-to-speech engine
engine = pyttsx3.init()

# Streamlit UI setup
st.set_page_config(page_title="Interview Voice Bot", page_icon="🎤")
st.title("🎤 AI Interview Voice Bot")
st.markdown("Ask your interview-style question below. This bot responds as **Sathwika Goud** would in a job interview.")

user_input = st.text_input("💬 Your Question:")

if user_input:
    with st.spinner("Thinking..."):
        try:
            # ChatGPT API call
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You're answering as Sathwika Goud in a job interview. Be thoughtful, confident, and realistic."},
                    {"role": "user", "content": user_input}
                ]
            )
            reply = response['choices'][0]['message']['content']
            st.success(reply)

            # Speak the answer
            engine.say(reply)
            engine.runAndWait()

        except Exception as e:
            st.error(f"❌ Error: {e}")
