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



@st.dialog(" ",width='large')
def pdf(file):
  st.pdf(file, height="stretch", key=None)
  st.download_button(
    label="Download pdf",
    data=file,
    file_name="file.pdf",
    # mime="text/csv",
    icon=":material/download:"
  )


if st.button("Rapport"):
  pdf("page/TEST_SMP_APP.pdf")
