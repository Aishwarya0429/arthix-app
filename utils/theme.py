import streamlit as st

def apply_theme():
    st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        font-size: 14px;
    }

    #MainMenu, footer, header { visibility: hidden; }

    .block-container {
        padding-top: 0 !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1280px;
    }

    /* ══════════════════════════════════════
       SIDEBAR
    ══════════════════════════════════════ */
    section[data-testid="stSidebar"] {
        background-color: #0f1e3d !important;
        border-right: none !important;
        min-width: 220px !important;
        max-width: 220px !important;
    }
    section[data-testid="stSidebar"] > div {
        padding-top: 0 !important;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div {
        color: rgba(255,255,255,0.5) !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Sidebar nav buttons */
    section[data-testid="stSidebar"] .stButton button {
        background: transparent !important;
        border: none !important;
        border-left: 3px solid transparent !important;
        border-radius: 0 !important;
        color: rgba(255,255,255,0.55) !important;
        font-size: 13px !important;
        font-weight: 400 !important;
        font-family: 'Inter', sans-serif !important;
        text-align: left !important;
        padding: 10px 20px !important;
        width: 100% !important;
        box-shadow: none !important;
        transition: all 0.2s ease !important;
        letter-spacing: 0.01em !important;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background: rgba(255,255,255,0.06) !important;
        border-left: 3px solid #60a5fa !important;
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] .stButton button:focus {
        background: rgba(96,165,250,0.12) !important;
        border-left: 3px solid #60a5fa !important;
        color: #ffffff !important;
        box-shadow: none !important;
    }

    /* Logout button */
    section[data-testid="stSidebar"] .stButton:last-of-type button {
        color: #f87171 !important;
        margin-top: 4px !important;
    }
    section[data-testid="stSidebar"] .stButton:last-of-type button:hover {
        background: rgba(248,113,113,0.08) !important;
        border-left: 3px solid #f87171 !important;
        color: #fca5a5 !important;
    }

    /* ══════════════════════════════════════
       SIDEBAR BRAND & ELEMENTS
    ══════════════════════════════════════ */
    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 20px 20px 16px;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 4px;
    }
    .brand-icon-box {
        width: 34px;
        height: 34px;
        border-radius: 8px;
        background: linear-gradient(135deg, #1d4ed8, #3b82f6);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 15px;
        color: #ffffff;
        flex-shrink: 0;
        font-weight: 600;
    }
    .brand-text {
        font-size: 15px !important;
        font-weight: 600 !important;
        color: #f0f6ff !important;
        letter-spacing: 0.01em;
    }
    .brand-sub {
        font-size: 10px !important;
        color: rgba(255,255,255,0.3) !important;
        margin-top: 1px;
        letter-spacing: 0.02em;
    }
    .sidebar-biz {
        font-size: 11px !important;
        color: rgba(255,255,255,0.35) !important;
        padding: 10px 20px 2px;
        letter-spacing: 0.01em;
    }
    .sidebar-role {
        padding: 4px 20px 8px;
    }
    .role-badge {
        font-size: 10px !important;
        color: #93c5fd !important;
        border: 1px solid rgba(96,165,250,0.3) !important;
        background: rgba(96,165,250,0.1) !important;
        border-radius: 20px;
        padding: 2px 10px;
        letter-spacing: 0.06em;
        font-weight: 500;
    }
    .sidebar-section-label {
        font-size: 10px !important;
        color: rgba(255,255,255,0.2) !important;
        letter-spacing: 0.10em;
        padding: 16px 20px 4px;
        text-transform: uppercase;
        font-weight: 600 !important;
    }
    .session-info {
        font-size: 10px !important;
        color: rgba(255,255,255,0.25) !important;
        padding: 0 20px 6px;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    .sidebar-user {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 12px 20px;
        border-top: 1px solid rgba(255,255,255,0.06);
        margin-top: 4px;
    }
    .sidebar-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: linear-gradient(135deg, #1d4ed8, #3b82f6);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
        font-weight: 600;
        color: #ffffff !important;
        flex-shrink: 0;
    }
    .sidebar-username {
        font-size: 12px !important;
        font-weight: 500 !important;
        color: rgba(255,255,255,0.8) !important;
    }
    .sidebar-userrole {
        font-size: 10px !important;
        color: rgba(255,255,255,0.3) !important;
        margin-top: 1px;
    }

    /* ══════════════════════════════════════
       TOP BAR
    ══════════════════════════════════════ */
    .arthix-topbar {
        background: #ffffff;
        padding: 15px 28px;
        border-bottom: 1px solid #eef0f4;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 0 -2rem 1.8rem -2rem;
    }
    .arthix-topbar-title {
        font-size: 17px;
        font-weight: 600;
        color: #0f1e3d;
        letter-spacing: -0.01em;
    }
    .arthix-topbar-sub {
        font-size: 12px;
        color: #94a3b8;
        margin-top: 2px;
        font-weight: 400;
    }

    /* ══════════════════════════════════════
       PAGE TITLES
    ══════════════════════════════════════ */
    .page-title {
        font-size: 22px;
        font-weight: 600;
        color: #0f1e3d;
        margin-bottom: 3px;
        letter-spacing: -0.02em;
    }
    .page-subtitle {
        font-size: 13px;
        color: #94a3b8;
        margin-bottom: 24px;
        font-weight: 400;
    }

    /* ══════════════════════════════════════
       KPI METRIC CARDS
    ══════════════════════════════════════ */
    .metric-card {
        background: #ffffff;
        border: 1px solid #eef0f4;
        border-radius: 12px;
        padding: 18px 20px;
        margin-bottom: 8px;
        transition: box-shadow 0.2s;
    }
    .metric-card:hover {
        box-shadow: 0 4px 16px rgba(15,30,61,0.06);
    }
    .metric-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 14px;
    }
    .metric-icon {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        font-weight: 600;
    }
    .metric-badge {
        font-size: 11px;
        border-radius: 20px;
        padding: 3px 9px;
        font-weight: 500;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 600;
        color: #0f1e3d;
        letter-spacing: -0.02em;
        margin-bottom: 3px;
    }
    .metric-label {
        font-size: 12px;
        color: #94a3b8;
        font-weight: 400;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-delta-pos { font-size: 11px; color: #059669; font-weight: 500; }
    .metric-delta-neg { font-size: 11px; color: #dc2626; font-weight: 500; }

    /* ══════════════════════════════════════
       CARD TITLES
    ══════════════════════════════════════ */
    .card-title {
        font-size: 13px;
        font-weight: 600;
        color: #0f1e3d;
        margin-bottom: 14px;
        letter-spacing: -0.01em;
    }

    /* ══════════════════════════════════════
       AUTH / LOGIN PAGE
    ══════════════════════════════════════ */
    .auth-page-wrapper {
        min-height: 100vh;
        background: #f4f6f9;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .auth-logo {
        font-size: 28px;
        font-weight: 700;
        color: #0f1e3d;
        letter-spacing: -0.03em;
        font-family: 'Inter', sans-serif;
    }
    .auth-tagline {
        font-size: 13px;
        color: #94a3b8;
        margin-top: 4px;
        font-weight: 400;
        letter-spacing: 0.01em;
    }
    .auth-logo-box {
        width: 52px;
        height: 52px;
        border-radius: 14px;
        background: linear-gradient(135deg, #1d4ed8, #3b82f6);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 12px;
        font-size: 22px;
        color: white;
        font-weight: 700;
    }
    .info-box {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 10px;
        padding: 12px 14px;
        font-size: 12px;
        color: #1e40af;
        line-height: 1.7;
    }
    .card {
        background: #ffffff;
        border: 1px solid #eef0f4;
        border-radius: 12px;
        padding: 16px 18px;
        margin-top: 12px;
    }

    /* ══════════════════════════════════════
       TABS
    ══════════════════════════════════════ */
    .stTabs [data-baseweb="tab-list"] {
        background: #f4f6f9 !important;
        border-radius: 10px !important;
        padding: 4px !important;
        gap: 2px !important;
        border: none !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border: none !important;
        border-radius: 8px !important;
        color: #64748b !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        padding: 8px 20px !important;
        font-family: 'Inter', sans-serif !important;
    }
    .stTabs [aria-selected="true"] {
        background: #ffffff !important;
        color: #0f1e3d !important;
        box-shadow: 0 1px 4px rgba(15,30,61,0.08) !important;
    }
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }

    /* ══════════════════════════════════════
       INPUTS & FORMS
    ══════════════════════════════════════ */
    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {
        background: #ffffff !important;
        border: 1.5px solid #e2e8f0 !important;
        border-radius: 8px !important;
        color: #0f1e3d !important;
        font-size: 13px !important;
        font-family: 'Inter', sans-serif !important;
        padding: 10px 14px !important;
        transition: border-color 0.2s !important;
    }
    .stTextInput input:focus,
    .stNumberInput input:focus,
    .stTextArea textarea:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37,99,235,0.08) !important;
        outline: none !important;
    }
    .stSelectbox > div > div {
        background: #ffffff !important;
        border: 1.5px solid #e2e8f0 !important;
        border-radius: 8px !important;
        color: #0f1e3d !important;
        font-size: 13px !important;
        font-family: 'Inter', sans-serif !important;
    }
    .stTextInput label,
    .stNumberInput label,
    .stTextArea label,
    .stSelectbox label {
        font-size: 12px !important;
        font-weight: 500 !important;
        color: #374151 !important;
        margin-bottom: 4px !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* ══════════════════════════════════════
       BUTTONS
    ══════════════════════════════════════ */
    .stButton > button {
        background: #2563eb !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        padding: 10px 20px !important;
        letter-spacing: 0.01em !important;
        transition: background 0.2s, transform 0.1s !important;
        box-shadow: 0 1px 4px rgba(37,99,235,0.2) !important;
    }
    .stButton > button:hover {
        background: #1d4ed8 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(37,99,235,0.25) !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* Form submit primary button */
    .stFormSubmitButton > button {
        background: #2563eb !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        padding: 12px 24px !important;
        width: 100% !important;
        letter-spacing: 0.01em !important;
        transition: background 0.2s !important;
        box-shadow: 0 2px 8px rgba(37,99,235,0.25) !important;
        margin-top: 8px !important;
    }
    .stFormSubmitButton > button:hover {
        background: #1d4ed8 !important;
        box-shadow: 0 4px 16px rgba(37,99,235,0.3) !important;
    }

    /* ══════════════════════════════════════
       ALERTS & NOTIFICATIONS
    ══════════════════════════════════════ */
    .alert {
        padding: 10px 14px;
        border-radius: 8px;
        font-size: 13px;
        margin-bottom: 8px;
        font-weight: 400;
        line-height: 1.5;
    }
    .alert-danger  {
        background: #fef2f2;
        color: #991b1b;
        border: 1px solid #fecaca;
    }
    .alert-warning {
        background: #fffbeb;
        color: #92400e;
        border: 1px solid #fde68a;
    }
    .alert-success {
        background: #f0fdf4;
        color: #065f46;
        border: 1px solid #bbf7d0;
    }

    /* Streamlit native alerts */
    .stAlert {
        border-radius: 8px !important;
        font-size: 13px !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* ══════════════════════════════════════
       TABLES & DATAFRAMES
    ══════════════════════════════════════ */
    .stDataFrame {
        border: 1px solid #eef0f4 !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }
    .stDataFrame th {
        background: #f8fafc !important;
        color: #374151 !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        padding: 10px 14px !important;
    }
    .stDataFrame td {
        font-size: 13px !important;
        color: #0f1e3d !important;
        padding: 10px 14px !important;
    }

    /* ══════════════════════════════════════
       MISC
    ══════════════════════════════════════ */
    .forecast-tag {
        font-size: 12px;
        color: #475569;
        margin-top: 8px;
        padding: 8px 12px;
        background: #f0f6ff;
        border-radius: 8px;
        border: 1px solid #bfdbfe;
        font-weight: 400;
    }
    hr {
        border-color: #eef0f4 !important;
        margin: 1.5rem 0 !important;
    }
    .stSpinner {
        font-family: 'Inter', sans-serif !important;
        font-size: 13px !important;
    }

    </style>
    """, unsafe_allow_html=True)
