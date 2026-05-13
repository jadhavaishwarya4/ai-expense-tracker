# utils/export.py
# ============================================================
# Export Utilities
# Handles CSV and PDF export of expense data
# ============================================================

import pandas as pd
import io
from datetime import datetime
import os

# PDF generation using reportlab
try:
    from reportlab.lib.pagesizes import A4, letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch, cm
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


# ============================================================
# CSV EXPORT
# ============================================================

def export_expenses_to_csv(expenses_df: pd.DataFrame) -> bytes:
    """
    Convert expenses DataFrame to CSV bytes for download.
    Returns bytes object ready for st.download_button.
    """
    if expenses_df is None or expenses_df.empty:
        return b"No data to export"

    # Select and rename columns for clean export
    export_cols = {
        "date": "Date",
        "category": "Category",
        "amount": "Amount",
        "description": "Description",
        "is_recurring": "Recurring",
        "tags": "Tags",
        "created_at": "Added On"
    }

    df = expenses_df.copy()
    available_cols = [c for c in export_cols.keys() if c in df.columns]
    df = df[available_cols].rename(columns={k: v for k, v in export_cols.items() if k in available_cols})

    # Format date columns
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%d-%b-%Y")
    if "Added On" in df.columns:
        df["Added On"] = pd.to_datetime(df["Added On"]).dt.strftime("%d-%b-%Y %H:%M")

    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8")


def export_income_to_csv(income_df: pd.DataFrame) -> bytes:
    """Convert income DataFrame to CSV bytes."""
    if income_df is None or income_df.empty:
        return b"No data to export"

    export_cols = {
        "date": "Date",
        "source": "Source",
        "amount": "Amount",
        "description": "Description",
        "frequency": "Frequency",
    }

    df = income_df.copy()
    available_cols = [c for c in export_cols.keys() if c in df.columns]
    df = df[available_cols].rename(columns={k: v for k, v in export_cols.items() if k in available_cols})

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%d-%b-%Y")

    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8")


# ============================================================
# PDF EXPORT
# ============================================================

