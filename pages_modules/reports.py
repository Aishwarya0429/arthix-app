import streamlit as st
import pandas as pd
import io
from datetime import date, timedelta
from utils.database import get_transactions, get_products, get_daily_summary, get_category_summary
from utils.forecasting import kpi_summary


def _generate_pdf(bid, biz_name, start, end):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    Table, TableStyle, HRFlowable)
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    PURPLE  = colors.HexColor("#6C63FF")
    TEAL    = colors.HexColor("#00D4AA")
    RED     = colors.HexColor("#FF6B6B")
    DARK    = colors.HexColor("#0A0E1A")
    DGRAY   = colors.HexColor("#1C2540")
    LGRAY   = colors.HexColor("#8892B0")
    WHITE   = colors.white

    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("h1", fontSize=22, textColor=PURPLE,
                         fontName="Helvetica-Bold", spaceAfter=4, alignment=TA_CENTER)
    h2 = ParagraphStyle("h2", fontSize=14, textColor=DARK,
                         fontName="Helvetica-Bold", spaceAfter=6, spaceBefore=14)
    body = ParagraphStyle("body", fontSize=10, textColor=colors.HexColor("#333333"),
                           fontName="Helvetica", leading=14)
    sub  = ParagraphStyle("sub", fontSize=9, textColor=LGRAY,
                           fontName="Helvetica", alignment=TA_CENTER)

    txns = get_transactions(bid, str(start), str(end))
    kpi  = kpi_summary(get_transactions(bid))
    inc_cat, exp_cat = get_category_summary(bid)

    df = pd.DataFrame(txns) if txns else pd.DataFrame()
    total_inc = df[df["type"] == "Income"]["amount"].sum() if not df.empty else 0
    total_exp = df[df["type"] == "Expense"]["amount"].sum() if not df.empty else 0
    net_profit = total_inc - total_exp
    margin     = (net_profit / total_inc * 100) if total_inc > 0 else 0

    story = []

    # Header
    story.append(Paragraph("📊 Arthix Analytics", h1))
    story.append(Paragraph(f"Business Report — {biz_name}", sub))
    story.append(Paragraph(f"Period: {start.strftime('%d %b %Y')} to {end.strftime('%d %b %Y')}", sub))
    story.append(Spacer(1, 0.4*cm))
    story.append(HRFlowable(width="100%", thickness=2, color=PURPLE))
    story.append(Spacer(1, 0.4*cm))

    # KPI Summary Table
    story.append(Paragraph("Executive Summary", h2))
    kpi_data = [
        ["Metric", "Value"],
        ["Total Revenue",  f"INR {total_inc:,.2f}"],
        ["Total Expenses", f"INR {total_exp:,.2f}"],
        ["Net Profit",     f"INR {net_profit:,.2f}"],
        ["Profit Margin",  f"{margin:.1f}%"],
        ["Transactions",   str(len(df))],
    ]
    kpi_table = Table(kpi_data, colWidths=[9*cm, 8*cm])
    kpi_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), PURPLE),
        ("TEXTCOLOR",    (0,0), (-1,0), WHITE),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,0), 11),
        ("ALIGN",        (0,0), (-1,-1), "LEFT"),
        ("FONTSIZE",     (0,1), (-1,-1), 10),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#F9F9FF"), WHITE]),
        ("GRID",         (0,0), (-1,-1), 0.5, colors.HexColor("#E0E0E0")),
        ("LEFTPADDING",  (0,0), (-1,-1), 12),
        ("RIGHTPADDING", (0,0), (-1,-1), 12),
        ("TOPPADDING",   (0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0), (-1,-1), 8),
        ("TEXTCOLOR",    (1,3), (1,3), TEAL if net_profit >= 0 else RED),
        ("FONTNAME",     (1,3), (1,3), "Helvetica-Bold"),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 0.6*cm))

    # Category breakdown
    if not inc_cat.empty:
        story.append(Paragraph("Income by Category", h2))
        inc_data = [["Category", "Amount (INR)", "Share %"]]
        for _, row in inc_cat.sort_values("amount", ascending=False).iterrows():
            share = row["amount"] / total_inc * 100 if total_inc else 0
            inc_data.append([row["category"], f"{row['amount']:,.2f}", f"{share:.1f}%"])
        t = Table(inc_data, colWidths=[9*cm, 5*cm, 3*cm])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,0), TEAL),
            ("TEXTCOLOR",     (0,0), (-1,0), WHITE),
            ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE",      (0,0), (-1,-1), 9),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#F0FFF8"), WHITE]),
            ("GRID",          (0,0), (-1,-1), 0.5, colors.HexColor("#E0E0E0")),
            ("LEFTPADDING",   (0,0), (-1,-1), 10),
            ("TOPPADDING",    (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ]))
        story.append(t)
        story.append(Spacer(1, 0.6*cm))

    if not exp_cat.empty:
        story.append(Paragraph("Expense by Category", h2))
        exp_data = [["Category", "Amount (INR)", "Share %"]]
        for _, row in exp_cat.sort_values("amount", ascending=False).iterrows():
            share = row["amount"] / total_exp * 100 if total_exp else 0
            exp_data.append([row["category"], f"{row['amount']:,.2f}", f"{share:.1f}%"])
        t2 = Table(exp_data, colWidths=[9*cm, 5*cm, 3*cm])
        t2.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,0), RED),
            ("TEXTCOLOR",     (0,0), (-1,0), WHITE),
            ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE",      (0,0), (-1,-1), 9),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#FFF5F5"), WHITE]),
            ("GRID",          (0,0), (-1,-1), 0.5, colors.HexColor("#E0E0E0")),
            ("LEFTPADDING",   (0,0), (-1,-1), 10),
            ("TOPPADDING",    (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ]))
        story.append(t2)
        story.append(Spacer(1, 0.6*cm))

    # Transaction log
    if not df.empty:
        story.append(Paragraph("Transaction Log", h2))
        txn_data = [["Date", "Type", "Category", "Amount (INR)", "Notes"]]
        for _, row in df.sort_values("txn_date", ascending=False).head(30).iterrows():
            txn_data.append([
                row["txn_date"],
                row["type"],
                row.get("category", ""),
                f"{row['amount']:,.2f}",
                (row.get("description") or "")[:40],
            ])
        t3 = Table(txn_data, colWidths=[3*cm, 2.5*cm, 3.5*cm, 4*cm, 4*cm])
        t3.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,0), DGRAY),
            ("TEXTCOLOR",     (0,0), (-1,0), WHITE),
            ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE",      (0,0), (-1,-1), 8),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#FAFAFA"), WHITE]),
            ("GRID",          (0,0), (-1,-1), 0.3, colors.HexColor("#E8E8E8")),
            ("LEFTPADDING",   (0,0), (-1,-1), 6),
            ("TOPPADDING",    (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ]))
        story.append(t3)

    # Footer
    story.append(Spacer(1, 0.8*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=PURPLE))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        f"Generated by Arthix on {date.today().strftime('%d %B %Y')} · Confidential Business Report",
        sub
    ))

    doc.build(story)
    buf.seek(0)
    return buf.getvalue()


