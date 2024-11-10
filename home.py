import streamlit as st
from streamlit_gsheets import GSheetsConnection


conn = st.connection("gsheets", type=GSheetsConnection)
df_references = conn.read(ttl=0,worksheet="multipage_users")

name = st.text_input("Name")
password = st.text_input("Password",type='password')

try:
    index = df_references[df_references['username']==name].index[0]
    true_password = df_references.loc[index,"password"]

    if password == true_password:
        # placeholder.empty()
        st.session_state.login = {"name": name, "password": password}
        pass
        
    else:
        st.error('Wrong password!!')
        st.stop()

except:
    st.stop()

status = df_references[df_references['username']==name].reset_index(drop=True)['type'].loc[0]


page_1 = st.Page("page/page_1.py", title="page 1", )
page_2 = st.Page("page/page_2.py", title="page 2")
page_3 = st.Page("page/page_3.py", title="page 3")

if status == 'admin':
    pg = st.navigation(
        {
            "Account": [page_1],
            "Reports": [page_2],
            "Tools": [page_3],
        }
    )
elif status == 'user':
    pg = st.navigation(
        {
            "Account": [page_1],
            "Reports": [page_2, page_3],
        }
    )
elif status == 'visitor':
    pg = st.navigation([page_3])
  

pg.run()
