import streamlit as st
import plotly.express as px
from utils.data_loader import load_data
from utils.theme import (
    inject_theme, eyebrow, hud_title, rule, status_pill,
    kpi_panel, cta, apply_plotly_theme, COLORS
)

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)

inject_theme()

df = load_data()

eyebrow("MODULE 01 // OVERVIEW")
hud_title("Global Threat Overview", "Aggregate incident metrics drawn from the full GTD record set.")
status_pill(f"RECORDS LOADED: {len(df):,}", ok=True)

rule()
eyebrow("KEY INDICATORS")

c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi_panel("Incidents", f"{len(df):,}")
with c2:
    kpi_panel("Fatalities", f"{int(df['nkill'].sum()):,}", accent="gold")
with c3:
    kpi_panel("Injured", f"{int(df['nwound'].sum()):,}", accent="gold")
with c4:
    kpi_panel("Countries", f"{df['country_txt'].nunique():,}", accent="blue")

rule()

eyebrow("TEMPORAL TREND")

yearly = (
    df.groupby("iyear")
      .size()
      .reset_index(name="Attacks")
)

fig = px.line(
    yearly,
    x="iyear",
    y="Attacks",
    markers=True,
)
fig.update_traces(
    line=dict(color=COLORS["accent_blue"], width=2),
    marker=dict(color=COLORS["accent_gold"], size=5, line=dict(width=0)),
)
fig.update_xaxes(title="Year")
fig.update_yaxes(title="Attacks")
apply_plotly_theme(fig, height=420)

st.markdown('<div class="hud-panel">', unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
st.markdown('</div>', unsafe_allow_html=True)

rule()

cta('&rarr; Open <b>Global Threat Map</b> from the sidebar to explore incidents geographically.')