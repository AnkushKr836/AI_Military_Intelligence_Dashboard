import streamlit as st
import plotly.express as px
from utils.data_loader import load_data
from utils.theme import (
    inject_theme, eyebrow, hud_title, rule, status_pill,
    kpi_panel, panel_open, panel_close, apply_plotly_theme, COLORS
)

st.set_page_config(
    page_title="Country Analysis",
    page_icon="🌎",
    layout="wide"
)

inject_theme()

df = load_data()

# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.markdown('<div class="hud-eyebrow">TARGET SELECTION</div>', unsafe_allow_html=True)

countries = sorted(df["country_txt"].dropna().unique())

country = st.sidebar.selectbox(
    "Select Country",
    countries
)

country_df = df[df["country_txt"] == country]

eyebrow("MODULE 03 // COUNTRY DOSSIER")
hud_title(f"Intelligence Report: {country}", "Per-country breakdown of incidents, actors, and methods.")
status_pill(f"RECORDS: {len(country_df):,}", ok=True)

rule()

# -----------------------------
# KPIs
# -----------------------------

eyebrow("KEY INDICATORS")

c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi_panel("Incidents", f"{len(country_df):,}")
with c2:
    kpi_panel("Fatalities", f"{int(country_df['nkill'].sum()):,}", accent="gold")
with c3:
    kpi_panel("Injured", f"{int(country_df['nwound'].sum()):,}", accent="gold")
with c4:
    kpi_panel("Groups", f"{country_df['gname'].nunique():,}", accent="blue")

rule()

# -----------------------------
# Attacks Over Time
# -----------------------------

eyebrow("TRENDS")

left, right = st.columns(2)

with left:

    yearly = (
        country_df
        .groupby("iyear")
        .size()
        .reset_index(name="Attacks")
    )

    fig = px.line(
        yearly,
        x="iyear",
        y="Attacks",
        markers=True,
        title="Attacks Over Years"
    )
    fig.update_traces(
        line=dict(color=COLORS["accent_blue"], width=2),
        marker=dict(color=COLORS["accent_gold"], size=5),
    )
    apply_plotly_theme(fig, height=380)

    panel_open(padding="6px")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    panel_close()

with right:

    attack = (
        country_df
        .groupby("attacktype1_txt")
        .size()
        .reset_index(name="Count")
    )

    fig = px.pie(
        attack,
        names="attacktype1_txt",
        values="Count",
        title="Attack Types",
        hole=0.55,
    )
    apply_plotly_theme(fig, height=380)

    panel_open(padding="6px")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    panel_close()

rule()

# -----------------------------
# Organizations
# -----------------------------

eyebrow("ACTORS & METHODS")

left, right = st.columns(2)

with left:

    groups = (
        country_df
        .groupby("gname")
        .size()
        .reset_index(name="Attacks")
        .sort_values("Attacks", ascending=False)
        .head(10)
    )

    fig = px.bar(
        groups,
        x="Attacks",
        y="gname",
        orientation="h",
        title="Top Terrorist Organizations"
    )
    apply_plotly_theme(fig, height=380)

    panel_open(padding="6px")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    panel_close()

with right:

    weapon = (
        country_df
        .groupby("weaptype1_txt")
        .size()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    fig = px.bar(
        weapon,
        x="weaptype1_txt",
        y="Count",
        title="Weapon Types"
    )
    apply_plotly_theme(fig, height=380)

    panel_open(padding="6px")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    panel_close()

rule()

# -----------------------------
# Incident Map
# -----------------------------

eyebrow("INCIDENT LOCATIONS")

map_df = country_df.dropna(
    subset=["latitude", "longitude"]
)

fig = px.scatter_geo(
    map_df,
    lat="latitude",
    lon="longitude",
    hover_name="city",
    hover_data={
        "country_txt": True,
        "iyear": True,
        "attacktype1_txt": True,
        "gname": True,
        "nkill": True,
        "latitude": False,
        "longitude": False
    },
    color="attacktype1_txt",
    projection="natural earth",
    title=f"Terrorist Incidents in {country}",
    height=600
)

fig.update_geos(
    bgcolor=COLORS["panel"],
    landcolor="#131B2B",
    oceancolor=COLORS["bg"],
    showocean=True,
    lakecolor=COLORS["bg"],
    coastlinecolor=COLORS["border_bright"],
    countrycolor=COLORS["border"],
)
apply_plotly_theme(fig)
fig.update_layout(margin=dict(l=0, r=0, t=50, b=0))

panel_open(padding="6px")
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
panel_close()

rule()

# -----------------------------
# Incident Table
# -----------------------------

eyebrow("INCIDENT DETAILS")

cols = [
    "iyear",
    "city",
    "attacktype1_txt",
    "targtype1_txt",
    "weaptype1_txt",
    "gname",
    "nkill",
    "nwound"
]

st.dataframe(
    country_df[cols],
    use_container_width=True
)

# -----------------------------
# Download
# -----------------------------

csv = country_df.to_csv(
    index=False
).encode()

st.download_button(
    "Download Country Data",
    csv,
    file_name=f"{country}.csv",
    mime="text/csv"
)