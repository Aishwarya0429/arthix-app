import streamlit as st
import pandas as pd
from datetime import date
from utils.database import get_transactions, get_businesses, get_products
from utils.forecasting import kpi_summary


def show():
    uid  = st.session_state.user_id
    bid  = st.session_state.business_id
    biz  = st.session_state.business_name

    st.markdown('<div class="page-title">👤 My Profile</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Account settings, business info & activity overview</div>',
                unsafe_allow_html=True)

    tab_profile, tab_biz, tab_activity = st.tabs([
        "  👤 Account  ", "  🏢 Business  ", "  📊 My Activity  "
    ])

    # ── Account ────────────────────────────────────────────────────────────────
    with tab_profile:
        col_info, col_edit = st.columns([1, 1.5])

        with col_info:
            initials = "".join([w[0].upper() for w in st.session_state.username.split()[:2]])
            st.markdown(f"""
            <div class="card" style="text-align:center; padding:2rem;">
                <div style="
                    width:80px; height:80px; border-radius:50%;
                    background:linear-gradient(135deg,#6C63FF,#00D4AA);
                    display:flex; align-items:center; justify-content:center;
                    margin:0 auto 1rem; font-size:2rem; font-weight:800;
                    color:white; font-family:'Syne',sans-serif;
                ">{initials}</div>
                <div style="font-family:'Syne',sans-serif; font-size:1.3rem; font-weight:700;
                            color:#F0F4FF; margin-bottom:0.3rem;">
                    {st.session_state.username}
                </div>
                <div class="role-badge" style="margin:0;">{st.session_state.role}</div>
                <div style="color:#8892B0; font-size:0.85rem; margin-top:1rem;">
                    📅 Member since {date.today().strftime('%B %Y')}
                </div>
                <div style="color:#8892B0; font-size:0.85rem;">
                    🏢 {biz}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_edit:
            st.markdown('<div class="card-title">Edit Profile</div>', unsafe_allow_html=True)
            with st.form("profile_form"):
                name  = st.text_input("Full Name", value=st.session_state.username)
                email = st.text_input("Email Address", placeholder="your@email.com")
                st.text_input("New Password", type="password", placeholder="Leave blank to keep current")
                st.text_input("Confirm Password", type="password", placeholder="Repeat new password")
                if st.form_submit_button("Update Profile", use_container_width=True, type="primary"):
                    st.success("✅ Profile updated successfully!")
                    if name:
                        st.session_state.username = name

    # ── Business ────────────────────────────────────────────────────────────────
    with tab_biz:
        businesses = get_businesses(uid)

        for biz_item in businesses:
            is_active = biz_item["id"] == bid
            border    = "border: 1px solid #6C63FF;" if is_active else ""
            st.markdown(f"""
            <div class="card" style="{border}">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div class="card-title" style="margin-bottom:0.2rem;">{biz_item['name']}</div>
                        <div style="color:#8892B0; font-size:0.82rem;">
                            {biz_item.get('category','—')} · {biz_item.get('currency','INR')}
                            · Created {biz_item.get('created_at','')[:10]}
                        </div>
                    </div>
                    {'<span class="badge badge-ok">Active</span>' if is_active else '<span class="badge">Other</span>'}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="card-title">Edit Business Info</div>', unsafe_allow_html=True)
        with st.form("biz_form"):
            c1, c2 = st.columns(2)
            bname = c1.text_input("Business Name", value=biz)
            bcat  = c2.selectbox("Category", [
                "Retail", "Food & Beverage", "Services", "Manufacturing",
                "E-Commerce", "Wholesale", "Healthcare", "Education", "Other"
            ])
            c3, c4 = st.columns(2)
            bcur  = c3.selectbox("Currency", ["INR", "USD", "EUR", "GBP"])
            btax  = c4.text_input("GST / Tax Number", placeholder="27XXXXX1234X1ZX")
            baddr = st.text_area("Business Address", placeholder="Shop No. 4, Market Lane...", height=80)
            if st.form_submit_button("Save Business Info", use_container_width=True, type="primary"):
                st.session_state.business_name = bname
                st.success("✅ Business info updated!")

    # ── Activity ────────────────────────────────────────────────────────────────
    with tab_activity:
        txns     = get_transactions(bid)
        products = get_products(bid)
        kpi      = kpi_summary(txns)

        if kpi:
            c1, c2, c3 = st.columns(3)
            for col, label, val, color in [
                (c1, "Total Transactions", kpi["txn_count"],       "#6C63FF"),
                (c2, "Total Revenue",      f"₹{kpi['total_income']:,.0f}", "#00D4AA"),
                (c3, "Products Tracked",   len(products),           "#FFB347"),
            ]:
                with col:
                    st.markdown(f"""
                    <div class="metric-card" style="border-top:3px solid {color}; padding:1rem;">
                        <div class="metric-label">{label}</div>
                        <div class="metric-value" style="font-size:1.5rem;">{val}</div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        if txns:
            df = pd.DataFrame(txns)
            df["txn_date"] = pd.to_datetime(df["txn_date"])
            df["month"]    = df["txn_date"].dt.to_period("M").astype(str)
            monthly = df.groupby(["month", "type"])["amount"].sum().unstack(fill_value=0).reset_index()

            st.markdown('<div class="card-title">Monthly Activity Summary</div>', unsafe_allow_html=True)
            if "Income" in monthly.columns:
                monthly["Profit"] = monthly.get("Income", 0) - monthly.get("Expense", 0)
            st.dataframe(monthly, use_container_width=True, hide_index=True)
