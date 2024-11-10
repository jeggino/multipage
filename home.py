import streamlit as st
from streamlit_gsheets import GSheetsConnection
from functions import *


conn = st.connection("gsheets", type=GSheetsConnection)
df_references = conn.read(ttl=0,worksheet="df_users")






#---APP---
page_1 = st.Page("page/page_1.py", title="Scatter",icon="🔥" )
page_3 = st.Page("page/page_3.py", title="Map",icon="🔥")

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

if st.session_state.login['type'] == 'user':
    pg = st.navigation(
        {
            "Home": [page_1],
            "Reports": [page_3],
        }
    )

elif st.session_state.login['type'] == 'visitor':
    pg = st.navigation([page_3])
  

pg.run()
