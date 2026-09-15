import os
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.abspath('backend'))
import fitz
from app.services.pipeline import ShortlistingPipeline

def main():
    start_time = time.time()
    ext_dir = Path("data/external_resumes")
    resume_files = sorted([p for p in ext_dir.rglob("*.pdf") if not p.name.startswith('.')])
    
    print(f"Testing ShortlistingPipeline on {len(resume_files)} external resumes...")

    # Create a realistic test JD in memory / temp file
    jd_doc = fitz.open()
    jd_page = jd_doc.new_page()
    jd_text = """
    Job Title: Senior Fullstack Software Engineer
    Location: Hybrid / Remote

    Required Qualifications:
    - 3+ years of professional backend development with Python
    - Strong database skills with SQL, PostgreSQL, or MySQL

    Preferred Qualifications:
    - Hands-on experience with containerization using Docker or Kubernetes
    - Cloud infrastructure deployment experience with AWS or GCP
    """
    jd_page.insert_text((50, 72), jd_text)
    temp_jd_path = Path("scratch/temp_smoke_jd.pdf")
    jd_doc.save(str(temp_jd_path))
    jd_doc.close()

    pipeline = ShortlistingPipeline.get_instance()
    
    resume_inputs = [(p.name, p) for p in resume_files]
    response = pipeline.process_batch(temp_jd_path, resume_inputs)

    elapsed_time = time.time() - start_time

    print("\n" + "="*60)
    print("PHASE 9 PIPELINE SMOKE TEST REPORT")
    print("="*60)
    print(f"Resumes discovered: {len(resume_files)}")
    print(f"Resumes received: {response.total_resumes_received}")
    print(f"Candidates processed: {response.total_candidates_processed}")
    print(f"Candidates ranked: {response.total_ranked}")
    print(f"Failed candidates isolated: {len(response.failed_candidates)}")
    print(f"Total pipeline runtime: {elapsed_time:.2f}s")
    print(f"Average time per candidate: {(elapsed_time / len(resume_files)):.3f}s")

    if response.failed_candidates:
        print("\nFailed candidate details:")
        for fc in response.failed_candidates:
            print(f"  - {fc.filename}: {fc.error}")
    else:
        print("Zero document failures detected across all 54 PDFs.")

    print("\nTop 3 Ranked Candidates:")
    for c in response.ranked_candidates[:3]:
        print(f"  Rank #{c.rank}: {c.candidate_name or c.candidate_id} | Score: {c.overall_score:.1f}/100")
        print(f"    Why: {c.why_ranked_here}")
        if c.strengths:
            print(f"    Top Strength: {c.strengths[0]}")

    print("\nLowest Ranked Candidate:")
    bottom = response.ranked_candidates[-1]
    print(f"  Rank #{bottom.rank}: {bottom.candidate_name or bottom.candidate_id} | Score: {bottom.overall_score:.1f}/100")

    # Clean up temp file
    if temp_jd_path.exists():
        temp_jd_path.unlink()

if __name__ == "__main__":
    main()
