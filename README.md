# AI-Based Military Intelligence Dashboard

A Streamlit dashboard for exploring and forecasting terrorism incidents using
the [Global Terrorism Database (GTD)](https://www.kaggle.com/datasets/START-UMD/gtd).

## Modules

| # | Page | Description |
|---|------|--------------|
| 01 | Home | Summary metrics & yearly trend |
| 02 | Global Threat Map | Geospatial incident view |
| 03 | Country Analysis | Per-country intelligence report |
| 04 | Attack Prediction | Classifies likely attack type |
| 05 | Threat Level | AI-scored incident severity |
| 06 | Forecasting | Projected attack volume |
| 07 | AI Intelligence | Auto-generated summary report |
| 08 | Data Explorer | Filter, search, export raw data |
| 09 | Settings | Dashboard configuration |

## Project Structure

```
Military_Intelligence_Dashboard/
├── app.py                     # Landing page
├── train_attack_model.py      # One-time script to train the attack-type model
├── data/
│   └── globalterrorism.csv    # GTD dataset (download from Kaggle, not in repo)
├── models/
│   ├── attack_prediction_model.pkl
│   ├── feature_encoders.pkl
│   └── target_encoder.pkl
├── pages/
│   ├── 1_Home.py
│   ├── 2_Global_Threat_Map.py
│   ├── 3_Country_Analysis.py
│   ├── 4_Attack_Prediction.py
│   ├── 5_Threat_Level.py
│   ├── 6_Forecasting.py
│   ├── 7_AI_Intelligence.py
│   ├── 8_Data_Explorer.py
│   └── 9_Setting.py
└── utils/
    ├── data_loader.py
    └── theme.py
```

## Setup

1. **Clone the repo**
   ```
   git clone https://github.com/AnkushKr836/AI_Military_Intelligence_Dashboard.git
   cd AI_Military_Intelligence_Dashboard
   ```

2. **Create a virtual environment and install dependencies**
   ```
   python -m venv venv
   venv\Scripts\activate          # Windows
   source venv/bin/activate       # macOS/Linux
   pip install -r requirements.txt
   ```

3. **Add the dataset**
   Download `globalterrorism.csv` from
   [Kaggle](https://www.kaggle.com/datasets/START-UMD/gtd) and place it at:
   ```
   data/globalterrorism.csv
   ```

4. **Train the attack-prediction model** (generates the `.pkl` files in `models/`)
   ```
   python train_attack_model.py
   ```

5. **Run the app**
   ```
   streamlit run app.py
   ```

## Notes

- `data/*.csv` and `models/*.pkl` are gitignored since they're large/regeneratable —
  run step 3–4 above after cloning.
- Built with Streamlit, Plotly, and scikit-learn.