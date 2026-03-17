import streamlit as st
from utils.auth import login, register


def show():
    _, col, _ = st.columns([1, 1.5, 1])

    with col:
        st.markdown("""
        <div style="text-align:center; padding:2rem 0 0.5rem;">
            <div style="font-size:3rem; margin-bottom:0.3rem;">📊</div>
            <div class="auth-logo">Arthix</div>
            <div class="auth-tagline">Money. Tracked. Mastered.</div>
        </div>
        """, unsafe_allow_html=True)

        tab_login, tab_reg = st.tabs(["  🔐 Sign In  ", "  📝 Create Account  "])

        # ── Sign In ───────────────────────────────────────────
        with tab_login:
            st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

            with st.form("login_form"):
                email    = st.text_input("Email Address",
                                         placeholder="owner@mybusiness.com")
                password = st.text_input("Password", type="password",
                                         placeholder="••••••••")
                submitted = st.form_submit_button(
                    "Sign In →", use_container_width=True, type="primary")

            if submitted:
                if not email or not password:
                    st.error("Please enter both email and password.")
                else:
                    with st.spinner("Verifying credentials & generating JWT…"):
                        ok, msg = login(email, password)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

            # JWT info
            st.markdown("""
            <div class="info-box" style="margin-top:1rem;">
                🔒 <b>Secured with JWT Authentication</b><br>
                Your session is protected by a signed JSON Web Token (HS256)
                with <b>8-hour expiry</b> and automatic silent refresh for 7 days.
                Passwords stored as <b>SHA-256 hashes</b> — never plain text.
            </div>
            """, unsafe_allow_html=True)

            # Demo credentials
            st.markdown("""
            <div class="card" style="padding:0.9rem 1.1rem;">
                <div class="card-title" style="font-size:0.82rem;">🧪 Demo Credentials</div>
                <div style="color:var(--text-secondary);font-size:0.80rem;line-height:2;">
                    <b>Owner</b> →
                    <code>owner@arthix.com</code> / <code>demo123</code><br>
                    <b>Accountant</b> →
                    <code>accountant@arthix.com</code> / <code>demo123</code>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Create Account ────────────────────────────────────
        with tab_reg:
            st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

            with st.form("register_form"):
                st.markdown('<div class="card-title">Personal Details</div>',
                            unsafe_allow_html=True)
                r1, r2 = st.columns(2)
                name = r1.text_input("Full Name *",   placeholder="Arjun Sharma")
                role = r2.selectbox("Your Role *",    ["Owner", "Accountant", "Staff"])

                email_r = st.text_input("Email Address *", placeholder="you@email.com")

                p1, p2 = st.columns(2)
                pass_r = p1.text_input("Password *", type="password",
                                        placeholder="Min 6 characters")
                pass_c = p2.text_input("Confirm Password *", type="password",
                                        placeholder="Repeat password")

                st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)
                st.markdown('<div class="card-title">Business Details</div>',
                            unsafe_allow_html=True)
                b1, b2 = st.columns(2)
                biz_name = b1.text_input("Business Name *",
                                          placeholder="My General Store")
                biz_cat  = b2.selectbox("Category *", [
                    "Retail", "Food & Beverage", "Services",
                    "Manufacturing", "E-Commerce", "Wholesale",
                    "Healthcare", "Education", "Other",
                ])

                submitted_r = st.form_submit_button(
                    "Create Account & Sign In →",
                    use_container_width=True, type="primary")

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
                    with st.spinner("Creating account & issuing JWT…"):
                        ok, msg = register(name, email_r, pass_r,
                                           role, biz_name, biz_cat)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

            st.markdown("""
            <div class="info-box" style="margin-top:0.8rem;">
                🔒 Password is <b>SHA-256 hashed</b> before storage.
                A signed <b>JWT access token (HS256)</b> is issued immediately
                after registration — no separate login step needed.
            </div>
            """, unsafe_allow_html=True)
