import streamlit as st

st.write('page 3')

import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

chart_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=["lat", "lon"],
)

chart_data["capital-cities"] = 'Roma'

chart_data

chart=pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=37.76,
            longitude=-122.4,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=chart_data,
                get_position="[lon, lat]",
                get_color="[200, 30, 0, 160]",
                get_radius=100,
                id="capital-cities",
            ),
        ],
    )

event = st.pydeck_chart(chart, on_select="rerun", selection_mode="multi-object")

event.selection
