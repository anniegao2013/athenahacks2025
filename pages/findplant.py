import streamlit as st
from PIL import Image
import os
import tempfile
import requests
import json
# MongoDB imports
from pymongo.server_api import ServerApi
import pymongo
from streamlit_extras.switch_page_button import switch_page

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

API_KEY = "2b104yodLOKaoU2uasSjUWIatu"
PROJECT = "all"
api_endpoint = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={API_KEY}"

# MongoDB Functions

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

#function to use api
def identify_plant(image_path):
    try:
        with open(image_path, 'rb') as image_file:
            files = [
                ('images', (image_path, image_file)),
            ]
            data = {
                'organs': ['flower'],  # Specify the organs you want to identify (leaf, flower, etc.)
            }
            req = requests.Request('Post', url=api_endpoint, files=files, data=data)
            prepared = req.prepare()
            s = requests.Session()
            response = s.send(prepared)
            json_result = json.loads(response.text)
            if response.status_code != 200:
                st.write("Sorry! Result unavailable")
            else:
                species_info = json_result["results"][0].get("species", {})
                name = species_info.get("commonNames", "No common names found")[0]
                return name
    finally:
        if os.path.exists(image_path):
            os.remove(image_path)

#uploads image
st.markdown("<h1 style='text-align: center; color: black;'>Upload image</h1>", unsafe_allow_html=True)
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

#make temporary directory
TEMP_DIR = "temp_images"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)
#save image to temporary directory
def save_image_to_temp(image, temp_dir=TEMP_DIR):
    temp_file = tempfile.NamedTemporaryFile(delete=False, dir=temp_dir, suffix=".jpg")
    image.save(temp_file, format="JPEG")
    temp_file.close()
    return temp_file.name

# Print plant info

def get_user_plants(username):
    db = client['plant_go'].get_collection('user_info')
    user_data = db.find_one({"username": username})  # Find a specific user by username
    if user_data:
        return user_data.get('plants', {})
    return {}

def get_all_plants():
    db = client['plant_go'].get_collection('plant_info')
    return list(db.find({}, {"_id": 0}))

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

# Update Plant Info
def update_plant_info(name):
    db = client['plant_go'].get_collection('user_info')
    user_plants = get_user_plants(user)
    new_found_count = user_plants.get(name, 0) + 1
    #user_data = db.find_one({"username": user})  # Find a specific user by username
    query_filter = {"username": user}
    update_operation = {'$set' :
                            {f"plants.{name}": new_found_count}
                        }
    db.update_one(query_filter, update_operation)
    return

# Actual code for the page

user = st.session_state['username']

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image.", use_container_width=True)
    temp_image_path = save_image_to_temp(image)
    plant_name = identify_plant(temp_image_path)
    #plant_name = identify_plant(temp_image_path).lower().replace("-", " ")
    #st.write(plant_name)
    update_plant_info(plant_name)
    print_plant_info(plant_name)