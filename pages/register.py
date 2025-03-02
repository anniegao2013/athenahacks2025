import streamlit as st
from pymongo.server_api import ServerApi
import pymongo
from streamlit_extras.switch_page_button import switch_page

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return pymongo.MongoClient(st.secrets["mongo"]["uri"], server_api=ServerApi('1'))

client = init_connection()

# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
# @st.cache_data(ttl=600)
def get_data():
    db = client['plant_go'].get_collection('user_info')
    items = list(db.find())
    return items

# Add User to Database
def add_user(username, password):
    db = client['plant_go'].get_collection('user_info')
    db.insert_one({
        "username":username,
        "password":password,
        "points":0,
        "plants":{"Broadleaf harebell":0,"Bush allamanda":0,"Hydrangea":0,"Lily-of-the-valley":0,"Mexican-Sunflower":0},
        "garden":{"Broadleaf harebell":0,"Bush allamanda":0,"Hydrangea":0,"Lily-of-the-valley":0,"Mexican-Sunflower":0}
    })
    return

st.markdown(
    """
    <style>
        body {
            background-color: white;
        }
        .main-header {
            text-align: left;
            color: black;
            font-size: 40px;
            font-weight: bold;
            border-radius: 10px;
        }
        .login-container {
            width: 40%;
            margin: auto;
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }
        .stTextInput>div>div>input {
            text-align: center;
        }
        .stButton>button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 10px;
        }
        .register-link {
            margin-top: 10px;
            font-size: 14px;
        }
        .register-link a {
            color: #4CAF50;
            text-decoration: none;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='main-header'>Register</div>", unsafe_allow_html=True)
st.markdown("<div class='login-container>", unsafe_allow_html=True)
username = st.text_input("Username")
password = st.text_input("Password", type="password")
login = st.button("Register")
st.markdown("</div></div>", unsafe_allow_html=True)

userExists = False
loginValid = False

if login:
    items = get_data()
    # for item in items:
    #     theUsername = item.get('username')
    #     thePassword = item.get('password')
    #     if username==theUsername and password==thePassword:
    #         loginValid=True
    #         break
    items = get_data()
    userExists = any(item.get('username') == username for item in items)

    if userExists:
        st.error("User already exists. Please try again.")
    else:
        add_user(username, password)
        st.success("Register successful! Welcome, " + username + "!")
        st.session_state['username'] = username
        switch_page("findplant")

    # st.markdown("</div>", unsafe_allow_html=True)