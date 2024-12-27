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

from credentials import *

st.set_page_config(
    initial_sidebar_state="collapsed",
    layout="wide",
    page_title="🦇🪶 SMP-App",
    
)


conn = st.connection("gsheets", type=GSheetsConnection)
df_references = conn.read(ttl=0,worksheet="df_users")

st.markdown(
    """
    <style>
    [data-testid="collapsedControl"] svg {
        height: 0rem;
        width: 0rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("""
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK{ display: none; } #MainMenu{ visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True)



reduce_header_height_style = """
<style>
    div.block-container {padding-top: 1rem; padding-bottom: 0rem; padding-left: 1rem; padding-right: 1rem; margin-top: 0rem; margin-bottom: 0rem;}
</style>
""" 

st.markdown(reduce_header_height_style, unsafe_allow_html=True)


#--FUNCTIONS---
def logIn():
    name = st.text_input("Vul uw gebruikersnaam in, alstublieft",value=None)  
    password = st.text_input("Vul uw wachtwoord in, alstublieft")
    try:
        if name == None:
            st.stop()
        
        index = df_references[df_references['username']==name].index[0]
        true_password = df_references.loc[index,"password"]
        type = df_references.loc[index,"type"]

    except:
        st.warning("De gebruikersnaam is niet correct.")
        st.stop()
                             
    if st.button("logIn"):
        if password == true_password:
            st.session_state.login = {"name": name, "password": password, 'type':type}
            st.rerun()

        else:
            st.markdown(f"Sorry {name.split()[0]}, het wachtwoord is niet correct.")

def project():
    st.subheader(f"Welkom {st.session_state.login['name'].split()[0]}!!",divider='grey')
    index_project = df_references[df_references['username']==st.session_state.login["name"]].index[0]
    project_list = df_references.loc[index_project,"project"].split(',')
    project = st.selectbox("Aan welke project ga je werken?",project_list,label_visibility="visible")
    opdracht = st.selectbox("Aan welke opdracht ga je werken?",DICTIONARY_PROJECTS[project],label_visibility="visible")
    # try:
    #     geometry_file = f"geometries/{project}.geojson" 
    #     gdf_areas = gpd.read_file(geometry_file)
    #     area = st.selectbox("Aan welke gebied ga je werken?",gdf_areas['Wijk'].unique(),label_visibility="visible")
    #     gdf_areas = gdf_areas[gdf_areas['Wijk']==area]
    # except:
    #     area = None
    #     gdf_areas = None
    if st.session_state.login['type'] == 'user':
        on = st.toggle("🚲")
    else:
        on = False
    if st.button(":rainbow[**Begin**]"):
         st.session_state.project = {"project_name": project,"opdracht": opdracht,'auto_start':on,
                                     # 'area':area, 'gdf':gdf_areas
                                    }
         st.rerun()
        
def logOut():
    if st.button("logOut",use_container_width=True):
        del st.session_state.login
        del st.session_state.project     
        st.rerun()

def logOut_project():
    if st.button("Opdracht wijzigen",use_container_width=True):
        del st.session_state.project
        st.rerun()


#---APP---
page_1 = st.Page("page/🧭_navigatie.py", title="Navigatie",icon="🧭" )
page_2 = st.Page("page/📌_Voeg_een_waarneming_in.py", title="Voeg een waarneming in",icon="📌" )
page_3 = st.Page("page/📝_Dagverlag_formulier.py", title="Dagverlag formulier",icon="📝" )
# page_4 = st.Page("page/📊_ Statistik.py", title="Statistik",icon="📊" )

#---APP---
IMAGE = "image/logo.png"
IMAGE_2 ="image/menu.jpg"
st.logo(IMAGE,  link=None, size="large",icon_image=IMAGE)

if "login" not in st.session_state:
    logIn()
    st.stop()


if 'project' not in st.session_state:  
    project()
    st.stop()

if st.session_state.login['type'] == 'user':
    if st.session_state.project['opdracht'] != 'Overig':
        pg = st.navigation([page_1,page_2,page_3])
    else:
        pg = st.navigation([page_1,page_2])
    
else:
    pg = st.navigation([page_1])
  

pg.run()
