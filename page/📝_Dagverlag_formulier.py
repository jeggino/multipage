import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import geopandas as gpd
import datetime
from datetime import datetime, timedelta, date

from credentials import *

from streamlit_option_menu import option_menu




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

# --- FUNCTIONS ---
def insert_dagverslag(waarnemer,project,opdracht,gebied_id,doel,datum,start_time,eind_time,extra_velfwerker,
                      temperatuur,bewolking,neerslag,windkrcht,windrichting,opmerking,df_old):
    
    data = [{"waarnemer":waarnemer,"project":project,"opdracht":opdracht,"gebied_id":gebied_id,'doel':doel,"datum":datum,
             "start_time":start_time,"eind_time":eind_time, "extra_velfwerker":extra_velfwerker, "temperatuur":temperatuur, "bewolking":bewolking,
             "neerslag":neerslag,"windkrcht":windkrcht,"windrichting":windrichting,"opmerking":opmerking}]
    df_new = pd.DataFrame(data)
    df_updated = pd.concat([df_old,df_new],ignore_index=True)
    
    return conn.update(worksheet="df_dagverslagen",data=df_updated)

#---DATASET---
ttl = '10m'
ttl_references = '10m'
conn = st.connection("gsheets", type=GSheetsConnection)
df_old = conn.read(ttl=ttl,worksheet="df_dagverslagen")
df_projects = conn.read(ttl=ttl_references,worksheet="df_ekomaps_projects")

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

selected = option_menu(None,["Formulier", 'Databank'], icons=['house', 'Tasks'],orientation="horizontal",)

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
            
        datum = st.date_input("Datum","today")       
        two_hours_from_now = datetime.now() + timedelta(hours=1)
        four_hours_from_now = datetime.now() + timedelta(hours=3)
        start_time = st.time_input("Start tijd", two_hours_from_now)
        eind_time = st.time_input("Eind tijd", four_hours_from_now)
        
        extra_velfwerker_list = df_projects.set_index('project').loc[project,"user"].split(',')
        if project != "Overig":
            extra_velfwerker_list.remove(waarnemer)
            extra_velfwerker = st.multiselect("Extra veldwerker",extra_velfwerker_list)
    
        else:
            extra_velfwerker = "---"
        
        temperatuur = st.number_input("Temperatuur",key='temperatuur', min_value=0)
        bewolking = st.selectbox("Bewolking",("Onbewolkt (<10%)", "Halfbewolkt (10-80%)", "Bewolkt (>80%)"))
        neerslag = st.selectbox("Neerslag",("Droog", "Nevel/mist", "Motregen", "Regen","Zware regen","Sneeuw"))
        windkrcht = st.number_input("Windkracht",key='windkrcht', min_value=1)
        windrichting = st.selectbox("Windrichting",("Noord", "Noordoost", "Oost", "Zuidoost","Zuid","Zuidwest","West","Noordwest"))
            
        opmerking = st.text_area("", placeholder="Vul hier een opmerking in ...")
        
        if st.form_submit_button("**Gegevens opslaan**",use_container_width=True):
            if gebied_id == None:
                st.error("Selecteer een gebied, alstublieft",icon="⚠️")
                st.stop()
            insert_dagverslag(waarnemer,project,opdracht,gebied_id,doel,datum,start_time,eind_time,extra_velfwerker,temperatuur,bewolking,neerslag,windkrcht,windrichting,opmerking,df_old)
        
            # st.switch_page("page/🧭_navigatie.py")
        "---"

elif selected == 'Databank':
    geometry_file = f"geometries/{st.session_state.project["project_name"]}.geojson" 
    gdf_areas = gpd.read_file(geometry_file)
    gebied_id_list = gdf_areas['Gebied'].unique()
    gebied_id = st.sidebar.selectbox("Gebied",gebied_id_list,index=None)
    doel = st.sidebar.selectbox('Doel',('Kraamverblijf','Winterverblijf','Paarverblijf'),index=None)
    if doel:
        df_filter = df_old[(df_old['doel']==doel)&(df_old['gebied_id']==gebied_id)]
        date_options = df_filter['datum'].unique()
        date_input = st.sidebar.selectbox('Datum',date_options,index=None)
    try:
        df_filter_2 = df_filter[(df_filter['datum']==date_input)].reset_index(drop=True)
        st.write('Waarnemer: 'df_filter_2.loc[0,'waarnemer'])
        st.write('Start time: 'df_filter_2.loc[0,'start_time'])
        st.write('Eind time: ' df_filter_2.loc[0,'eind_time'])
        st.write('temperatuur: 'df_filter_2.loc[0,'temperatuur'])
        st.write('bewolking: 'df_filter_2.loc[0,'bewolking'])
        st.write('neerslag: 'df_filter_2.loc[0,'neerslag'])
        st.write('windkrcht: 'df_filter_2.loc[0,'windkrcht'])
        st.write('windrichting: 'df_filter_2.loc[0,'windrichting'])
        st.write('opmerking: 'df_filter_2.loc[0,'opmerking'])
    except:
        st.stop()

    
    
        
# except:
#     st.switch_page("page/🧭_navigatie.py")
