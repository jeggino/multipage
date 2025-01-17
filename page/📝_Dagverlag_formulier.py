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


# --- FUNCTIONS ---
def insert_dagverslag(waarnemer,project,opdracht,gebied_id,doel,datum,start_time,eind_time,
                      temperatuur,bewolking,neerslag,windkrcht,windrichting,opmerking):
    
    data = {"waarnemer":waarnemer,"project":project,"opdracht":opdracht,"gebied_id":gebied_id,'doel':doel,"datum":datum,
             "start_time":start_time,"eind_time":eind_time,"temperatuur":temperatuur, "bewolking":bewolking,
             "neerslag":neerslag,"windkrcht":windkrcht,"windrichting":windrichting,"opmerking":opmerking}
                          
    response = (
            supabase.table("df_dagverslagen")
            .insert(data)
            .execute()
        )

#---DATASET---


# --- APP ---
IMAGE = "image/logo.png"
IMAGE_2 ="image/menu.jpg"
st.logo(IMAGE,  link=None, size="large", icon_image=IMAGE)

# try:
waarnemer = st.session_state.login['name']
project = st.session_state.project['project_name']
opdracht = st.session_state.project['opdracht']



st.title(f'{project}')
st.header(f'Opdracht: **{opdracht}**',divider=True)

selected = option_menu(None,["Formulier", 'Data'], icons=['bi-pen-fill', 'bi-database'],orientation="horizontal",)

if selected == "Formulier":
    with st.form("my_form", clear_on_submit=True,border=True):
        
        if opdracht == 'Vleermuizen':
            if project != "Overig":
                doel = st.selectbox('Doel',('Kraamverblijf','Winterverblijf','Paarverblijf'))
            else:
                doel = st.selectbox('Doel',('Overig','Kraamverblijf','Winterverblijf','Paarverblijf'))
                
        elif opdracht == 'Vogels':
            if project != "Overig":
                doel = st.selectbox('Doel',BIRD_NAMES)
            else:
                doel = st.selectbox('Doel',['Overig'] + BIRD_NAMES)
                
        try: 
            geometry_file = f"geometries/{st.session_state.project["project_name"]}.geojson" 
            gdf_areas = gpd.read_file(geometry_file)
            gebied_id_list = gdf_areas['Gebied'].unique()
            gebied_id = st.selectbox("Gebied",gebied_id_list,index=None)
        except:
            gebied_id = "---"
        # key = random.randint(1,100000000000)    
        datum = st.date_input("Datum","today")       
        two_hours_from_now = datetime.now() + timedelta(hours=1)
        four_hours_from_now = datetime.now() + timedelta(hours=3)
        start_time = st.time_input("Start tijd", two_hours_from_now)
        eind_time = st.time_input("Eind tijd", four_hours_from_now)               
        temperatuur = st.number_input("Temperatuur",key='temperatuur', min_value=0)
        bewolking = st.selectbox("Bewolking",("Onbewolkt (<10%)", "Halfbewolkt (10-80%)", "Bewolkt (>80%)"))
        neerslag = st.selectbox("Neerslag",("Droog", "Nevel/mist", "Motregen", "Regen"))
        windkrcht = st.number_input("Windkracht (Bft)",key='windkrcht', min_value=1)
        windrichting = st.selectbox("Windrichting",("Noord", "Noordoost", "Oost", "Zuidoost","Zuid","Zuidwest","West","Noordwest"))     
        opmerking = st.text_area("", placeholder="Vul hier een opmerking in ...")
        
        if st.form_submit_button("**Gegevens opslaan**",use_container_width=True):
            if gebied_id == None:
                st.error("Selecteer een gebied, alstublieft",icon="⚠️")
                st.stop()
            insert_dagverslag(waarnemer,project,opdracht,gebied_id,doel,str(datum),str(start_time),str(eind_time),temperatuur,bewolking,neerslag,windkrcht,windrichting,opmerking)
        
            # st.switch_page("page/🧭_navigatie.py")
        "---"

elif selected == 'Data':

    col1,col2 = st.columns([1,2])
    col1.image('https://th.bing.com/th/id/R.9b05c7a5db7a093407c47efc77073a34?rik=IElQBmbi8QoEpA&riu=http%3a%2f%2fkinderscientific.com%2fwp-content%2fuploads%2f2018%2f06%2fWork-in-Progress.jpg&ehk=Udc6o7K7mopYeuVxHWM7qb%2f%2f6udgrt%2fp%2bYwVywZTQCc%3d&risl=&pid=ImgRaw&r=0')
    with col2:
        st.write("In deze sectie kunt u de onderzoeks- en dagrapportgegevens downloaden in CSV-formaat.")
        rows_points = supabase.table("df_observations").select("*").execute()
        df_point = pd.DataFrame(rows_points.data)
        df_download_points = df_point[df_point['project']==project].to_csv().encode("utf-8")

        st.download_button(label="Download waarnemingen",data=df_download_points,file_name="waarnemingen.csv",mime="text/csv", use_container_width=True) 

        try:
            rows_dagverslagen = supabase.table("df_dagverslagen").select("*").execute()
            df_dagverslagen = pd.DataFrame(rows_dagverslagen.data)
            df_download_dagverslagen = df_dagverslagen[df_dagverslagen['project']==project].to_csv().encode("utf-8")
            
            st.download_button(label="Download dagverslagen",data=df_download_dagverslagen,file_name="dagverslagen.csv",mime="text/csv", use_container_width=True)
        except:
            pass

    
        
# # except:
# #     st.switch_page("page/🧭_navigatie.py")
