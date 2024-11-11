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


conn = st.connection("gsheets", type=GSheetsConnection)
df_references = conn.read(ttl=0,worksheet="df_users")

#--FUNCTIONS---
def logIn():
    name = st.text_input("Vul uw gebruikersnaam in, alstublieft",value=None)  
    password = st.text_input("Vul uw wachtwoord in, alstublieft")
    try:
        if name == None:
            st.stop()
        
        index = df_references[df_references['username']==name].index[0]
        true_password = df_references.loc[index,"password"]

    except:
        st.warning("De gebruikersnaam is niet correct.")
        st.stop()
                             
    if st.button("logIn"):
        if password == true_password:
            st.session_state.login = {"name": name, "password": password}
            st.rerun()

        else:
            st.markdown(f"Sorry {name.split()[0]}, het wachtwoord is niet correct.")

def project():
    st.subheader(f"Welkom {st.session_state.login['name'].split()[0]}!!",divider='grey')
    index_project = df_references[df_references['username']==st.session_state.login["name"]].index[0]
    project_list = df_references.loc[index_project,"project"].split(',')
    project = st.selectbox("Aan welke project ga je werken?",project_list,label_visibility="visible")
    opdracht = st.selectbox("Aan welke opdracht ga je werken?",DICTIONARY_PROJECTS[project],label_visibility="visible")
    try:
        geometry_file = f"geometries/{project}.geojson" 
        gdf_areas = gpd.read_file(geometry_file)
        area = st.selectbox("Aan welke gebied ga je werken?",gdf_areas['Wijk'].unique(),label_visibility="visible")
        gdf_areas = gdf_areas[gdf_areas['Wijk']==area]
    except:
        area = None
        gdf_areas = None
    on = st.toggle("💻")
    if st.button(":rainbow[**Begin**]"):
         st.session_state.project = {"project_name": project,"opdracht": opdracht,'auto_start':on,'area':area, 'gdf':gdf_areas}
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
page_2 = st.Page("page/✍️_Voeg_een_waarneming_in.py", title="Voeg een waarneming in",icon="✍️" )
page_3 = st.Page("page/📝_Dagverlag_formulier.py", title="Dagverlag formulier",icon="📝" )
page_4 = st.Page("page/📊_ Statistik.py", title="Statistik",icon="📊" )

#---APP---
# IMAGE = "image/logo.png"
IMAGE_2 ="image/menu.jpg"
st.logo(IMAGE_2,  link=None, icon_image=IMAGE_2)

if "login" not in st.session_state:
    logIn()
    st.stop()


if 'project' not in st.session_state:  
    project()
    st.stop()

if st.session_state.login['type'] == 'user':
    pg = st.navigation([page_1,page_2,page_3])

elif st.session_state.login['type'] == 'visitor':
    pg = st.navigation([page_4])
  

pg.run()
