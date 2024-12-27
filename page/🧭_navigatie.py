import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import geopandas as gpd
import random

import folium
from folium.plugins import Draw, Fullscreen, LocateControl, GroupedLayerControl
from folium.features import DivIcon
from streamlit_folium import st_folium
from branca.element import Template, MacroElement, IFrame

import datetime
from datetime import datetime, timedelta, date
import random

import ast

from credentials import *


#---DATASET---
ttl = 0
ttl_references = 0
conn = st.connection("gsheets", type=GSheetsConnection)
df_point = conn.read(ttl=ttl,worksheet="df_observations")
df_references = conn.read(ttl=ttl_references,worksheet="df_users")


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


# --- DIMENSIONS ---
OUTPUT_width = '95%'
OUTPUT_height = 550
ICON_SIZE = (20,20)

ICON_SIZE_huismus = (28,28)
ICON_SIZE_BAT_EXTRA = (60,25)
ICON_SIZE_RUIGE = (70,35)
ICON_SIZE_BIRD = (70,50)
ICON_SIZE_Huiszwaluw = (80,45)

# --- FUNCTIONS ---


def legend(species_colors_dict,dragable=True):


    legend_temp=''
    
    
    for species in species_colors_dict.keys():
        legend_temp = legend_temp + f"<li><span style='background: {species_colors_dict[species]}; opacity: 0.75;'></span>{species}</li>"
        
    
    legend_body = f"""  
    <!doctype html>
    <html lang="en">
    <body>
    <div id='maplegend' class='maplegend' 
        style='position: absolute; z-index: 9999; background-color: rgba(255, 255, 255, 0.7);
         border-radius: 8px; padding: 10px; font-size: 11px; left: 10px; bottom: 35px; '>     
    <div class='legend-scale'>
      <ul class='legend-labels'>

        <li><strong>Sorten</strong></li>
    
        {legend_temp}

        <li><strong>Functie</strong></li>
        <li><span class="fa fa-circle" style="color:grey" opacity: 0.75;'></span>Geen / Ombekend</li>
        <li><span class="fa fa-star" style="color:grey" opacity: 0.75;'></span>Zommerverblijf</li>
        <li><span class="fa fa-burst" style="color:grey" opacity: 0.75;'></span>Kraamverblif</li>
        <li><span class="fa fa-snowflake" style="color:grey" opacity: 0.75;'></span>Winterverblijf</li>
        <li><span class="fa fa-heart" style="color:grey" opacity: 0.75;'></span>Paarverblijf</li>
        <li><strong>Functiegebied</strong></li>
        <li><span class="fa fa-object-ungroup" style="color:green" opacity: 0.75;'></span>Foerageergebied</li>
        <li><span class="fa fa-object-ungroup" style="color:red" opacity: 0.75;'></span>Baltsterritorium</li>
      </ul> 
    </body>
    </html>
    """
       
    legend_style = """<style type='text/css'>
      .maplegend .legend-scale ul {margin: 0; padding: 0; color: #0f0f0f;}
      .maplegend .legend-scale ul li {list-style: none; line-height: 18px; margin-bottom: 1.5px;}
      .maplegend ul.legend-labels li span {float: left; height: 16px; width: 16px; margin-right: 4.5px;}
    </style>
    
    {% endmacro %}
    """
    legend_dragable = """{% macro html(this, kwargs) %}
        <!doctype html>
        <html lang="en">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>jQuery UI Draggable - Default functionality</title>
          <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
        
          <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
          <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
          
          <script>
          $( function() {
            $( "#maplegend" ).draggable({
                            start: function (event, ui) {
                                $(this).css({
                                    right: "auto",
                                    top: "auto",
                                    bottom: "auto"
                                });
                            }
                        });
        });
        
          </script>
        </head>
        """
    
    legend_normal = "{% macro html(this, kwargs) %}"
    
    if dragable == True:
        legend = legend_dragable + legend_body + legend_style
    else:
        legend = legend_normal + legend_body + legend_style
    
    return legend
    
