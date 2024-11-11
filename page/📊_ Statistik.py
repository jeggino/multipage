import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

import geopandas as gpd
from shapely.geometry import Polygon

import pydeck as pdk
import altair as alt

import datetime
from datetime import datetime, timedelta, date
import random

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


#---DATASET---
ttl = 0
conn = st.connection("gsheets", type=GSheetsConnection)
df_point = conn.read(ttl=ttl,worksheet="df_observations")
df_dagverslag = conn.read(ttl=ttl,worksheet="df_ekomaps_dagverslagen")


# --- APP ---
IMAGE = "image/logo.png"
IMAGE_2 ="image/menu.jpg"
st.logo(IMAGE_2,  link=None, icon_image=IMAGE_2)

try:
    project = st.session_state["project"]['project_name']
    opdracht = st.session_state["project"]['opdracht']
    gdf_areas = gpd.read_file(f"geometries/{project}.geojson")
    gdf_areas.geometry = gdf_areas.geometry.apply(lambda x: Polygon(x.coords)) 
    df_point = df_point[(df_point['project']==project)&(df_point['soortgroup']==opdracht)&(df_point['geometry_type']=="Point")].reset_index(drop=True)
    
    if opdracht == 'Vogels':
        functie = BIRD_FUNCTIE
        option_3 = st.selectbox("Selecteer een soort",BIRD_NAMES ,label_visibility="visible")
        df_point = df_point[df_point['sp']==option_3]
    elif opdracht == 'Vleermuizen':
        functie =BAT_FUNCTIE 

    radio = st.radio("", ['Kaarten 🗺️','Dagverslagen 🗒️'], horizontal=True, captions=None, label_visibility="collapsed")

    if radio == 'Kaarten 🗺️':
        option_1 = st.selectbox("Selecteer een functie",functie,
                                label_visibility="visible",help="Selecteer een specifieke functie om de gebieden met de hoogste concentratie te identificeren en hun verspreiding beter te begrijpen.")
        
        tab1, tab2 = st.tabs(["Gebiedenlaag", "Puntenlaag"])
        with tab1:
            col_1,col_2 = st.columns([1,2])
            df_point_option_1 = df_point[df_point['functie']==option_1]
            df_point_option_2 = df_point_option_1.groupby(['gebied'],as_index=False).size()
            df_merge_option_1 = gdf_areas.rename(columns={'Wijk':'gebied'}).merge(df_point_option_2, on='gebied',how='left').fillna(0)
            
            chart_1 = alt.Chart(df_merge_option_1).mark_bar().encode(x=alt.X('size:Q',axis=alt.Axis(grid=False,domain=True,ticks=False),title=None, 
                                                                             scale=alt.Scale(domain=[0,df_merge_option_1['size'].max()+2])),
                                                                     y=alt.Y('gebied:N',
                                                                           axis=alt.Axis(grid=False,domain=False,ticks=True,title=None),
                                                                           sort=alt.EncodingSortField(field="size",  order='descending'),
                                                                           title="")
                                                                    ).properties(
                height=275,
                title=alt.Title(
                    text="",
                    subtitle="",
                    anchor='start'
                )
            ).configure_view(stroke=None)
            
            col_1.altair_chart(chart_1, theme=None, use_container_width=True)
            
            INITIAL_VIEW_STATE = pdk.ViewState(latitude=gdf_areas.dissolve().centroid.y[0], longitude=gdf_areas.dissolve().centroid.x[0], zoom=11, max_zoom=24, pitch=45, bearing=0)
            
            geojson = pdk.Layer(
                "GeoJsonLayer",
                df_merge_option_1,
                opacity=0.8,
                stroked=False,
                filled=True,
                pickable=True,
                extruded=True,
                wireframe=True,
                get_elevation="size * 200",
                get_fill_color="[255, 255, size * 100]",
                get_line_color=[255, 255, 255],
            )
            
            tooltip = {
                "html": "<b>{gebied}</b> <br /><b>Aantal: {size}</b>",
                "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
            }
            
    
            r = pdk.Deck(layers=[geojson], initial_view_state=INITIAL_VIEW_STATE,tooltip=tooltip,
                   map_provider='mapbox', 
                   map_style="mapbox://styles/jeggino/cm2vtvb2l000w01qz9wet0mv9",)
    
            
            
            col_2.pydeck_chart(pydeck_obj=r,use_container_width=True, width=None, height=275, selection_mode="single-object", on_select="ignore", key=None)
        
        with tab2:
            col_3,col_4 = st.columns([1,1])
            
            # col_3.metric(label="Totaal", value=len(df_point_option_1))
            ICON_URL = r"https://th.bing.com/th/id/R.777337676efe7eba1ff59d4cc3cb0925?rik=fYzsmMt8OcULbw&riu=http%3a%2f%2ficons.veryicon.com%2fpng%2fSystem%2fSmall+%26+Flat%2fmap+marker.png&ehk=k0sMbnPz2zaMTgfpmhRFaLz8ozkaIMH1xRTGm3e5XY0%3d&risl=&pid=ImgRaw&r=0"
            
            icon_data = {
                # Icon from Wikimedia, used the Creative Commons Attribution-Share Alike 3.0
                # Unported, 2.5 Generic, 2.0 Generic and 1.0 Generic licenses
                "url": ICON_URL,
                "width": 242,
                "height": 242,
                "anchorY": 242,
            }
            
            data = df_point_option_1
            data["icon_data"] = None
            for i in data.index:
                data["icon_data"][i] = icon_data
    
            icon_layer = pdk.Layer(
                type="IconLayer",
                data=data,
                get_icon="icon_data",
                get_size=4,
                size_scale=15,
                get_position=["lng", "lat"],
                pickable=True,
            )
    
            tooltip = {
                "html": """<b>Datum: {datum}</b> <br />
                <b>Soort: {sp}</b>  <br />
                <b>Aantal: {aantal}</b>  <br />
                <b>Gedrag: {gedrag}</b>  <br />
                <b>Functie: {functie}</b>  <br />
                <b>Verblijf: {verblijf}</b>  <br />
                <b>Aantal: {aantal}</b>  <br />
                <b>Opmerking: {opmerking}</b>  <br />""",
                "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
            }
            r_3 = pdk.Deck(layers=[icon_layer], initial_view_state=INITIAL_VIEW_STATE, tooltip=tooltip,
                           map_provider='mapbox', 
                           map_style='road'
                          )
            
            col_3.pydeck_chart(pydeck_obj=r_3,use_container_width=True, width=None, height=275, 
                               selection_mode="single-object", on_select="ignore", key=None)
                    

            layer = pdk.Layer(
                "HeatmapLayer",
                data=df_point_option_1,
                opacity=0.9,
                get_position=["lng", "lat"],
                threshold=0.85,
                pickable=True,
            )
        
            r_2 = pdk.Deck(layers=[layer], initial_view_state=INITIAL_VIEW_STATE,
                           map_provider='mapbox', 
                           map_style="mapbox://styles/jeggino/cm2vtvb2l000w01qz9wet0mv9",)
            
            col_4.pydeck_chart(pydeck_obj=r_2,use_container_width=True, width=None, height=275, 
                               selection_mode="single-object", on_select="ignore", key=None)
      
    if radio == 'Dagverslagen 🗒️':
    
    # option_2 = st.selectbox("Selecteer een gebied",gdf_areas['Wijk'].unique(),
    #                         label_visibility="visible",help="Selecteer een gebied om het bemonsteringsproces te beoordelen. Door op de punten te klikken, kunt u gedetailleerde informatie over de individuele enquête ophalen.")
        df_dagverslag_option_2 = df_dagverslag[df_dagverslag['opdracht']==opdracht]
        df_dagverslag_option_2['datum'] = pd.to_datetime(df_dagverslag_option_2['datum'])
        df_dagverslag_option_2['year'] = df_dagverslag_option_2['datum'].dt.year
        
        year_min = df_dagverslag_option_2['year'].min()
        year_max = df_dagverslag_option_2['year'].max() + 1
        
        chart_2 = alt.Chart(df_dagverslag_option_2).mark_circle(size=70).encode(
            alt.X('datum:T',axis=alt.Axis(grid=False,domain=True,ticks=False,),title=None, 
                  scale=alt.Scale(domain=[str(year_min),str(year_max)])),
            alt.Y('gebied_id:N',
                  axis=alt.Axis(grid=False,domain=False,ticks=True,title=None),
                  title=""),
            # stroke=alt.Color('doel',scale=alt.Scale( range=['red', 'yellow', 'blue'])),
            fill=alt.Color('doel',legend=alt.Legend(orient="bottom",
                                                    titleAnchor='middle',
                                                    symbolSize=100,
                                                    direction='horizontal',
                                                    title='Doel',
                                                    ),
                           scale=alt.Scale(domain=['Kraamverblijf', 'Winterverblijf', 'Paarverblijf'], range=['red', 'blue', 'yellow'])
                          ),
            tooltip=[alt.Tooltip("waarnemer:N",title = "Waarnemer"),
                     alt.Tooltip("extra_velfwerker:N",title ="Extra veldwerkers"),
                     alt.Tooltip("doel:N",title ="Doel"),
                     alt.Tooltip("datum:T",title ="Datum"),
                     alt.Tooltip("start_time:N",title ="Begin tijd"),
                     alt.Tooltip("eind_time:N",title ="Eind tijd"),
                     alt.Tooltip("temperatuur:N",title ="Temperatuur"),
                     alt.Tooltip("bewolking:N",title ="Bewolking"),
                     alt.Tooltip("neerslag:N",title ="Neerslag"),
                     alt.Tooltip("windkrcht:N",title ="Windkrcht"),
                     alt.Tooltip("windrichting:N",title ="Windrichting"),
                     alt.Tooltip("opmerking:N",title ="Opmerking"),
                    ],
        ).properties(
            height=400,
            title=alt.Title(
                text="",
                subtitle="",
                anchor='start'
            )
        ).configure_view(stroke=None)
        
        st.altair_chart(chart_2, theme=None, use_container_width=True)

    

except:
    st.switch_page("page/🧭_navigatie.py")
