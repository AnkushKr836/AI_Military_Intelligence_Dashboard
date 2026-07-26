import pandas as pd
#
import streamlit as st
#streamlit helps in dashboard making
@st.cache_data 
#caching makes us read data only once
def load_data():
#use this function when required to call data
    df = pd.read_csv(
#it rreads the data to the pandas 
        "data/globalterrorism.csv",
#path
        encoding="latin1",
#it is used to encode text with spatial symbol
        low_memory=False
#it tells pandas to read every data and findout the data type for every #cell without any assumpition
    )
    df["nkill"] = df["nkill"].fillna(0)
#handling missing data
    df["nwound"] = df["nwound"].fillna(0)
    return df
#sending clean data back to the code 
#so basically data cleaning chal raha hai


@st.cache_data
def load_raw_data():
    """
    Cached read of the untouched GTD CSV (no fillna applied).
    Pages that need to `dropna()` on specific columns (prediction /
    threat-level / forecasting / explorer pages) should call this instead
    of each defining their own `pd.read_csv(...)` — previously every page
    re-read and re-cached its own full copy of the file, which is slow on
    first load of each page and wastes memory holding near-duplicate
    DataFrames. Centralizing it here means the CSV is parsed once and every
    page reuses the same cached object.
    """
    df = pd.read_csv(
        "data/globalterrorism.csv",
        encoding="latin1",
        low_memory=False
    )
    return df