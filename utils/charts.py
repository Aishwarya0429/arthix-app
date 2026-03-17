"""
Chart helpers for Arthix.
Uses Plotly when available (pip install plotly), falls back to Matplotlib.
"""

try:
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

COLORS = {
    "accent":  "#0EA5E9",   # sky blue
    "accent2": "#06B6D4",   # cyan
    "accent3": "#F43F5E",   # rose
    "accent4": "#F59E0B",   # amber
    "bg":      "#0B1A2E",
    "bg2":     "#102440",
    "text":    "#E0F2FE",
    "text2":   "#7AA2C0",
    "grid":    "#102440",
}
MPL_PALETTE = [COLORS["accent"], COLORS["accent2"], COLORS["accent3"],
               COLORS["accent4"], "#38BDF8", "#22D3EE", "#FB923C", "#A78BFA"]

def _dark_fig(figsize=(10, 4)):
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor("none")
    ax.set_facecolor("none")
    ax.tick_params(colors=COLORS["text2"], labelsize=9)
    for spine in ax.spines.values():
        spine.set_edgecolor(COLORS["grid"])
    ax.grid(True, color=COLORS["grid"], linewidth=0.7, linestyle="--", alpha=0.8)
    ax.set_axisbelow(True)
    return fig, ax

def _hex_to_rgba(hex_color, alpha=0.1):
    """Convert #RRGGBB hex to rgba(r,g,b,alpha) string safe for Plotly."""
    h = hex_color.lstrip("#")
    if len(h) == 6:
        r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
        return f"rgba({r},{g},{b},{alpha})"
    return hex_color  # already rgba or named color


