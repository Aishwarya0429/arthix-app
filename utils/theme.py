import streamlit as st

def apply_theme():
    st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    #MainMenu, footer, header { visibility: hidden; }

    .block-container {
        padding-top: 0 !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        max-width: 1200px;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background-color: #0f1e3d !important;
        border-right: none !important;
    }
    section[data-testid="stSidebar"] > div {
        padding-top: 0 !important;
    }

    /* Sidebar all text default */
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: rgba(255,255,255,0.45) !important;
    }

    /* Sidebar buttons */
    section[data-testid="stSidebar"] .stButton button {
        background: transparent !important;
        border: none !important;
        border-left: 2px solid transparent !important;
        border-radius: 0 6px 6px 0 !important;
        color: rgba(255,255,255,0.45) !important;
        font-size: 13px !important;
        font-weight: 400 !important;
        text-align: left !important;
        padding: 9px 16px !important;
        width: 100% !important;
        box-shadow: none !important;
        transition: all 0.15s !important;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background: rgba(96,165,250,0.1) !important;
        border-left: 2px solid #60a5fa !important;
        color: #fff !important;
    }

    /* Logout button red */
    section[data-testid="stSidebar"] .stButton:last-of-type button {
        color: #f87171 !important;
    }
    section[data-testid="stSidebar"] .stButton:last-of-type button:hover {
        background: rgba(248,113,113,0.1) !important;
        border-left: 2px solid #f87171 !important;
        color: #f87171 !important;
    }

    /* ── Top bar ── */
    .arthix-topbar {
        background: #ffffff;
        padding: 14px 24px;
        border-bottom: 0.5px solid #e8ecf0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: -1.5rem -1.5rem 1.5rem -1.5rem;
    }
    .arthix-topbar-title {
        font-size: 16px;
        font-weight: 500;
        color: #0f1e3d;
    }
    .arthix-topbar-sub {
        font-size: 11px;
        color: #94a3b8;
        margin-top: 1px;
    }

    /* ── Page greeting ── */
    .page-title {
        font-size: 20px;
        font-weight: 500;
        color: #0f1e3d;
        margin-bottom: 2px;
    }
    .page-subtitle {
        font-size: 12px;
        color: #94a3b8;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 5px;
    }

    /* ── KPI metric cards ── */
    .metric-card {
        background: #ffffff;
        border: 0.5px solid #e8ecf0;
        border-radius: 10px;
        padding: 16px 18px;
        margin-bottom: 8px;
    }
    .metric-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 10px;
    }
    .metric-icon {
        width: 34px;
        height: 34px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }
    .metric-badge {
        font-size: 10px;
        border-radius: 20px;
        padding: 2px 8px;
    }
    .metric-label {
        font-size: 11px;
        color: #94a3b8;
        margin-bottom: 4px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .metric-value {
        font-size: 22px;
        font-weight: 500;
        color: #0f1e3d;
    }
    .metric-delta-pos { font-size: 11px; color: #059669; }
    .metric-delta-neg { font-size: 11px; color: #e24b4a; }

    /* ── Card titles ── */
    .card-title {
        font-size: 12px;
        font-weight: 500;
        color: #0f1e3d;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* ── Sidebar brand ── */
    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 18px 16px 14px;
        border-bottom: 0.5px solid rgba(255,255,255,0.07);
    }
    .brand-icon-box {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        background: #1a3a6e;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        color: #60a5fa;
        flex-shrink: 0;
    }
    .brand-text {
        font-size: 14px;
        font-weight: 500;
        color: #f0f4ff !important;
    }
    .brand-sub {
        font-size: 11px;
        color: rgba(255,255,255,0.3) !important;
        margin-top: 1px;
    }
    .sidebar-biz {
        font-size: 11px;
        color: rgba(255,255,255,0.3) !important;
        padding: 8px 16px 0;
    }
    .sidebar-role { padding: 4px 16px 10px; }
    .role-badge {
        font-size: 10px;
        color: #60a5fa !important;
        border: 1px solid #1a3a6e;
        background: #162d5c;
        border-radius: 20px;
        padding: 2px 10px;
        letter-spacing: 0.05em;
    }
    .sidebar-section-label {
        font-size: 10px;
        color: rgba(255,255,255,0.25) !important;
        letter-spacing: 0.08em;
        padding: 12px 16px 4px;
        text-transform: uppercase;
    }
    .sidebar-user {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 10px 16px;
        border-top: 0.5px solid rgba(255,255,255,0.07);
    }
    .sidebar-avatar {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background: #1a3a6e;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: 500;
        color: #60a5fa !important;
        flex-shrink: 0;
    }
    .sidebar-username {
        font-size: 12px;
        color: rgba(255,255,255,0.7) !important;
    }
    .sidebar-userrole {
        font-size: 10px;
        color: rgba(255,255,255,0.3) !important;
    }
    .session-info {
        font-size: 10px;
        color: rgba(255,255,255,0.3) !important;
        padding: 0 16px 8px;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    /* ── Forecast tag ── */
    .forecast-tag {
        font-size: 12px;
        color: #64748b;
        margin-top: 6px;
        padding: 6px 10px;
        background: #f4f6f9;
        border-radius: 6px;
        border: 0.5px solid #e8ecf0;
    }

    /* ── Alert boxes ── */
    .alert {
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 12px;
        margin-bottom: 6px;
    }
    .alert-danger  { background: #fef2f2; color: #b91c1c; border: 0.5px solid #fecaca; }
    .alert-warning { background: #fffbeb; color: #92400e; border: 0.5px solid #fde68a; }
    .alert-success { background: #f0fdf4; color: #065f46; border: 0.5px solid #bbf7d0; }

    /* ── Tables ── */
    .stDataFrame {
        border: 0.5px solid #e8ecf0 !important;
        border-radius: 8px !important;
    }

    /* ── Inputs ── */
    .stTextInput input,
    .stSelectbox select,
    .stNumberInput input,
    .stTextArea textarea {
        background: #ffffff !important;
        border: 0.5px solid #e8ecf0 !important;
        color: #0f1e3d !important;
        border-radius: 8px !important;
        font-size: 13px !important;
    }
    .stTextInput input:focus,
    .stSelectbox select:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 2px rgba(37,99,235,0.1) !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background-color: #2563eb !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        padding: 8px 18px !important;
    }
    .stButton > button:hover {
        background-color: #1d4ed8 !important;
    }

    /* ── Dividers ── */
    hr { border-color: #e8ecf0 !important; }

    </style>
    """, unsafe_allow_html=True)
