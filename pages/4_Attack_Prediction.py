import streamlit as st
import joblib
import pandas as pd
from utils.data_loader import load_raw_data
from utils.theme import (
    inject_theme, eyebrow, hud_title, rule,
    kpi_panel, status_panel
)

st.set_page_config(
    page_title="Attack Prediction",
    page_icon="🤖",
    layout="wide"
)

inject_theme()


# -------------------------
# Cached model loading
# -------------------------
# joblib.load() hits disk every call. Without caching, all three .pkl files
# were being re-read from disk on *every* rerun (every widget interaction),
# not just on first load. st.cache_resource loads them once per session.
@st.cache_resource
def load_model_bundle():
    model = joblib.load("models/attack_prediction_model.pkl")
    encoders = joblib.load("models/feature_encoders.pkl")
    target_encoder = joblib.load("models/target_encoder.pkl")
    return model, encoders, target_encoder


try:
    model, encoders, target_encoder = load_model_bundle()
except FileNotFoundError as e:
    st.error(f"Model files not found: {e}. Train the model first (see train_attack_model.py).")
    st.stop()

eyebrow("MODULE 04 // CLASSIFICATION MODEL")
hud_title("Attack Type Prediction", "Enter the incident details below and run the classifier.")

rule()

# -------------------------
# Load Dataset (cached, shared across pages)
# -------------------------

df = load_raw_data()

df = df.dropna(subset=[
    "country_txt",
    "region_txt",
    "weaptype1_txt",
    "targtype1_txt",
    "gname"
])

# -------------------------
# Create Input Form
# -------------------------

eyebrow("INCIDENT PARAMETERS")

with st.form("prediction_form"):

    col1, col2 = st.columns(2)

    with col1:

        country = st.selectbox(
            "🌍 Country",
            sorted(df["country_txt"].unique())
        )

        region = st.selectbox(
            "🌎 Region",
            sorted(df["region_txt"].unique())
        )

        weapon = st.selectbox(
            "🔫 Weapon Type",
            sorted(df["weaptype1_txt"].unique())
        )

        target = st.selectbox(
            "🎯 Target Type",
            sorted(df["targtype1_txt"].unique())
        )

    with col2:

        group = st.selectbox(
            "👥 Terrorist Group",
            sorted(df["gname"].unique())
        )

        success = st.selectbox(
            "✅ Attack Successful?",
            [0, 1],
            format_func=lambda x: "Yes" if x == 1 else "No"
        )

        suicide = st.selectbox(
            "💣 Suicide Attack?",
            [0, 1],
            format_func=lambda x: "Yes" if x == 1 else "No"
        )

        nkill = st.number_input(
            "☠ Number of Fatalities",
            min_value=0,
            value=0,
            step=1
        )

        nwound = st.number_input(
            "🏥 Number of Injured",
            min_value=0,
            value=0,
            step=1
        )

    submitted = st.form_submit_button("🚀 Predict Attack Type")

rule()
eyebrow("MODEL OUTPUT")

# Previously this whole block ran unconditionally on every page load/rerun —
# meaning it silently predicted on the *default* form values before the user
# ever clicked the button, which is both misleading and wasted compute.
# It's now gated behind the actual form submission.
if not submitted:
    status_panel("Model Output", "Awaiting input — fill the form and click Predict.", level="warn")
else:
    try:
        encoded_country = encoders["country_txt"].transform([country])[0]
        encoded_region = encoders["region_txt"].transform([region])[0]
        encoded_weapon = encoders["weaptype1_txt"].transform([weapon])[0]
        encoded_target = encoders["targtype1_txt"].transform([target])[0]
        encoded_group = encoders["gname"].transform([group])[0]

        input_df = pd.DataFrame({
            "country_txt": [encoded_country],
            "region_txt": [encoded_region],
            "weaptype1_txt": [encoded_weapon],
            "targtype1_txt": [encoded_target],
            "gname": [encoded_group],
            "success": [success],
            "suicide": [suicide],
            "nkill": [nkill],
            "nwound": [nwound]
        })

        prediction = model.predict(input_df)
        attack_type = target_encoder.inverse_transform(prediction)[0]
        probabilities = model.predict_proba(input_df)
        confidence = probabilities.max() * 100

        r1, r2 = st.columns([2, 1])
        with r1:
            status_panel("Predicted Attack Type", attack_type, level="ok")
        with r2:
            kpi_panel("Prediction Confidence", f"{confidence:.2f}%", accent="gold")

    except ValueError as e:
        # A selected category wasn't seen by the encoders during training
        # (e.g. model trained on an older/filtered slice of the dataset).
        # Without this, the whole page would crash with a raw traceback.
        status_panel("Model Output", "Unable to predict — one of the selected values wasn't in the training data.", level="bad")
        st.caption(f"Details: {e}")