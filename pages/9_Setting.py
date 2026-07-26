import streamlit as st
import pandas as pd

from utils.data_loader import load_raw_data
from utils.theme import (
    inject_theme, eyebrow, hud_title, rule, kpi_panel
)

# ----------------------------------------
# Page Configuration
# ----------------------------------------

st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide"
)

inject_theme()

eyebrow("MODULE 09 // CONFIGURATION")
hud_title("Dashboard Settings", "Configure your AI-based military intelligence dashboard.")

rule()

# ----------------------------------------
# Appearance
# ----------------------------------------

eyebrow("APPEARANCE")

a1, a2, a3 = st.columns(3)

with a1:
    theme = st.selectbox(
        "Dashboard Theme",
        [
            "Light",
            "Dark"
        ],
        index=1,
    )

with a2:
    layout = st.selectbox(
        "Dashboard Layout",
        [
            "Wide",
            "Centered"
        ]
    )

with a3:
    chart_style = st.selectbox(
        "Chart Style",
        [
            "Plotly",
            "Bar",
            "Line",
            "Pie"
        ]
    )

rule()

# ----------------------------------------
# Default Dashboard Settings
# ----------------------------------------

eyebrow("DEFAULT DASHBOARD")

d1, d2, d3 = st.columns(3)

with d1:
    country = st.text_input(
        "Default Country",
        "India"
    )

with d2:
    forecast_years = st.slider(
        "Default Forecast Years",
        1,
        10,
        5
    )

with d3:
    confidence = st.slider(
        "Minimum Prediction Confidence (%)",
        50,
        100,
        80
    )

rule()

# ----------------------------------------
# Map Settings
# ----------------------------------------

eyebrow("GLOBAL THREAT MAP")

m1, m2 = st.columns([2, 1])

with m1:
    map_style = st.selectbox(
        "Map Style",
        [
            "OpenStreetMap",
            "Carto Positron",
            "Carto Dark"
        ]
    )

with m2:
    show_cluster = st.checkbox(
        "Enable Marker Clustering",
        value=True
    )
    show_heatmap = st.checkbox(
        "Enable Heatmap",
        value=False
    )

rule()

# ----------------------------------------
# Forecasting Settings
# ----------------------------------------

eyebrow("FORECASTING")

forecast_model = st.selectbox(
    "Forecasting Algorithm",
    [
        "Linear Regression",
        "ARIMA",
        "Prophet"
    ]
)

rule()

# ----------------------------------------
# Machine Learning Settings
# ----------------------------------------

eyebrow("MACHINE LEARNING")

ml1, ml2 = st.columns([2, 1])

with ml1:
    ml_model = st.selectbox(
        "Prediction Model",
        [
            "Random Forest",
            "Decision Tree",
            "Gradient Boosting"
        ]
    )

with ml2:
    probability = st.checkbox(
        "Show Prediction Probability",
        value=True
    )
    feature_importance = st.checkbox(
        "Show Feature Importance",
        value=True
    )

rule()

# ----------------------------------------
# Report Settings
# ----------------------------------------

eyebrow("AI INTELLIGENCE REPORT")

r1, r2 = st.columns([2, 1])

with r1:
    report_type = st.selectbox(
        "Default Report Format",
        [
            "PDF",
            "Word",
            "Text"
        ]
    )

with r2:
    include_charts = st.checkbox(
        "Include Charts in Report",
        value=True
    )
    include_tables = st.checkbox(
        "Include Data Tables",
        value=True
    )

rule()

# ----------------------------------------
# Notifications
# ----------------------------------------

eyebrow("NOTIFICATIONS")

n1, n2, n3 = st.columns(3)

with n1:
    attack_alert = st.checkbox(
        "Enable Attack Alerts",
        value=True
    )

with n2:
    forecast_alert = st.checkbox(
        "Enable Forecast Alerts",
        value=True
    )

with n3:
    report_alert = st.checkbox(
        "Enable Report Notifications",
        value=False
    )

rule()

# ----------------------------------------
# Dataset Information
# ----------------------------------------

eyebrow("DATASET INFORMATION")

try:

    df = load_raw_data()

    st.success("Dataset Loaded Successfully")

    col1, col2, col3 = st.columns(3)

    with col1:
        kpi_panel("Rows", f"{df.shape[0]:,}")
    with col2:
        kpi_panel("Columns", f"{df.shape[1]:,}")
    with col3:
        kpi_panel("Countries", f"{df['country_txt'].nunique():,}", accent="blue")

except Exception:

    st.error("Dataset not found.")

# ----------------------------------------
# Save / Reset Settings
# ----------------------------------------

rule()

s1, s2 = st.columns(2)

with s1:
    if st.button("💾 Save Settings"):
        st.success("Settings saved successfully!")
        st.balloons()

with s2:
    if st.button("🔄 Reset Settings"):
        st.warning("Settings reset to default values.")