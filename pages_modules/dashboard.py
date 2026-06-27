import streamlit as st
import pandas as pd
from datetime import date, timedelta
from utils.database import get_transactions, get_products, get_daily_summary, get_category_summary
from utils.forecasting import kpi_summary, forecast_revenue
from utils import charts as ch


def fmt(val, currency="₹"):
    if val >= 1_00_00_000:
        return f"{currency}{val/1_00_00_000:.2f}Cr"
    elif val >= 1_00_000:
        return f"{currency}{val/1_00_000:.2f}L"
    elif val >= 1_000:
        return f"{currency}{val/1_000:.1f}K"
    return f"{currency}{val:,.0f}"


def delta_html(val, suffix="%"):
    arrow = "▲" if val >= 0 else "▼"
    cls   = "metric-delta-pos" if val >= 0 else "metric-delta-neg"
    return f'<span class="{cls}">{arrow} {abs(val):.1f}{suffix} vs last month</span>'


def show():
    bid = st.session_state.business_id
    biz = st.session_state.business_name

    st.markdown(f"""
    <div class="page-title">Good day, {st.session_state.username.split()[0]} 👋</div>
    <div class="page-subtitle">{biz} · Live business pulse · {date.today().strftime("%B %d, %Y")}</div>
    """, unsafe_allow_html=True)

    txns     = get_transactions(bid)
    products = get_products(bid)
    kpi      = kpi_summary(txns)

    if not kpi:
        st.info("No transactions yet. Add some from the Transactions page.")
        return

    # ── KPI Cards ─────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    cards = [
        (c1, "💰", "Total Revenue",  kpi["month_income"],  kpi.get("income_growth", 0),   "#00D4AA"),
        (c2, "💸", "Total Expenses", kpi["month_expense"],
         ((kpi["month_expense"]-kpi["last_expense"])/kpi["last_expense"]*100 if kpi["last_expense"] else 0), "#FF6B6B"),
        (c3, "📈", "Net Profit",     kpi["month_profit"],  kpi.get("income_growth", 0),    "#6C63FF"),
        (c4, "🏷️", "Profit Margin",  kpi["margin"],        0,                               "#FFB347"),
    ]
    for col, icon, label, value, delta, color in cards:
        with col:
            display = f"{value:.1f}%" if "Margin" in label else fmt(value)
            d_html  = delta_html(delta) if delta != 0 else ""
            col_style = f"border-top: 3px solid {color};"
            st.markdown(f"""
            <div class="metric-card" style="{col_style}">
                <span class="metric-icon">{icon}</span>
                <div class="metric-label">{label} (This Month)</div>
                <div class="metric-value">{display}</div>
                {d_html}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # ── Charts row 1 ──────────────────────────────────────────────────────────
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown('<div class="card-title">📊 Revenue vs Expenses (Last 30 Days)</div>', unsafe_allow_html=True)
        daily = get_daily_summary(bid, days=30)
        if not daily.empty:
            fig = ch.area_chart(daily, "txn_date", ["income", "expense", "profit"],
                                title="")
            ch.render_chart(st, fig)
        else:
            st.info("Not enough data.")

    with col_right:
        st.markdown('<div class="card-title">🍕 Expense Breakdown</div>', unsafe_allow_html=True)
        _, exp_cat = get_category_summary(bid)
        if not exp_cat.empty:
            fig = ch.donut_chart(exp_cat["category"].tolist(),
                                  exp_cat["amount"].tolist(),
                                  title="")
            ch.render_chart(st, fig)

    # ── Charts row 2 ──────────────────────────────────────────────────────────
    col_l2, col_r2 = st.columns([1, 2])

    with col_l2:
        st.markdown('<div class="card-title">🏆 Top Income Sources</div>', unsafe_allow_html=True)
        inc_cat, _ = get_category_summary(bid)
        if not inc_cat.empty:
            top = inc_cat.sort_values("amount", ascending=False).head(5)
            fig = ch.bar_chart(top, "category", "amount", color="#00D4AA",
                               title="", orientation="h")
            ch.render_chart(st, fig)

    with col_r2:
        st.markdown('<div class="card-title">🔮 30-Day Profit Forecast</div>', unsafe_allow_html=True)
        daily_all = get_daily_summary(bid, days=90)
        if not daily_all.empty and len(daily_all) >= 7:
            fcast = forecast_revenue(daily_all, days_ahead=30)
            fig   = ch.forecast_chart(
                daily_all.tail(30), fcast,
                "txn_date", "income",
                title="",
            )
            ch.render_chart(st, fig)
            if not fcast.empty:
                next_m_profit = fcast["profit"].sum()
                st.markdown(f"""
                <div class="forecast-tag">
                    🤖 AI Prediction · Next 30 days estimated profit:
                    <strong style="color:#6C63FF">{fmt(next_m_profit)}</strong>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Alerts + Inventory snapshot ───────────────────────────────────────────
    col_al, col_inv = st.columns([1, 2])

    with col_al:
        st.markdown('<div class="card-title">🚨 Inventory Alerts</div>', unsafe_allow_html=True)
        low = [p for p in products if 0 < p["stock"] <= p["low_stock_threshold"]]
        out = [p for p in products if p["stock"] == 0]
        if out:
            for p in out[:3]:
                st.markdown(f'<div class="alert alert-danger">🔴 <b>{p["name"]}</b> — Out of stock!</div>',
                            unsafe_allow_html=True)
        if low:
            for p in low[:3]:
                st.markdown(f'<div class="alert alert-warning">⚠️ <b>{p["name"]}</b> — Only {p["stock"]} left</div>',
                            unsafe_allow_html=True)
        if not low and not out:
            st.markdown('<div class="alert alert-success">✅ All products adequately stocked</div>',
                        unsafe_allow_html=True)

    with col_inv:
        st.markdown('<div class="card-title">📦 Inventory Overview</div>', unsafe_allow_html=True)
        if products:
            df_prod = pd.DataFrame(products)[["name", "stock", "sale_price", "low_stock_threshold"]]
            df_prod["Status"] = df_prod.apply(
                lambda r: "🔴 Out" if r["stock"] == 0 else ("⚠️ Low" if r["stock"] <= r["low_stock_threshold"] else "✅ OK"),
                axis=1
            )
            df_prod["Stock Value"] = df_prod["stock"] * df_prod["sale_price"]
            df_prod["Stock Value"] = df_prod["Stock Value"].apply(lambda x: fmt(x))
            df_prod = df_prod.rename(columns={"name": "Product", "stock": "Stock", "sale_price": "Price"})
            st.dataframe(df_prod[["Product", "Stock", "Price", "Status", "Stock Value"]],
                         use_container_width=True, hide_index=True)

    # ── Recent Transactions ───────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="card-title">🧾 Recent Transactions</div>', unsafe_allow_html=True)
    recent = txns[:10]
    if recent:
        df_r = pd.DataFrame(recent)[["txn_date", "type", "category", "amount", "description"]]
        df_r["amount"] = df_r["amount"].apply(lambda x: f"₹{x:,.2f}")
        df_r["type"]   = df_r["type"].apply(
            lambda t: f"🟢 {t}" if t == "Income" else f"🔴 {t}"
        )
        df_r.columns = ["Date", "Type", "Category", "Amount", "Description"]
        st.dataframe(df_r, use_container_width=True, hide_index=True)
