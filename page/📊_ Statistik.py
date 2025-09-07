import streamlit as st
from streamlit_option_menu import option_menu

from supabase import create_client, Client

from media_credentials import *

from streamlit_cookies_controller import CookieController
import time


controller = CookieController()



# st.markdown("""
#     <style>
#     .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK{ display: none; } #MainMenu{ visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
#     </style>
#     """,
#     unsafe_allow_html=True)



# reduce_header_height_style = """
# <style>
#     div.block-container {padding-top: 1rem; padding-bottom: 0rem; padding-left: 1rem; padding-right: 1rem; margin-top: 1rem; margin-bottom: 0rem;}
# </style>
# """ 

# st.markdown(reduce_header_height_style, unsafe_allow_html=True)

def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()

# def upload_photo():

#     # response = (
#     # supabase.storage
#     #     .from_("smp")
#     #     .list(
#     #         # "video-ts",
#     #         # {
#     #         #     "limit": 100,
#     #         #     "offset": 0,
#     #         #     "sortBy": {"column": "name", "order": "desc"},
#     #         # }
#     #     )
#     # )

#     # return response

#     uploaded_files = st.file_uploader(
#         "Upload a pictures", accept_multiple_files=False,label_visibility='collapsed',type="jpg"
#     )



#     if st.button("upload"):
#         st.image(uploaded_files)
#         with open(uploaded_files, "rb") as fs:
#             response = supabase.storage.from_('smp').upload('photos-zo/avatar1.jpg', fs, {'content-type': 'image/jpeg'})



# --- APP ---
IMAGE = "image/logo.png"
st.logo(IMAGE,  link=None, size="large",icon_image=IMAGE)

selected = option_menu(None,["Foto's", "Video's"], icons=['bi-camera', 'bi-camera-reels'],orientation="horizontal",)

if selected == "Foto's":
    # with st.expander("Upload a picture"):
    #     upload_photo()

    try:
        for key in media_dict[controller.get('project_name')][controller.get('opdracht')]['Photos']:
            with st.container(border=True):
                st.image(key)
                st.caption(media_dict[controller.get('project_name')][controller.get('opdracht')]['Photos'][key])
    except:
        st.image('https://cf.ltkcdn.net/travel/images/std/198833-425x283-Not-There-Yet.jpg')

elif selected == "Video's":
    try:
        for key in media_dict[controller.get('project_name')][controller.get('opdracht')]['Videos']:
            with st.container(border=False,horizontal_alignment="center"):
                st.video(key,loop=True, autoplay=False, muted=True,width=950)
                st.caption(media_dict[controller.get('project_name')][controller.get('opdracht')]['Videos'][key],width=950)
                "---"
    except:
        st.image('https://cf.ltkcdn.net/travel/images/std/198833-425x283-Not-There-Yet.jpg')
   

