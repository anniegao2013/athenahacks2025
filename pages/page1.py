import streamlit as st
from PIL import Image
import os
import tempfile
import requests
import json

API_KEY = "2b104yodLOKaoU2uasSjUWIatu"
PROJECT = "all"
api_endpoint = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={API_KEY}"

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
                st.write("Your plant is a", name)
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
    return temp_file.name

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image.", use_container_width=True)
    temp_image_path = save_image_to_temp(image)
    identify_plant(temp_image_path)