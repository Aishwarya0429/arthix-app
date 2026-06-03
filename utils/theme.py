import streamlit as st

def apply_theme():
    st.markdown("""
    <style>

    /* ── Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: #F8F5FF;
        color: #1E1B4B;
    }

    /* ── Hide Streamlit default chrome ── */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1rem;
        max-width: 1200px;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #EDE9FE;
        padding-top: 0;
    }
    section[data-testid="stSidebar"] > div {
        padding-top: 1rem;
    }

    /* Sidebar nav links */
    section[data-testid="stSidebar"] .stRadio label,
    section[data-testid="stSidebar"] .stButton button {
        display: flex;
        align-items: center;
        gap: 10px;
        width: 100%;
        padding: 9px 20px;
        font-size: 13px;
        font-weight: 400;
        color: #64748B;
        background: transparent;
        border: none;
        border-left: 2px solid transparent;
        border-radius: 0;
        text-align: left;
        cursor: pointer;
        transition: all 0.15s;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        color: #7C3AED;
        background-color: #F5F3FF;
        border-left: 2px solid #C4B5FD;
    }

    /* ── KPI metric cards ── */
    [data-testid="metric-container"] {
        background: #FFFFFF;
        border: 0.5px solid #EDE9FE;
        border-radius: 10px;
        padding: 14px 16px;
    }
    [data-testid="metric-container"] label {
        font-size: 10px !important;
        color: #94A3B8 !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 22px !important;
        font-weight: 500 !important;
        color: #1E1B4B !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricDelta"] {
        font-size: 11px !important;
    }

    /* ── Cards / containers ── */
    .arthix-card {
        background: #FFFFFF;
        border: 0.5px solid #EDE9FE;
        border-radius: 10px;
        padding: 16px 18px;
        margin-bottom: 12px;
    }
    .arthix-card-title {
        font-size: 12px;
        font-weight: 500;
        color: #7C3AED;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* ── Greeting header ── */
    .arthix-greeting {
        font-size: 24px;
        font-weight: 500;
        color: #1E1B4B;
        margin-bottom: 2px;
    }
    .arthix-subline {
        font-size: 12px;
        color: #94A3B8;
        margin-bottom: 20px;
    }

    /* ── Buttons ── */
    .stButton > button {
        background-color: #7C3AED;
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 500;
        padding: 8px 18px;
        transition: background 0.15s;
    }
    .stButton > button:hover {
        background-color: #6D28D9;
    }

    /* ── Inputs ── */
    .stTextInput input,
    .stSelectbox select,
    .stNumberInput input {
        border: 0.5px solid #DDD6FE;
        border-radius: 8px;
        background: #FFFFFF;
        color: #1E1B4B;
        font-size: 13px;
    }
    .stTextInput input:focus,
    .stSelectbox select:focus {
        border-color: #7C3AED;
        box-shadow: 0 0 0 2px rgba(124,58,237,0.1);
    }

    /* ── Tables ── */
    .stDataFrame, .stTable {
        border: 0.5px solid #EDE9FE;
        border-radius: 8px;
        overflow: hidden;
    }

    /* ── Alerts ── */
    .stAlert {
        border-radius: 8px;
        font-size: 13px;
    }

    /* ── Divider ── */
    hr {
        border-color: #EDE9FE;
    }

    </style>
    """, unsafe_allow_html=True)
