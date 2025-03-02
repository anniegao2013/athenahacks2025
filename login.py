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

# Get data
#items = get_data()

# {"_id":{"$oid":"573a1390f29313caabcd42e8"},"plot":"A group of bandits stage a brazen train hold-up, only to find a determined posse hot on their heels.","genres":["Short","Western"],"runtime":{"$numberInt":"11"},"cast":["A.C. Abadie","Gilbert M. 'Broncho Billy' Anderson","George Barnes","Justus D. Barnes"],"poster":"https://m.media-amazon.com/images/M/MV5BMTU3NjE5NzYtYTYyNS00MDVmLWIwYjgtMmYwYWIxZDYyNzU2XkEyXkFqcGdeQXVyNzQzNzQxNzI@._V1_SY1000_SX677_AL_.jpg","title":"The Great Train Robbery","fullplot":"Among the earliest existing films in American cinema - notable as the first film that presented a narrative story to tell - it depicts a group of cowboy outlaws who hold up a train and rob the passengers. They are then pursued by a Sheriff's posse. Several scenes have color included - all hand tinted.","languages":["English"],"released":{"$date":{"$numberLong":"-2085523200000"}},"directors":["Edwin S. Porter"],"rated":"TV-G","awards":{"wins":{"$numberInt":"1"},"nominations":{"$numberInt":"0"},"text":"1 win."},"lastupdated":"2015-08-13 00:27:59.177000000","year":{"$numberInt":"1903"},"imdb":{"rating":{"$numberDouble":"7.4"},"votes":{"$numberInt":"9847"},"id":{"$numberInt":"439"}},"countries":["USA"],"type":"movie","tomatoes":{"viewer":{"rating":{"$numberDouble":"3.7"},"numReviews":{"$numberInt":"2559"},"meter":{"$numberInt":"75"}},"fresh":{"$numberInt":"6"},"critic":{"rating":{"$numberDouble":"7.6"},"numReviews":{"$numberInt":"6"},"meter":{"$numberInt":"100"}},"rotten":{"$numberInt":"0"},"lastUpdated":{"$date":{"$numberLong":"1439061370000"}}},"num_mflix_comments":{"$numberInt":"0"}}

# Print results.
#for item in items:
#    st.write(f"User: {item.get('username', 'N/A')} | Password: {item.get('password', 'N/A')}")

# Style

st.set_page_config(initial_sidebar_state="collapsed")

st.markdown(
    """
    <style>
        [data-testid="stBaseButton-headerNoPadding"] {
            display: none
        }
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

st.markdown("<div class='main-header'>Welcome to PlantGo </div>", unsafe_allow_html=True)
st.markdown("<div class='login-container>", unsafe_allow_html=True)
username = st.text_input("Username")
password = st.text_input("Password", type="password")
login = st.button("Login")
register = st.markdown("<p class='register-link'>Don't have an account? <a href=/register>Sign up</a></p>", unsafe_allow_html=True)
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
    loginValid = any(item.get('username') == username and item.get('password') == password for item in items)

    if loginValid:
        st.success("Login successful! Welcome, " + username + "!")
        st.session_state['username'] = username
        switch_page("findplant")
    elif not userExists:
        st.error("User does not exist. Please make an account or try again.")
    else:
        st.error("Invalid username or password. Please try again.")

    # st.markdown("</div>", unsafe_allow_html=True)

# if register:
#     switch_page("register")