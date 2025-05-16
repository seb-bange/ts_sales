# data_utils/utils.py

import pandas as pd

def load_filtered_data(filepath):
    df = pd.read_csv(filepath, parse_dates=["date"])
    return df

def get_store_item_lists(df):
    stores = sorted(df["store_nbr"].unique())
    items = sorted(df["item_nbr"].unique())
    return stores, items

import matplotlib.pyplot as plt
import pandas as pd

def plot_year_overview(df):
    """
    Plot total daily unit sales for the year 2013.
    """
    df["date"] = pd.to_datetime(df["date"])
    df_2013 = df[df["date"].dt.year == 2013]
    daily_sales = df_2013.groupby("date")["unit_sales"].sum()

    fig, ax = plt.subplots(figsize=(12, 5))
    daily_sales.plot(ax=ax)
    ax.set_title("Daily Unit Sales in 2013", fontsize=14)
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Unit Sales")
    ax.grid(True)

    return fig