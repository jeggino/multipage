import streamlit as st

import folium
from folium.plugins import Draw, Fullscreen, LocateControl
from streamlit_folium import st_folium

import pandas as pd
from streamlit_gsheets import GSheetsConnection

import geopandas as gpd
import datetime
from datetime import datetime, timedelta, date

from credentials import *



# # ---LAYOUT---
# st.set_page_config(
#     page_title="🦇🪶 SMPs",
#     initial_sidebar_state="collapsed",
#     page_icon="🦇🪶",
#     layout="wide",
    
# )


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

# --- DIMENSIONS ---
OUTPUT_width = '95%'
OUTPUT_height = 550


    
# --- FUNCTIONS ---
def insert_json(key,waarnemer,datum,time,soortgroup,aantal,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,coordinates,project,gebied,df_old):
    
    data = [{"key":key, "waarnemer":waarnemer,"datum":datum,"time":time,"soortgroup":soortgroup, "aantal":aantal,
                   "sp":sp, "gedrag":gedrag, "functie":functie, "verblijf":verblijf,
                   "geometry_type":geometry_type,"lat":lat,"lng":lng,"opmerking":opmerking,"coordinates":coordinates,"project":project,'gebied':gebied}]
    df_new = pd.DataFrame(data)
    df_updated = pd.concat([df_old,df_new],ignore_index=True)
    
    return conn.update(worksheet="df_observations",data=df_updated)
  
def map():
    
    m = folium.Map()
    folium.TileLayer(tiles='https://api.mapbox.com/styles/v1/jeggino/cm2vtvb2l000w01qz9wet0mv9/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiamVnZ2lubyIsImEiOiJjbHdscmRkZHAxMTl1MmlyeTJpb3Z2eHdzIn0.N9TRN7xxTikk235dVs1YeQ',
                 attr='XXX Mapbox Attribution',overlay=False,show=False,name="Satellietkaart").add_to(m)
    
    if st.session_state.project['opdracht'] == 'Vleermuizen':
        Draw(draw_options={'circle': False,'rectangle': False,'circlemarker': False, 'polyline': False, 'polygon': True},
            position="topright",).add_to(m)

    else:
        Draw(draw_options={'circle': False,'rectangle': False,'circlemarker': False, 'polyline': False, 'polygon': False},
            position="topright",).add_to(m)
        
    Fullscreen(position="topright").add_to(m)
    folium.LayerControl().add_to(m)

    # if auto_start==True:
    #     auto_start_2 = False
    # else:
    #     auto_start_2 = True
        
    LocateControl(auto_start=True,position="topright").add_to(m)
    
    try:
        folium.GeoJson(
            st.session_state.project['gdf'],
            name=f"Gebied: {st.session_state.project['area']}",
            style_function=lambda feature: {
                "color": "black",
                "weight": 1,
            },
        ).add_to(m)
        
    except:
        pass

    
    output = st_folium(m, returned_objects=["all_drawings"],width=OUTPUT_width, height=OUTPUT_height)
    output["features"] = output.pop("all_drawings")
    
    return  output

        
@st.dialog(" ")
def input_data(output,df_old,auto_start):

    waarnemer = st.session_state.login['name']
    project = st.session_state.project['project_name']
    soortgroup = st.session_state.project['opdracht']

    try:
        gebied = st.session_state.project['area']
    except:
        gebied = None
    
    datum = st.date_input("Datum","today")       
    nine_hours_from_now = datetime.now() + timedelta(hours=1)
    time = st.time_input("Tijd", nine_hours_from_now)

    geometry_type = output["features"][0]["geometry"]["type"]
    
    st.divider()
    
    if soortgroup == 'Vleermuizen':
    
        sp = st.selectbox("Soort", BAT_NAMES)
        
        if geometry_type == 'Polygon':
            gedrag = None
            functie = st.selectbox("Functie", GEBIED_OPTIONS)
            verblijf = None

        else:
            gedrag = st.selectbox("Gedrag", BAT_BEHAVIOURS)
            functie = st.selectbox("Functie", BAT_FUNCTIE) 
            verblijf = st.selectbox("Verblijf", BAT_VERBLIJF) 
                
    elif soortgroup == 'Vogels':
    
        sp = st.selectbox("Soort", BIRD_NAMES)
        gedrag = st.selectbox("Gedrag", BIRD_BEHAVIOURS) 
        functie = st.selectbox("Functie", BIRD_FUNCTIE) 
        verblijf = st.selectbox("Verblijf", BIRD_VERBLIJF) 

    elif soortgroup == 'Vogels-Overig':
    
        sp = st.selectbox("Soort", BIRD_NAMES_ANDER)
        gedrag = st.selectbox("Gedrag", BIRD_BEHAVIOURS) 
        functie = st.selectbox("Functie", BIRD_FUNCTIE) 
        verblijf = st.selectbox("Verblijf", BIRD_VERBLIJF) 
    
    elif soortgroup == 'Vleermuiskast':
        functie = st.selectbox("Voorwaarde", VLEERMUISKAST_OPTIONS)
        bat_names = ["onbekend"] + BAT_NAMES
        sp = st.selectbox("Soort", bat_names) 
        gedrag = None
        verblijf = None     

    aantal = st.number_input("Aantal", min_value=1)
    opmerking = st.text_input("", placeholder="Vul hier een opmerking in ...")
    
    st.divider()

    placeholder = st.empty()
    submitted = placeholder.button("**Gegevens opslaan**",use_container_width=True)
    if submitted:           
        coordinates = output["features"][0]["geometry"]["coordinates"] 
        
        if geometry_type in ["LineString",'Polygon']:

            lng = coordinates[0][0][0]
            lat = coordinates[0][0][1]
            key = str(lng)+str(lat)
        
        else: 
            
            lng = coordinates[0]
            lat = coordinates[1]
            coordinates = None
            
            key = str(lng)+str(lat)

        if len(output["features"]) > 1:
            st.error("U kunt niet meer dan één waarneming tegelijk uploaden!")
            st.stop()

        else:
            placeholder.success('Gegevens opgeslagen!', icon="✅",)
            insert_json(key,waarnemer,str(datum),str(time),soortgroup,aantal,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,coordinates,project,gebied,df_old)
        
        if auto_start == False:
            st.switch_page("page/🧭_navigatie.py")
        else:
            st.rerun()
                     


# --- APP ---  
try:
    IMAGE = "image/logo.png"
    IMAGE_2 ="image/menu.jpg"
    st.logo(IMAGE_2,  link=None, icon_image=IMAGE_2)
    
    waarnemer = st.session_state.login['name']
    
    
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_old = conn.read(ttl='10m',worksheet="df_observations")
    
    output_map = map()
    st.write('ciao')
    
    
    try:
        if len(output_map["features"]) >= 1:
            input_data(output_map,df_old)
            
        else:
            st.stop()      
            
    except:
        st.stop()
    
except:
    st.switch_page("page/🧭_navigatie.py")
