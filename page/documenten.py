import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import geopandas as gpd
import random

import folium
from folium.plugins import Draw, Fullscreen, LocateControl, GroupedLayerControl
from streamlit_folium import st_folium
import datetime
from datetime import datetime, timedelta, date
import random

import ast

from supabase import create_client, Client

from credentials import *

from streamlit_cookies_controller import CookieController
import time



def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()
rows_points = supabase.table("df_observations").select("*").execute()
df_point = pd.DataFrame(rows_points.data)

df_point = df_point[df_point['geometry_type']=='Point']

import geopandas as gpd


# # Create geometry column
# geometry = gpd.points_from_xy(df_point["lng"], df_point["lat"])

# # Convert to GeoDataFrame
# gdf = gpd.GeoDataFrame(df_point, geometry=geometry, crs="EPSG:4326")
# gdf

# map = folium.Map(zoom_start=10,zoom_control=False,font_size= '0.8rem')
# output = st_folium(map)


# st.download_button(
#     label="Download HTML",
#     data=output,
#     file_name="SMP_terschelling_html_test.html",
#     mime="html",
#     icon=":material/download:",
# )

from streamlit.components.v1 import html

# Example: Load a sample GeoDataFrame
world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

# Ensure CRS is set (important for .explore)
if world.crs is None:
    world = world.set_crs(epsg=4326)

# Create interactive map using GeoPandas' explore()
m = world.explore(
    column="pop_est",  # Color by population
    cmap="viridis",
    tooltip=["name", "pop_est"],
    popup=True
)

# Save map to HTML file
html_file = "map.html"
m.save(html_file)

# Option 1: Display inside Streamlit
with open(html_file, "r", encoding="utf-8") as f:
    html(f.read(), height=600)

# Option 2: Provide download button
with open(html_file, "rb") as f:
    st.download_button(
        label="Download map as HTML",
        data=f,
        file_name="map.html",
        mime="text/html"
    )

# @st.dialog(" ",width='large')
# def pdf(file):
#   st.pdf(file, height="stretch", key=None)
  
#   with open(file, "rb") as pdf_file:
#     PDFbyte = pdf_file.read()

#   st.download_button(
#     label="Download pdf",
#     data=PDFbyte,
#     file_name="file.pdf",
#     # mime='application/octet-stream',
#     icon=":material/download:"
#   )


# if st.button("Rapport"):
#   pdf("page/TEST_SMP_APP.pdf")
