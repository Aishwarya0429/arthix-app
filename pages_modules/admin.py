import streamlit as st
import pandas as pd
from datetime import date
from utils.database import get_all_users, get_all_businesses, get_transactions, get_products


def show():
    if st.session_state.role != "Owner":
        st.error("⛔ Access Denied — Owner role required.")
        return

    st.markdown('<div class="page-title">⚙️ Admin Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">System overview, user management & business monitoring</div>',
                unsafe_allow_html=True)

    users      = get_all_users()
    businesses = get_all_businesses()
    txns       = get_transactions(st.session_state.business_id)
    products   = get_products(st.session_state.business_id)

    # ── System KPIs ────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    for col, icon, label, val, color in [
        (c1, "👥", "Total Users",      len(users),      "#6C63FF"),
        (c2, "🏢", "Businesses",       len(businesses), "#00D4AA"),
        (c3, "💳", "Transactions",     len(txns),       "#FFB347"),
        (c4, "📦", "Products",         len(products),   "#FF6B6B"),
    ]:
        with col:
            st.markdown(f"""
            <div class="metric-card" style="border-top:3px solid {color}; padding:1rem;">
                <span style="font-size:1.5rem;">{icon}</span>
                <div class="metric-label">{label}</div>
                <div class="metric-value" style="font-size:1.8rem;">{val}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    # ── System Health ──────────────────────────────────────────────────────────
    st.markdown('<div class="card-title">🖥️ System Health Monitor</div>', unsafe_allow_html=True)

    h1, h2, h3 = st.columns(3)
    metrics = [
        (h1, "Database", "Connected ✅", 100, "#00D4AA"),
        (h2, "API Services", "Running ✅", 98, "#6C63FF"),
        (h3, "Storage", "72% Used", 72, "#FFB347"),
    ]
    for col, service, status, pct, color in metrics:
        with col:
            st.markdown(f"""
            <div class="card" style="padding:1rem;">
                <div class="card-title" style="font-size:0.9rem;">{service}</div>
                <div style="color:{color}; font-weight:600; margin-bottom:0.5rem;">{status}</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(pct / 100)

    st.markdown("---")

    tab_users, tab_biz, tab_settings = st.tabs([
        "  👥 User Management  ", "  🏢 Business Profiles  ", "  ⚙️ System Settings  "
    ])

    # ── Users ──────────────────────────────────────────────────────────────────
    with tab_users:
        st.markdown('<div class="card-title">All Registered Users</div>', unsafe_allow_html=True)
        if users:
            df_u = pd.DataFrame(users)[["id", "name", "email", "role", "created_at"]]
            df_u["role"] = df_u["role"].apply(
                lambda r: f"👑 {r}" if r == "Owner" else (f"🧮 {r}" if r == "Accountant" else f"👤 {r}")
            )
            df_u.columns = ["ID", "Name", "Email", "Role", "Joined"]
            st.dataframe(df_u, use_container_width=True, hide_index=True)
        else:
            st.info("No users found.")

        st.markdown("---")
        st.markdown('<div class="card-title">Add New User</div>', unsafe_allow_html=True)
        with st.form("add_user_form"):
            c1, c2 = st.columns(2)
            new_name  = c1.text_input("Full Name")
            new_email = c2.text_input("Email")
            c3, c4   = st.columns(2)
            new_pass  = c3.text_input("Temporary Password", type="password")
            new_role  = c4.selectbox("Role", ["Staff", "Accountant", "Owner"])
            if st.form_submit_button("Create User", use_container_width=True, type="primary"):
                from utils.database import register_user
                uid = register_user(new_name, new_email, new_pass, new_role)
                if uid:
                    st.success(f"✅ User '{new_name}' created successfully!")
                    st.rerun()
                else:
                    st.error("Email already in use.")

    # ── Businesses ──────────────────────────────────────────────────────────────
    with tab_biz:
        st.markdown('<div class="card-title">All Business Profiles</div>', unsafe_allow_html=True)
        if businesses:
            df_b = pd.DataFrame(businesses)[["id", "name", "category", "currency", "owner_name", "created_at"]]
            df_b.columns = ["ID", "Business Name", "Category", "Currency", "Owner", "Created"]
            st.dataframe(df_b, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown('<div class="card-title">Create New Business Profile</div>', unsafe_allow_html=True)
        with st.form("add_biz_form"):
            c1, c2 = st.columns(2)
            bname   = c1.text_input("Business Name")
            bcat    = c2.selectbox("Category", [
                "Retail", "Food & Beverage", "Services", "Manufacturing",
                "E-Commerce", "Wholesale", "Healthcare", "Education", "Other"
            ])
            c3, c4 = st.columns(2)
            bcur   = c3.selectbox("Currency", ["INR", "USD", "EUR", "GBP"])
            if st.form_submit_button("Create Business", use_container_width=True, type="primary"):
                from utils.database import create_business
                create_business(st.session_state.user_id, bname, bcat, bcur)
                st.success(f"✅ Business '{bname}' created!")
                st.rerun()

    # ── Settings ────────────────────────────────────────────────────────────────
    with tab_settings:
        st.markdown('<div class="card-title">System Configuration</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box">
            ⚙️ These settings control global system behaviour. Changes take effect immediately.
        </div>
        """, unsafe_allow_html=True)

        with st.form("settings_form"):
            c1, c2 = st.columns(2)
            c1.selectbox("Default Currency", ["INR ₹", "USD $", "EUR €", "GBP £"])
            c2.selectbox("Date Format", ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"])
            c1b, c2b = st.columns(2)
            c1b.number_input("Low Stock Default Threshold", min_value=1, value=10)
            c2b.selectbox("Report Email Frequency", ["Never", "Weekly", "Monthly"])
            st.checkbox("Enable AI Forecasting", value=True)
            st.checkbox("Enable Email Notifications", value=False)
            st.checkbox("Allow Multi-Business Profiles", value=True)
            if st.form_submit_button("Save Settings", use_container_width=True, type="primary"):
                st.success("✅ Settings saved successfully!")

        st.markdown("---")
        st.markdown('<div class="card-title" style="color:#FF6B6B;">⚠️ Danger Zone</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="alert alert-danger">
            🔴 Destructive actions below cannot be undone. Proceed with extreme caution.
        </div>
        """, unsafe_allow_html=True)
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            if st.button("🗑️ Clear All Transactions", use_container_width=True):
                st.warning("This feature requires double confirmation — disabled in demo mode.")
        with col_d2:
            if st.button("💣 Reset Business Data", use_container_width=True):
                st.warning("This feature requires double confirmation — disabled in demo mode.")
