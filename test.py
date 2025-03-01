import streamlit as st
import pandas as pd
import numpy as np

#this is how to make a table - might be helpful for information / data? not sure where you would want to print a table
df = pd.DataFrame({
    'first column': [1,2,3,4],
    'second column': [10,20,30,40]
})

st.write(df)
st.table(df)

dataframe = np.random.randn(10,20)
st.dataframe(dataframe)

#map - this could be something to use - worldwide map of plants
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [34.02, -118.28],
    columns=['lat', 'lon'])

st.map(map_data, size=20, color="#0044ff")

#slider - won't need this
x = st.slider("x")
st.write(x, "squared is", x*x)

login = st.button("Login")
if login:
    st.write("thanks for logging in")
else:
    st.write("")