def generate_monthly_report_pdf(
    user_name: str,
    month: int,
    year: int,
    expenses_df: pd.DataFrame,
    income_df: pd.DataFrame,
    category_summary: pd.DataFrame,
    currency: str = "₹"
) -> bytes:
    """
    Generate a professional monthly financial report as PDF.
    Returns bytes for download.
    """
    if not REPORTLAB_AVAILABLE:
        return generate_simple_txt_report(user_name, month, year, expenses_df, income_df, currency)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm
    )

    story = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=22,
        textColor=colors.HexColor("#6366f1"),
        spaceAfter=6,
        fontName="Helvetica-Bold"
    )
    header_style = ParagraphStyle(
        "SectionHeader",
        parent=styles["Heading2"],
        fontSize=13,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=12,
        spaceAfter=6,
        fontName="Helvetica-Bold"
    )
    normal_style = ParagraphStyle(
        "CustomNormal",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#475569")
    )

    import calendar as cal
    month_name = cal.month_name[month]

    # --- HEADER ---
    story.append(Paragraph("💰 Personal Finance Report", title_style))
    story.append(Paragraph(f"{month_name} {year} — {user_name}", normal_style))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%d %B %Y, %I:%M %p')}", normal_style))
    story.append(Spacer(1, 0.3 * cm))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#6366f1")))
    story.append(Spacer(1, 0.3 * cm))

    # --- SUMMARY CARDS ---
    total_income = income_df["amount"].sum() if income_df is not None and not income_df.empty else 0
    total_expense = expenses_df["amount"].sum() if expenses_df is not None and not expenses_df.empty else 0
    net_savings = total_income - total_expense
    savings_pct = (net_savings / total_income * 100) if total_income > 0 else 0

    story.append(Paragraph("📊 Monthly Summary", header_style))

    summary_data = [
        ["Metric", "Amount", "Status"],
        ["Total Income", f"{currency}{total_income:,.2f}", "✅"],
        ["Total Expenses", f"{currency}{total_expense:,.2f}", "⚠️" if total_expense > total_income * 0.8 else "✅"],
        ["Net Savings", f"{currency}{net_savings:,.2f}", "✅" if net_savings > 0 else "🔴"],
        ["Savings Rate", f"{savings_pct:.1f}%", "✅" if savings_pct >= 20 else "⚠️"],
    ]

    summary_table = Table(summary_data, colWidths=[6 * cm, 5 * cm, 2 * cm])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#6366f1")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f8fafc"), colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.4 * cm))

    # --- CATEGORY BREAKDOWN ---
    if category_summary is not None and not category_summary.empty:
        story.append(Paragraph("📂 Expenses by Category", header_style))
        cat_data = [["Category", "Amount", "Transactions", "% of Total"]]
        for _, row in category_summary.iterrows():
            pct = (row["total_amount"] / total_expense * 100) if total_expense > 0 else 0
            cat_data.append([
                row["category"],
                f"{currency}{row['total_amount']:,.2f}",
                str(int(row.get("transaction_count", 0))),
                f"{pct:.1f}%"
            ])

        cat_table = Table(cat_data, colWidths=[5 * cm, 4 * cm, 3 * cm, 3 * cm])
        cat_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f1f5f9"), colors.white]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("PADDING", (0, 0), (-1, -1), 6),
            ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ]))
        story.append(cat_table)
        story.append(Spacer(1, 0.4 * cm))

    # --- TRANSACTIONS TABLE ---
    if expenses_df is not None and not expenses_df.empty:
        story.append(Paragraph("📝 All Transactions", header_style))
        txn_data = [["Date", "Category", "Description", "Amount"]]
        for _, row in expenses_df.sort_values("date", ascending=False).head(50).iterrows():
            txn_data.append([
                str(row["date"])[:10],
                row.get("category", ""),
                (str(row.get("description", "")) or "")[:40],
                f"{currency}{float(row['amount']):,.2f}"
            ])

        txn_table = Table(txn_data, colWidths=[3 * cm, 3.5 * cm, 7 * cm, 3.5 * cm])
        txn_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#374151")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f9fafb"), colors.white]),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#e5e7eb")),
            ("PADDING", (0, 0), (-1, -1), 5),
            ("ALIGN", (3, 0), (3, -1), "RIGHT"),
        ]))
        story.append(txn_table)

    # --- FOOTER ---
    story.append(Spacer(1, 0.5 * cm))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0")))
    story.append(Paragraph("Generated by Expense Tracker — Personal Finance Management System", normal_style))

    doc.build(story)
    return buffer.getvalue()


def generate_simple_txt_report(user_name, month, year, expenses_df, income_df, currency) -> bytes:
    """Fallback text-based report when ReportLab is unavailable."""
    import calendar as cal
    lines = [
        f"PERSONAL FINANCE REPORT",
        f"{'=' * 40}",
        f"User: {user_name}",
        f"Period: {cal.month_name[month]} {year}",
        f"Generated: {datetime.now().strftime('%d-%b-%Y %H:%M')}",
        f"{'=' * 40}",
        "",
        "SUMMARY",
        "-" * 30,
    ]

    total_income = income_df["amount"].sum() if income_df is not None and not income_df.empty else 0
    total_expense = expenses_df["amount"].sum() if expenses_df is not None and not expenses_df.empty else 0
    net_savings = total_income - total_expense

    lines += [
        f"Total Income:   {currency}{total_income:,.2f}",
        f"Total Expenses: {currency}{total_expense:,.2f}",
        f"Net Savings:    {currency}{net_savings:,.2f}",
        "",
        "TRANSACTIONS",
        "-" * 30,
    ]

    if expenses_df is not None and not expenses_df.empty:
        for _, row in expenses_df.sort_values("date", ascending=False).iterrows():
            lines.append(f"{str(row['date'])[:10]} | {row['category']:15} | {currency}{float(row['amount']):>10,.2f} | {row.get('description', '')[:30]}")

    return "\n".join(lines).encode("utf-8")
