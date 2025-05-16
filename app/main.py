import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# Add project root to sys.path for module imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# --- App config and helpers ---
from app.config import APP_TITLE, FEATURES, TARGET, FORECAST_CUTOFF, FORECAST_END, DATA_PATH
from data_utils.utils import load_filtered_data, get_store_item_lists, plot_year_overview
from model.model_utils import run_forecast

# --- Page setup ---
st.set_page_config(page_title=APP_TITLE, layout="centered")
st.title(APP_TITLE)

# --- Load data (from local CSV) ---
data_path = os.path.join(project_root, DATA_PATH)
df = load_filtered_data(data_path)

# --- Sidebar ---
st.sidebar.header("❓ App Guide")
st.sidebar.markdown("""
**How to use this app:**
- Use the tabs below to explore:
  - 2013 historical unit sales (Overview tab)
  - Forecast by Store & Item (Forecast tab)
- Forecast is computed live using XGBoost with Hyperopt.
""")

# --- Tabs ---
tab1, tab2 = st.tabs(["📊 2013 Sales Overview", "🔍 Store & Item Forecast"])

# --- Tab 1: Overview ---
with tab1:
    st.subheader("Total Unit Sales – 2013")
    fig = plot_year_overview(df)
    st.pyplot(fig)

# --- Tab 2: Forecast ---
with tab2:
    st.subheader("Forecast by Store and Item")

    # Selection
    stores, items = get_store_item_lists(df)
    store_id = st.selectbox("Select Store:", stores)
    item_id = st.selectbox("Select Item:", items)

    if st.button("⏳ Run Forecast"):
        forecast_df, fig = run_forecast(df, store_id, item_id)
        st.pyplot(fig)

        csv = forecast_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Forecast CSV", csv, file_name=f"forecast_store{store_id}_item{item_id}.csv")