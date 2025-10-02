import pandas as pd
from tabulate import tabulate
from pathlib import Path
from datetime import datetime, timezone
from src.storage import db
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def export_csv_pdf():
    rows = db.query("SELECT indicator, type, score, country, asn, source FROM indicators")
    if not rows:
        print("No records in DB.")
        return

    df = pd.DataFrame(rows, columns=["Indicator", "Type", "Score", "Country", "ASN", "Source"])

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_dir = Path("reports")
    out_dir.mkdir(parents=True, exist_ok=True)

    # === CSV Export ===
    csv_path = out_dir / f"report_{stamp}.csv"
    df.to_csv(csv_path, index=False)
    print("CSV exported ->", csv_path)

    # === PDF Export ===
    pdf_path = out_dir / f"report_{stamp}.pdf"
    doc = SimpleDocTemplate(str(pdf_path))
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"Threat Intelligence Report - {stamp}", styles["Title"]))
    story.append(Spacer(1, 12))

    # Summary stats
    story.append(Paragraph("Summary Statistics", styles["Heading2"]))
    story.append(Paragraph(df["Score"].describe().to_frame().to_html(), styles["Normal"]))
    story.append(Spacer(1, 12))

    # Top 10 indicators
    story.append(Paragraph("Top 10 Indicators", styles["Heading2"]))
    top10 = df.sort_values(by="Score", ascending=False).head(10)
    table_data = [list(top10.columns)] + top10.values.tolist()
    table = Table(table_data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.grey),
        ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
    ]))
    story.append(table)

    doc.build(story)
    print("PDF exported ->", pdf_path)

if __name__ == "__main__":
    export_csv_pdf()
