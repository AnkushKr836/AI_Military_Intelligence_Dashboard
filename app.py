import streamlit as st
from utils.theme import inject_theme, eyebrow, hud_title, rule, status_pill

st.set_page_config(
    page_title="AI Military Intelligence Dashboard",
    page_icon="🛡",
    layout="wide"
)

inject_theme()

eyebrow("SYSTEM // MILITARY INTELLIGENCE PLATFORM")
hud_title(
    "AI-Based Military<br>Intelligence Dashboard",
    "Threat analysis and attack forecasting built on the Global Terrorism "
    "Database (GTD). Select a module from the sidebar to begin."
)
status_pill("STATUS: OPERATIONAL &nbsp;·&nbsp; SOURCE: GTD 1970–2021 &nbsp;·&nbsp; MODEL: ACTIVE", ok=True)

rule()


eyebrow("MODULE INDEX")

modules = [
    ("01", "Home", "Summary metrics & yearly trend"),
    ("02", "Global Threat Map", "Geospatial incident view"),
    ("03", "Country Analysis", "Per-country intelligence report"),
    ("04", "Attack Prediction", "Classify likely attack type"),
    ("05", "Threat Level", "AI-scored incident severity"),
    ("06", "Forecasting", "Projected attack volume"),
    ("07", "AI Intelligence", "Auto-generated summary report"),
    ("08", "Data Explorer", "Filter, search, export raw data"),
    ("09", "Settings", "Dashboard configuration"),
]

rows_html = "".join(
    f"""<div class="hud-module">
            <span class="idx">{idx}</span>
            <span class="name">{name}</span>
            <span class="desc">{desc}</span>
        </div>"""
    for idx, name, desc in modules
)

st.markdown(f'<div class="hud-panel">{rows_html}</div>', unsafe_allow_html=True)

st.markdown(
    '<p style="font-family:\'JetBrains Mono\',monospace;font-size:0.78rem;'
    'color:#6B7A94;margin-top:14px;">&larr; Use the sidebar to navigate between modules.</p>',
    unsafe_allow_html=True,
)