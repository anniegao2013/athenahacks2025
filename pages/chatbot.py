import streamlit as st
import google.generativeai as genai
import os

# Load external CSS file
with open("assets/otherstyles.css") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

#change navbar - this must be in every page but login.py and register.py
st.markdown(
    """
    <style>
        a[href="http://localhost:8501/login"] {
            display: none;
        }
        a[href="http://localhost:8501/register"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True
)

GOOGLE_API_KEY = "AIzaSyCeLzlhglcW8HeGvtDaczMsTETdcZFHruM"
genai.configure(api_key=GOOGLE_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<div class='main-header'>Gemini Chatbot</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: black;'>Ask Gemini about the plants you discovered, and more!</h1>", unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    model = genai.GenerativeModel("models/gemini-2.0-flash-exp")
    response = model.generate_content(prompt + "generate two sentences")
    bot_reply = response.text

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    with st.chat_message("assistant"):
        st.markdown(bot_reply)