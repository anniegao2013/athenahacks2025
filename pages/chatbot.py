import streamlit as st
import google.generativeai as genai
import os

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

st.markdown("<h1 style='text-align: center; color: black;'>Gemini Chatbot</h1>", unsafe_allow_html=True)

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