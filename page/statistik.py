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

rows_points = supabase.table("df_observations").select("*").execute()
df_point = pd.DataFrame(rows_points.data)
if project == 'Overig':
    df_download_points = df_point[(df_point['soortgroup']==opdracht)].drop('key',axis=1)
else:   
    df_download_points = df_point[(df_point['project']==project) & (df_point['soortgroup']==opdracht)].drop('key',axis=1)

option_species = st.selectbox("",options = list(set(['Alle sorten']) | set(df_download_points['sp'].unique())),label_visibility='collapsed')
if option_species == 'Alle sorten':
    df = df_download_points[df_download_points['geometry_type']=='Point'].groupby(['datum','functie'],as_index=False).size()

else:
    df = df_download_points[(df_download_points['geometry_type']=='Point')&(df_download_points['sp']==option_species)].groupby(['datum','functie'],as_index=False).size()
    
df = df.pivot(index='datum',columns='functie',values='size',).fillna(0).astype(int).reset_index()
df['datum'] = pd.to_datetime(df['datum'])
# applying the groupby function on df 
df = df.groupby(pd.Grouper(key='datum', axis=0,freq='W')).sum().reset_index()
df = df.melt(id_vars='datum')

chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('week(datum):T',axis=alt.Axis(grid=True,domain=True,ticks=True,),title=None,
           ),
    y=alt.Y('sum(value):Q',axis=alt.Axis(grid=False,domain=True,ticks=True,),title=None,
           ),
    color=alt.Color('functie').title('Functie'),
    row=alt.Row('functie',title=None,header=None),
    tooltip=[ alt.Tooltip("functie:N",title ="Functie"), alt.Tooltip("value:N",title ="Aantal")]
).properties(
            width=1050,
            height=110,

            title=alt.Title(
            text="",
            subtitle="",
            anchor='start'
            )
            ).configure_view(stroke=None)

col1, col2 = st.columns([0.2,0.8],gap="large", vertical_alignment="top", border=False)

col2.altair_chart(chart, use_container_width=False,theme=None)
col1.dataframe(df.groupby('functie')['value'].sum(),use_container_width=True)
    
st.download_button(label="Downloaden alle waarnemingen",data=df_download_points.to_csv().encode("utf-8"),
                   file_name=f"{project}_{opdracht}_Waarnemingen.csv",mime="text/csv", use_container_width=False)

