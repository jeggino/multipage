import streamlit as st
import pandas as pd
import geopandas as gpd
import datetime
from datetime import datetime, timedelta, date

import altair as alt

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
                      temperatuur,bewolking,neerslag,windkracht,windrichting,opmerking):
    
    data = {"waarnemer":waarnemer,"project":project,"opdracht":opdracht,"gebied_id":gebied_id,'doel':doel,"datum":datum,
             "start_time":start_time,"eind_time":eind_time,"temperatuur":temperatuur, "bewolking":bewolking,
             "neerslag":neerslag,"windkracht":windkracht,"windrichting":windrichting,"opmerking":opmerking}
                          
    response = (
            supabase.table("df_dagverslagen")
            .insert(data)
            .execute()
        )

# @st.dialog(" ")
# def update_dagverslag(id,df):
    
#   df_filter = df[df["key"]==id].reset_index(drop=True)


#   id_date = df_filter['datum'][0]
#   # id_time = df_filter['time'][0]
#   id_lat = df_filter['lat'][0]
#   id_lng = df_filter['lng'][0]
#   id_waarnemer = df_filter['waarnemer'][0]
#   id_key = df_filter['key'][0]
#   id_soortgroup = df_filter['soortgroup'][0]
#   id_geometry_type = df_filter['geometry_type'][0]
#   id_coordinates = df_filter['coordinates'][0]
#   id_project = df_filter['project'][0]
#   id_functie = df_filter['functie'][0]
#   id_gedrag = df_filter['gedrag'][0]
#   id_verblijf = df_filter['verblijf'][0]
#   id_sp = df_filter['sp'][0]
#   id_aantal = df_filter['aantal'][0]
#   id_opmerking = df_filter['opmerking'][0]
  
#   datum = st.date_input("Datum",id_date)
#   # nine_hours_from_now = datetime.now() + timedelta(hours=2)
#   time = st.time_input("Tijd" )
  
#   if st.session_state.project['opdracht'] == 'Vleermuizen':

#     sp = st.selectbox("Soort", BAT_NAMES,index=BAT_NAMES.index(id_sp))
 
#     if output["last_active_drawing"]["geometry"]["type"] == 'Polygon':
#         gedrag = None
#         functie = st.selectbox("Functie", GEBIED_OPTIONS,index=GEBIED_OPTIONS.index(id_functie))
#         verblijf = None
#     else:
#         gedrag = st.selectbox("Gedrag", BAT_BEHAVIOURS,index=BAT_BEHAVIOURS.index(id_gedrag)) 
#         functie = st.selectbox("Functie", BAT_FUNCTIE,index=BAT_FUNCTIE.index(id_functie))
#         verblijf = st.selectbox("Verblijf", BAT_VERBLIJF,index=BAT_VERBLIJF.index(id_verblijf)) 

#   elif st.session_state.project['opdracht'] == 'Vogels':
  
#     sp = st.selectbox("Soort", BIRD_NAMES,index=BIRD_NAMES.index(id_sp))
#     gedrag = st.selectbox("Gedrag", BIRD_BEHAVIOURS,index=BIRD_BEHAVIOURS.index(id_gedrag)) 
#     functie = st.selectbox("Functie", BIRD_FUNCTIE,index=BIRD_FUNCTIE.index(id_functie)) 
#     verblijf = st.selectbox("Verblijf", BIRD_VERBLIJF,index=BIRD_VERBLIJF.index(id_verblijf)) 

    
#   aantal = st.number_input("Aantal", min_value=1,value=int(id_aantal))    
#   opmerking = st.text_area("", placeholder="Vul hier een opmerking in ...",value=id_opmerking)

#   if st.button("**Update**",use_container_width=True):
      
#     data = {"key":id_key,"waarnemer":id_waarnemer,"datum":str(datum),"time":str(time),"soortgroup":id_soortgroup, "aantal":aantal,
#                    "sp":sp, "gedrag":gedrag, "functie":functie, "verblijf":verblijf,
#                    "geometry_type":id_geometry_type,"lat":id_lat,"lng":id_lng,"opmerking":opmerking,"coordinates":id_coordinates,"project":id_project}
      
#     response = (
#         supabase.table("df_observations")
#         .update(data)
#         .eq("key", id)
#         .execute()
#     )

#     st.rerun()
#---DATASET---


# --- APP ---
IMAGE = "image/logo.png"
IMAGE_2 ="image/menu.jpg"
st.logo(IMAGE,  link=None, size="large", icon_image=IMAGE)

# try:
waarnemer = st.session_state.login['name']
project = st.session_state.project['project_name']
opdracht = st.session_state.project['opdracht']



# st.title(f'{project}')
# st.header(f'Opdracht: **{opdracht}**',divider=True)

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
                doel = st.selectbox('Doel',['Gierzwaluw','Huismus'])
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
        windkracht = st.number_input("Windkracht (Bft)",key='windkracht', min_value=1)
        windrichting = st.selectbox("Windrichting",("Noord", "Noordoost", "Oost", "Zuidoost","Zuid","Zuidwest","West","Noordwest"))     
        opmerking = st.text_area("", placeholder="Vul hier een opmerking in ...")
        
        if st.form_submit_button("**Gegevens opslaan**",use_container_width=True):
            if gebied_id == None:
                st.error("Selecteer een gebied, alstublieft",icon="⚠️")
                st.stop()
            insert_dagverslag(waarnemer,project,opdracht,gebied_id,doel,str(datum),str(start_time),str(eind_time),temperatuur,bewolking,neerslag,windkracht,windrichting,opmerking)
        
            # st.switch_page("page/🧭_navigatie.py")
        "---"

