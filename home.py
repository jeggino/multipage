import streamlit as st
from streamlit_gsheets import GSheetsConnection


conn = st.connection("gsheets", type=GSheetsConnection)
df_references = conn.read(ttl=0,worksheet="multipage_users")

st.dataframe(df_references)


# search = st.Page("tools/search.py", title="Search", icon=":material/search:")
# search = st.Page("tools/search.py", title="Search", icon=":material/search:")
# search = st.Page("tools/search.py", title="Search", icon=":material/search:")
# search = st.Page("tools/search.py", title="Search", icon=":material/search:")


# if st.session_state.logged_in:
#     pg = st.navigation(
#         {
#             "Account": [logout_page],
#             "Reports": [dashboard, bugs, alerts],
#             "Tools": [search, history],
#         }
#     )
# else:
#     pg = st.navigation([login_page])

# pg.run()
