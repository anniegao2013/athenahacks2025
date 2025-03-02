import streamlit as st
from pymongo.server_api import ServerApi
import pymongo
import os

# Load external CSS file
with open("assets/otherstyles.css") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

# Change navbar - this must be in every page but login.py and register.py
st.markdown(
    """
    <style>
        a[href="http://localhost:8501/login"] { display: none; }
        a[href="http://localhost:8501/register"] { display: none; }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize MongoDB connection
@st.cache_resource
def init_connection():
    return pymongo.MongoClient(st.secrets["mongo"]["uri"], server_api=ServerApi('1'))

client = init_connection()

# Fetch all plants from the database
def get_all_plants():
    db = client['plant_go'].get_collection('plant_info')
    return list(db.find({}, {"_id": 0}))

# Fetch user-specific plant data
def get_user_plants(username):
    db = client['plant_go'].get_collection('user_info')
    user_data = db.find_one({"username": username})
    return user_data.get('plants', {}) if user_data else {}

# Display plant information and image
def print_plant_info(name):
    plant_list = get_all_plants()
    user_plants = get_user_plants(user)
    plant_data = next((plant for plant in plant_list if plant["Plant"] == name), None)
    
    st.subheader(name.replace("-", " "))
    
    # Display plant image
    image_path = f"assets/images/{name}.jpg"
    if os.path.exists(image_path):
        st.image(image_path, caption=name)
    else:
        st.write("No image available for this plant.")
    
    if plant_data:
        st.write(f"**Conservation Status:** {plant_data['Conservation status']}")
        st.write(f"**Medicinal Usage:** {plant_data['Medicinal usage']}")
        st.write(f"**Victorian Flower Language:** {plant_data['Victorian flower language']}")
        found_count = user_plants.get(name, 0)
        st.write(f"**Times Found:** {found_count}")
    else:
        st.write("Sorry! No information right now.")

# Ensure user is logged in
if 'username' not in st.session_state:
    st.error("You must be logged in to view this page.")
    st.stop()

user = st.session_state['username']

# Page header
st.markdown("<div class='main-header'>Plant Collection</div>", unsafe_allow_html=True)

# Fetch plant data
plant_list = get_all_plants()
selected_plant = st.selectbox("Select a plant to view details:", [plant["Plant"] for plant in plant_list])

# Display selected plant info
if selected_plant:
    print_plant_info(selected_plant)