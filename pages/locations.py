import streamlit as st
import pydeck as pdk

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

plant_ranges = {
     "Bush allamanda": [(-26.55, -46.63), (-34.61, -58.38), (-27.48, -58.83)],
     "Mexican-sunflower": [(7.36, -81.97), (14.94, -86.9), (18.31, -98.86), (25.8, -104.84)],
     "Broadleaf harebell": [(45.3, -80.2), (40.7, -92.9), (42.3, -108.7), (49.4, -118.5), (50.3, -71.3), (50.3, -85), (51, -100),
                            (60.4, -74.9), (54.5, -59.7), (65.4, -44.6), (47.4, 5.8), (50.2, 20.6)],
     "Lily-of-the-valley": [(45.74, 2.5), (53, 5.75), (59, 19), (47,19), (52, 33), (33,-84), (38.5, -80), (37.2, 139.8), (41, 123)],
     "Hydrangea": [(33,-84), (40.3, -78.6), (-24.3, -67.4), (-31.4, -69), (-40.5, -71.2), (35.6, 139.3), (40.5, 123.1),
                   (34.65, 118.2), (25.5, 116.8)]
}

plant = st.selectbox("Select a plant:", list(plant_ranges.keys()))

if plant:
    locations = plant_ranges[plant]
    plant = plant.lower()
    st.write(f"**Geographical Range of {plant}:**")

    view_state = pdk.ViewState(latitude=0, longitude=0, zoom=0.5)
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=[{"lat": lat, "lon": lon} for lat, lon in locations],
        get_position="[lon, lat]",
        get_radius=700000,
        get_color=[0, 173, 87, 100],
        pickable=True
    )

    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
