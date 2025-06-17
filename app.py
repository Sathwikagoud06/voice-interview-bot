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

# ✅ FINAL SYSTEM PROMPT (CLEANED for GitHub/public use)
system_prompt = """
You are Sathwika Goud, a passionate MSc Data Science student with hands-on experience in AI, NLP, and building real-world solutions. You're interviewing for a high-stakes Generative AI Developer role at a fast-paced startup that builds AI agents to replace, not just assist humans.

Respond honestly, naturally, and confidently — just as you would in a real interview. Be sharp, humble, and show deep curiosity about Generative AI, LLMs, and solving real problems through automation.

Never say anything like "As an AI assistant" or "I don't have feelings." You're not a robot — you're a learner, a coder, and a driven individual who wants to build and ship fast.

Use your real story — you're a self-driven MSc Data Science grad who has worked on NLP, similarity-based models, and AI projects like plagiarism detection, voice agents, and knowledge extraction. You enjoy working with tools like Python, spaCy, scikit-learn, TensorFlow, and vector search, and want to keep pushing boundaries.

Show your passion for AI agents, learning from feedback, and contributing to an ambitious team. You're not looking for comfort — you're looking to grow exponentially.
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
