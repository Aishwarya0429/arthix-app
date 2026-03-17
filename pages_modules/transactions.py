import streamlit as st
import pandas as pd
from datetime import date, timedelta
from io import StringIO
from utils.database import (
    add_transaction, get_transactions,
    delete_transaction, update_transaction,
)

# ── Constants ─────────────────────────────────────────────────────────────────
INCOME_CATS = [
    "Product Sales", "Service Fees", "Online Sales",
    "Wholesale", "Consulting", "Rental Income", "Other Income",
]
EXPENSE_CATS = [
    "Rent", "Utilities", "Supplies", "Salaries", "Marketing",
    "Transport", "Maintenance", "Taxes", "Insurance", "Other Expense",
]
ALL_CATS = INCOME_CATS + EXPENSE_CATS

CSV_TEMPLATE = """date,type,category,amount,description
2026-03-01,Income,Product Sales,5000.00,Morning sales batch
2026-03-01,Expense,Supplies,800.00,Stationery and packaging
2026-03-02,Income,Online Sales,3200.00,Flipkart orders
2026-03-02,Expense,Transport,450.00,Delivery charges
"""

# ── Helpers ───────────────────────────────────────────────────────────────────
def _kpi_bar(txns: list) -> None:
    """Render 4 KPI cards above a transaction table."""
    if not txns:
        return
    df  = pd.DataFrame(txns)
    inc = df[df["type"] == "Income"]["amount"].sum()
    exp = df[df["type"] == "Expense"]["amount"].sum()
    pft = inc - exp

    c1, c2, c3, c4 = st.columns(4)
    for col, label, val, color, fmt in [
        (c1, "Total Income",   inc,       "#00D4AA", "₹{:,.2f}"),
        (c2, "Total Expenses", exp,       "#FF6B6B", "₹{:,.2f}"),
        (c3, "Net Profit",     pft,       "#6C63FF", "₹{:,.2f}"),
        (c4, "Transactions",   len(txns), "#FFB347", "{:,}"),
    ]:
        with col:
            st.markdown(
                f"""
                <div class="metric-card" style="border-top:3px solid {color}; padding:1rem 1.2rem;">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value" style="font-size:1.35rem;">{fmt.format(val)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)


def _display_table(txns: list) -> None:
    """Render a styled dataframe from a list of transaction dicts."""
    df = pd.DataFrame(txns)[["txn_date","type","category","amount","description"]].copy()
    df["amount"] = df["amount"].apply(lambda x: f"₹{x:,.2f}")
    df["type"]   = df["type"].apply(lambda t: "🟢 Income" if t == "Income" else "🔴 Expense")
    df.columns   = ["Date", "Type", "Category", "Amount", "Description"]
    st.dataframe(df, use_container_width=True, hide_index=True)


def _validate_csv_df(df: pd.DataFrame):
    """
    Validate a mapped CSV DataFrame.
    Returns (cleaned_df, errors_list).
    cleaned_df is None if there are blocking errors.
    """
    errors  = []
    cleaned = df.copy()

    # --- type validation ---
    valid_types = {"income", "expense"}
    bad_types   = cleaned[~cleaned["type"].str.lower().isin(valid_types)]
    if not bad_types.empty:
        errors.append(
            f"❌ **Type column** has {len(bad_types)} invalid value(s). "
            f"Allowed: Income, Expense. Found: {bad_types['type'].unique().tolist()[:5]}"
        )

    # --- amount validation ---
    cleaned["amount"] = pd.to_numeric(cleaned["amount"], errors="coerce")
    bad_amounts = cleaned["amount"].isna() | (cleaned["amount"] <= 0)
    if bad_amounts.any():
        errors.append(
            f"⚠️ **Amount column** has {bad_amounts.sum()} row(s) with missing or zero values — "
            f"these will be skipped."
        )
        cleaned = cleaned[~bad_amounts]

    # --- date validation ---
    parsed_dates = pd.to_datetime(cleaned["date"], errors="coerce", format="mixed")
    bad_dates = parsed_dates.isna()
    if bad_dates.any():
        errors.append(
            f"⚠️ **Date column** has {bad_dates.sum()} unparseable row(s) — these will be skipped."
        )
        cleaned = cleaned[~bad_dates]
        parsed_dates = parsed_dates[~bad_dates]

    cleaned["date"] = parsed_dates.dt.strftime("%Y-%m-%d")

    # --- normalise type casing ---
    cleaned["type"] = cleaned["type"].str.strip().str.capitalize()
    cleaned = cleaned[cleaned["type"].isin(["Income", "Expense"])]

    # --- category fallback ---
    if "category" not in cleaned.columns or cleaned["category"].isna().all():
        cleaned["category"] = cleaned["type"].map(
            {"Income": "Other Income", "Expense": "Other Expense"}
        )
    else:
        cleaned["category"] = cleaned["category"].fillna(
            cleaned["type"].map({"Income": "Other Income", "Expense": "Other Expense"})
        )

    # --- description fallback ---
    if "description" not in cleaned.columns:
        cleaned["description"] = ""
    else:
        cleaned["description"] = cleaned["description"].fillna("").astype(str)

    if cleaned.empty:
        errors.append("❌ No valid rows remain after validation. Please fix your file.")
        return None, errors

    return cleaned, errors


# ── Main page ─────────────────────────────────────────────────────────────────
def show():
    bid = st.session_state.business_id

    st.markdown('<div class="page-title">💳 Transactions</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">'
        "Log manually, bulk-upload via CSV, manage & analyse all business transactions"
        "</div>",
        unsafe_allow_html=True,
    )

    tab_all, tab_manual, tab_csv, tab_edit = st.tabs([
        "  📋 All Transactions  ",
        "  ✏️ Add Manually  ",
        "  📂 Upload CSV  ",
        "  🔧 Edit / Delete  ",
    ])

    # ══════════════════════════════════════════════════════════════
    # TAB 1 — ALL TRANSACTIONS
    # ══════════════════════════════════════════════════════════════
    with tab_all:
        st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

        # Filters
        with st.expander("🔍  Filter Transactions", expanded=True):
            f1, f2, f3, f4 = st.columns(4)
            start_date  = f1.date_input("From",  value=date.today() - timedelta(days=30))
            end_date    = f2.date_input("To",    value=date.today())
            type_filter = f3.selectbox("Type",   ["All", "Income", "Expense"])
            search_term = f4.text_input("Search", placeholder="keyword in description/category…")

        txn_type = None if type_filter == "All" else type_filter
        txns = get_transactions(bid, str(start_date), str(end_date), txn_type)

        if search_term:
            q    = search_term.lower()
            txns = [t for t in txns
                    if q in (t.get("description") or "").lower()
                    or q in (t.get("category") or "").lower()]

        if txns:
            _kpi_bar(txns)
            _display_table(txns)

            # Export
            csv_bytes = pd.DataFrame(txns).to_csv(index=False).encode()
            st.download_button(
                "⬇️  Export Filtered Transactions as CSV",
                csv_bytes,
                f"transactions_{start_date}_{end_date}.csv",
                "text/csv",
                use_container_width=False,
            )
        else:
            st.markdown(
                '<div class="alert alert-info">'
                'ℹ️ No transactions found for the selected filters.'
                "</div>",
                unsafe_allow_html=True,
            )

    # ══════════════════════════════════════════════════════════════
    # TAB 2 — ADD MANUALLY
    # ══════════════════════════════════════════════════════════════
    with tab_manual:
        st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

        left, right = st.columns([1.6, 1])

        with left:
            st.markdown('<div class="section-title">New Transaction</div>', unsafe_allow_html=True)

            with st.form("manual_txn_form", clear_on_submit=True):
                # Type selector
                txn_type_m = st.radio(
                    "Transaction Type",
                    ["Income", "Expense"],
                    horizontal=True,
                )

                cats = INCOME_CATS if txn_type_m == "Income" else EXPENSE_CATS

                r1c1, r1c2 = st.columns(2)
                category = r1c1.selectbox("Category", cats)
                amount   = r1c2.number_input(
                    "Amount (₹)",
                    min_value=0.01, step=1.0, format="%.2f",
                )

                txn_date    = st.date_input("Transaction Date", value=date.today())
                description = st.text_area(
                    "Description / Notes  (optional)",
                    placeholder="e.g. Morning counter sales, Electricity bill for March…",
                    height=85,
                )

                submitted = st.form_submit_button(
                    "✓  Add Transaction",
                    use_container_width=True,
                    type="primary",
                )

            if submitted:
                if amount <= 0:
                    st.error("Amount must be greater than ₹0.")
                else:
                    add_transaction(bid, txn_type_m, category, amount, description, str(txn_date))
                    st.success(
                        f"✅ **{txn_type_m}** of ₹{amount:,.2f} added under *{category}* "
                        f"for {txn_date.strftime('%d %b %Y')}."
                    )

        with right:
            st.markdown('<div class="section-title">Quick Tips</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="info-box">
                Log transactions <strong>daily</strong> for accurate profit tracking
                and better AI forecasting results.
            </div>

            <div class="card" style="padding:1rem 1.2rem;">
                <div class="card-title">Income Categories</div>
                <ul style="color:var(--text-secondary);font-size:0.82rem;
                           line-height:2;margin:0;padding-left:1rem;">
                    <li><b>Product Sales</b> — Counter / in-store revenue</li>
                    <li><b>Online Sales</b> — Amazon, Flipkart, website</li>
                    <li><b>Service Fees</b> — Repair, consultation charges</li>
                    <li><b>Wholesale</b> — Bulk orders to retailers</li>
                </ul>
            </div>

            <div class="card" style="padding:1rem 1.2rem; margin-top:0.8rem;">
                <div class="card-title">Expense Categories</div>
                <ul style="color:var(--text-secondary);font-size:0.82rem;
                           line-height:2;margin:0;padding-left:1rem;">
                    <li><b>Supplies</b> — Raw material / packaging</li>
                    <li><b>Salaries</b> — Staff wages, contractor fees</li>
                    <li><b>Marketing</b> — Ads, pamphlets, promotions</li>
                    <li><b>Utilities</b> — Electricity, water, internet</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # TAB 3 — CSV UPLOAD
    # ══════════════════════════════════════════════════════════════
    with tab_csv:
        st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

        # ── Step 0: Download template ──────────────────────────────
        st.markdown('<div class="section-title">Step 1 — Download Template (optional)</div>',
                    unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box">
            Your CSV must have these columns (in any order):
            <strong>date</strong>, <strong>type</strong> (Income / Expense),
            <strong>amount</strong>. Optional: <strong>category</strong>,
            <strong>description</strong>.
        </div>
        """, unsafe_allow_html=True)

        dl_col, _ = st.columns([1, 2])
        with dl_col:
            st.download_button(
                "⬇️  Download CSV Template",
                CSV_TEMPLATE,
                "arthix_template.csv",
                "text/csv",
                use_container_width=True,
            )

        st.markdown("---")

        # ── Step 1: Upload ─────────────────────────────────────────
        st.markdown('<div class="section-title">Step 2 — Upload Your CSV File</div>',
                    unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "Drag & drop or click to browse",
            type=["csv"],
            label_visibility="collapsed",
        )

        if uploaded is None:
            st.markdown("""
            <div style="text-align:center; padding:2rem 1rem; color:var(--text-secondary);
                        font-size:0.85rem;">
                📂 &nbsp; Upload a <code>.csv</code> file to begin bulk import
            </div>
            """, unsafe_allow_html=True)
            st.stop()

        # ── Parse the file ─────────────────────────────────────────
        try:
            raw_df = pd.read_csv(uploaded)
        except Exception as e:
            st.error(f"❌ Could not read the file: {e}")
            st.stop()

        # Normalise column names
        raw_df.columns = [c.strip().lower().replace(" ", "_") for c in raw_df.columns]

        st.markdown("---")

        # ── Step 2: Column Mapping ─────────────────────────────────
        st.markdown('<div class="section-title">Step 3 — Map Your Columns</div>',
                    unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box">
            Match each required Arthix field to a column in your uploaded file.
            If your file already uses the standard names they'll be auto-selected.
        </div>
        """, unsafe_allow_html=True)

        available_cols = ["— not in file —"] + list(raw_df.columns)

        def _auto(name):
            return name if name in raw_df.columns else "— not in file —"

        st.markdown('<div class="col-map-panel">', unsafe_allow_html=True)
        st.markdown('<div class="col-map-label">Required fields</div>', unsafe_allow_html=True)
        mp1, mp2, mp3 = st.columns(3)
        col_date   = mp1.selectbox("📅 Date column *",   available_cols, index=available_cols.index(_auto("date")))
        col_type   = mp2.selectbox("🔄 Type column *",   available_cols, index=available_cols.index(_auto("type")))
        col_amount = mp3.selectbox("💰 Amount column *", available_cols, index=available_cols.index(_auto("amount")))

        st.markdown('<div class="col-map-label" style="margin-top:0.8rem;">Optional fields</div>',
                    unsafe_allow_html=True)
        op1, op2 = st.columns(2)
        col_cat  = op1.selectbox("🏷️  Category column", available_cols, index=available_cols.index(_auto("category")))
        col_desc = op2.selectbox("📝 Description column", available_cols, index=available_cols.index(_auto("description")))
        st.markdown("</div>", unsafe_allow_html=True)

        # Check required columns are mapped
        missing_req = [n for n, v in [("date", col_date), ("type", col_type), ("amount", col_amount)]
                       if v == "— not in file —"]
        if missing_req:
            st.error(f"❌ Please map the required column(s): **{', '.join(missing_req)}**")
            st.stop()

        # Build working df
        mapped: dict = {"date": col_date, "type": col_type, "amount": col_amount}
        if col_cat  != "— not in file —": mapped["category"]    = col_cat
        if col_desc != "— not in file —": mapped["description"]  = col_desc

        work_df = raw_df[[v for v in mapped.values()]].rename(
            columns={v: k for k, v in mapped.items()}
        )

        st.markdown("---")

        # ── Step 3: Validate & Preview ─────────────────────────────
        st.markdown('<div class="section-title">Step 4 — Preview & Validate</div>',
                    unsafe_allow_html=True)

        clean_df, val_errors = _validate_csv_df(work_df)

        # Show validation messages
        for msg in val_errors:
            if msg.startswith("❌"):
                st.error(msg)
            else:
                st.warning(msg)

        if clean_df is None:
            st.stop()

        # Stats row
        n_income  = (clean_df["type"] == "Income").sum()
        n_expense = (clean_df["type"] == "Expense").sum()
        total_inc = clean_df[clean_df["type"] == "Income"]["amount"].sum()
        total_exp = clean_df[clean_df["type"] == "Expense"].get("amount", pd.Series(dtype=float)).sum()

        st.markdown(f"""
        <div class="csv-stats-row">
            <div class="csv-stat-pill">📄 <strong>{len(clean_df)}</strong> valid rows</div>
            <div class="csv-stat-pill">🟢 <strong>{n_income}</strong> income entries</div>
            <div class="csv-stat-pill">🔴 <strong>{n_expense}</strong> expense entries</div>
            <div class="csv-stat-pill">💰 Net: <strong>₹{total_inc - total_exp:,.2f}</strong></div>
        </div>
        """, unsafe_allow_html=True)

        # Data preview (first 10 rows)
        preview = clean_df.head(10).copy()
        preview["amount"] = preview["amount"].apply(lambda x: f"₹{x:,.2f}")
        st.markdown('<div class="card-title">Preview (first 10 rows)</div>', unsafe_allow_html=True)
        st.dataframe(preview, use_container_width=True, hide_index=True)

        if len(clean_df) > 10:
            st.caption(f"… and {len(clean_df) - 10} more rows not shown")

        st.markdown("---")

        # ── Step 4: Import ─────────────────────────────────────────
        st.markdown('<div class="section-title">Step 5 — Import to Database</div>',
                    unsafe_allow_html=True)

        imp1, imp2 = st.columns([2, 1])
        with imp1:
            st.markdown(f"""
            <div class="alert alert-info">
                ℹ️ This will add <strong>{len(clean_df)} transactions</strong> to
                <em>{st.session_state.business_name}</em>.
                Duplicate entries are <strong>not</strong> auto-detected — 
                make sure you haven't uploaded this file before.
            </div>
            """, unsafe_allow_html=True)

        with imp2:
            do_import = st.button(
                f"🚀  Import {len(clean_df)} Transactions",
                use_container_width=True,
                type="primary",
            )

        if do_import:
            progress = st.progress(0, text="Importing…")
            errors_during: list[str] = []
            ok_count = 0

            for i, row in clean_df.iterrows():
                try:
                    cat = row.get("category", "") or (
                        "Other Income" if row["type"] == "Income" else "Other Expense"
                    )
                    desc = row.get("description", "") or ""
                    add_transaction(
                        bid,
                        row["type"],
                        cat,
                        float(row["amount"]),
                        str(desc),
                        str(row["date"]),
                    )
                    ok_count += 1
                except Exception as e:
                    errors_during.append(f"Row {i+1}: {e}")

                progress.progress((ok_count + len(errors_during)) / len(clean_df),
                                  text=f"Imported {ok_count} / {len(clean_df)}…")

            progress.empty()

            if errors_during:
                st.warning(
                    f"⚠️ Import finished with {len(errors_during)} error(s):\n"
                    + "\n".join(errors_during[:5])
                )

            if ok_count:
                st.success(
                    f"✅ Successfully imported **{ok_count} transactions** "
                    f"into *{st.session_state.business_name}*!"
                )
                st.balloons()

    # ══════════════════════════════════════════════════════════════
    # TAB 4 — EDIT / DELETE
    # ══════════════════════════════════════════════════════════════
    with tab_edit:
        st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

        all_txns = get_transactions(bid)
        if not all_txns:
            st.info("No transactions yet. Add some first.")
            return

        st.markdown('<div class="section-title">Select a Transaction</div>',
                    unsafe_allow_html=True)

        options = {
            f"#{t['id']}  ·  {t['txn_date']}  ·  {t['type']}  ·  "
            f"₹{t['amount']:,.2f}  ·  {t['category']}": t
            for t in all_txns[:60]
        }
        sel_label = st.selectbox("Transaction", list(options.keys()),
                                 label_visibility="collapsed")
        sel = options[sel_label]

        st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

        edit_col, del_col = st.columns([2.2, 1])

        # ── Edit form ──────────────────────────────────────────────
        with edit_col:
            st.markdown('<div class="section-title">Edit Details</div>',
                        unsafe_allow_html=True)

            with st.form("edit_txn_form"):
                cats_e  = INCOME_CATS if sel["type"] == "Income" else EXPENSE_CATS
                cat_idx = cats_e.index(sel["category"]) if sel["category"] in cats_e else 0

                ec1, ec2 = st.columns(2)
                new_cat    = ec1.selectbox("Category", cats_e, index=cat_idx)
                new_amount = ec2.number_input(
                    "Amount (₹)",
                    value=float(sel["amount"]),
                    min_value=0.01,
                    format="%.2f",
                )
                new_date = st.date_input(
                    "Date",
                    value=pd.to_datetime(sel["txn_date"]),
                )
                new_desc = st.text_area(
                    "Description",
                    value=sel.get("description") or "",
                    height=80,
                )
                if st.form_submit_button("💾  Save Changes",
                                         use_container_width=True, type="primary"):
                    update_transaction(
                        sel["id"], new_cat, new_amount, new_desc, str(new_date)
                    )
                    st.success("✅ Transaction updated successfully!")
                    st.rerun()

        # ── Delete panel ───────────────────────────────────────────
        with del_col:
            st.markdown('<div class="section-title">Danger Zone</div>',
                        unsafe_allow_html=True)
            st.markdown(f"""
            <div class="card" style="
                background: var(--danger-bg);
                border-color: var(--danger-border);
                padding: 1rem 1.1rem;
            ">
                <div class="card-title" style="color:var(--danger);">⚠️ Delete Transaction</div>
                <p style="color:var(--text-secondary); font-size:0.82rem; line-height:1.55; margin:0;">
                    This will <strong>permanently remove</strong>
                    transaction <strong>#{sel['id']}</strong>
                    (₹{sel['amount']:,.2f} on {sel['txn_date']}).
                    This action cannot be undone.
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

            if "confirm_delete" not in st.session_state:
                st.session_state.confirm_delete = False

            if not st.session_state.confirm_delete:
                if st.button("🗑️  Delete Transaction",
                             use_container_width=True):
                    st.session_state.confirm_delete = True
                    st.rerun()
            else:
                st.warning("Are you sure? This cannot be undone.")
                y_col, n_col = st.columns(2)
                if y_col.button("✅ Yes, Delete", use_container_width=True, type="primary"):
                    delete_transaction(sel["id"])
                    st.session_state.confirm_delete = False
                    st.success("Deleted.")
                    st.rerun()
                if n_col.button("❌ Cancel", use_container_width=True):
                    st.session_state.confirm_delete = False
                    st.rerun()
