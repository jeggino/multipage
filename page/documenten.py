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


# Create geometry column
geometry = gpd.points_from_xy(df_point["lng"], df_point["lat"])

# Convert to GeoDataFrame
gdf = gpd.GeoDataFrame(df_point, geometry=geometry, crs="EPSG:4326").explore('sp')
gdf
st.download_button(
    label="Download HTML",
    data=gdf,
    file_name="SMP_terschelling_html_test.html",
    mime="html",
    icon=":material/download:",
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