def _generate_excel(bid, biz_name, start, end):
    txns     = get_transactions(bid, str(start), str(end))
    products = get_products(bid)
    inc_cat, exp_cat = get_category_summary(bid)

    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        # Transactions sheet
        if txns:
            df = pd.DataFrame(txns)[["txn_date", "type", "category", "amount", "description"]]
            df.columns = ["Date", "Type", "Category", "Amount (INR)", "Notes"]
            df.to_excel(writer, sheet_name="Transactions", index=False)

        # Summary sheet
        if txns:
            df_all = pd.DataFrame(txns)
            inc = df_all[df_all["type"] == "Income"]["amount"].sum()
            exp = df_all[df_all["type"] == "Expense"]["amount"].sum()
            summary = pd.DataFrame([
                {"Metric": "Business Name", "Value": biz_name},
                {"Metric": "Report Period", "Value": f"{start} to {end}"},
                {"Metric": "Total Revenue", "Value": inc},
                {"Metric": "Total Expenses", "Value": exp},
                {"Metric": "Net Profit", "Value": inc - exp},
                {"Metric": "Profit Margin %", "Value": f"{(inc-exp)/inc*100:.1f}%" if inc else "N/A"},
                {"Metric": "Total Transactions", "Value": len(df_all)},
            ])
            summary.to_excel(writer, sheet_name="Summary", index=False)

        # Income Categories
        if not inc_cat.empty:
            inc_cat.to_excel(writer, sheet_name="Income by Category", index=False)

        # Expense Categories
        if not exp_cat.empty:
            exp_cat.to_excel(writer, sheet_name="Expenses by Category", index=False)

        # Inventory
        if products:
            df_prod = pd.DataFrame(products)[["name", "sku", "cost_price", "sale_price", "stock"]]
            df_prod["COGS"] = df_prod["stock"] * df_prod["cost_price"]
            df_prod["Retail Value"] = df_prod["stock"] * df_prod["sale_price"]
            df_prod.columns = ["Product", "SKU", "Cost Price", "Sale Price", "Stock", "COGS", "Retail Value"]
            df_prod.to_excel(writer, sheet_name="Inventory", index=False)

    buf.seek(0)
    return buf.getvalue()


