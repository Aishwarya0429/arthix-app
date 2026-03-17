import pandas as pd
import numpy as np
from datetime import timedelta


def _moving_avg(series, window=7):
    return series.rolling(window=window, min_periods=1).mean()


def forecast_revenue(daily_df, days_ahead=30):
    """
    Simple linear regression + seasonal smoothing forecast.
    Returns a DataFrame with date, predicted_income, predicted_expense, predicted_profit,
    upper, lower confidence bounds.
    """
    if daily_df.empty or len(daily_df) < 7:
        return pd.DataFrame()

    df = daily_df.copy()
    df = df.sort_values("txn_date")
    df["t"] = np.arange(len(df))

    results = {}
    for col in ["income", "expense"]:
        if col not in df.columns:
            df[col] = 0
        y = df[col].values
        t = df["t"].values
        # Polyfit degree-1 (linear trend)
        coeffs = np.polyfit(t, y, 1)
        slope, intercept = coeffs

        # Residual std for confidence interval
        residuals = y - (slope * t + intercept)
        std = residuals.std()

        future_t = np.arange(len(df), len(df) + days_ahead)
        predicted = slope * future_t + intercept
        # Clamp to non-negative
        predicted = np.maximum(predicted, 0)

        results[col] = {
            "predicted": predicted,
            "upper": predicted + 1.65 * std,
            "lower": np.maximum(predicted - 1.65 * std, 0),
        }

    last_date = pd.to_datetime(df["txn_date"].max())
    future_dates = [last_date + timedelta(days=i+1) for i in range(days_ahead)]

    forecast_df = pd.DataFrame({
        "txn_date": future_dates,
        "income":   results["income"]["predicted"],
        "expense":  results["expense"]["predicted"],
        "upper":    results["income"]["upper"],
        "lower":    results["income"]["lower"],
    })
    forecast_df["profit"] = forecast_df["income"] - forecast_df["expense"]
    return forecast_df


def growth_rate(series):
    """Return month-over-month growth rate as percentage."""
    if len(series) < 2 or series.iloc[0] == 0:
        return 0.0
    return ((series.iloc[-1] - series.iloc[0]) / series.iloc[0]) * 100


def profit_margin(income, expense):
    if income == 0:
        return 0.0
    return ((income - expense) / income) * 100


def kpi_summary(transactions):
    """Return KPI dict from list of transaction dicts."""
    import pandas as pd
    from datetime import date, timedelta

    if not transactions:
        return {}

    df = pd.DataFrame(transactions)
    df["txn_date"] = pd.to_datetime(df["txn_date"])
    df["amount"] = df["amount"].astype(float)

    today = pd.Timestamp(date.today())
    this_month = df[df["txn_date"].dt.month == today.month]
    last_month = df[df["txn_date"].dt.month == (today - pd.offsets.MonthBegin(1)).month]

    def _sum(subset, typ):
        return subset[subset["type"] == typ]["amount"].sum()

    inc_m  = _sum(this_month, "Income")
    exp_m  = _sum(this_month, "Expense")
    inc_lm = _sum(last_month, "Income")
    exp_lm = _sum(last_month, "Expense")

    inc_all = _sum(df, "Income")
    exp_all = _sum(df, "Expense")

    return {
        "total_income":   inc_all,
        "total_expense":  exp_all,
        "total_profit":   inc_all - exp_all,
        "month_income":   inc_m,
        "month_expense":  exp_m,
        "month_profit":   inc_m - exp_m,
        "last_income":    inc_lm,
        "last_expense":   exp_lm,
        "last_profit":    inc_lm - exp_lm,
        "margin":         profit_margin(inc_m, exp_m),
        "income_growth":  profit_margin(inc_m, inc_lm) if inc_lm else 0,
        "txn_count":      len(df),
    }
