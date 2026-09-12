import time
from pathlib import Path
from playwright.sync_api import sync_playwright

SCREENSHOT_DIR = Path("/Users/jahnaviakveti/.gemini/antigravity/brain/419c77ea-f195-458f-84de-29b63941287f/screenshots")

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    )
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://127.0.0.1:5173")
    page.wait_for_load_state("networkidle")

    # Upload JD and 15 resumes
    jd_path = Path("scratch/qa_senior_fullstack_jd.pdf")
    ext_dir = Path("data/external_resumes")
    resumes_15 = sorted([p for p in ext_dir.rglob("*.pdf") if not p.name.startswith('.')])[:15]

    page.set_input_files('input[type="file"]:first-of-type', str(jd_path.resolve()))
    page.set_input_files('input[type="file"][multiple]', [str(r.resolve()) for r in resumes_15])
    time.sleep(0.3)
    page.locator("button.btn-primary").click()
    page.wait_for_selector(".podium-grid", timeout=25000)
    time.sleep(1)

    # Open Rank #1 modal
    page.locator(".top-card.rank-1 .btn-inspect").click()
    page.wait_for_selector(".modal-content", timeout=5000)
    time.sleep(0.5)

    # Scroll modal down to reveal requirements & evidence
    page.evaluate("document.querySelector('.modal-content').scrollTop = 450")
    time.sleep(0.5)
    page.screenshot(path=str(SCREENSHOT_DIR / "state_F_candidate_modal_evidence_scrolled.png"))

    browser.close()
    print("Modal evidence scrolled screenshot captured!")