def show():
    bid  = st.session_state.business_id
    biz  = st.session_state.business_name

    st.markdown('<div class="page-title">📄 Reports & Export</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Generate professional PDF or Excel reports for any period</div>',
                unsafe_allow_html=True)

    # ── Date range ─────────────────────────────────────────────────────────────
    col_r1, col_r2, col_r3 = st.columns([1, 1, 2])
    with col_r1:
        quick = st.selectbox("Quick Period", [
            "Custom", "This Month", "Last Month", "Last 30 Days",
            "Last 90 Days", "This Year"
        ])
    today = date.today()
    if quick == "This Month":
        start = today.replace(day=1); end = today
    elif quick == "Last Month":
        first_this = today.replace(day=1)
        end   = first_this - timedelta(days=1)
        start = end.replace(day=1)
    elif quick == "Last 30 Days":
        start = today - timedelta(days=30); end = today
    elif quick == "Last 90 Days":
        start = today - timedelta(days=90); end = today
    elif quick == "This Year":
        start = today.replace(month=1, day=1); end = today
    else:
        with col_r2:
            start = st.date_input("From", value=today - timedelta(days=30))
        with col_r3:
            end   = st.date_input("To",   value=today)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ── Preview ────────────────────────────────────────────────────────────────
    txns = get_transactions(bid, str(start), str(end))
    kpi  = kpi_summary(txns) if txns else {}

    if kpi:
        c1, c2, c3, c4 = st.columns(4)
        for col, label, val, color in [
            (c1, "Revenue",      kpi.get("total_income", 0),  "#00D4AA"),
            (c2, "Expenses",     kpi.get("total_expense", 0), "#FF6B6B"),
            (c3, "Net Profit",   kpi.get("total_profit", 0),  "#6C63FF"),
            (c4, "Transactions", kpi.get("txn_count", 0),     "#FFB347"),
        ]:
            with col:
                disp = str(int(val)) if "Trans" in label else f"₹{val:,.2f}"
                st.markdown(f"""
                <div class="metric-card" style="border-top:3px solid {color}; padding:1rem;">
                    <div class="metric-label">{label} (selected period)</div>
                    <div class="metric-value" style="font-size:1.4rem;">{disp}</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    # ── Download buttons ───────────────────────────────────────────────────────
    col_pdf, col_xl = st.columns(2)

    with col_pdf:
        st.markdown("""
        <div class="card">
            <div class="card-title">📕 PDF Report</div>
            <div class="info-box">
                Professional branded PDF with executive summary, category analysis,
                and full transaction log. Ready to share with stakeholders.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⬇️ Generate & Download PDF", use_container_width=True, type="primary"):
            with st.spinner("Generating PDF report..."):
                pdf_bytes = _generate_pdf(bid, biz, start, end)
            fname = f"Arthix_{biz.replace(' ','_')}_{start}_{end}.pdf"
            st.download_button("📥 Download PDF", pdf_bytes, fname, "application/pdf",
                               use_container_width=True)

    with col_xl:
        st.markdown("""
        <div class="card">
            <div class="card-title">📗 Excel Workbook</div>
            <div class="info-box">
                Multi-sheet Excel file including Transactions, Summary, Category Breakdowns,
                and Inventory — ready for further analysis.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⬇️ Generate & Download Excel", use_container_width=True, type="primary"):
            with st.spinner("Building Excel workbook..."):
                xl_bytes = _generate_excel(bid, biz, start, end)
            fname = f"Arthix_{biz.replace(' ','_')}_{start}_{end}.xlsx"
            st.download_button("📥 Download Excel", xl_bytes, fname,
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               use_container_width=True)

    # ── Report history simulation ─────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="card-title">📜 Recent Reports Generated</div>', unsafe_allow_html=True)
    recent_reports = [
        {"Type": "PDF", "Period": "Feb 2026", "Generated": "2026-03-01 09:15", "Size": "248 KB"},
        {"Type": "Excel", "Period": "Jan 2026", "Generated": "2026-02-01 10:32", "Size": "186 KB"},
        {"Type": "PDF", "Period": "Q4 2025", "Generated": "2026-01-05 14:20", "Size": "512 KB"},
        {"Type": "Excel", "Period": "Dec 2025", "Generated": "2026-01-02 11:05", "Size": "204 KB"},
    ]
    st.dataframe(pd.DataFrame(recent_reports), use_container_width=True, hide_index=True)
