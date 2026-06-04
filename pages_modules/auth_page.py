import streamlit as st
from utils.auth import login, register


def show():
    _, col, _ = st.columns([1, 1.4, 1])

    with col:
        # Logo
        st.markdown("""
        <div style="text-align:center; padding:2.5rem 0 1.5rem;">
            <div class="auth-logo-box">A</div>
            <div class="auth-logo">Arthix</div>
            <div class="auth-tagline">Money. Tracked. Mastered.</div>
        </div>
        """, unsafe_allow_html=True)

        tab_login, tab_reg = st.tabs(["Sign In", "Create Account"])

        # ── Sign In ───────────────────────────────────────────
        with tab_login:
            st.markdown("<div style='height:0.8rem'></div>",
                        unsafe_allow_html=True)

            with st.form("login_form"):
                email    = st.text_input("Email Address",
                                         placeholder="owner@mybusiness.com")
                password = st.text_input("Password", type="password",
                                         placeholder="Enter your password")
                submitted = st.form_submit_button(
                    "Sign In", use_container_width=True, type="primary")

            if submitted:
                if not email or not password:
                    st.error("Please enter both email and password.")
                else:
                    with st.spinner("Verifying credentials..."):
                        ok, msg = login(email, password)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

            st.markdown("""
            <div class="info-box" style="margin-top:1rem;">
                <b>Secured with JWT Authentication</b><br>
                Sessions protected by HS256 signed tokens with
                8-hour expiry and 7-day silent refresh.
                Passwords stored as SHA-256 hashes.
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="card" style="margin-top:12px;">
                <div class="card-title" style="font-size:12px; margin-bottom:8px;">
                    Demo Credentials
                </div>
                <div style="color:#64748b; font-size:12px; line-height:2;">
                    <b>Owner</b> &nbsp;
                    <code style="background:#f1f5f9; padding:2px 6px; border-radius:4px;">
                        owner@arthix.com
                    </code> /
                    <code style="background:#f1f5f9; padding:2px 6px; border-radius:4px;">
                        demo123
                    </code><br>
                    <b>Accountant</b> &nbsp;
                    <code style="background:#f1f5f9; padding:2px 6px; border-radius:4px;">
                        accountant@arthix.com
                    </code> /
                    <code style="background:#f1f5f9; padding:2px 6px; border-radius:4px;">
                        demo123
                    </code>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Create Account ────────────────────────────────────
        with tab_reg:
            st.markdown("<div style='height:0.8rem'></div>",
                        unsafe_allow_html=True)

            with st.form("register_form"):
                st.markdown(
                    '<div class="card-title" style="font-size:12px; color:#64748b; '
                    'text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px;">'
                    'Personal Details</div>',
                    unsafe_allow_html=True)
                r1, r2 = st.columns(2)
                name = r1.text_input("Full Name *",
                                     placeholder="Arjun Sharma")
                role = r2.selectbox("Your Role *",
                                    ["Owner", "Accountant", "Staff"])

                email_r = st.text_input("Email Address *",
                                        placeholder="you@email.com")
                p1, p2  = st.columns(2)
                pass_r  = p1.text_input("Password *", type="password",
                                         placeholder="Min 6 characters")
                pass_c  = p2.text_input("Confirm Password *", type="password",
                                         placeholder="Repeat password")

                st.markdown("<div style='height:0.5rem'></div>",
                            unsafe_allow_html=True)
                st.markdown(
                    '<div class="card-title" style="font-size:12px; color:#64748b; '
                    'text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px;">'
                    'Business Details</div>',
                    unsafe_allow_html=True)
                b1, b2   = st.columns(2)
                biz_name = b1.text_input("Business Name *",
                                          placeholder="My General Store")
                biz_cat  = b2.selectbox("Category *", [
                    "Retail", "Food & Beverage", "Services",
                    "Manufacturing", "E-Commerce", "Wholesale",
                    "Healthcare", "Education", "Other",
                ])

                submitted_r = st.form_submit_button(
                    "Create Account", use_container_width=True,
                    type="primary")

            if submitted_r:
                errors = []
                if not all([name, email_r, pass_r, pass_c, biz_name]):
                    errors.append("All fields marked * are required.")
                if pass_r and len(pass_r) < 6:
                    errors.append("Password must be at least 6 characters.")
                if pass_r and pass_c and pass_r != pass_c:
                    errors.append("Passwords do not match.")
                if errors:
                    for e in errors:
                        st.error(e)
                else:
                    with st.spinner("Creating your account..."):
                        ok, msg = register(name, email_r, pass_r,
                                           role, biz_name, biz_cat)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

            st.markdown("""
            <div class="info-box" style="margin-top:1rem;">
                Password is <b>SHA-256 hashed</b> before storage.
                A signed <b>JWT access token</b> is issued immediately
                after registration.
            </div>
            """, unsafe_allow_html=True)
