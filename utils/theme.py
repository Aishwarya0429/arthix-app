import streamlit as st

def apply_theme():
    st.markdown("""
    <style>

    /* ── Sidebar back to dark ── */
    section[data-testid="stSidebar"] {
        background-color: #0A0F1A !important;
        border-right: 1px solid #1E2A3A !important;
    }
    section[data-testid="stSidebar"] * {
        color: #94A3B8 !important;
    }

    /* ── Sidebar buttons clean alignment ── */
    section[data-testid="stSidebar"] .stButton button {
        background: transparent !important;
        border: none !important;
        border-left: 2px solid transparent !important;
        border-radius: 0 6px 6px 0 !important;
        color: #94A3B8 !important;
        font-size: 13px !important;
        font-weight: 400 !important;
        text-align: left !important;
        padding: 9px 16px !important;
        width: 100% !important;
        transition: all 0.15s !important;
        box-shadow: none !important;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background: #131D2E !important;
        border-left: 2px solid #7C3AED !important;
        color: #A78BFA !important;
    }

    /* ── Hide the duplicate logout button ── */
    section[data-testid="stSidebar"] .stButton:last-child button {
        color: #EF4444 !important;
    }

    /* ── Main background dark ── */
    .main, .block-container {
        background-color: #0F1623 !important;
    }
    .block-container {
        padding-top: 1.5rem;
        max-width: 1200px;
    }

    /* ── Hide Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }

    /* ── Page title ── */
    .page-title {
        font-size: 26px;
        font-weight: 600;
        color: #E2E8F0;
        margin-bottom: 2px;
    }
    .page-subtitle {
        font-size: 12px;
        color: #475569;
        margin-bottom: 20px;
    }

    /* ── KPI metric cards ── */
    .metric-card {
        background: #131D2E;
        border: 0.5px solid #1E2A3A;
        border-radius: 10px;
        padding: 16px 18px;
        margin-bottom: 8px;
    }
    .metric-icon {
        font-size: 18px;
        display: block;
        margin-bottom: 6px;
        color: #94A3B8;
    }
    .metric-label {
        font-size: 10px;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 22px;
        font-weight: 600;
        color: #E2E8F0;
    }
    .metric-delta-pos {
        font-size: 11px;
        color: #10B981;
    }
    .metric-delta-neg {
        font-size: 11px;
        color: #EF4444;
    }

    /* ── Card titles ── */
    .card-title {
        font-size: 13px;
        font-weight: 500;
        color: #94A3B8;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* ── Forecast tag ── */
    .forecast-tag {
        font-size: 12px;
        color: #64748B;
        margin-top: 6px;
        padding: 6px 10px;
        background: #131D2E;
        border-radius: 6px;
        border: 0.5px solid #1E2A3A;
    }

    /* ── Alert boxes ── */
    .alert {
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 12px;
        margin-bottom: 6px;
    }
    .alert-danger  { background: #2D1515; color: #FCA5A5; border: 0.5px solid #7F1D1D; }
    .alert-warning { background: #2D2515; color: #FCD34D; border: 0.5px solid #78350F; }
    .alert-success { background: #152D1E; color: #6EE7B7; border: 0.5px solid #064E3B; }

    /* ── Sidebar brand ── */
    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 4px 16px 8px;
        font-size: 16px;
        font-weight: 600;
        color: #E2E8F0 !important;
    }
    .brand-icon {
        font-size: 20px;
    }
    .brand-text {
        color: #E2E8F0 !important;
    }
    .sidebar-biz {
        font-size: 11px;
        color: #475569 !important;
        padding: 0 16px 6px;
    }
    .sidebar-role {
        padding: 0 16px 12px;
    }
    .role-badge {
        font-size: 10px;
        color: #7C3AED !important;
        border: 1px solid #4C1D95;
        background: #1E1035;
        border-radius: 20px;
        padding: 2px 10px;
        letter-spacing: 0.05em;
    }

    /* ── Tables ── */
    .stDataFrame {
        border: 0.5px solid #1E2A3A;
        border-radius: 8px;
    }

    /* ── Inputs ── */
    .stTextInput input,
    .stSelectbox select,
    .stNumberInput input {
        background: #131D2E !important;
        border: 0.5px solid #1E2A3A !important;
        color: #E2E8F0 !important;
        border-radius: 8px !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background-color: #7C3AED !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }
    .stButton > button:hover {
        background-color: #6D28D9 !important;
    }

    /* ── Divider ── */
    hr { border-color: #1E2A3A !important; }

    </style>
    """, unsafe_allow_html=True)
