import streamlit as st
from utils.database import init_db
from utils.auth import verify_session, logout, _token_expiry_info
from utils.theme import apply_theme

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Arthix – Small Business Analyzer",
    page_icon="🅰",
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
        <div style="padding: 0 12px 16px; border-bottom: 1px solid #EDE9FE; margin-bottom: 4px;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
                <div style="width:30px; height:30px; border-radius:8px;
                            background:linear-gradient(135deg,#7C3AED,#06B6D4);
                            display:flex; align-items:center; justify-content:center;
                            flex-shrink:0;">
                    <span style="color:white; font-weight:700; font-size:14px;">A</span>
                </div>
                <span style="font-size:16px; font-weight:600; color:#1E1B4B;">Arthix</span>
            </div>
            <div style="font-size:11px; color:#94A3B8; margin-bottom:6px;">
                {st.session_state.business_name}
            </div>
            <span style="font-size:10px; color:#7C3AED; border:1px solid #C4B5FD;
                         background:#F5F3FF; border-radius:20px;
                         padding:2px 10px; letter-spacing:0.05em;">
                {st.session_state.role.upper()}
            </span>
        </div>
        """, unsafe_allow_html=True)

        # Live JWT session timer
        timer = _token_expiry_info()
        if timer:
            st.markdown(
                f'<div style="font-size:10px; color:#94A3B8; '
                f'padding: 6px 14px 2px; display:flex; align-items:center; gap:4px;">'
                f'&#9679; {timer}</div>',
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # Navigation
        pages_map = {
            "&#9632;  Dashboard":    "dashboard",
            "&#8645;  Transactions": "transactions",
            "&#9723;  Inventory":    "inventory",
            "&#9641;  Analytics":    "analytics",
            "&#9644;  Reports":      "reports",
            "&#9711;  Profile":      "profile",
        }
        if st.session_state.role == "Owner":
            pages_map["&#9881;  Admin"] = "admin"

        for label, key in pages_map.items():
            is_active = st.session_state.page == key
            if is_active:
                st.markdown(f"""
                <div style="display:flex; align-items:center; gap:10px;
                            padding:9px 14px; font-size:13px; font-weight:500;
                            color:#7C3AED; background:#F5F3FF;
                            border-left:3px solid #7C3AED;
                            border-radius:0 6px 6px 0; margin-bottom:2px;">
                    {label}
                </div>
                """, unsafe_allow_html=True)
                # invisible button to still allow re-click
                st.button("", key=f"nav_{key}", use_container_width=True,
                          disabled=True)
            else:
                if st.button(label, key=f"nav_{key}", use_container_width=True):
                    st.session_state.page = key
                    st.rerun()

        st.markdown("<hr style='border-color:#EDE9FE; margin: 8px 0'>",
                    unsafe_allow_html=True)

        # Logout
        if st.button("&#10550;  Logout", use_container_width=True, key="nav_logout"):
            logout()
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
