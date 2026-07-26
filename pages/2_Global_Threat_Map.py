import streamlit as st
import plotly.express as px
from utils.data_loader import load_data
from utils.theme import (
    inject_theme, eyebrow, hud_title, rule, status_pill,
    panel_open, panel_close, cta, apply_plotly_theme, COLORS
)

st.set_page_config(
    page_title="Global Threat Map",
    page_icon="🌍",
    layout="wide"
)

inject_theme()

df = load_data()

eyebrow("MODULE 02 // GEOSPATIAL")
hud_title("Global Threat Map", "Incident locations plotted by attack type across all recorded years.")

st.sidebar.markdown('<div class="hud-eyebrow">FILTERS</div>', unsafe_allow_html=True)
year = st.sidebar.selectbox(
    "Year",
    ["All"] + sorted(df["iyear"].unique().tolist())
)

@st.cache_data
def get_map_data(year):
    d = load_data()
    if year != "All":
        d = d[d["iyear"] == year]
    return d.dropna(subset=["latitude", "longitude"])

df = get_map_data(year)

status_pill(f"PLOTTED INCIDENTS: {len(df):,}", ok=True)

rule()

fig = px.scatter_mapbox(
    df,
    lat="latitude",
    lon="longitude",
    color="attacktype1_txt",
    hover_name="country_txt",
    hover_data=["city", "gname", "nkill"],
    zoom=1,
    height=560,
)
fig.update_layout(mapbox_style="carto-darkmatter")

apply_plotly_theme(fig, height=560)

panel_open(padding="6px")
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
panel_close()

rule()

cta('&larr; Change <b>Year</b> from the sidebar to filter the map.')