elif selected == 'Data':
    try:
        rows_dagverslagen = supabase.table("df_dagverslagen").select("*").execute()
        df_dagverslagen = pd.DataFrame(rows_dagverslagen.data)                
        df_download_dagverslagen = df_dagverslagen[(df_dagverslagen['project']==project) & (df_dagverslagen['opdracht']==opdracht)]
        st.download_button(label="Downloaden alle dagverslagen",data=df_download_dagverslagen.to_csv().encode("utf-8"),file_name="dagverslagen.csv",mime="text/csv", use_container_width=False)


        
        with st.container(border=True):
            option_areas_filter = st.selectbox(
                "Selecteer een gebied",
                df_download_dagverslagen['gebied_id'].unique(),
                index=None,
                placeholder="Selecteer een gebied...",
                label_visibility="collapsed",
                
            )
            try:
                df_filter = df_download_dagverslagen[df_download_dagverslagen['gebied_id']==option_areas_filter].sort_values('datum').reset_index(drop=True)
                
                c = (
                alt.Chart(df_filter).mark_circle(size=105).encode(x=alt.X('datum:T',axis=alt.Axis(grid=False,domain=True,ticks=False,),title=None,
                                                                          scale=alt.Scale(domain=['2025','2026'])),
                                                                  color=alt.Color('doel').title(None), 
                                                                  tooltip=[alt.Tooltip("datum:T",title = "Datum"), alt.Tooltip("doel:N",title ="Doel")]
                                                                 ).properties(
                # width=450,
                height=80,
                title=alt.Title(
                text="",
                subtitle="",
                anchor='start'
                )
                ).configure_view(stroke=None)
                )
                
                 
                with st.container(border=True):
                    st.altair_chart(c, use_container_width=True,theme=None,)

                col1,col2 = st.columns([2,4],gap='medium',border=True)

                with col1:
                    if len(df_filter)==0:
                        st.stop()
                    else:
                        
                        event = st.dataframe(
                            df_filter,
                            column_config={
                                "datum": "Datum",
                                "doel": "Doel",
                            },
                            hide_index=True,
                            column_order=('datum','doel'),
                            on_select="rerun",
                            selection_mode=["single-row"],
                            use_container_width=False
                        )
     
    
                with col2:
                    if len(event.selection['rows'])==0:
                        st.info('Selecteer een rij om de Dagverlageninformatie te krijgen')
                    else:
                        key = df_filter.loc[event.selection['rows'][0],'key']
                        st.write(f"**:blue[Samensteller:]** {df_filter.loc[event.selection['rows'][0],'waarnemer']}")
                        st.write(f"**:blue[Begin tijd:]** {df_filter.loc[event.selection['rows'][0],'start_time']}")
                        st.write(f"**:blue[Eind tijd:]** {df_filter.loc[event.selection['rows'][0],'eind_time']}")
                        st.write(f"**:blue[Temperatuur:]** {df_filter.loc[event.selection['rows'][0],'temperatuur']}")
                        st.write(f"**:blue[Bewolking:]** {df_filter.loc[event.selection['rows'][0],'bewolking']}")
                        st.write(f"**:blue[Neerslag:]** {df_filter.loc[event.selection['rows'][0],'neerslag']}")
                        st.write(f"**:blue[Windkracht:]** {df_filter.loc[event.selection['rows'][0],'windkracht']}")
                        st.write(f"**:blue[Windrichting:]** {df_filter.loc[event.selection['rows'][0],'windrichting']}")
                        st.write(f"{df_filter.loc[event.selection['rows'][0],'opmerking']}")

            except:
                pass

        
    except:
        st.image('https://t4.ftcdn.net/jpg/04/72/65/73/360_F_472657366_6kV9ztFQ3OkIuBCkjjL8qPmqnuagktXU.jpg',
                width=450)

'---'

#     col1,col2 = st.columns([1,2])
#     col1.image('https://th.bing.com/th/id/R.9b05c7a5db7a093407c47efc77073a34?rik=IElQBmbi8QoEpA&riu=http%3a%2f%2fkinderscientific.com%2fwp-content%2fuploads%2f2018%2f06%2fWork-in-Progress.jpg&ehk=Udc6o7K7mopYeuVxHWM7qb%2f%2f6udgrt%2fp%2bYwVywZTQCc%3d&risl=&pid=ImgRaw&r=0')
#     with col2:
#         st.write("In deze sectie kunt u de onderzoeks- en dagrapportgegevens downloaden in CSV-formaat.")
#         rows_points = supabase.table("df_observations").select("*").execute()
#         df_point = pd.DataFrame(rows_points.data)
#         df_download_points = df_point[df_point['project']==project].to_csv().encode("utf-8")

#         st.download_button(label="Download waarnemingen",data=df_download_points,file_name="waarnemingen.csv",mime="text/csv", use_container_width=True) 

#         try:
#             rows_dagverslagen = supabase.table("df_dagverslagen").select("*").execute()
#             df_dagverslagen = pd.DataFrame(rows_dagverslagen.data)
#             df_download_dagverslagen = df_dagverslagen[df_dagverslagen['project']==project].to_csv().encode("utf-8")
            
#             st.download_button(label="Download dagverslagen",data=df_download_dagverslagen,file_name="dagverslagen.csv",mime="text/csv", use_container_width=True)
#         except:
#             pass

    
        
# # except:
# #     st.switch_page("page/🧭_navigatie.py")