if HAS_PLOTLY:
    LAYOUT = dict(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans, sans-serif", color=COLORS["text2"], size=12),
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(bgcolor="rgba(22,29,47,0.7)", bordercolor=COLORS["grid"],
                    borderwidth=1, font=dict(size=11)),
        xaxis=dict(gridcolor=COLORS["grid"], linecolor=COLORS["grid"],
                   tickfont=dict(color=COLORS["text2"], size=11)),
        yaxis=dict(gridcolor=COLORS["grid"], linecolor=COLORS["grid"],
                   tickfont=dict(color=COLORS["text2"], size=11)),
    )

    def area_chart(df, x, cols, title="", colors=None):
        clrs = colors or [COLORS["accent2"], COLORS["accent3"], COLORS["accent"]]
        fig = go.Figure()
        for i, col in enumerate(cols):
            if col not in df.columns: continue
            c = clrs[i % len(clrs)]
            fig.add_trace(go.Scatter(
                x=df[x], y=df[col], mode="lines", name=col.capitalize(),
                line=dict(color=c, width=2.5, shape="spline"),
                fill="tozeroy",
                fillcolor=_hex_to_rgba(c, 0.08),
                hovertemplate=f"<b>{col}</b>: ₹%{{y:,.0f}}<extra></extra>",
            ))
        fig.update_layout(title=dict(text=title, font=dict(family="Syne", size=15, color=COLORS["text"])), **LAYOUT)
        return fig

    def bar_chart(df, x, y, color=None, title="", orientation="v"):
        clr = color or COLORS["accent"]
        kwargs = dict(x=df[x], y=df[y]) if orientation == "v" else dict(x=df[y], y=df[x])
        fig = go.Figure(go.Bar(
            **kwargs, marker=dict(color=clr, opacity=0.85), orientation=orientation,
            hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>" if orientation=="v"
                          else "<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>",
        ))
        fig.update_layout(title=dict(text=title, font=dict(family="Syne", size=15, color=COLORS["text"])),
                          bargap=0.35, **LAYOUT)
        return fig

    def grouped_bar(df, x, cols, title=""):
        clrs = [COLORS["accent2"], COLORS["accent3"], COLORS["accent"]]
        fig = go.Figure()
        for i, col in enumerate(cols):
            if col not in df.columns: continue
            fig.add_trace(go.Bar(
                name=col.capitalize(), x=df[x], y=df[col],
                marker_color=clrs[i % len(clrs)], opacity=0.85,
                hovertemplate=f"<b>{col}</b>: ₹%{{y:,.0f}}<extra></extra>",
            ))
        fig.update_layout(barmode="group", bargap=0.2, bargroupgap=0.05,
                          title=dict(text=title, font=dict(family="Syne", size=15, color=COLORS["text"])), **LAYOUT)
        return fig

    def donut_chart(labels, values, title="", colors=None):
        clrs = colors or [COLORS["accent"], COLORS["accent2"], COLORS["accent3"],
                          COLORS["accent4"], "#A78BFA", "#34D399", "#FB923C"]
        fig = go.Figure(go.Pie(
            labels=labels, values=values, hole=0.55,
            marker=dict(colors=clrs[:len(labels)], line=dict(color=COLORS["bg"], width=2)),
            hovertemplate="<b>%{label}</b><br>₹%{value:,.0f} (%{percent})<extra></extra>",
        ))
        fig.update_layout(
            title=dict(text=title, font=dict(family="Syne", size=15, color=COLORS["text"])),
            paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=10, r=10, t=40, b=10),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["text2"], size=11)),
        )
        return fig

    def forecast_chart(hist_df, forecast_df, x_col, y_col, title=""):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hist_df[x_col], y=hist_df[y_col], mode="lines+markers",
            name="Historical", line=dict(color=COLORS["accent2"], width=2.5, shape="spline"),
            marker=dict(size=5), hovertemplate="₹%{y:,.0f}<extra>Historical</extra>",
        ))
        if forecast_df is not None and not forecast_df.empty:
            fig.add_trace(go.Scatter(
                x=forecast_df[x_col], y=forecast_df[y_col], mode="lines+markers",
                name="Forecast", line=dict(color=COLORS["accent"], width=2.5, dash="dash", shape="spline"),
                marker=dict(size=6, symbol="diamond"),
                hovertemplate="₹%{y:,.0f}<extra>Forecast</extra>",
            ))
            if "upper" in forecast_df.columns:
                fig.add_trace(go.Scatter(
                    x=list(forecast_df[x_col]) + list(reversed(forecast_df[x_col])),
                    y=list(forecast_df["upper"]) + list(reversed(forecast_df["lower"])),
                    fill="toself",
                    fillcolor=_hex_to_rgba(COLORS["accent"], 0.12),
                    line=dict(color="rgba(0,0,0,0)"),
                    name="Confidence Band",
                ))
        fig.update_layout(
            title=dict(text=title, font=dict(family="Syne", size=15, color=COLORS["text"])), **LAYOUT)
        return fig

    def sparkline(values, color=None):
        clr = color or COLORS["accent2"]
        fig = go.Figure(go.Scatter(
            y=values, mode="lines",
            line=dict(color=clr, width=2, shape="spline"),
            fill="tozeroy",
            fillcolor=_hex_to_rgba(clr, 0.08),
        ))
        fig.update_layout(
            margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(visible=False), yaxis=dict(visible=False),
            showlegend=False, height=60,
        )
        return fig

