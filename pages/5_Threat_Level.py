import streamlit as st
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

from utils.data_loader import load_raw_data
from utils.theme import (
    inject_theme, eyebrow, hud_title, rule,
    kpi_panel, status_panel, panel_open, panel_close,
    apply_plotly_theme, COLORS
)
import plotly.express as px

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Threat Level Prediction",
    page_icon="🚨",
    layout="wide"
)

inject_theme()

eyebrow("MODULE 05 // SEVERITY MODEL")
hud_title("AI Threat Level Prediction System", "Random-forest severity classifier trained on impact (fatalities + injuries).")

rule()

FEATURE_COLS = [
    "country_txt",
    "region_txt",
    "attacktype1_txt",
    "weaptype1_txt",
    "targtype1_txt",
]


def classify_threat(x):
    if x <= 2:
        return "LOW"
    elif x <= 10:
        return "MEDIUM"
    else:
        return "HIGH"


# -------------------------------
# Cached: load data, build labels, train model
# -------------------------------
# BUG FIX: the original code label-encoded the FEATURE_COLS columns
# in place, on the same DataFrame whose text values fed the sidebar
# selectboxes — so the dropdowns ended up showing raw integer codes
# ("0", "1", "2"...) instead of country/region/attack names. Here we
# keep a clean text-valued `display_df` for the widgets and build a
# separate numeric-encoded copy for training.
#
# PERFORMANCE FIX: training a 200-tree RandomForest is expensive and
# was previously re-run on *every* rerun (every widget change/button
# click). It's now wrapped in st.cache_resource so it trains exactly
# once per session.
@st.cache_resource
def load_and_train():
    df = load_raw_data()

    df = df[FEATURE_COLS + ["nkill", "nwound"]].dropna()

    display_df = df.copy()  # keeps original text values for the UI

    df = df.copy()
    df["impact"] = df["nkill"] + df["nwound"]
    df["threat_level"] = df["impact"].apply(classify_threat)

    encoders = {}
    for col in FEATURE_COLS:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    target_encoder = LabelEncoder()
    df["threat_level"] = target_encoder.fit_transform(df["threat_level"])

    X = df[FEATURE_COLS + ["nkill", "nwound"]]
    y = df["threat_level"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    return model, encoders, target_encoder, display_df


model, encoders, target_encoder, display_df = load_and_train()

# -------------------------------
# Sidebar Inputs (now correctly shows text labels, not codes)
# -------------------------------
st.sidebar.markdown('<div class="hud-eyebrow">INPUT PARAMETERS</div>', unsafe_allow_html=True)

country = st.sidebar.selectbox("Country", sorted(display_df["country_txt"].unique()))
region = st.sidebar.selectbox("Region", sorted(display_df["region_txt"].unique()))
attack = st.sidebar.selectbox("Attack Type", sorted(display_df["attacktype1_txt"].unique()))
weapon = st.sidebar.selectbox("Weapon Type", sorted(display_df["weaptype1_txt"].unique()))
target = st.sidebar.selectbox("Target Type", sorted(display_df["targtype1_txt"].unique()))

nkill = st.sidebar.number_input("Number Killed", 0, 1000, 0)
nwound = st.sidebar.number_input("Number Wounded", 0, 1000, 0)

# -------------------------------
# Prediction Button
# -------------------------------
eyebrow("ASSESSMENT")

if st.button("🚨 Predict Threat Level"):

    try:
        input_data = np.array([[
            encoders["country_txt"].transform([country])[0],
            encoders["region_txt"].transform([region])[0],
            encoders["attacktype1_txt"].transform([attack])[0],
            encoders["weaptype1_txt"].transform([weapon])[0],
            encoders["targtype1_txt"].transform([target])[0],
            nkill,
            nwound
        ]])

        prediction = model.predict(input_data)
        probability = model.predict_proba(input_data)

        result = target_encoder.inverse_transform(prediction)[0]
        confidence = np.max(probability) * 100

        level_map = {"LOW": "ok", "MEDIUM": "warn", "HIGH": "bad"}
        icon_map = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴"}

        r1, r2 = st.columns([2, 1])
        with r1:
            status_panel("Threat Level", f"{icon_map[result]} {result}", level=level_map[result])
        with r2:
            kpi_panel("Confidence Score", f"{confidence:.2f}%", accent="gold")

        rule()
        eyebrow("PROBABILITY DISTRIBUTION")

        prob_df = pd.DataFrame({
            "Threat Level": target_encoder.inverse_transform(np.arange(len(probability[0]))),
            "Probability": probability[0],
        })

        fig = px.bar(prob_df, x="Threat Level", y="Probability")
        fig.update_traces(marker_color=COLORS["accent_blue"])
        apply_plotly_theme(fig, height=340)

        panel_open(padding="6px")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        panel_close()

    except ValueError as e:
        status_panel("Model Output", "Unable to predict — one of the selected values wasn't in the training data.", level="bad")
        st.caption(f"Details: {e}")
else:
    status_panel("Model Output", "Set parameters in the sidebar and click Predict.", level="warn")