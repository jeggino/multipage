# import streamlit as st
# from streamlit_cookies_manager import EncryptedCookieManager
# import pandas as pd
# from supabase import create_client, Client


# # Create a cookie manager instance
# cookies = EncryptedCookieManager(
#     prefix="myapp_",  # Prefix for all cookies to avoid conflicts
#     password="a_secure_random_password_here"  # Encryption key
# )

# # This must be called at the start of your app
# if not cookies.ready():
#     st.stop()  # Wait until cookies are ready

# st.title("Streamlit Cookies Manager Example")

# st.set_page_config(
#     initial_sidebar_state="collapsed",
#     layout="wide",
#     page_title="🦇🪶 SMP-App",
    
# )

# def init_connection():
#     url = st.secrets["SUPABASE_URL"]
#     key = st.secrets["SUPABASE_KEY"]
#     return create_client(url, key)

# supabase = init_connection()
# rows_users = supabase.table("df_users").select("*").execute()
# df_references = pd.DataFrame(rows_users.data)

# name = st.text_input("Vul uw gebruikersnaam in, alstublieft",value=None)  
# password = st.text_input("Vul uw wachtwoord in, alstublieft",type="password")


# # Set a cookie
# if st.button("Set Cookie"):
#     cookies["username"] = name
#     cookies["password"] = password
#     cookies.save()  # Save changes to browser
#     st.success("Cookie set!")

# # Get a cookie
# if "username" in cookies:
#     st.write(f"Hello, {cookies['username']}!")
#     st.write(f"Password, {cookies['password']}!")

# # Delete a cookie
# if st.button("Delete Cookie"):
#     cookies["username"] = "delete"
#     cookies.save()
#     st.success("Cookie deleted!")


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

from supabase import create_client, Client

from credentials import *

from streamlit_cookies_controller import CookieController
import time

st.set_page_config(
    initial_sidebar_state="collapsed",
    layout="wide",
    page_title="🦇 Nature Logger 🪶",
    
)

def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()
rows_users = supabase.table("df_users").select("*").execute()
df_references = pd.DataFrame(rows_users.data)


controller = CookieController()


# --FUNCTIONS---
def logIn():
    name = st.text_input("Vul uw gebruikersnaam in, alstublieft",value=None)  
    password = st.text_input("Vul uw wachtwoord in, alstublieft",type="password")
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
            controller.set("name", name)
            controller.set("password", password)
            controller.set("type", type)
            st.rerun()

        else:
            st.markdown(f"Sorry {name.split()[0]}, het wachtwoord is niet correct.")



def project():
    index_project = df_references[df_references['username']==controller.get('name')].index[0]
    project_list = df_references.loc[index_project,"project"].split(',')
    project = st.selectbox("Kies een project",project_list,label_visibility="visible")
    opdracht = st.selectbox("Kies een opdracht",DICTIONARY_PROJECTS[project],label_visibility="visible")
    if project == 'SMPs-ZuidOost':
        gebied = st.selectbox("Kies een gebied",list(range(1,23)),label_visibility="visible")

        if controller.get('type')== 'user':
            on = st.toggle("🚲")
        else:
            on = False
        if st.button(":rainbow[**Begin**]"):
            controller.set("project_name", project)
            controller.set("opdracht", opdracht)
            controller.set("auto_start", on)
            controller.set("gebied", gebied)

            st.rerun()
    else:
        if controller.get('type')== 'user':
            on = st.toggle("🚲")
        else:
            on = False
        if st.button(":rainbow[**Begin**]"):
            controller.set("project_name", project)
            controller.set("opdracht", opdracht)
            controller.set("auto_start", on)
            
            st.rerun()
            

#---APP---
page_1 = st.Page("page/🧭_navigatie.py", title="Navigatie",icon=":material/explore:" )
page_2 = st.Page("page/📌_Voeg_een_waarneming_in.py", title="Voeg een waarneming in",icon=":material/add_location_alt:" )
page_3 = st.Page("page/📝_Dagverlag_formulier.py", title="Dagverslag",icon=":material/edit_note:" )
page_4 = st.Page("page/📊_ Statistik.py", title="Foto's & Video's",icon=":material/photo_camera:" )
page_5 = st.Page("page/statistik.py", title="Statistieken",icon=":material/bar_chart:" )
page_6 = st.Page("page/documenten.py", title="Documenten",icon=":material/folder:" )


#---APP---
IMAGE = "image/logo.png"
IMAGE_2 ="image/menu.jpg"
st.logo(IMAGE,  link=None, size="large",icon_image=IMAGE)


user_id = controller.get("name")
project_id = controller.get("project_name")

time.sleep(1)
if not user_id:
    logIn()
    st.stop()

if not project_id:
    project()
    st.stop()




# if st.session_state.login['type'] == 'user':
#     if st.session_state.project['project_name'] != 'Admin':
#         if st.session_state.project['project_name'] == 'Overig':
#             if st.session_state.project['auto_start'] == False:
#                 pg = st.navigation([page_1,page_2,page_5])
#             if st.session_state.project['auto_start'] == True:
#                 pg = st.navigation([page_1,page_2])
#         else:
#             if st.session_state.project['auto_start'] == False:
#                 pg = st.navigation([page_1,page_2,page_3,page_5,page_4],position="top",)
#             if st.session_state.project['auto_start'] == True:
#                 pg = st.navigation([page_1,page_2,page_3],position="top",)
            
#     else:
#         pg = st.navigation([page_1,page_2])
    
# else:
#     pg = st.navigation([page_1,page_5,page_4])


if controller.get("type") == 'user':
    if controller.get("project_name") != 'Admin':
        if controller.get("project_name") == 'Overig':
            if controller.get("auto_start") == False:
                pg = st.navigation([page_1,page_2,page_5])
            if controller.get("auto_start") == True:
                pg = st.navigation([page_1,page_2])
        else:
            if controller.get("auto_start") == False:
                pg = st.navigation([page_1,page_2,page_3,page_5,page_6,page_4],position="top",)
            if controller.get("auto_start") == True:
                pg = st.navigation([page_1,page_2,page_3],position="top",)
            
    else:
        pg = st.navigation([page_1,page_2])
    
else:
    pg = st.navigation([page_1,page_5,page_6,page_4])


pg.run()
