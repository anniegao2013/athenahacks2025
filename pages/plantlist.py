import streamlit as st
from pymongo.server_api import ServerApi
import pymongo
from streamlit_extras.switch_page_button import switch_page

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

# Pull data from the collection.
def get_user_plants(username):
    db = client['plant_go'].get_collection('user_info')
    user_data = db.find_one({"username": username})  # Find a specific user by username
    if user_data:
        return user_data.get('plants', {})
    return {}

def get_all_plants():
    db = client['plant_go'].get_collection('plant_info')
    return list(db.find({}, {"_id": 0}))

# Print functions

def print_user_plants():
    user_plants = get_user_plants(user)
    for plant in user_plants:
        st.markdown(plant)
    return

def print_all_plants():
    db = client['plant_go'].get_collection('plant_info')
    return

# Print plant info
def print_plant_info(name):
    plant_list = get_all_plants()
    user_plants = get_user_plants(user)
    plant_data = next((plant for plant in plant_list if plant["Plant"] == name), None)

    st.subheader(name.replace("-", " "))
    
    if plant_data:
        st.write(f"**Conservation Status:** {plant_data['Conservation status']}")
        st.write(f"**Medicinal Usage:** {plant_data['Medicinal usage']}")
        st.write(f"**Victorian Flower Language:** {plant_data['Victorian flower language']}")
        found_count = user_plants.get(name, 0)
        st.write(f"**Times Found:** {found_count}")
    else:
        st.write("Sorry! No information right now.")

user = st.session_state['username']

st.markdown("<div class='main-header'>Plant Collection</div>", unsafe_allow_html=True)

user_plants = get_user_plants(user)
plant_list = get_all_plants()

selected_plant = st.selectbox("Select a plant to view details:", [plant["Plant"] for plant in plant_list])

if selected_plant:
    print_plant_info(selected_plant)