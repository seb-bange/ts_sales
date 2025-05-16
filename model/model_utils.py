# model/model_utils.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import xgboost as xgb
from sklearn.metrics import mean_absolute_error
from hyperopt import fmin, tpe, hp, Trials, STATUS_OK
from app.config import FEATURES, TARGET, FORECAST_CUTOFF, FORECAST_END

# --- Forecast runner ---
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.metrics import mean_absolute_error
from hyperopt import fmin, tpe, hp, Trials, STATUS_OK
from app.config import FEATURES, TARGET, FORECAST_CUTOFF, FORECAST_END

def run_forecast(df, store_id, item_id):
    # Filter by store and item
    df_filtered = df[(df["store_nbr"] == store_id) & (df["item_nbr"] == item_id)].copy()
    df_filtered["date"] = pd.to_datetime(df_filtered["date"])

    # Time-based split
    cutoff = pd.to_datetime(FORECAST_CUTOFF)
    end = pd.to_datetime(FORECAST_END)
    train = df_filtered[df_filtered["date"] <= cutoff]
    test = df_filtered[(df_filtered["date"] > cutoff) & (df_filtered["date"] <= end)]

    X_train = train[FEATURES].fillna(0)
    y_train = train[TARGET]
    X_test = test[FEATURES].fillna(0)
    y_test = test[TARGET]

    def objective(params):
        model = xgb.XGBRegressor(**params, random_state=42)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        loss = mean_absolute_error(y_test, preds)
        return {"loss": loss, "status": STATUS_OK}

    space = {
        "max_depth": hp.choice("max_depth", [3, 4, 5]),
        "learning_rate": hp.uniform("learning_rate", 0.01, 0.3),
        "n_estimators": hp.choice("n_estimators", [50, 100, 150])
    }

    trials = Trials()
    best = fmin(fn=objective, space=space, algo=tpe.suggest, max_evals=15, trials=trials, show_progressbar=False)

    # Final model with best params
    model = xgb.XGBRegressor(
        max_depth=[3, 4, 5][best["max_depth"]],
        learning_rate=best["learning_rate"],
        n_estimators=[50, 100, 150][best["n_estimators"]],
        random_state=42
    )
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    # Forecast DataFrame
    forecast_df = test[["date"]].copy()
    forecast_df["actual"] = y_test.values[:len(preds)].astype(int)
    forecast_df["forecast"] = np.round(preds).astype(int)

    # Plot forecast
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(forecast_df["date"], forecast_df["actual"], label="Actual")
    ax.plot(forecast_df["date"], forecast_df["forecast"], label="Forecast")
    ax.set_title(f"Forecast for Store {store_id} – Item {item_id}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Unit Sales")
    ax.legend()
    ax.grid(True)

    return forecast_df, fig

# --- Forecast Plot ---
def plot_forecast(df, store, item):
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df["date"], df["actual"], label="Actual", alpha=0.8)
    ax.plot(df["date"], df["forecast"], label="Forecast", alpha=0.8, color="orange")
    ax.set_title(f"Forecast vs Actual – Q1 2014 (Store {store}, Item {item})")
    ax.set_xlabel("Date")
    ax.set_ylabel("Unit Sales")
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    st.pyplot(fig)
