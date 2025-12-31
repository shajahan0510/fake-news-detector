import streamlit as st
from groq import Groq
import os

# -------------------------------------------------
# SECURE API KEY CONFIGURATION
# -------------------------------------------------
# This code looks for the key in Streamlit Secrets (for Cloud)
# or Environment Variables (for Local PC). 
# It does NOT have the key hardcoded here.
try:
    # Used when deployed on Streamlit Cloud
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    # Used when running locally (e.g., via terminal export)
    api_key = os.getenv("GROQ_API_KEY")

# Stop if no key is found
if not api_key:
    st.error("⚠️ API Key not found! Please add it to Streamlit Secrets or set the Environment Variable.")
    st.stop()

# Initialize Client
try:
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Error initializing Groq Client: {e}")
    st.stop()

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="Fake News Detection AI",
    page_icon="📰",
    layout="centered"
)

# -----------------------------
# UI
# -----------------------------
st.title("📰 Fake News Detection (AI)")
st.write("Paste a news article or headline. AI will classify it as **REAL** or **FAKE**.")

news_text = st.text_area("Enter news text", height=200)

# -----------------------------
# AI FUNCTION
# -----------------------------
def detect_fake_news(news):
    prompt = f"""
You are a fake news detection system.

Task:
1. Decide whether the news is REAL or FAKE.
2. Give a short reason.
3. Show confidence percentage.

Respond strictly in this format:
Label: [REAL or FAKE]
Confidence: [XX%]
Reason: [short explanation]

News:
{news}
"""

    try:
        # CHANGED MODEL TO A SUPPORTED ONE
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error contacting AI: {str(e)}"

# -----------------------------
# BUTTON ACTION
# -----------------------------
if st.button("🔍 Check News"):
    if news_text.strip() == "":
        st.warning("Please enter some news text.")
    else:
        with st.spinner("Analyzing with AI..."):
            result = detect_fake_news(news_text)

        st.subheader("🧠 AI Result")
        st.success(result)