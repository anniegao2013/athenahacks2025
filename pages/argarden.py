import streamlit as st

# Load external CSS file
with open("assets/otherstyles.css") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

st.markdown("<div class='main-header'>Your Garden</div>", unsafe_allow_html=True)

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

st.components.v1.iframe("https://temp-athena2025.vercel.app/", width=640, height=480)