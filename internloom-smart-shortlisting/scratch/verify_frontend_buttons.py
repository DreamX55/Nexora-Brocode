import sys
import time
from pathlib import Path
import fitz
from playwright.sync_api import sync_playwright

# 1. Create a valid test JD PDF
jd_text = """
Job Title: Senior Backend Engineer
Required Qualifications:
- 3+ years Python experience
- PostgreSQL database experience
Preferred Qualifications:
- Docker containerization
"""
jd_doc = fitz.open()
jd_page = jd_doc.new_page()
jd_page.insert_text((50, 72), jd_text)
jd_path = Path("scratch/btn_test_jd.pdf")
jd_doc.save(str(jd_path))
jd_doc.close()

# 2. Get resumes from external directory
ext_dir = Path("data/external_resumes")
all_resumes = sorted([str(p.resolve()) for p in ext_dir.rglob("*.pdf") if not p.name.startswith('.')])
resumes_14 = all_resumes[:14]
resumes_15 = all_resumes[:15]
resumes_18 = all_resumes[:18]
resumes_19 = all_resumes[:19]

print(f"Total available resumes: {len(all_resumes)}")

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    )
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    
    # -------------------------------------------------------------
    # CASE 1: 14 RESUMES
    # -------------------------------------------------------------
    page.goto("http://127.0.0.1:5173")
    page.wait_for_load_state("networkidle")
    
    # Set JD
    page.set_input_files('input[type="file"]:not([multiple])', str(jd_path.resolve()))
    page.wait_for_timeout(300)
    
    # Set 14 resumes
    page.set_input_files('input[type="file"][multiple]', resumes_14)
    page.wait_for_timeout(300)
    
    btn_14 = page.locator(".action-bar button")
    is_disabled_14 = btn_14.is_disabled()
    text_14 = btn_14.inner_text()
    dom_disabled_14 = page.evaluate("() => document.querySelector('.action-bar button').disabled")
    
    results["14_resumes"] = {
        "is_disabled": is_disabled_14,
        "dom_disabled": dom_disabled_14,
        "button_text": text_14
    }
    print(f"[TEST 14 RESUMES] is_disabled: {is_disabled_14}, dom_disabled: {dom_disabled_14}, text: {text_14}")
    assert is_disabled_14 is True, "Button should be disabled at 14 resumes!"
    assert dom_disabled_14 is True, "DOM property disabled should be True at 14 resumes!"

    # -------------------------------------------------------------
    # CASE 2: 15 RESUMES
    # -------------------------------------------------------------
    page.goto("http://127.0.0.1:5173")
    page.wait_for_load_state("networkidle")
    
    page.set_input_files('input[type="file"]:not([multiple])', str(jd_path.resolve()))
    page.wait_for_timeout(300)
    
    page.set_input_files('input[type="file"][multiple]', resumes_15)
    page.wait_for_timeout(300)
    
    btn_15 = page.locator(".action-bar button")
    is_disabled_15 = btn_15.is_disabled()
    text_15 = btn_15.inner_text()
    dom_disabled_15 = page.evaluate("() => document.querySelector('.action-bar button').disabled")
    
    results["15_resumes"] = {
        "is_disabled": is_disabled_15,
        "dom_disabled": dom_disabled_15,
        "button_text": text_15
    }
    print(f"[TEST 15 RESUMES] is_disabled: {is_disabled_15}, dom_disabled: {dom_disabled_15}, text: {text_15}")
    assert is_disabled_15 is False, "Button should be enabled at 15 resumes!"
    assert dom_disabled_15 is False, "DOM property disabled should be False at 15 resumes!"

    # -------------------------------------------------------------
    # CASE 3: 18 RESUMES
    # -------------------------------------------------------------
    page.goto("http://127.0.0.1:5173")
    page.wait_for_load_state("networkidle")
    
    page.set_input_files('input[type="file"]:not([multiple])', str(jd_path.resolve()))
    page.wait_for_timeout(300)
    
    page.set_input_files('input[type="file"][multiple]', resumes_18)
    page.wait_for_timeout(300)
    
    btn_18 = page.locator(".action-bar button")
    is_disabled_18 = btn_18.is_disabled()
    text_18 = btn_18.inner_text()
    dom_disabled_18 = page.evaluate("() => document.querySelector('.action-bar button').disabled")
    
    results["18_resumes"] = {
        "is_disabled": is_disabled_18,
        "dom_disabled": dom_disabled_18,
        "button_text": text_18
    }
    print(f"[TEST 18 RESUMES] is_disabled: {is_disabled_18}, dom_disabled: {dom_disabled_18}, text: {text_18}")
    assert is_disabled_18 is False, "Button should be enabled at 18 resumes!"
    assert dom_disabled_18 is False, "DOM property disabled should be False at 18 resumes!"

    # -------------------------------------------------------------
    # CASE 4: 19 RESUMES
    # -------------------------------------------------------------
    page.goto("http://127.0.0.1:5173")
    page.wait_for_load_state("networkidle")
    
    page.set_input_files('input[type="file"]:not([multiple])', str(jd_path.resolve()))
    page.wait_for_timeout(300)
    
    page.set_input_files('input[type="file"][multiple]', resumes_19)
    page.wait_for_timeout(300)
    
    btn_19 = page.locator(".action-bar button")
    is_disabled_19 = btn_19.is_disabled()
    text_19 = btn_19.inner_text()
    dom_disabled_19 = page.evaluate("() => document.querySelector('.action-bar button').disabled")
    
    results["19_resumes"] = {
        "is_disabled": is_disabled_19,
        "dom_disabled": dom_disabled_19,
        "button_text": text_19
    }
    print(f"[TEST 19 RESUMES] is_disabled: {is_disabled_19}, dom_disabled: {dom_disabled_19}, text: {text_19}")
    assert is_disabled_19 is True, "Button should be disabled at 19 resumes!"
    assert dom_disabled_19 is True, "DOM property disabled should be True at 19 resumes!"

    browser.close()

print("ALL FRONTEND BUTTON VALIDATION CHECKS PASSED PERFECTLY!")
