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
@st.cache_data(ttl=600)
def get_data():
    db = client['plant_go'].get_collection('user_info')
    items = list(db.find())
    return items

# Pull data from the collection.
@st.cache_data(ttl=600)
def get_user_plants(username):
    db = client['plant_go'].get_collection('user_info')
    user_data = db.find_one({"username": username})  # Find a specific user by username
    if user_data:
        return user_data.get('plants', [])
    return []

user = st.session_state['username']

@st.cache_data(ttl=600)
def print_plants():
    user_plants = get_user_plants(user)
    for plant in user_plants:
        st.markdown(plant)
    return

print_plants()