import streamlit as st

st.write('page 1')

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        np.random.randn(20, 3), columns=["a", "b", "c"]
    )
df = st.session_state.data

point_selector = alt.selection_point("point_selection")
interval_selector = alt.selection_interval("interval_selection")
chart = (
    alt.Chart(df)
    .mark_circle()
    .encode(
        x="a",
        y="b",
        size="c",
        color="c",
        tooltip=["a", "b", "c"],
        fillOpacity=alt.condition(point_selector, alt.value(1), alt.value(0.3)),
    )
    .add_params(point_selector, interval_selector)
)

event = st.altair_chart(chart, key="alt_chart", on_select="rerun")

event
