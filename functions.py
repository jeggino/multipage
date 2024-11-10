import streamlit as st


import datetime
from datetime import datetime, timedelta, date
import random

import ast




def logIn(df_references):
    name = st.text_input("Vul uw gebruikersnaam in, alstublieft",value=None)  
    password = st.text_input("Vul uw wachtwoord in, alstublieft",type="password",)
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

# def project(df_references):
#     st.subheader(f"Welkom {st.session_state.login['name'].split()[0]}!!",divider='grey')
#     index_project = df_references[df_references['username']==st.session_state.login["name"]].index[0]
#     project_list = df_references.loc[index_project,"project"].split(',')
#     project = st.selectbox("Aan welke project ga je werken?",project_list,label_visibility="visible")
#     opdracht = st.selectbox("Aan welke opdracht ga je werken?",DICTIONARY_PROJECTS[project],label_visibility="visible")
#     try:
#         geometry_file = f"geometries/{project}.geojson" 
#         gdf_areas = gpd.read_file(geometry_file)
#         area = st.selectbox("Aan welke gebied ga je werken?",gdf_areas['Wijk'].unique(),label_visibility="visible")
#         gdf_areas = gdf_areas[gdf_areas['Wijk']==area]
#     except:
#         area = None
#         gdf_areas = None
#     on = st.toggle("💻")
#     if st.button(":rainbow[**Begin**]"):
#          st.session_state.project = {"project_name": project,"opdracht": opdracht,'auto_start':on,'area':area, 'gdf':gdf_areas}
#          st.rerun()
        
def logOut():
    if st.button("logOut",use_container_width=True):
        del st.session_state.login
        # del st.session_state.project     
        st.rerun()

# def logOut_project():
#     if st.button("Opdracht wijzigen",use_container_width=True):
#         del st.session_state.project
#         st.rerun()
