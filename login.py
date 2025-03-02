import streamlit as st

st.markdown("<h1 style='text-align: center; color: black;'>Welcome to ________! </h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: black;'>Some text here perhaps? Information? </p>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: black;'>Username</h3>", unsafe_allow_html=True)
username = st.text_input("")
st.markdown("<h3 style='text-align: center; color: black;'>Password</h3>", unsafe_allow_html=True)
password = st.text_input(" ", type="password")
login = st.button("Login")