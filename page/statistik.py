import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import geopandas as gpd
import altair as alt
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

selected = option_menu(None,["Cijfers", 'Data'], icons=['bi bi-clipboard2-data', 'bi-database'],orientation="horizontal",)

if selected == "Cijfers":
    st.image('https://th.bing.com/th/id/R.9b05c7a5db7a093407c47efc77073a34?rik=IElQBmbi8QoEpA&riu=http%3a%2f%2fkinderscientific.com%2fwp-content%2fuploads%2f2018%2f06%2fWork-in-Progress.jpg&ehk=Udc6o7K7mopYeuVxHWM7qb%2f%2f6udgrt%2fp%2bYwVywZTQCc%3d&risl=&pid=ImgRaw&r=0',
            width=450)

    
elif selected == "Data":
    
    

    options = ["Waarnemingen", "Dagverlagen"]
    selection = st.segmented_control(
        "Directions", options, selection_mode="single",default="Waarnemingen", label_visibility="collapsed"
    )
    
    if selection=="Waarnemingen":
        rows_points = supabase.table("df_observations").select("*").execute()
        df_point = pd.DataFrame(rows_points.data)
        df_download_points = df_point[(df_point['project']==project) & (df_point['soortgroup']==opdracht)]
        with st.popover("Filters"):
            name = st.text_input("What's your name?")
        st.download_button(label="Downloaden alle dagverslagen",data=df_download_points.to_csv().encode("utf-8"),
                           file_name=f"waarnemingen_{opdracht}.csv",mime="text/csv", use_container_width=False)
        if len(df_download_points)==0:
            st.image('https://t4.ftcdn.net/jpg/04/72/65/73/360_F_472657366_6kV9ztFQ3OkIuBCkjjL8qPmqnuagktXU.jpg',
                        width=450)
        else:
            df_download_points

    elif selection=="Dagverlagen":
        try:
            rows_dagverslagen = supabase.table("df_dagverslagen").select("*").execute()
            df_dagverslagen = pd.DataFrame(rows_dagverslagen.data)                
            df_download_dagverslagen = df_dagverslagen[(df_dagverslagen['project']==project) & (df_dagverslagen['opdracht']==opdracht)]
            st.download_button(label="Downloaden alle dagverslagen",data=df_download_dagverslagen.to_csv().encode("utf-8"),
                               file_name="dagverslagen.csv",mime="text/csv", use_container_width=False)
            col1,col2 = st.columns([4,4],gap='medium',border=True)
            
            with st.container(border=True):
                option_areas_filter = col1.selectbox(
                    "Selecteer een gebied",
                    df_download_dagverslagen['gebied_id'].unique(),
                    index=None,
                    placeholder="Selecteer een gebied...",
                    label_visibility="collapsed"
                )
                try:
                    df_filter = df_download_dagverslagen[df_download_dagverslagen['gebied_id']==option_areas_filter].sort_values('datum').reset_index(drop=True)
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

                        c = (
                           alt.Chart(df_filter)
                           .mark_circle(size=30,)
                           .encode(x="datum", color="doel", tooltip=["datum", "doel"])
                        )
                        
                        st.altair_chart(c, use_container_width=True,theme=None,)

                        
        
                        with col2:
                            if len(event.selection['rows'])==0:
                                st.info('Selecteer een rij om de Dagverlageninformatie te krijgen')
                            else:
                                st.write(f"**:blue[Samensteller:]** {df_filter.loc[event.selection['rows'][0],'waarnemer']}")
                                st.write(f"**:blue[Begin tijd:]** {df_filter.loc[event.selection['rows'][0],'start_time']}")
                                st.write(f"**:blue[Eind tijd:]** {df_filter.loc[event.selection['rows'][0],'eind_time']}")
                                st.write(f"**:blue[Temperatuur:]** {df_filter.loc[event.selection['rows'][0],'temperatuur']}")
                                st.write(f"**:blue[Bewolking:]** {df_filter.loc[event.selection['rows'][0],'bewolking']}")
                                st.write(f"**:blue[Neerslag:]** {df_filter.loc[event.selection['rows'][0],'neerslag']}")
                                st.write(f"**:blue[Windkrcht:]** {df_filter.loc[event.selection['rows'][0],'windkrcht']}")
                                st.write(f"**:blue[Windrichting:]** {df_filter.loc[event.selection['rows'][0],'windrichting']}")
                                st.write(f"{df_filter.loc[event.selection['rows'][0],'opmerking']}")
        
                except:
                    pass
        except:
            st.image('https://t4.ftcdn.net/jpg/04/72/65/73/360_F_472657366_6kV9ztFQ3OkIuBCkjjL8qPmqnuagktXU.jpg',
                    width=450)

'---'
