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
def get_user_data(username):
    db = client['plant_go'].get_collection('user_info')
    return db.find_one({"username":username})

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
user_data = get_user_data(user)

st.markdown("<div class='main-header'>Profile</div>", unsafe_allow_html=True)

st.subheader("Account Information")
st.write(f"**Username:** {user_data['username']}")

show_password = st.checkbox("Show Password")
password = user_data['password']

if show_password:
    st.write(f"**Password:** {user_data['password']}")
else:
    st.write(f"**Password:** {'•' * len(password)}")

# Logout
if st.button("Logout"):
    del st.session_state["username"]
    switch_page("login")