else:
    # Matplotlib fallbacks
    def area_chart(df, x, cols, title="", colors=None):
        clrs = colors or [COLORS["accent2"], COLORS["accent3"], COLORS["accent"]]
        fig, ax = _dark_fig()
        x_vals = pd.to_datetime(df[x]) if df[x].dtype == object else df[x]
        for i, col in enumerate(cols):
            if col not in df.columns: continue
            c = clrs[i % len(clrs)]
            ax.fill_between(x_vals, df[col], alpha=0.15, color=c)
            ax.plot(x_vals, df[col], color=c, linewidth=2, label=col.capitalize())
        ax.set_title(title, color=COLORS["text"], fontsize=12)
        ax.legend(facecolor="none", edgecolor=COLORS["grid"], labelcolor=COLORS["text2"])
        fig.autofmt_xdate(rotation=30)
        plt.tight_layout()
        return fig

    def bar_chart(df, x, y, color=None, title="", orientation="v"):
        clr = color or COLORS["accent"]
        fig, ax = _dark_fig()
        if orientation == "h":
            ax.barh(df[x], df[y], color=clr, alpha=0.85)
        else:
            ax.bar(df[x], df[y], color=clr, alpha=0.85)
        ax.set_title(title, color=COLORS["text"], fontsize=12)
        fig.autofmt_xdate(rotation=30)
        plt.tight_layout()
        return fig

    def grouped_bar(df, x, cols, title=""):
        clrs = [COLORS["accent2"], COLORS["accent3"], COLORS["accent"]]
        fig, ax = _dark_fig()
        n = len(cols); w = 0.7 / n
        xi = np.arange(len(df))
        for i, col in enumerate(cols):
            if col not in df.columns: continue
            ax.bar(xi + i * w, df[col], width=w, label=col.capitalize(),
                   color=clrs[i % len(clrs)], alpha=0.85)
        ax.set_xticks(xi + w*(n-1)/2)
        ax.set_xticklabels(df[x], rotation=30, ha="right", fontsize=8, color=COLORS["text2"])
        ax.set_title(title, color=COLORS["text"], fontsize=12)
        ax.legend(facecolor="none", edgecolor=COLORS["grid"], labelcolor=COLORS["text2"])
        plt.tight_layout()
        return fig

    def donut_chart(labels, values, title="", colors=None):
        clrs = (colors or MPL_PALETTE)[:len(labels)]
        fig, ax = plt.subplots(figsize=(6, 5))
        fig.patch.set_facecolor("none"); ax.set_facecolor("none")
        wedges, texts, autotexts = ax.pie(values, labels=None, colors=clrs, autopct="%1.1f%%",
            startangle=90, wedgeprops=dict(width=0.55, edgecolor=COLORS["bg"], linewidth=2), pctdistance=0.8)
        for t in autotexts: t.set_color(COLORS["text"]); t.set_fontsize(8)
        ax.legend(wedges, labels, loc="lower center", bbox_to_anchor=(0.5, -0.12),
                  ncol=3, facecolor="none", edgecolor="none", labelcolor=COLORS["text2"], fontsize=8)
        ax.set_title(title, color=COLORS["text"], fontsize=12)
        plt.tight_layout()
        return fig

    def forecast_chart(hist_df, forecast_df, x_col, y_col, title=""):
        fig, ax = _dark_fig()
        x_h = pd.to_datetime(hist_df[x_col])
        ax.plot(x_h, hist_df[y_col], color=COLORS["accent2"], linewidth=2,
                label="Historical", marker="o", markersize=3)
        if forecast_df is not None and not forecast_df.empty:
            x_f = pd.to_datetime(forecast_df[x_col])
            ax.plot(x_f, forecast_df[y_col], color=COLORS["accent"], linewidth=2,
                    linestyle="--", label="Forecast", marker="D", markersize=4)
            if "upper" in forecast_df.columns:
                ax.fill_between(x_f, forecast_df["lower"], forecast_df["upper"],
                                alpha=0.12, color=COLORS["accent"], label="Confidence Band")
        ax.set_title(title, color=COLORS["text"], fontsize=12)
        ax.legend(facecolor="none", edgecolor=COLORS["grid"], labelcolor=COLORS["text2"])
        fig.autofmt_xdate(rotation=30)
        plt.tight_layout()
        return fig

    def sparkline(values, color=None):
        clr = color or COLORS["accent2"]
        fig, ax = plt.subplots(figsize=(3, 0.8))
        fig.patch.set_facecolor("none"); ax.set_facecolor("none")
        ax.plot(values, color=clr, linewidth=1.5)
        ax.fill_between(range(len(values)), values, alpha=0.15, color=clr)
        ax.axis("off"); plt.tight_layout(pad=0)
        return fig


def render_chart(st, fig, **kwargs):
    """Universal chart renderer — works with both Plotly and Matplotlib figures."""
    if HAS_PLOTLY:
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, **kwargs)
    else:
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
