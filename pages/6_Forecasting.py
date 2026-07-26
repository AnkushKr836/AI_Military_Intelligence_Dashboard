import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from sklearn.linear_model import LinearRegression

from utils.data_loader import load_raw_data
from utils.theme import (
    inject_theme, eyebrow, hud_title, rule,
    kpi_panel, status_panel, panel_open, panel_close,
    apply_plotly_theme, COLORS
)

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------
st.set_page_config(
    page_title="Forecasting",
    page_icon="📈",
    layout="wide"
)

inject_theme()

eyebrow("MODULE 06 // PROJECTION MODEL")
hud_title("Terrorism Attack Forecasting", "Linear-regression projection of future attack volume from historical GTD data.")

rule()

# ----------------------------------------------------
# Load Dataset (cached, shared across pages)
# ----------------------------------------------------
df = load_raw_data()

# ----------------------------------------------------
# Sidebar Filters
# ----------------------------------------------------
st.sidebar.markdown('<div class="hud-eyebrow">FORECAST SETTINGS</div>', unsafe_allow_html=True)

countries = sorted(df["country_txt"].dropna().unique())

country = st.sidebar.selectbox(
    "Select Country",
    countries
)

forecast_years = st.sidebar.slider(
    "Forecast Years",
    1,
    10,
    5
)

# ----------------------------------------------------
# Prepare Data
# ----------------------------------------------------
country_df = df[df["country_txt"] == country]

yearly = (
    country_df
    .groupby("iyear")
    .size()
    .reset_index(name="Attacks")
)

yearly = yearly.sort_values("iyear")

# ----------------------------------------------------
# Check data availability
# ----------------------------------------------------
if len(yearly) < 5:
    st.warning("Not enough historical data for forecasting.")
    st.stop()

# ----------------------------------------------------
# Train Linear Regression Model
# ----------------------------------------------------
X = yearly[["iyear"]]
y = yearly["Attacks"]

model = LinearRegression()
model.fit(X, y)

# ----------------------------------------------------
# Future Prediction
# ----------------------------------------------------
last_year = yearly["iyear"].max()

future_years = np.arange(
    last_year + 1,
    last_year + forecast_years + 1
)

future_df = pd.DataFrame({
    "iyear": future_years
})

predictions = model.predict(future_df)

predictions = np.maximum(predictions, 0)

forecast = pd.DataFrame({
    "Year": future_years,
    "Forecasted Attacks": predictions.astype(int)
})

# ----------------------------------------------------
# Historical + Forecast Plot
# ----------------------------------------------------
eyebrow(f"ATTACK FORECAST — {country.upper()}")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=yearly["iyear"],
        y=yearly["Attacks"],
        mode="lines+markers",
        name="Historical",
        line=dict(color=COLORS["accent_blue"], width=2),
        marker=dict(size=5),
    )
)

fig.add_trace(
    go.Scatter(
        x=forecast["Year"],
        y=forecast["Forecasted Attacks"],
        mode="lines+markers",
        name="Forecast",
        line=dict(color=COLORS["accent_gold"], width=2, dash="dash"),
        marker=dict(size=5),
    )
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Number of Attacks",
)
apply_plotly_theme(fig, height=560)

panel_open(padding="6px")
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
panel_close()

rule()

# ----------------------------------------------------
# Forecast Table
# ----------------------------------------------------
eyebrow("FORECAST RESULTS")

st.dataframe(
    forecast,
    use_container_width=True
)

# ----------------------------------------------------
# Growth Analysis
# ----------------------------------------------------
historical_last = yearly.iloc[-1]["Attacks"]
forecast_last = forecast.iloc[-1]["Forecasted Attacks"]

growth = (
    (forecast_last - historical_last)
    / max(historical_last, 1)
) * 100

rule()
eyebrow("GROWTH ANALYSIS")

col1, col2, col3 = st.columns(3)

with col1:
    kpi_panel("Current Attacks", f"{int(historical_last):,}")
with col2:
    kpi_panel(f"Forecast ({forecast_years}Y)", f"{int(forecast_last):,}", accent="blue")
with col3:
    kpi_panel("Growth %", f"{growth:.2f}%", accent="gold")

# ----------------------------------------------------
# Risk Assessment
# ----------------------------------------------------
rule()
eyebrow("RISK ASSESSMENT")

if growth < 0:
    status_panel("Threat Trend", "🟢 DECREASING", level="ok")
elif growth < 15:
    status_panel("Threat Trend", "🟡 STABLE", level="warn")
else:
    status_panel("Threat Trend", "🔴 INCREASING", level="bad")

# ----------------------------------------------------
# Download Forecast
# ----------------------------------------------------
csv = forecast.to_csv(index=False)

st.download_button(
    label="📥 Download Forecast CSV",
    data=csv,
    file_name=f"{country}_forecast.csv",
    mime="text/csv"
)