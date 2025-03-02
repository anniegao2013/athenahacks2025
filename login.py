import streamlit as st
from pymongo.server_api import ServerApi
import pymongo
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(initial_sidebar_state="collapsed")

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return pymongo.MongoClient(st.secrets["mongo"]["uri"], server_api=ServerApi('1'))

client = init_connection()

# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def get_data():
    db = client['plant_go'].get_collection('user_info')
    items = list(db.find())
    return items


st.markdown(
    """
    <style>
        [data-testid="stBaseButton-headerNoPadding"] {
            display: none
        }
        .stTextInput>div>div>input {
            text-align: left !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Load external CSS file
with open("assets/styles.css") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

st.markdown("<div class='main-header'>Welcome to PlantGo</div>", unsafe_allow_html=True)
with st.container(key="login-container"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login = st.button("Login")
    st.markdown("<p class='register-link'>Don't have an account? <a href=/register target='_self'>Sign up</a></p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

userExists = False
loginValid = False

if login:
    items = get_data()
    userExists = any(item.get('username') == username for item in items)
    loginValid = any(item.get('username') == username and item.get('password') == password for item in items)

    if loginValid:
        st.success("Login successful! Welcome, " + username + "!")
        st.session_state['username'] = username
        switch_page("Find")
    elif not userExists:
        st.error("User does not exist. Please make an account or try again.")
    else:
        st.error("Invalid username or password. Please try again.")