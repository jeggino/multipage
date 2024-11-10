import streamlit as st
from streamlit_gsheets import GSheetsConnection


conn = st.connection("gsheets", type=GSheetsConnection)
df_references = conn.read(ttl=0,worksheet="multipage_users")

placeholder_1 = st.empty()
placeholder_2 = st.empty()
name = placeholder_1.text_input("Name")
password = placeholder_2.text_input("Password",type='password')

try:
    index = df_references[df_references['username']==name].index[0]
    true_password = df_references.loc[index,"password"]

    if password == true_password:
        placeholder_1.empty()
        placeholder_2.empty()
        st.session_state.login = {"name": name, "password": password}
        status = df_references[df_references['username']==st.session_state.login["name"]].reset_index(drop=True)['type'].loc[0]
        
        pass
        
    else:
        st.error('Wrong password!!')
        st.stop()

except:
    st.stop()




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
    pg = st.navigation([page_1,page_3])

elif status == 'visitor':
    pg = st.navigation([page_3])
  

pg.run()