def popup_polygons(row):
    
    i = row

    project=df_2['project'].iloc[i]
    # gebied=df_2['gebied'].iloc[i]
    datum=df_2['datum'].iloc[i] 
    time=df_2['time'].iloc[i]
    sp = df_2['sp'].iloc[i] 
    functie=df_2['functie'].iloc[i]
    opmerking=df_2['opmerking'].iloc[i]
    aantal=df_2['aantal'].iloc[i]
    waarnemer=df_2['waarnemer'].iloc[i] 
       

    left_col_color = "#19a7bd"
    right_col_color = "#f2f0d3"
    
    html = """<!DOCTYPE html>
    <html>
    <table style="height: 126px; width: 300;">
    <tbody>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Project</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(project) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Waarnemer</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(waarnemer) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Datum</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(datum) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Tijd</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(time) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Soort</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(sp) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Functie</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(functie) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Aantal</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(int(aantal)) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Opmerking</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(opmerking) + """
    </tr>
    </tbody>
    </table>
    </html>
    """
    return html


def popup_html(row):
    
    i = row

    project=df_2['project'].iloc[i]
    # gebied=df_2['gebied'].iloc[i]
    datum=df_2['datum'].iloc[i] 
    time=df_2['time'].iloc[i]
    verblijf=df_2['verblijf'].iloc[i]
    sp = df_2['sp'].iloc[i] 
    functie=df_2['functie'].iloc[i]
    gedrag=df_2['gedrag'].iloc[i]
    verblijf=df_2['verblijf'].iloc[i]
    opmerking=df_2['opmerking'].iloc[i]
    aantal=df_2['aantal'].iloc[i]
    waarnemer=df_2['waarnemer'].iloc[i] 
       

    left_col_color = "#19a7bd"
    right_col_color = "#f2f0d3"
    
    html = """<!DOCTYPE html>
    <html>
    <table style="height: 126px; width: 300;">
    <tbody>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Project</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(project) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Waarnemer</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(waarnemer) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Datum</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(datum) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Tijd</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(time) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Soort</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(sp) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Functie</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(functie) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Gedrag</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(gedrag) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Verblijf</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(verblijf) + """
    </tr>
    
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Aantal</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(int(aantal)) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Opmerking</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(opmerking) + """
    </tr>
    </tbody>
    </table>
    </html>
    """
    return html


@st.dialog(" ")
def update_item(id):
  df = conn.read(ttl=0,worksheet="df_observations")
  df_filter = df[df["key"]==id].reset_index(drop=True)
  df_drop = df[~df.apply(tuple, axis=1).isin(df_filter.apply(tuple, axis=1))]

  df_drop
  
  datum = st.date_input("Datum","today")
  nine_hours_from_now = datetime.now() + timedelta(hours=2)
  time = st.time_input("Tijd", nine_hours_from_now)
  
  if st.session_state.project['opdracht'] == 'Vleermuizen':

    sp = st.selectbox("Soort", BAT_NAMES)
 
    if output["last_active_drawing"]["geometry"]["type"] == 'Polygon':
        gedrag = None
        functie = st.selectbox("Functie", GEBIED_OPTIONS)
        verblijf = None
    else:
        gedrag = st.selectbox("Gedrag", BAT_BEHAVIOURS) 
        functie = st.selectbox("Functie", BAT_FUNCTIE)
        verblijf = st.selectbox("Verblijf", BAT_VERBLIJF) 

  elif st.session_state.project['opdracht'] == 'Vogels':
  
    sp = st.selectbox("Soort", BIRD_NAMES)
    gedrag = st.selectbox("Gedrag", BIRD_BEHAVIOURS) 
    functie = st.selectbox("Functie", BIRD_FUNCTIE) 
    verblijf = st.selectbox("Verblijf", BIRD_VERBLIJF) 

  elif st.session_state.project['opdracht'] == 'Vogels-Overig':
  
    sp = st.selectbox("Soort", BIRD_NAMES_ANDER)
    gedrag = st.selectbox("Gedrag", BIRD_BEHAVIOURS) 
    functie = st.selectbox("Functie", BIRD_FUNCTIE) 
    verblijf = st.selectbox("Verblijf", BIRD_VERBLIJF) 
  
  elif st.session_state.project['opdracht'] == 'Vleermuiskast':
    
    functie = st.selectbox("Voorwaarde", VLEERMUISKAST_OPTIONS)
    bat_names = ["onbekend"] + BAT_NAMES
    sp = st.selectbox("Soort", bat_names) 
    gedrag = None
    verblijf = None
    
  aantal = st.number_input("Aantal", min_value=0)    
  opmerking = st.text_input("", placeholder="Vul hier een opmerking in ...")

  if st.button("**Update**",use_container_width=True):
    
    df = conn.read(ttl=0,worksheet="df_observations")
    df_filter = df[df["key"]==id].reset_index(drop=True)
      
    id_lat = df_filter['lat'][0]
    id_lng = df_filter['lng'][0]
    id_waarnemer = df_filter['waarnemer'][0]
    id_key = df_filter['key'][0]
    id_soortgroup = df_filter['soortgroup'][0]
    id_geometry_type = df_filter['geometry_type'][0]
    id_coordinates = df_filter['coordinates'][0]
    id_project = df_filter['project'][0]
      
    conn.update(worksheet='df_observations',data=df_drop)
    df_old = conn.read(ttl=0,worksheet="df_observations")
      
    data = [{"key":id_key,"waarnemer":id_waarnemer,"datum":str(datum),"time":time,"soortgroup":id_soortgroup, "aantal":aantal,
                   "sp":sp, "gedrag":gedrag, "functie":functie, "verblijf":verblijf,
                   "geometry_type":id_geometry_type,"lat":id_lat,"lng":id_lng,"opmerking":opmerking,"coordinates":id_coordinates,"project":id_project}]
      
    df_new = pd.DataFrame(data)
    df_updated = pd.concat([df,df_new],ignore_index=True)
    conn.update(worksheet='df_observations',data=df_updated)

    st.rerun()




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
    # try:
    #     geometry_file = f"geometries/{project}.geojson" 
    #     gdf_areas = gpd.read_file(geometry_file)
    #     area = st.selectbox("Aan welke gebied ga je werken?",gdf_areas['Wijk'].unique(),label_visibility="visible")
    #     gdf_areas = gdf_areas[gdf_areas['Wijk']==area]
    # except:
    #     area = None
    #     gdf_areas = None
    on = st.toggle("🚲")
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
IMAGE = "image/logo.png"
IMAGE_2 ="image/menu.jpg"
st.logo(IMAGE,  link=None, size="large", icon_image=IMAGE)

if "login" not in st.session_state:
    logIn()
    st.stop()


if 'project' not in st.session_state:  
    project()
    st.stop()

with st.sidebar:
    logOut_project()
    logOut()
    st.divider()


if st.session_state.project['project_name'] not in ['Admin','Overig']:
    df_2 = df_point[df_point['project']==st.session_state.project['project_name']]
    df_2 = df_2[df_2['soortgroup']==st.session_state.project['opdracht']]

elif st.session_state.project['project_name'] == 'Overig':
    df_2 = df_point[df_point['project']!='Admin']
    df_2 = df_2[df_2['soortgroup']==st.session_state.project['opdracht']]

else:
    df_2 = df_point[df_point['soortgroup']==st.session_state.project['opdracht']]


if len(df_2)>0:
    try:
        df_2["datum"] = pd.to_datetime(df_2["datum"]).dt.date
        st.sidebar.subheader("Filter op",divider=False)
        d = st.sidebar.slider("Datum", min_value=df_2.datum.min(),max_value=df_2.datum.max(),value=(df_2.datum.min(), df_2.datum.max()),format="DD-MM-YYYY")
        
        df_2 = df_2[(df_2['datum']>=d[0]) & (df_2['datum']<=d[1])]
    except:
        pass
    
    species_filter_option = df_2["sp"].unique()
    species_filter = st.sidebar.multiselect("Sorten",species_filter_option,species_filter_option)
    df_2 = df_2[df_2['sp'].isin(species_filter)]


    st.sidebar.divider()

try:
    df_2["icon_data"] = df_2.apply(lambda x: None if x["geometry_type"] in ["LineString","Polygon"] 
                                   else (icon_dictionary[x["soortgroup"]][x["sp"]][x["functie"]] if x["soortgroup"] in ['Vogels','Vleermuizen',"Vogels-Overig"] 
                                         else icon_dictionary[x["soortgroup"]][x["functie"]]), 
                                   axis=1)
    
    df_2 = df_2.reset_index(drop=True)

except:
    pass


try:
    geometry_file = f"geometries/{st.session_state.project["project_name"]}.geojson" 
    gdf_areas = gpd.read_file(geometry_file)
    geometry_names_file = f"geometries/{st.session_state.project["project_name"]}_names.geojson" 
    gdf_names = gpd.read_file(geometry_names_file)
    lat = gdf_areas.centroid.y.mean()
    lng = gdf_areas.centroid.x.mean()
    map = folium.Map(location=[lat, lng], zoom_start=10,zoom_control=False,tiles=None)
except:
    map = folium.Map(tiles=None, zoom_start=8,zoom_control=False)
    
LocateControl(auto_start=st.session_state.project['auto_start'],position="topleft").add_to(map)
Fullscreen(position="topleft").add_to(map)

functie_dictionary = {}

try:
    functie_len = df_2['functie'].unique()
    
    for functie in functie_len:
        functie_dictionary[functie] = folium.FeatureGroup(name=functie)    
    
    for feature_group in functie_dictionary.keys():
        map.add_child(functie_dictionary[feature_group])
except:
    pass

folium.TileLayer('OpenStreetMap',overlay=False,show=True,name="Stratenkaart").add_to(map)
folium.TileLayer(tiles="CartoDB Positron",overlay=False,show=False,name="Witte kaart").add_to(map)
folium.TileLayer(tiles='https://api.mapbox.com/styles/v1/jeggino/cm2vtvb2l000w01qz9wet0mv9/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiamVnZ2lubyIsImEiOiJjbHdscmRkZHAxMTl1MmlyeTJpb3Z2eHdzIn0.N9TRN7xxTikk235dVs1YeQ',
                 attr='XXX Mapbox Attribution',overlay=False,show=False,name="Satellietkaart").add_to(map)


try:
       
    folium.GeoJson(
        gdf_areas,
        name="Gebiedsgrens",
        style_function=lambda feature: {
            "color": "black",
            "weight": 3,
        },
    ).add_to(map)
    
    names = folium.FeatureGroup(name="Gebiedsnamen").add_to(map)
    for row,columns in gdf_names.iterrows():
    
        folium.Marker([columns['lat'],columns['lng']],
                          icon=DivIcon(
                        icon_size=(.0, .0),
                        icon_anchor=(5, 5),
                        html=f'<b style="font-size: 8pt; color : blue; background-color:white;border:2px solid Tomato;">{columns['Gebied']}</b>'
                        ,
                    )
                         ).add_to(names)
except:
    pass
    
df_2['functie_shape'] = df_2['functie'].map({'paarverblijfplaats':'heart',
                               'vleermuis waarneming':'circle',
                              'zomerverblijfplaats':'star',
                              'kraamverblijfplaats':'burst',
                              'winterverblijfplaats':'snowflake'})

colors  =['red', 'blue', 'green', 'purple', 'orange', 'darkred',
         'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue',
         'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen',
         'gray', 'black', 'lightgray']

species_colors_dict=dict(zip(df_2['sp'].unique(),colors[:len(df_2['sp'].unique())]))
df_2['color'] = df_2['sp'].map(species_colors_dict)
    
for i in range(len(df_2)):

    if df_2.iloc[i]['geometry_type'] == "Point":

        if df_2.iloc[i]['soortgroup'] == "Vogels":

            if (df_2.iloc[i]['sp']=="Huismus"):
                ICON_SIZE_2 = ICON_SIZE_huismus
    
            elif (df_2.iloc[i]['sp'] == 'Huiszwaluw'):
                ICON_SIZE_2 = ICON_SIZE_Huiszwaluw
    
            else:             
                ICON_SIZE_2 = ICON_SIZE
                
    
            html = popup_html(i)
            popup = folium.Popup(folium.Html(html, script=True), max_width=300)
            fouctie_loop = functie_dictionary[df_2.iloc[i]['functie']]
    
            folium.Marker([df_2.iloc[i]['lat'], df_2.iloc[i]['lng']],
                          popup=popup,
                          icon=folium.features.CustomIcon(df_2.iloc[i]["icon_data"], icon_size=ICON_SIZE_2)
                         ).add_to(fouctie_loop)

        elif df_2.iloc[i]['soortgroup'] == "Vleermuizen":
            

            html = popup_html(i)
            popup = folium.Popup(folium.Html(html, script=True), max_width=300)
            fouctie_loop = functie_dictionary[df_2.iloc[i]['functie']]
            
            folium.Marker([df_2.iloc[i]['lat'], df_2.iloc[i]['lng']],
              popup=popup,
              icon=folium.Icon(icon=df_2.iloc[i]['functie_shape'],
                              prefix='fa',
                              icon_color='black',
                              color=df_2.iloc[i]['color'],)
              ).add_to(fouctie_loop)

    elif df_2.iloc[i]['geometry_type'] == "Polygon":
        html = popup_polygons(i)
        popup = folium.Popup(folium.Html(html, script=True), max_width=300)
        fouctie_loop = functie_dictionary[df_2.iloc[i]['functie']]
        location = df_2.iloc[i]['coordinates']
        location = ast.literal_eval(location)
        location = [i[::-1] for i in location[0]]
                    
        if df_2.iloc[i]['functie']=="Baltsterritorium":
            fill_color="red"

        else:
            fill_color="green"
            
        folium.Polygon(location,fill_color=fill_color,weight=0,fill_opacity=0.5,
                      popup=popup
                      ).add_to(fouctie_loop)

folium.LayerControl().add_to(map)

if st.session_state.project['opdracht'] == 'Vleermuizen':
    legend_template = legend(species_colors_dict,False)
    macro = MacroElement()
    macro._template = Template(legend_template)
    map.get_root().add_child(macro)

output = st_folium(map,returned_objects=["last_active_drawing"],width=OUTPUT_width, height=OUTPUT_height,
                     feature_group_to_add=list(functie_dictionary.values()))

if st.session_state.login['type'] == 'user':
    try:
        try:
            id = str(output["last_active_drawing"]['geometry']['coordinates'][0])+str(output["last_active_drawing"]['geometry']['coordinates'][1])
            name = f"{id}"
        except:
            id = str(output["last_active_drawing"]['geometry']['coordinates'][0][0][0])+str(output["last_active_drawing"]['geometry']['coordinates'][0][0][1])
            name = f"{id}"
        
        with st.sidebar:
            st.write(id)
            if st.button("Waarneming bijwerken",use_container_width=True):
                
                update_item(id)
            if st.button(":red[**Verwijder waarneming**]",use_container_width=True):
                df = conn.read(ttl=0,worksheet="df_observations")
                df_filter = df_point[df_point["key"]==id]
                df_drop = df_point[~df_point.apply(tuple, axis=1).isin(df_filter.apply(tuple, axis=1))]
                conn.update(worksheet='df_observations',data=df_drop)
                st.success('Waarneming verwijderd', icon="✅")
                st.page_link('page/🧭_navigatie.py', label="Opnieuw opstarten", icon="♻️",use_container_width=True)
                                           
    except:
        st.stop()

# except:
#     st.image("https://media.istockphoto.com/photos/open-empty-cardboard-box-on-a-white-background-picture-id172167710?k=6&m=172167710&s=612x612&w=0&h=Z4fueCweh9q-X_VBRAPCYSalyaAnXG3ioErb8oJSVek=")
#     st.stop()
