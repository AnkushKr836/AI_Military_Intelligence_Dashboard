import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_raw_data
from utils.theme import (
    inject_theme, eyebrow, hud_title, rule,
    kpi_panel, panel_open, panel_close,
    apply_plotly_theme, COLORS
)

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="AI Intelligence Report",
    page_icon="🧠",
    layout="wide"
)

inject_theme()

eyebrow("MODULE 07 // AUTO-GENERATED REPORT")
hud_title("AI Intelligence Report", "Auto-generated intelligence summary from the Global Terrorism Database (GTD).")

rule()

# -------------------------------------------------
# Load Dataset (cached, shared across pages)
# -------------------------------------------------

df = load_raw_data()

# -------------------------------------------------
# Sidebar Filters
# -------------------------------------------------

st.sidebar.markdown('<div class="hud-eyebrow">REPORT FILTERS</div>', unsafe_allow_html=True)

years = sorted(df["iyear"].unique())

selected_year = st.sidebar.selectbox(
    "Select Year",
    ["All"] + list(years)
)

if selected_year != "All":
    df = df[df["iyear"] == selected_year]

# -------------------------------------------------
# Key Statistics
# -------------------------------------------------

total_incidents = len(df)

total_killed = int(df["nkill"].fillna(0).sum())

total_wounded = int(df["nwound"].fillna(0).sum())

countries = df["country_txt"].nunique()

groups = df["gname"].nunique()

# -------------------------------------------------
# Top Countries
# -------------------------------------------------

top_countries = (
    df["country_txt"]
    .value_counts()
    .head(10)
)

# -------------------------------------------------
# Top Terrorist Groups
# -------------------------------------------------

top_groups = (
    df["gname"]
    .value_counts()
    .head(10)
)

# -------------------------------------------------
# Attack Types
# -------------------------------------------------

attack_types = (
    df["attacktype1_txt"]
    .value_counts()
)

# -------------------------------------------------
# Weapon Types
# -------------------------------------------------

weapon_types = (
    df["weaptype1_txt"]
    .value_counts()
)

# -------------------------------------------------
# Threat Level
# -------------------------------------------------

avg_killed = df["nkill"].fillna(0).mean()

if avg_killed < 2:
    threat = "LOW 🟢"
    threat_accent = ""
elif avg_killed < 5:
    threat = "MEDIUM 🟡"
    threat_accent = "gold"
else:
    threat = "HIGH 🔴"
    threat_accent = "gold"

# -------------------------------------------------
# Dashboard Metrics
# -------------------------------------------------

eyebrow("KEY INTELLIGENCE INDICATORS")

col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_panel("Incidents", f"{total_incidents:,}")
with col2:
    kpi_panel("Fatalities", f"{total_killed:,}", accent="gold")
with col3:
    kpi_panel("Injuries", f"{total_wounded:,}", accent="gold")
with col4:
    kpi_panel("Threat Level", threat, accent=threat_accent)

rule()

# -------------------------------------------------
# Executive Summary
# -------------------------------------------------

eyebrow("EXECUTIVE SUMMARY")

summary = f"""
During the selected period, <b>{total_incidents:,}</b> terrorist incidents were recorded across <b>{countries}</b> countries.<br><br>
The attacks resulted in <b>{total_killed:,}</b> fatalities and <b>{total_wounded:,}</b> injuries.<br><br>
The overall threat level is assessed as <b>{threat}</b>.<br><br>
The most affected country is <b>{top_countries.index[0]}</b>.<br><br>
The most active terrorist organization is <b>{top_groups.index[0]}</b>.<br><br>
The most common attack type is <b>{attack_types.index[0]}</b>.<br><br>
The most frequently used weapon is <b>{weapon_types.index[0]}</b>.
"""

panel_open()
st.markdown(f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.85rem;line-height:1.7;color:#E8EDF4;">{summary}</div>', unsafe_allow_html=True)
panel_close()

rule()

# -------------------------------------------------
# Top Countries
# -------------------------------------------------

eyebrow("TOP 10 HIGH-RISK COUNTRIES")

fig = px.bar(
    top_countries,
    x=top_countries.values,
    y=top_countries.index,
    orientation="h",
    labels={
        "x":"Incidents",
        "y":"Country"
    }
)
fig.update_traces(marker_color=COLORS["accent_blue"])
apply_plotly_theme(fig, height=420)

panel_open(padding="6px")
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
panel_close()

rule()

# -------------------------------------------------
# Terrorist Groups
# -------------------------------------------------

eyebrow("MOST ACTIVE TERRORIST GROUPS")

fig2 = px.bar(
    top_groups,
    x=top_groups.values,
    y=top_groups.index,
    orientation="h",
    labels={
        "x":"Attacks",
        "y":"Group"
    }
)
fig2.update_traces(marker_color=COLORS["accent_gold"])
apply_plotly_theme(fig2, height=420)

panel_open(padding="6px")
st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
panel_close()

rule()

# -------------------------------------------------
# AI Intelligence Assessment
# -------------------------------------------------

eyebrow("AI INTELLIGENCE ASSESSMENT")

recommendation_items = [
    f"Increase surveillance in {top_countries.index[0]}.",
    f"Closely monitor activities associated with {top_groups.index[0]}.",
    "Strengthen protection of infrastructure that is frequently targeted.",
    "Enhance intelligence sharing among agencies.",
    "Increase monitoring of explosive-based attacks.",
    "Continue trend analysis using predictive machine learning models.",
]

rec_html = "".join(
    f'<div class="hud-module"><span class="idx">{i+1:02d}</span><span class="name" style="text-transform:none;font-size:0.92rem;">{item}</span></div>'
    for i, item in enumerate(recommendation_items)
)

st.markdown(f'<div class="hud-panel">{rec_html}</div>', unsafe_allow_html=True)

recommendation = "\n\n".join(f"{i+1}. {item}" for i, item in enumerate(recommendation_items))

rule()

# -------------------------------------------------
# Download Report
# -------------------------------------------------

report = f"""

==============================

AI INTELLIGENCE REPORT

==============================

Total Incidents : {total_incidents}

Fatalities : {total_killed}

Injuries : {total_wounded}

Threat Level : {threat}

Top Country : {top_countries.index[0]}

Top Group : {top_groups.index[0]}

Most Common Attack :
{attack_types.index[0]}

Most Common Weapon :
{weapon_types.index[0]}

Recommendations

{recommendation}

"""

st.download_button(
    "📄 Download Intelligence Report",
    report,
    file_name="AI_Intelligence_Report.txt"
)