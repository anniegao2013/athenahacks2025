import streamlit as st
import pandas as pd
import numpy as np

map_data = pd.DataFrame(
    np.random.randn(1000, 2) + [39.83, -98.58],
    columns=['lat', 'lon'])

st.map(map_data, size=1, color="#0044ff", zoom=3)