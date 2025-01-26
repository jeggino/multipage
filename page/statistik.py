import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import geopandas as gpd
import datetime
from datetime import datetime, timedelta, date

from credentials import *

from supabase import create_client, Client

from streamlit_option_menu import option_menu

import random


st.markdown("""
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK{ display: none; } #MainMenu{ visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True)



reduce_header_height_style = """
<style>
    div.block-container {padding-top: 1rem; padding-bottom: 0rem; padding-left: 1rem; padding-right: 1rem; margin-top: 1rem; margin-bottom: 0rem;}
</style>
""" 

st.markdown(reduce_header_height_style, unsafe_allow_html=True)

def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()

project = st.session_state.project['project_name']
opdracht = st.session_state.project['opdracht']


selected = option_menu(None,["Numbers", 'Data'], icons=['bi-pen-fill', 'bi-database'],orientation="horizontal",)

if selected == "Numbers":
    st.image('https://th.bing.com/th/id/R.9b05c7a5db7a093407c47efc77073a34?rik=IElQBmbi8QoEpA&riu=http%3a%2f%2fkinderscientific.com%2fwp-content%2fuploads%2f2018%2f06%2fWork-in-Progress.jpg&ehk=Udc6o7K7mopYeuVxHWM7qb%2f%2f6udgrt%2fp%2bYwVywZTQCc%3d&risl=&pid=ImgRaw&r=0')

    
elif selected == "Data":

    options = ["Waarnemingen", "Dagverlagen"]
    selection = st.segmented_control(
        "Directions", options, selection_mode="single"
    )

    if selection=="Waarnemingen":
        rows_points = supabase.table("df_observations").select("*").execute()
        df_point = pd.DataFrame(rows_points.data)
        df_download_points = df_point[df_point['project']==project]
        df_download_points
        st.write(len(df_download_points))
        st.download_button(label="Download waarnemingen",data=df_download_points.to_csv().encode("utf-8"),file_name="waarnemingen.csv",mime="text/csv", use_container_width=True) 
    elif selection=="Dagverlagen":
        try:
            rows_dagverslagen = supabase.table("df_dagverslagen").select("*").execute()
            df_dagverslagen = pd.DataFrame(rows_dagverslagen.data)                
            df_download_dagverslagen = df_dagverslagen[df_dagverslagen['project']==project]
            df_download_dagverslagen
            st.download_button(label="Download dagverslagen",data=df_download_dagverslagen.to_csv().encode("utf-8"),file_name="dagverslagen.csv",mime="text/csv", use_container_width=True)
        except:
            st.image('https://t4.ftcdn.net/jpg/04/72/65/73/360_F_472657366_6kV9ztFQ3OkIuBCkjjL8qPmqnuagktXU.jpg')
