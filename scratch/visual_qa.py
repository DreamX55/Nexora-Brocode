import os
import sys
import time
from pathlib import Path
import fitz

# Ensure screenshot directory exists
SCREENSHOT_DIR = Path("/Users/jahnaviakveti/.gemini/antigravity/brain/419c77ea-f195-458f-84de-29b63941287f/screenshots")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

# 1. Prepare test JD PDF
jd_text = """
Job Title: Senior Fullstack Software Engineer
Location: Remote / Hybrid

Required Qualifications:
- 3+ years of professional backend development with Python
- Strong database proficiency with PostgreSQL or SQL
- Solid foundation in REST API design and distributed services

Preferred Qualifications:
- Experience with containerization using Docker or Kubernetes
- Cloud deployment experience on AWS or GCP
"""
jd_doc = fitz.open()
jd_page = jd_doc.new_page()
jd_page.insert_text((50, 72), jd_text)
jd_pdf_path = Path("scratch/qa_senior_fullstack_jd.pdf")
jd_doc.save(str(jd_pdf_path))
jd_doc.close()

# 2. Get list of external resumes
ext_dir = Path("data/external_resumes")
all_resumes = sorted([p for p in ext_dir.rglob("*.pdf") if not p.name.startswith('.')])
resumes_14 = all_resumes[:14]
resumes_15 = all_resumes[:15]
resumes_19 = all_resumes[:19]

# 3. Create a corrupt resume PDF for test H
corrupt_pdf_path = Path("scratch/corrupt_candidate_resume.pdf")
with open(corrupt_pdf_path, "wb") as f:
    f.write(b"%PDF-1.4 corrupt content that cannot be opened")

from playwright.sync_api import sync_playwright

print(f"Starting Visual QA pass with Playwright against http://127.0.0.1:5173...")

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    )

    # --- TEST SUITE 1: DESKTOP (1440x900) ---
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://127.0.0.1:5173")
    page.wait_for_load_state("networkidle")
    time.sleep(1)

    # A. Upload Screen — Empty State (Desktop, Laptop, Mobile)
    print("Capturing State A: Upload Screen — Empty State...")
    page.screenshot(path=str(SCREENSHOT_DIR / "state_A_upload_empty_desktop_1440x900.png"))
    
    page.set_viewport_size({"width": 1280, "height": 800})
    page.screenshot(path=str(SCREENSHOT_DIR / "state_A_upload_empty_laptop_1280x800.png"))

    page.set_viewport_size({"width": 390, "height": 844})
    page.screenshot(path=str(SCREENSHOT_DIR / "state_A_upload_empty_mobile_390x844.png"))

    # Reset to Desktop for interactive flow
    page.set_viewport_size({"width": 1440, "height": 900})

    # C. Upload Screen — Invalid Batch (14 resumes)
    print("Capturing State C: Upload Screen — Invalid Batch (14 resumes)...")
    page.set_input_files('input[type="file"]:first-of-type', str(jd_pdf_path.resolve()))
    page.set_input_files('input[type="file"][multiple]', [str(r.resolve()) for r in resumes_14])
    time.sleep(0.5)
    page.screenshot(path=str(SCREENSHOT_DIR / "state_C_upload_invalid_14_resumes.png"))

    # Also test 19 resumes (too many)
    print("Capturing State C: Upload Screen — Invalid Batch (19 resumes)...")
    page.set_input_files('input[type="file"][multiple]', [str(r.resolve()) for r in resumes_19])
    time.sleep(0.5)
    page.screenshot(path=str(SCREENSHOT_DIR / "state_C_upload_invalid_19_resumes.png"))

    # B. Upload Screen — Valid 15-Resume Batch
    print("Capturing State B: Upload Screen — Valid 15-Resume Batch...")
    page.set_input_files('input[type="file"][multiple]', [str(r.resolve()) for r in resumes_15])
    time.sleep(0.5)
    page.screenshot(path=str(SCREENSHOT_DIR / "state_B_upload_valid_15_resumes.png"))

    # D. Processing Screen
    print("Capturing State D: Processing Screen...")
    # Click analyze button
    analyze_btn = page.locator("button.btn-primary")
    analyze_btn.click()
    time.sleep(0.4) # Capture during processing
    page.screenshot(path=str(SCREENSHOT_DIR / "state_D_processing_screen.png"))

    # E. Results Dashboard
    print("Waiting for analysis completion and capturing State E: Results Dashboard...")
    page.wait_for_selector(".podium-grid", timeout=25000)
    time.sleep(1) # Ensure render settled
    page.screenshot(path=str(SCREENSHOT_DIR / "state_E_results_dashboard_desktop_1440x900.png"))

    page.set_viewport_size({"width": 1280, "height": 800})
    page.screenshot(path=str(SCREENSHOT_DIR / "state_E_results_dashboard_laptop_1280x800.png"))

    page.set_viewport_size({"width": 390, "height": 844})
    page.screenshot(path=str(SCREENSHOT_DIR / "state_E_results_dashboard_mobile_390x844.png"))

    # Reset to Desktop for detail modals
    page.set_viewport_size({"width": 1440, "height": 900})

    # F. Candidate Detail Modal — Rank #1
    print("Capturing State F: Candidate Detail Modal for Rank #1...")
    rank_1_inspect = page.locator(".top-card.rank-1 .btn-inspect")
    rank_1_inspect.click()
    page.wait_for_selector(".modal-content", timeout=5000)
    time.sleep(0.5)
    page.screenshot(path=str(SCREENSHOT_DIR / "state_F_candidate_modal_rank_1.png"))

    # Close modal
    close_btn = page.locator("button.btn-close")
    close_btn.click()
    time.sleep(0.5)

    # G. Candidate Detail Modal — Rank #2
    print("Capturing State G: Candidate Detail Modal for Rank #2...")
    rank_2_inspect = page.locator(".top-card.rank-2 .btn-inspect")
    rank_2_inspect.click()
    page.wait_for_selector(".modal-content", timeout=5000)
    time.sleep(0.5)
    page.screenshot(path=str(SCREENSHOT_DIR / "state_G_candidate_modal_rank_2.png"))

    # Close modal
    page.locator("button.btn-close").click()
    time.sleep(0.5)

    # H. Results State Containing Failed Candidates
    print("Capturing State H: Results State with Isolated Failed Candidates...")
    # Click Analyze New Batch
    page.locator("text=← Analyze New Batch").click()
    time.sleep(0.5)

    # Upload JD + 15 valid resumes + 1 corrupt resume (16 total resumes)
    batch_with_corrupt = resumes_15 + [corrupt_pdf_path]
    page.set_input_files('input[type="file"]:first-of-type', str(jd_pdf_path.resolve()))
    page.set_input_files('input[type="file"][multiple]', [str(r.resolve()) for r in batch_with_corrupt])
    time.sleep(0.5)
    page.locator("button.btn-primary").click()

    # Wait for results and capture failed candidate warning banner
    page.wait_for_selector(".warning-banner", timeout=25000)
    time.sleep(1)
    page.screenshot(path=str(SCREENSHOT_DIR / "state_H_results_with_failed_candidates.png"))

    browser.close()
    print("All Visual QA screenshots successfully captured!")

