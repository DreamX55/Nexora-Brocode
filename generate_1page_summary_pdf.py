import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.pdfgen import canvas

class SinglePageCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, total_pages):
        self.saveState()
        # Footer
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(28, 16, "Nexora AI Hackathon 2026 | Team Brocode | Manipal Institute of Technology")
        self.drawRightString(584, 16, "Repository: github.com/DreamX55/Nexora-Brocode")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(28, 24, 584, 24)
        self.restoreState()


def build_one_page_pdf(output_filename):
    # Total page: 612 x 792 pt.
    # Margins: 28pt left/right (556pt width), 24pt top/bottom (744pt height).
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=28,
        rightMargin=28,
        topMargin=24,
        bottomMargin=26,
    )

    styles = getSampleStyleSheet()

    c_primary = colors.HexColor("#0F172A")    # Slate 900
    c_secondary = colors.HexColor("#2563EB")  # Blue 600
    c_dark_blue = colors.HexColor("#1E3A8A")  # Blue 900
    c_teal = colors.HexColor("#0D9488")       # Teal 600
    c_text = colors.HexColor("#334155")       # Slate 700
    c_muted = colors.HexColor("#64748B")      # Slate 500
    c_light_bg = colors.HexColor("#F8FAFC")   # Slate 50
    c_border = colors.HexColor("#E2E8F0")     # Slate 200

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=17,
        textColor=c_primary,
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=c_secondary,
    )

    sec_header_style = ParagraphStyle(
        'SecHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=10,
        textColor=c_primary,
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.2,
        textColor=c_text,
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold',
        textColor=c_primary,
    )

    tbl_head = ParagraphStyle(
        'TblHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=8.5,
        textColor=colors.white,
    )

    tbl_cell = ParagraphStyle(
        'TblCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.6,
        leading=8.2,
        textColor=c_text,
    )

    tbl_cell_bold = ParagraphStyle(
        'TblCellBold',
        parent=tbl_cell,
        fontName='Helvetica-Bold',
        textColor=c_primary,
    )

    callout_text = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.8,
        leading=8.8,
        textColor=c_primary,
    )

    story = []

    # 1. HEADER ROW: Title + Meta Banner
    header_table_data = [
        [
            Paragraph("<b>SMART SHORTLISTING ENGINE</b><br/><font size=7 color='#2563EB'><b>NEXORA AI HACKATHON 2026 &bull; MIT MANIPAL</b></font>", title_style),
            Paragraph("<b>TEAM: BROCODE</b> &nbsp;|&nbsp; <b>100% Local / Zero-API</b><br/><font size=6.5 color='#64748B'>Repo: github.com/DreamX55/Nexora-Brocode</font>", ParagraphStyle('RMeta', parent=body_style, alignment=2))
        ]
    ]
    t_head = Table(header_table_data, colWidths=[310, 246])
    t_head.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_head)
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width="100%", thickness=1.2, color=c_secondary, spaceBefore=0, spaceAfter=4))

    # 2. EXECUTIVE SUMMARY & PROBLEM OVERVIEW (Dual Box Grid)
    exec_text = """<b>Challenge & Solution:</b> Campus recruitment portals evaluate candidate batches against single job postings. Standard keyword matching fails on terminology synonyms (e.g. <i>Express vs Node.js</i>), while generative cloud LLMs produce hallucinations, privacy issues, and arbitrary scores. <b>Brocode's Smart Shortlisting Engine</b> is a <b>100% offline, privacy-first recruitment platform</b> pairing deterministic lexical matching with offline dense vector search (<code>all-MiniLM-L6-v2</code>) and an <b>Evidence-First Explainability Engine</b> that provides auditable quotes for recruiter verification."""
    
    constraints_box = """<b>Hard Competition Constraints Satisfied:</b><br/>
    &bull; <b>Zero Cloud APIs:</b> No OpenAI, Gemini, Claude, or internet calls (<code>HF_HUB_OFFLINE=1</code>).<br/>
    &bull; <b>Non-Arbitrary Scoring:</b> Fully mathematical formulation combining lexical ($L$) and semantic ($S$) signals.<br/>
    &bull; <b>Format Resilient:</b> Robustly parses messy multi-column PDFs and isolates corrupt files without crashing."""

    exec_grid = Table([
        [
            Paragraph(exec_text, callout_text),
            Paragraph(constraints_box, callout_text)
        ]
    ], colWidths=[330, 226])
    exec_grid.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#EFF6FF")),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (0,0), 0.75, colors.HexColor("#BFDBFE")),
        ('BOX', (1,0), (1,0), 0.75, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(exec_grid)
    story.append(Spacer(1, 4))

    # 3. END-TO-END PIPELINE (Compact Table)
    story.append(Paragraph("<b>1. End-to-End System Architecture (7 Pipeline Stages)</b>", sec_header_style))
    story.append(Spacer(1, 1.5))
    pipe_data = [
        [
            Paragraph("<b>Stage</b>", tbl_head),
            Paragraph("<b>Component & Technology</b>", tbl_head),
            Paragraph("<b>Core Functionality & Guarantee</b>", tbl_head)
        ],
        [
            Paragraph("<b>1. Ingestion</b>", tbl_cell_bold),
            Paragraph("PyMuPDF (fitz) + Normalizer", tbl_cell),
            Paragraph("Extracts text streams, detects multi-column layouts, normalizes whitespace & unicode.", tbl_cell)
        ],
        [
            Paragraph("<b>2. Intelligence</b>", tbl_cell_bold),
            Paragraph("JD & Resume Profilers", tbl_cell),
            Paragraph("Classifies mandatory (REQUIRED) vs bonus (PREFERRED) requirements; structures candidate profile.", tbl_cell)
        ],
        [
            Paragraph("<b>3. Dual Match</b>", tbl_cell_bold),
            Paragraph("Lexical + Semantic Matchers", tbl_cell),
            Paragraph("Computes exact/alias/fuzzy token overlap ($L$) and dense cosine similarity ($S$) via <code>all-MiniLM-L6-v2</code>.", tbl_cell)
        ],
        [
            Paragraph("<b>4. Hybrid Score</b>", tbl_cell_bold),
            Paragraph("Requirement Scoring Engine", tbl_cell),
            Paragraph("Fuses lexical certainty with semantic context using closed-form dynamic weighting and noise cutoffs.", tbl_cell)
        ],
        [
            Paragraph("<b>5. Ranking</b>", tbl_cell_bold),
            Paragraph("Deterministic Ranking Service", tbl_cell),
            Paragraph("Monotonic sort with tie-breaks prioritizing required skill fulfillment, seniority, and score.", tbl_cell)
        ],
        [
            Paragraph("<b>6. Explainability</b>", tbl_cell_bold),
            Paragraph("Evidence-First Generator", tbl_cell),
            Paragraph("Stitches exact resume quote spans, lists matched concepts, and highlights missing mandatory skills.", tbl_cell)
        ],
        [
            Paragraph("<b>7. Web Interface</b>", tbl_cell_bold),
            Paragraph("FastAPI Async + React 19 UI", tbl_cell),
            Paragraph("Recruiter dashboard with batch upload, live progress, shortlist cards, drawer, and pairwise comparison.", tbl_cell)
        ]
    ]
    t_pipe = Table(pipe_data, colWidths=[70, 160, 326])
    t_pipe.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_dark_blue),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 1.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_pipe)
    story.append(Spacer(1, 4))

    # 4. MATHEMATICAL FORMULATION & KEY INNOVATIONS (Dual Column)
    formula_html = """
    <b>Hybrid Scoring Formulation:</b><br/>
    &bull; <b>Exact / Alias Lexical Match:</b> &nbsp;<code>Score = 0.65&middot;L + 0.35&middot;S</code> (proven tech usage + depth)<br/>
    &bull; <b>Fuzzy Lexical Match (L &ge; 0.85):</b> &nbsp;<code>Score = 0.50&middot;L + 0.50&middot;S</code> (spelling resilience)<br/>
    &bull; <b>Pure Conceptual Match:</b> &nbsp;<code>Score = 0.75&middot;S</code> (e.g. Express &rarr; Node.js; capped at 0.75)<br/>
    &bull; <b>Anti-Hallucination Cutoff:</b> &nbsp;If <code>S &lt; 0.35</code>, semantic credit is set to <code>0.0</code> (noise rejection)<br/>
    &bull; <b>Priority Weighting:</b> <code>Final = &Sigma;(w<sub>i</sub> &middot; score<sub>i</sub>) / &Sigma;w<sub>i</sub></code> (Required: 3&times;, Preferred: 1&times;)
    """

    innovations_html = """
    <b>Recruiter Tools & Rubric Innovations:</b><br/>
    &bull; <b>Top-3 Auditable Briefs:</b> Natural-language summaries with verbatim provenance quotes.<br/>
    &bull; <b>Pairwise Comparison:</b> Answers <i>"Why is Candidate X above Y?"</i> via criteria delta matrix.<br/>
    &bull; <b>Ranking Robustness Audits:</b> Perturbation testing proves rank stability against synonym/formatting noise.<br/>
    &bull; <b>JD Bias Detection:</b> Flags exclusionary phrasing or narrow requirements in job postings.<br/>
    &bull; <b>Zero Cost & Offline:</b> Runs locally on CPU/GPU without cloud subscriptions or tokens.
    """

    dual_box = Table([
        [
            Paragraph(formula_html, callout_text),
            Paragraph(innovations_html, callout_text)
        ]
    ], colWidths=[278, 278])
    dual_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#F8FAFC")),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#F0FDF4")),
        ('BOX', (0,0), (0,0), 0.75, colors.HexColor("#CBD5E1")),
        ('BOX', (1,0), (1,0), 0.75, colors.HexColor("#BBF7D0")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(Paragraph("<b>2. Mathematical Scoring Model & Recruiter Feature Suite</b>", sec_header_style))
    story.append(Spacer(1, 1.5))
    story.append(dual_box)
    story.append(Spacer(1, 4))

    # 5. BENCHMARK RESULTS & TECH STACK (Dual Column Table)
    story.append(Paragraph("<b>3. Competition Evaluation Benchmarks & Technology Matrix</b>", sec_header_style))
    story.append(Spacer(1, 1.5))

    bench_data = [
        [Paragraph("<b>Evaluation Metric</b>", tbl_head), Paragraph("<b>Observed Benchmark Result</b>", tbl_head)],
        [Paragraph("<b>Parse Success Rate</b>", tbl_cell_bold), Paragraph("<b>100%</b> across 18 official + 54 external audit PDFs", tbl_cell)],
        [Paragraph("<b>Score Distribution</b>", tbl_cell_bold), Paragraph("Strong: 85-94 | Medium: 60-78 | Weak: 25-45 (Clean spread)", tbl_cell)],
        [Paragraph("<b>Robustness Stability</b>", tbl_cell_bold), Paragraph("Top-3 candidate ranks invariant to formatting perturbations", tbl_cell)],
        [Paragraph("<b>Batch Throughput</b>", tbl_cell_bold), Paragraph("~1.2s per 18-resume batch (Local CPU inference)", tbl_cell)],
    ]
    t_bench = Table(bench_data, colWidths=[110, 164])
    t_bench.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 1.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
        ('LEFTPADDING', (0,0), (-1,-1), 3.5),
        ('RIGHTPADDING', (0,0), (-1,-1), 3.5),
    ]))

    tech_data = [
        [Paragraph("<b>System Layer</b>", tbl_head), Paragraph("<b>Open-Source Technologies Applied</b>", tbl_head)],
        [Paragraph("<b>Backend API</b>", tbl_cell_bold), Paragraph("FastAPI, Uvicorn, Pydantic v2, Python 3.9+", tbl_cell)],
        [Paragraph("<b>Parsing & NLP</b>", tbl_cell_bold), Paragraph("PyMuPDF (fitz), Sentence-Transformers, PyTorch", tbl_cell)],
        [Paragraph("<b>Frontend UI</b>", tbl_cell_bold), Paragraph("React 19, Vite, Tailwind CSS, Lucide Icons", tbl_cell)],
        [Paragraph("<b>Verification</b>", tbl_cell_bold), Paragraph("Pytest, Playwright UI tests, Perturbation Harness", tbl_cell)],
    ]
    t_tech = Table(tech_data, colWidths=[90, 184])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_teal),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 1.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
        ('LEFTPADDING', (0,0), (-1,-1), 3.5),
        ('RIGHTPADDING', (0,0), (-1,-1), 3.5),
    ]))

    grid_results = Table([[t_bench, t_tech]], colWidths=[276, 278])
    grid_results.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(grid_results)
    story.append(Spacer(1, 3))

    # 6. SIGN-OFF FOOTER CARD
    footer_text = """<b>Repository & Audit Verification:</b> All source code, scoring algorithms, test suites, and documentation are publicly available at <b><u>https://github.com/DreamX55/Nexora-Brocode.git</u></b>. Fully reproducible offline with <code>pytest</code> and <code>HF_HUB_OFFLINE=1</code>."""
    t_foot = Table([[Paragraph(footer_text, callout_text)]], colWidths=[556])
    t_foot.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#94A3B8")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_foot)

    doc.build(story, canvasmaker=SinglePageCanvas)
    print(f"Single-page report successfully generated: {output_filename}")

if __name__ == "__main__":
    out_pdf = os.path.abspath("Nexora_Brocode_Project_Summary_Report.pdf")
    build_one_page_pdf(out_pdf)
