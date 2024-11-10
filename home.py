import streamlit as st
from streamlit_gsheets import GSheetsConnection


conn = st.connection("gsheets", type=GSheetsConnection)
df_references = conn.read(ttl=0,worksheet="multipage_users")

# st.dataframe(df_references)

option = st.selectbox("Who are you?",("Luigi", "Daan", "Tommaso"),)

page_1 = st.Page("page_1.py", title="page 1", )
page_2 = st.Page("page_2.py", title="page 2")
page_3 = st.Page("page_3.py", title="page 3")

status = df_references[df_references['name']==option].reset_index(drop=True)['type'].loc[0]
# st.write(status)
if status == 'admin':
    pg = st.navigation(
        {
            "Account": [page_1],
            "Reports": [page_1, page_2, page_3],
            "Tools": [page_1, page_3],
        }
    )
elif status == 'user':
    pg = st.navigation(
        {
            "Account": [page_1],
            "Reports": [page_1, page_2, page_3],
        }
    )
elif status == 'visitor':
    pg = st.navigation([page_3])
  

pg.run()
