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

left, middle, right = st.columns(3)

middle.space('middle')
middle.image('https://static.vecteezy.com/system/resources/previews/010/726/610/original/no-documents-filled-line-style-icon-empty-states-vector.jpg',width=300)

# def init_connection():
#     url = st.secrets["SUPABASE_URL"]
#     key = st.secrets["SUPABASE_KEY"]
#     return create_client(url, key)

# supabase = init_connection()
# rows_points = supabase.table("df_observations").select("*").execute()
# df_point = pd.DataFrame(rows_points.data)

# df_point = df_point[df_point['geometry_type']=='Point']

# import geopandas as gpd


# # Create geometry column
# geometry = gpd.points_from_xy(df_point["lng"], df_point["lat"])

# # Convert to GeoDataFrame
# gdf = gpd.GeoDataFrame(df_point, geometry=geometry, crs="EPSG:4326")
# m = gdf.explore('sp')

# map = folium.Map(zoom_start=10,zoom_control=False,font_size= '0.8rem')
# output = st_folium(map)


# from streamlit.components.v1 import html


# # Save map to HTML file
# html_file = "map.html"
# m.save(html_file)


# # Option 2: Provide download button
# with open(html_file, "rb") as f:
#     st.download_button(
#         label="Download map as HTML",
#         data=f,
#         file_name="map.html",
#         mime="text/html"
#     )




# # @st.dialog(" ",width='large')
# # def pdf(file):
# #   st.pdf(file, height="stretch", key=None)
  
# #   with open(file, "rb") as pdf_file:
# #     PDFbyte = pdf_file.read()

# #   st.download_button(
# #     label="Download pdf",
# #     data=PDFbyte,
# #     file_name="file.pdf",
# #     # mime='application/octet-stream',
# #     icon=":material/download:"
# #   )


# # if st.button("Rapport"):
# #   pdf("page/TEST_SMP_APP.pdf")
