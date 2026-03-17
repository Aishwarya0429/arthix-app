import streamlit as st
import pandas as pd
from utils.database import get_products, add_product, update_stock, get_inventory_logs


def show():
    bid = st.session_state.business_id

    st.markdown('<div class="page-title">📦 Inventory Management</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Track stock levels, COGS, and get low-stock alerts</div>',
                unsafe_allow_html=True)

    products = get_products(bid)

    # ── KPI strip ─────────────────────────────────────────────────────────────
    if products:
        total_items  = len(products)
        low_items    = sum(1 for p in products if 0 < p["stock"] <= p["low_stock_threshold"])
        out_items    = sum(1 for p in products if p["stock"] == 0)
        total_value  = sum(p["stock"] * p["cost_price"] for p in products)
        retail_value = sum(p["stock"] * p["sale_price"] for p in products)
        potential_profit = retail_value - total_value

        c1, c2, c3, c4, c5 = st.columns(5)
        for col, icon, label, val, color in [
            (c1, "📦", "Total Products",  total_items,  "#6C63FF"),
            (c2, "⚠️", "Low Stock",       low_items,    "#FFB347"),
            (c3, "🔴", "Out of Stock",    out_items,    "#FF6B6B"),
            (c4, "💰", "Inventory Value", f"₹{total_value:,.0f}", "#00D4AA"),
            (c5, "📈", "Potential Profit",f"₹{potential_profit:,.0f}", "#6C63FF"),
        ]:
            with col:
                st.markdown(f"""
                <div class="metric-card" style="border-top:3px solid {color}; padding:1rem;">
                    <span style="font-size:1.4rem;">{icon}</span>
                    <div class="metric-label">{label}</div>
                    <div class="metric-value" style="font-size:1.5rem;">{val}</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    tab_stock, tab_add, tab_adjust, tab_log = st.tabs([
        "  📋 Stock Overview  ", "  ➕ Add Product  ",
        "  🔄 Adjust Stock  ", "  📜 Movement Log  "
    ])

    # ── Stock Overview ─────────────────────────────────────────────────────────
    with tab_stock:
        if not products:
            st.info("No products yet. Add your first product!")
        else:
            df = pd.DataFrame(products)
            df["COGS"] = df["stock"] * df["cost_price"]
            df["Retail Value"] = df["stock"] * df["sale_price"]
            df["Margin %"] = ((df["sale_price"] - df["cost_price"]) / df["sale_price"] * 100).round(1)
            df["Status"] = df.apply(
                lambda r: "🔴 Out of Stock" if r["stock"] == 0
                else ("⚠️ Low Stock" if r["stock"] <= r["low_stock_threshold"] else "✅ In Stock"),
                axis=1
            )

            # Color-code for low stock
            st.markdown('<div class="card-title">Stock Levels</div>', unsafe_allow_html=True)

            # Progress bars per product
            for _, row in df.iterrows():
                col_name, col_prog, col_meta = st.columns([2, 3, 1])
                with col_name:
                    st.markdown(f"""
                    <div style="padding:0.3rem 0;">
                        <div style="font-weight:500; color:#F0F4FF; font-size:0.9rem;">{row['name']}</div>
                        <div style="color:#8892B0; font-size:0.75rem;">SKU: {row.get('sku','—')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_prog:
                    max_stock = max(row["stock"], row["low_stock_threshold"] * 2, 1)
                    pct = min(row["stock"] / max_stock, 1.0)
                    color = "#FF6B6B" if row["stock"] == 0 else ("#FFB347" if row["stock"] <= row["low_stock_threshold"] else "#00D4AA")
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;padding:0.4rem 0;">
                        <div style="flex:1;background:#1C2540;border-radius:10px;height:8px;overflow:hidden;">
                            <div style="width:{pct*100:.0f}%;height:100%;background:{color};border-radius:10px;transition:width 0.3s;"></div>
                        </div>
                        <span style="color:{color};font-weight:600;font-size:0.85rem;min-width:40px;">{row['stock']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                with col_meta:
                    st.markdown(f"""
                    <div style="font-size:0.8rem;color:#8892B0;padding:0.3rem 0;">
                        {row['Status'].split()[0]}
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("---")
            df_show = df[["name", "sku", "cost_price", "sale_price", "stock", "COGS", "Margin %", "Status"]].copy()
            df_show.columns = ["Product", "SKU", "Cost (₹)", "Sell (₹)", "Stock", "COGS (₹)", "Margin %", "Status"]
            df_show["COGS (₹)"] = df_show["COGS (₹)"].apply(lambda x: f"₹{x:,.2f}")
            df_show["Cost (₹)"] = df_show["Cost (₹)"].apply(lambda x: f"₹{x:.2f}")
            df_show["Sell (₹)"] = df_show["Sell (₹)"].apply(lambda x: f"₹{x:.2f}")
            st.dataframe(df_show, use_container_width=True, hide_index=True)

    # ── Add Product ────────────────────────────────────────────────────────────
    with tab_add:
        col_f, col_t = st.columns([1.4, 1])
        with col_f:
            with st.form("add_product_form", clear_on_submit=True):
                pname     = st.text_input("Product Name *", placeholder="e.g. Basmati Rice 5kg")
                sku       = st.text_input("SKU / Code", placeholder="e.g. RICE5KG")
                c1, c2   = st.columns(2)
                cost_p    = c1.number_input("Cost Price (₹)", min_value=0.0, format="%.2f")
                sale_p    = c2.number_input("Sale Price (₹)", min_value=0.0, format="%.2f")
                c3, c4   = st.columns(2)
                init_stock= c3.number_input("Initial Stock (units)", min_value=0, step=1)
                threshold = c4.number_input("Low Stock Alert at", min_value=1, value=10, step=1)
                submitted = st.form_submit_button("Add Product ✓", use_container_width=True, type="primary")

            if submitted:
                if not pname:
                    st.error("Product name is required.")
                elif sale_p <= cost_p:
                    st.warning("Sale price is less than or equal to cost price — check your margins!")
                    add_product(bid, pname, sku, cost_p, sale_p, init_stock, threshold)
                    st.success(f"✅ '{pname}' added to inventory!")
                else:
                    add_product(bid, pname, sku, cost_p, sale_p, init_stock, threshold)
                    margin = (sale_p - cost_p) / sale_p * 100
                    st.success(f"✅ '{pname}' added — Margin: {margin:.1f}%")

        with col_t:
            st.markdown("""
            <div class="card" style="margin-top:0.5rem;">
                <div class="card-title">📐 Pricing Guide</div>
                <div class="info-box">
                    Typical healthy retail margins range from <b>20–50%</b> depending on category.
                </div>
                <ul style="color:#8892B0; font-size:0.85rem; line-height:1.8;">
                    <li><b>SKU</b>: Short unique code for fast lookup</li>
                    <li><b>COGS</b> = Cost Price × Stock sold</li>
                    <li>Set realistic low-stock thresholds for alerts</li>
                    <li>Sale Price must cover all operating costs</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    # ── Adjust Stock ───────────────────────────────────────────────────────────
    with tab_adjust:
        if not products:
            st.info("No products to adjust.")
        else:
            prod_names = {p["name"]: p for p in products}
            sel_name   = st.selectbox("Select Product", list(prod_names.keys()))
            sel_prod   = prod_names[sel_name]

            st.markdown(f"""
            <div class="info-box">
                Current stock of <b>{sel_name}</b>:
                <span style="color:#00D4AA; font-size:1.1rem; font-weight:700;">{sel_prod['stock']} units</span>
            </div>
            """, unsafe_allow_html=True)

            with st.form("adjust_stock_form"):
                c1, c2 = st.columns(2)
                adj_type = c1.radio("Adjustment Type", ["Add Stock", "Remove Stock"], horizontal=True)
                qty      = c2.number_input("Quantity", min_value=1, step=1, value=1)
                reason   = st.selectbox("Reason", [
                    "Purchase / Restock", "Sale / Dispatch",
                    "Damage / Expiry", "Correction / Count",
                    "Return from Customer", "Other"
                ])
                notes    = st.text_input("Additional Notes (optional)")
                change   = qty if adj_type == "Add Stock" else -qty
                sub      = st.form_submit_button("Apply Adjustment ✓", use_container_width=True, type="primary")

            if sub:
                new_stock = sel_prod["stock"] + change
                if new_stock < 0:
                    st.error(f"Cannot remove {qty} units — only {sel_prod['stock']} in stock!")
                else:
                    update_stock(sel_prod["id"], change, f"{reason} | {notes}")
                    st.success(f"✅ Stock updated: {sel_prod['stock']} → {new_stock} units")
                    st.rerun()

    # ── Movement Log ───────────────────────────────────────────────────────────
    with tab_log:
        logs = get_inventory_logs(bid)
        if not logs:
            st.info("No inventory movements recorded yet.")
        else:
            df_log = pd.DataFrame(logs)[["logged_at", "product_name", "change", "reason"]]
            df_log["Direction"] = df_log["change"].apply(lambda x: "🟢 +In" if x > 0 else "🔴 -Out")
            df_log["change"]    = df_log["change"].apply(lambda x: f"+{x}" if x > 0 else str(x))
            df_log.columns = ["Timestamp", "Product", "Qty Change", "Reason", "Direction"]
            st.dataframe(df_log[["Timestamp", "Product", "Direction", "Qty Change", "Reason"]],
                         use_container_width=True, hide_index=True)
