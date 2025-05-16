# app/config.py

APP_TITLE = "🧠 Sales Forecast App – Guayas Region"

DATA_PATH = "preprocessed/train_guayas_prepared.csv"

FORECAST_CUTOFF = "2013-12-31"
FORECAST_END = "2014-03-31"

FEATURES = [
    "onpromotion", "day", "month", "year", "day_of_week", "unit_sales_7d_avg"
]

TARGET = "unit_sales"