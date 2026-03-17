import streamlit as st
from utils.database import init_db
from utils.auth import verify_session, logout, _token_expiry_info
from utils.theme import apply_theme

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Arthix – Small Business Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
init_db()

# ── Session defaults (first load only) ───────────────────────
for k, v in {
    "logged_in":     False,
    "access_token":  None,
    "refresh_token": None,
    "user_id":       None,
    "username":      "",
    "email":         "",
    "role":          "",
    "business_id":   None,
    "business_name": "",
    "page":          "dashboard",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── JWT: Verify session on EVERY page load ────────────────────
# verify_session() runs before rendering anything:
#   • Valid access token  → render app
#   • Expired access + valid refresh → auto-refresh silently
#   • Both expired / no token → show login page
session_valid = verify_session()

# ── Router ────────────────────────────────────────────────────
if not session_valid:
    from pages_modules import auth_page
    auth_page.show()

else:
    from pages_modules import (
        dashboard, transactions, inventory,
        analytics, reports, admin, profile,
    )

    with st.sidebar:
        # Brand
        st.markdown(f"""
        <div class="sidebar-brand">
            <span class="brand-icon">📊</span>
            <span class="brand-text">Arthix</span>
        </div>
        <div class="sidebar-biz">{st.session_state.business_name}</div>
        <div class="sidebar-role">
            <span class="role-badge">{st.session_state.role}</span>
        </div>
        """, unsafe_allow_html=True)

        # Live JWT session timer
        timer = _token_expiry_info()
        if timer:
            st.markdown(
                f'<div style="font-size:0.7rem;color:#3A5570;'
                f'padding:0 1rem 0.4rem;letter-spacing:0.02em;">'
                f'🔒 {timer}</div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")

        # Navigation
        pages_map = {
            "Dashboard":    "dashboard",
            "Transactions": "transactions",
            "Inventory":    "inventory",
            "Analytics":    "analytics",
            "Reports":      "reports",
            "Profile":      "profile",
        }
        if st.session_state.role == "Owner":
            pages_map["⚙️  Admin"] = "admin"

        for label, key in pages_map.items():
            if st.button(label, key=f"nav_{key}", use_container_width=True):
                st.session_state.page = key
                st.rerun()

        st.markdown("---")

        # Logout clears both JWT tokens + session
        if st.button("🚪  Logout", use_container_width=True):
            logout()
            st.rerun()

    # ── Page rendering ────────────────────────────────────────
    page = st.session_state.page
    if   page == "dashboard":    dashboard.show()
    elif page == "transactions": transactions.show()
    elif page == "inventory":    inventory.show()
    elif page == "analytics":    analytics.show()
    elif page == "reports":      reports.show()
    elif page == "admin":        admin.show()
    elif page == "profile":      profile.show()
    else:                        dashboard.show()
