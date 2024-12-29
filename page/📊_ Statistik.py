import streamlit as st




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
st.logo(IMAGE,  link=None, icon_image=IMAGE)

col1,col2 = st.columns([2,1])

VIDEO_URL = "https://www.youtube.com/watch?v=6qO1mpw8Xow"
col1.video(VIDEO_URL)
text = "Laatvliegers foerageren boven fietspad te Lies, Terschelling. Lantaarnpaal trekt waarschijnlijk prooien aan en de laatvliegers maken daar gretig gebruik van."
col2.write(text)
