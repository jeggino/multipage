import streamlit as st
from media_credentials import *




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




# --- APP ---
IMAGE = "image/logo.png"
st.logo(IMAGE,  link=None, size="large",icon_image=IMAGE)

try:
    for key in media_dict[st.session_state.project['opdracht']]:
        col1,col2 = st.columns([2,1],gap="large", vertical_alignment="top", border=True)
        col1.video(key)
        col2.write(media_dict[st.session_state.project['opdracht']][key])
        "---"
except:
    st.write('Not yet')
    st.image('https://flic.kr/p/2ot2oFC')
    st.write('Not yet')
   
