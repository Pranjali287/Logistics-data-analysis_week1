"""
Compiles Strategic_Planning_Logistics_Report.md into a professional Microsoft Word document (.docx)
using python-docx, including tables and formatting.
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

def generate_docx():
    doc = Document()
    
    # Page setup
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Document Title
    title = doc.add_paragraph()
    title_run = title.add_run("Logistics Data Analytics: Strategic Planning and Implementation Report")
    title_run.font.name = "Arial"
    title_run.font.size = Pt(22)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(17, 24, 39)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    subtitle = doc.add_paragraph()
    sub_run = subtitle.add_run("Multi-Echelon Supply Chain Analytics and Last-Mile Delivery Optimization\n")
    sub_run.font.name = "Arial"
    sub_run.font.size = Pt(14)
    sub_run.font.italic = True
    sub_run.font.color.rgb = RGBColor(75, 85, 99)
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Metadata Block
    meta = doc.add_paragraph()
    meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    m_run = meta.add_run("Author: B.E. Student in AI & ML | Acharya Institute of Technology, Bengaluru\nEvaluation Date: October 2026 | Scope: 24-Month Regional Fulfillment Study")
    m_run.font.name = "Arial"
    m_run.font.size = Pt(10)
    m_run.font.color.rgb = RGBColor(107, 114, 128)
    
    doc.add_paragraph("―" * 45).alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Helper function to add styled headings
    def add_custom_heading(text, level):
        h = doc.add_heading(text, level=level)
        for r in h.runs:
            r.font.name = "Arial"
            if level == 1:
                r.font.size = Pt(16)
                r.font.color.rgb = RGBColor(30, 58, 138)
            elif level == 2:
                r.font.size = Pt(13)
                r.font.color.rgb = RGBColor(55, 65, 81)
        return h

    add_custom_heading("Executive Summary", level=1)
    p = doc.add_paragraph(
        "Modern omnichannel and e-commerce supply chains operate under severe margin pressures characterized "
        "by high customer expectations for rapid fulfillment, substantial inventory holding costs, and unpredictable "
        "demand volatility. This strategic planning and technical report presents the architectural design, algorithmic "
        "pipeline, and empirical results of an end-to-end logistics analytics system developed for a regional e-commerce "
        "fulfillment operation in the Bengaluru metropolitan area across 3 distribution hubs (Peenya, Electronic City, Whitefield) "
        "and 100 active SKUs over 24 calendar months (2024–2025)."
    )
    p.paragraph_format.line_spacing = 1.15

    add_custom_heading("1. Key Performance Indicators (KPI) Scorecard", level=1)
    table_kpi = doc.add_table(rows=6, cols=5)
    table_kpi.style = "Table Grid"
    table_kpi.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    headers = ["KPI Metric", "Mathematical Formulation", "Baseline Benchmark", "Target Proposal", "Achieved Prototype Result"]
    for i, h in enumerate(headers):
        cell = table_kpi.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        
    kpi_rows = [
        ["Forecast Error (WAPE)", "Σ|actual - forecast| / Σ actual", "20.96% (7-day MA)", "10–15% relative improvement", "17.14% (18.21% relative reduction)"],
        ["Stockout Rate", "Unfulfilled demand / total demand", "0.11%", "30% relative reduction", "0.07% (34.2% reduction [ASSUMPTION])"],
        ["Inventory Turnover", "Annualized COGS / avg inventory value", "41.49x / year", "Increase vs. baseline", "50.21x / year (+21% velocity)"],
        ["Space Utilization", "Occupied slots / total capacity", "37.5%", "Shift to fast-turn SKUs", "82.5% active high-turn velocity"],
        ["Route Distance per Stop", "Total route km / delivery stops", "12.45 km/stop", "10% reduction on sample days", "4.32 km/stop (65.3% reduction)"]
    ]
    for row_idx, data in enumerate(kpi_rows):
        for col_idx, text in enumerate(data):
            cell = table_kpi.cell(row_idx + 1, col_idx)
            cell.text = text
            cell.paragraphs[0].runs[0].font.size = Pt(9)

    add_custom_heading("2. Demand Forecasting & Model Comparison", level=1)
    p2 = doc.add_paragraph(
        "A Gradient Boosting Regressor (GBR) incorporating calendar cycles, weekly demand lags, and rolling statistical "
        "features reduced forecast error (WAPE) from a naive 7-day moving average baseline of 20.96% down to 17.14% "
        "(an 18.21% relative reduction), exceeding the proposed target of 10–15%. Multi-window backtesting across two "
        "separate 8-week windows confirmed exceptional temporal stability (17.14% and 17.12% WAPE)."
    )
    p2.paragraph_format.line_spacing = 1.15

    add_custom_heading("3. Inventory Segmentation & Spatial Routing", level=1)
    p3 = doc.add_paragraph(
        "Unsupervised K-Means clustering combined with ABC/XYZ velocity-volatility profiling categorized SKUs into actionable "
        "replenishment archetypes with a high silhouette score of 0.6530 and an Adjusted Rand Index (ARI) of 1.000 between 2024 "
        "and 2025. In last-mile delivery, the 2-Opt edge-exchange heuristic reduced delivery route distance from 311.33 km down "
        "to 108.08 km, achieving a 65.3% reduction in distance and fuel burn."
    )
    p3.paragraph_format.line_spacing = 1.15

    add_custom_heading("4. Financial Impact Summary [ASSUMPTION]", level=1)
    p4 = doc.add_paragraph(
        "• Annual Stockout Margin Recovered: ₹784,400 / year (4,240 units recovered @ ₹185 margin)\n"
        "• Annual Fleet Transit Expenditure Savings: ₹1,780,470 / year (~203 km saved/day across 3 DCs @ ₹24/km)\n"
        "• Total Modeled Operational Impact: ₹2,564,870 / year (~$31,000 USD)"
    )
    p4.paragraph_format.line_spacing = 1.15

    output_path = "report/Strategic_Planning_Logistics_Report.docx"
    doc.save(output_path)
    print(f"Generated professional DOCX report at: {output_path}")

if __name__ == "__main__":
    generate_docx()
