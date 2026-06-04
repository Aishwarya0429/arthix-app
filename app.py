import streamlit as st
from utils.database import init_db
from utils.auth import verify_session, logout, _token_expiry_info
from utils.theme import apply_theme

st.set_page_config(
    page_title="Arthix – Small Business Analyzer",
    page_icon="A",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_theme()
init_db()

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

session_valid = verify_session()

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
            <div class="brand-icon-box">&#9641;</div>
            <div>
                <div class="brand-text">Arthix</div>
                <div class="brand-sub">Business Analyzer</div>
            </div>
        </div>
        <div class="sidebar-biz">{st.session_state.business_name}</div>
        <div class="sidebar-role">
            <span class="role-badge">{st.session_state.role.upper()}</span>
        </div>
        """, unsafe_allow_html=True)

        # Session timer
        timer = _token_expiry_info()
        if timer:
            st.markdown(
                f'<div class="session-info">&#9679; {timer}</div>',
                unsafe_allow_html=True,
            )

        # Nav sections
        main_pages = {
            "&#9632;  Dashboard":    "dashboard",
            "&#8645;  Transactions": "transactions",
            "&#9723;  Inventory":    "inventory",
            "&#9641;  Analytics":    "analytics",
        }
        manage_pages = {
            "&#9644;  Reports": "reports",
        }
        account_pages = {
            "&#9711;  Profile": "profile",
        }
        if st.session_state.role == "Owner":
            manage_pages["&#9881;  Admin"] = "admin"

        st.markdown('<div class="sidebar-section-label">Main</div>',
                    unsafe_allow_html=True)
        for label, key in main_pages.items():
            if st.button(label, key=f"nav_{key}",
                         use_container_width=True):
                st.session_state.page = key
                st.rerun()

        st.markdown('<div class="sidebar-section-label">Manage</div>',
                    unsafe_allow_html=True)
        for label, key in manage_pages.items():
            if st.button(label, key=f"nav_{key}",
                         use_container_width=True):
                st.session_state.page = key
                st.rerun()

        st.markdown('<div class="sidebar-section-label">Account</div>',
                    unsafe_allow_html=True)
        for label, key in account_pages.items():
            if st.button(label, key=f"nav_{key}",
                         use_container_width=True):
                st.session_state.page = key
                st.rerun()

        # User info + logout
        uname = st.session_state.username
        initials = uname[0].upper() if uname else "A"
        st.markdown(f"""
        <div class="sidebar-user">
            <div class="sidebar-avatar">{initials}</div>
            <div>
                <div class="sidebar-username">{uname}</div>
                <div class="sidebar-userrole">{st.session_state.role}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("&#10550;  Logout", use_container_width=True,
                     key="nav_logout"):
            logout()
            st.rerun()

    # Page rendering
    page = st.session_state.page
    if   page == "dashboard":    dashboard.show()
    elif page == "transactions": transactions.show()
    elif page == "inventory":    inventory.show()
    elif page == "analytics":    analytics.show()
    elif page == "reports":      reports.show()
    elif page == "admin":        admin.show()
    elif page == "profile":      profile.show()
    else:                        dashboard.show()
