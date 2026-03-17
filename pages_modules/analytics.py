import streamlit as st
import pandas as pd
import numpy as np
from utils.database import get_transactions, get_daily_summary, get_category_summary
from utils.forecasting import forecast_revenue, kpi_summary
from utils import charts as ch


def show():
    bid = st.session_state.business_id

    st.markdown('<div class="page-title">📈 Analytics & Insights</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Deep-dive analytics, AI forecasting & trend intelligence</div>',
        unsafe_allow_html=True,
    )

    txns = get_transactions(bid)
    if not txns:
        st.info("No transactions found. Add some data first.")
        return

    period  = st.selectbox("Analysis Period",
                           ["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time"])
    n_days  = {"Last 7 Days": 7, "Last 30 Days": 30, "Last 90 Days": 90, "All Time": 3650}[period]
    daily   = get_daily_summary(bid, days=n_days)

    tab1, tab2, tab3, tab4 = st.tabs([
        "  📊 Trend Analysis  ", "  🍕 Category Breakdown  ",
        "  🔮 AI Forecasting  ", "  📐 Profit Deep Dive  ",
    ])

    # ── Tab 1: Trend Analysis ──────────────────────────────────────────────────
    with tab1:
        if daily.empty:
            st.info("Not enough data for trends.")
        else:
            st.markdown('<div class="card-title">Revenue, Expenses & Profit Trend</div>',
                        unsafe_allow_html=True)
            fig_trend = ch.area_chart(daily, "txn_date", ["income", "expense", "profit"])
            ch.render_chart(st, fig_trend)

            st.markdown("---")
            st.markdown('<div class="card-title">Weekly Revenue Summary</div>', unsafe_allow_html=True)
            dc = daily.copy()
            dc["week"] = pd.to_datetime(dc["txn_date"]).dt.to_period("W").astype(str)
            weekly = dc.groupby("week")[["income", "expense", "profit"]].sum().reset_index()
            weekly.columns = ["Week", "income", "expense", "profit"]
            fig_weekly = ch.grouped_bar(weekly, "Week", ["income", "expense", "profit"])
            ch.render_chart(st, fig_weekly)

            st.markdown("---")
            kpi = kpi_summary(txns)
            g1, g2, g3 = st.columns(3)
            avg_daily = daily["income"].mean() if "income" in daily.columns else 0
            for col, label, val, color in [
                (g1, "Revenue Growth (MoM)", kpi.get("income_growth", 0), "#00D4AA"),
                (g2, "Profit Margin",         kpi.get("margin", 0),       "#6C63FF"),
                (g3, "Avg Daily Revenue",     avg_daily,                  "#FFB347"),
            ]:
                with col:
                    disp = f"₹{val:,.0f}" if label == "Avg Daily Revenue" else f"{val:.1f}%"
                    st.markdown(f"""
                    <div class="metric-card" style="border-top:3px solid {color}; padding:1rem;">
                        <div class="metric-label">{label}</div>
                        <div class="metric-value" style="font-size:1.6rem;">{disp}</div>
                    </div>""", unsafe_allow_html=True)

    # ── Tab 2: Category Breakdown ──────────────────────────────────────────────
    with tab2:
        inc_cat, exp_cat = get_category_summary(bid)
        col_l, col_r = st.columns(2)

        with col_l:
            st.markdown('<div class="card-title">💚 Income by Category</div>', unsafe_allow_html=True)
            if not inc_cat.empty:
                fig_inc = ch.donut_chart(inc_cat["category"].tolist(), inc_cat["amount"].tolist())
                ch.render_chart(st, fig_inc)
                disp = inc_cat.sort_values("amount", ascending=False).copy()
                disp["amount"] = disp["amount"].apply(lambda x: f"₹{x:,.2f}")
                disp = disp.rename(columns={"category": "Category", "amount": "Total"})
                st.dataframe(disp, use_container_width=True, hide_index=True)
            else:
                st.info("No income data.")

        with col_r:
            st.markdown('<div class="card-title">🔴 Expenses by Category</div>', unsafe_allow_html=True)
            if not exp_cat.empty:
                fig_exp = ch.donut_chart(
                    exp_cat["category"].tolist(), exp_cat["amount"].tolist(),
                    colors=["#FF6B6B","#FF8E8E","#FFB347","#FFC84A","#CC5555","#AA3333","#882222"],
                )
                ch.render_chart(st, fig_exp)
                total_exp = exp_cat["amount"].sum()
                ep = exp_cat.copy()
                ep["Share"]  = (ep["amount"] / total_exp * 100).apply(lambda x: f"{x:.1f}%")
                ep["amount"] = ep["amount"].apply(lambda x: f"₹{x:,.2f}")
                ep = ep.rename(columns={"category": "Category", "amount": "Total"})
                st.dataframe(ep.sort_values("Share", ascending=False),
                             use_container_width=True, hide_index=True)

    # ── Tab 3: AI Forecasting ──────────────────────────────────────────────────
    with tab3:
        st.markdown("""
        <div class="forecast-tag">
            🤖 AI-Powered · Linear Regression + Trend Smoothing · 90% Confidence Intervals
        </div>""", unsafe_allow_html=True)

        if daily.empty or len(daily) < 7:
            st.warning("Need at least 7 days of data for forecasting.")
        else:
            ctrl_col, chart_col = st.columns([1, 2])
            with ctrl_col:
                forecast_days  = st.slider("Forecast Horizon (days)", 7, 60, 30, step=7)
                metric_to_show = st.radio("Forecast Metric", ["income", "expense", "profit"])

            forecast_df = forecast_revenue(daily, days_ahead=forecast_days)

            with chart_col:
                if not forecast_df.empty:
                    fig_fcast = ch.forecast_chart(
                        daily.tail(30), forecast_df, "txn_date", metric_to_show,
                        title=f"Forecasted {metric_to_show.capitalize()} – Next {forecast_days} Days",
                    )
                    ch.render_chart(st, fig_fcast)

            if not forecast_df.empty:
                st.markdown("---")
                st.markdown('<div class="card-title">📋 Forecast Summary</div>', unsafe_allow_html=True)
                fc_s = forecast_df[["txn_date","income","expense","profit"]].copy()
                fc_s["txn_date"] = pd.to_datetime(fc_s["txn_date"]).dt.strftime("%b %d, %Y")
                for c in ["income","expense","profit"]:
                    fc_s[c] = fc_s[c].apply(lambda x: f"₹{x:,.0f}")
                fc_s.columns = ["Date","Forecast Income","Forecast Expense","Forecast Profit"]
                st.dataframe(fc_s.head(15), use_container_width=True, hide_index=True)

                raw = forecast_revenue(daily, days_ahead=forecast_days)
                m1, m2, m3 = st.columns(3)
                for col, label, val, color in [
                    (m1, "Predicted Revenue",  raw["income"].sum(),  "#00D4AA"),
                    (m2, "Predicted Expenses", raw["expense"].sum(), "#FF6B6B"),
                    (m3, "Predicted Profit",   raw["profit"].sum(),  "#6C63FF"),
                ]:
                    with col:
                        st.markdown(f"""
                        <div class="metric-card" style="border-top:3px solid {color}; padding:1rem;">
                            <div class="metric-label">Next {forecast_days}d · {label}</div>
                            <div class="metric-value" style="font-size:1.5rem;">₹{val:,.0f}</div>
                        </div>""", unsafe_allow_html=True)

    # ── Tab 4: Profit Deep Dive ────────────────────────────────────────────────
    with tab4:
        if daily.empty:
            st.info("No data available.")
            return

        df_margin = daily.copy()
        df_margin["margin_pct"] = (
            (df_margin["profit"] / df_margin["income"].replace(0, np.nan)) * 100
        ).fillna(0)

        st.markdown('<div class="card-title">📉 Daily Profit Margin %</div>', unsafe_allow_html=True)

        if ch.HAS_PLOTLY:
            import plotly.graph_objects as go
            fig_margin = go.Figure()
            fig_margin.add_trace(go.Scatter(
                x=df_margin["txn_date"], y=df_margin["margin_pct"],
                mode="lines+markers",
                line=dict(color="#6C63FF", width=2.5, shape="spline"),
                fill="tozeroy", fillcolor="rgba(108,99,255,0.08)",
                marker=dict(size=4),
                hovertemplate="<b>%{x}</b><br>Margin: %{y:.1f}%<extra></extra>",
                name="Profit Margin %",
            ))
            fig_margin.add_hline(y=0, line_dash="dash", line_color="rgba(255,107,107,0.31)",
                                 annotation_text="Break-even", annotation_position="bottom right")
            fig_margin.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="DM Sans", color="#8892B0"),
                margin=dict(l=10, r=10, t=20, b=10),
                xaxis=dict(gridcolor="rgba(108,99,255,0.12)", linecolor="rgba(108,99,255,0.12)"),
                yaxis=dict(gridcolor="rgba(108,99,255,0.12)", linecolor="rgba(108,99,255,0.12)",
                           ticksuffix="%"),
            )
            ch.render_chart(st, fig_margin)
        else:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            fig_margin, ax = plt.subplots(figsize=(10, 3.5))
            fig_margin.patch.set_facecolor("none"); ax.set_facecolor("none")
            x_vals = pd.to_datetime(df_margin["txn_date"])
            ax.fill_between(x_vals, df_margin["margin_pct"], alpha=0.15, color="#6C63FF")
            ax.plot(x_vals, df_margin["margin_pct"], color="#6C63FF", linewidth=2)
            ax.axhline(0, linestyle="--", color="#FF6B6B", linewidth=1, alpha=0.6, label="Break-even")
            ax.set_ylabel("Margin %", color="#8892B0", fontsize=9)
            ax.tick_params(colors="#8892B0", labelsize=8)
            for sp in ax.spines.values(): sp.set_edgecolor("#1C2540")
            ax.grid(True, color="#1C2540", linewidth=0.6, linestyle="--", alpha=0.8)
            ax.legend(facecolor="none", edgecolor="#1C2540", labelcolor="#8892B0")
            fig_margin.autofmt_xdate(rotation=30)
            plt.tight_layout()
            st.pyplot(fig_margin, use_container_width=True)
            plt.close(fig_margin)

        st.markdown("---")
        st.markdown('<div class="card-title">📊 Monthly Comparison</div>', unsafe_allow_html=True)
        df2 = daily.copy()
        df2["month"] = pd.to_datetime(df2["txn_date"]).dt.to_period("M").astype(str)
        monthly = df2.groupby("month")[["income","expense","profit"]].sum().reset_index()
        monthly.columns = ["Month","income","expense","profit"]
        fig_monthly = ch.grouped_bar(monthly, "Month", ["income","expense","profit"])
        ch.render_chart(st, fig_monthly)

        st.markdown("---")
        cl, cr = st.columns(2)
        with cl:
            st.markdown('<div class="card-title">🏆 Top 5 Revenue Days</div>', unsafe_allow_html=True)
            top5 = daily.nlargest(5, "income")[["txn_date","income","profit"]].copy()
            top5["income"] = top5["income"].apply(lambda x: f"₹{x:,.0f}")
            top5["profit"] = top5["profit"].apply(lambda x: f"₹{x:,.0f}")
            top5.columns   = ["Date","Revenue","Profit"]
            st.dataframe(top5, use_container_width=True, hide_index=True)

        with cr:
            st.markdown('<div class="card-title">📉 Highest Expense Days</div>', unsafe_allow_html=True)
            bot5 = daily.nlargest(5, "expense")[["txn_date","expense","profit"]].copy()
            bot5["expense"] = bot5["expense"].apply(lambda x: f"₹{x:,.0f}")
            bot5["profit"]  = bot5["profit"].apply(lambda x: f"₹{x:,.0f}")
            bot5.columns    = ["Date","Expenses","Profit"]
            st.dataframe(bot5, use_container_width=True, hide_index=True)
