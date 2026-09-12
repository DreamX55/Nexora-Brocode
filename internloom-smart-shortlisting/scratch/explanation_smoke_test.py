import os
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.abspath('backend'))
from app.services.document_parser import DocumentParser
from app.services.resume_analyzer.analyzer import ResumeAnalyzer
from app.services.keyword_matcher import KeywordMatcher
from app.services.semantic_matcher import LocalSentenceTransformerEmbeddingModel, SemanticMatcher
from app.services.hybrid_evaluator import (
    RequirementEvaluator,
    ScoringEngine,
    RankingService
)
from app.services.explanation_engine import ExplanationEngine
from app.schemas.domain import (
    JobDescription,
    JDRequirement,
    RequirementCategory,
    RequirementPriority
)

def main():
    start_time = time.time()
    ext_dir = Path("data/external_resumes")
    all_files = sorted([p for p in ext_dir.rglob("*.pdf") if not p.name.startswith('.')])
    
    print(f"Discovered {len(all_files)} PDF resumes for explanation smoke test.")

    # 1. Initialize services
    parser = DocumentParser()
    analyzer = ResumeAnalyzer()
    keyword_matcher = KeywordMatcher()
    embedding_model = LocalSentenceTransformerEmbeddingModel("all-MiniLM-L6-v2")
    semantic_matcher = SemanticMatcher(embedding_model)
    evaluator = RequirementEvaluator(keyword_matcher, semantic_matcher)
    scoring_engine = ScoringEngine(evaluator)
    ranking_service = RankingService(scoring_engine)
    explanation_engine = ExplanationEngine()

    # 2. Representative Job Description
    jd = JobDescription(
        jd_id="jd_senior_fullstack",
        raw_text="Senior Full Stack Software Engineer JD",
        requirements=[
            JDRequirement(
                id="r1",
                requirement_text="Proficiency in Python or backend API development",
                category=RequirementCategory.SKILL,
                priority=RequirementPriority.REQUIRED,
                extracted_keywords=["Python", "API", "backend"]
            ),
            JDRequirement(
                id="r2",
                requirement_text="Experience with SQL databases such as PostgreSQL or MySQL",
                category=RequirementCategory.SKILL,
                priority=RequirementPriority.REQUIRED,
                extracted_keywords=["SQL", "PostgreSQL", "MySQL"]
            ),
            JDRequirement(
                id="r3",
                requirement_text="Hands-on experience with containerization using Docker or Kubernetes",
                category=RequirementCategory.SKILL,
                priority=RequirementPriority.PREFERRED,
                extracted_keywords=["Docker", "Kubernetes"]
            ),
            JDRequirement(
                id="r4",
                requirement_text="Cloud infrastructure on AWS or GCP",
                category=RequirementCategory.SKILL,
                priority=RequirementPriority.PREFERRED,
                extracted_keywords=["AWS", "GCP", "cloud"]
            )
        ]
    )

    # 3. Parse and analyze resumes
    candidates = []
    processed_count = 0
    crash_count = 0

    for pdf in all_files:
        try:
            doc = parser.parse_pdf(pdf)
            profile = analyzer.analyze(doc)
            candidates.append(profile)
            processed_count += 1
        except Exception as e:
            print(f"Error processing {pdf.name}: {e}")
            crash_count += 1

    # 4. Rank candidates
    ranked_results = ranking_service.rank_candidates(jd, candidates)
    print(f"Successfully ranked {len(ranked_results)} candidates.")

    # 5. Generate explanations
    explanations = explanation_engine.explain_all(ranked_results, jd)
    print(f"Generated {len(explanations)} candidate explanations.")

    # 6. Verify explanation structure and constraints
    verification_errors = []
    top_3_count = 0

    for expl in explanations:
        total_req_breakdowns = (
            len(expl.matched_requirements) +
            len(expl.partial_requirements) +
            len(expl.missing_required_requirements) +
            len(expl.missing_preferred_requirements)
        )
        if total_req_breakdowns != len(jd.requirements):
            verification_errors.append(
                f"Candidate {expl.candidate_id} has {total_req_breakdowns} req breakdowns, expected {len(jd.requirements)}"
            )

        if expl.rank <= 3:
            top_3_count += 1
            if not expl.why_ranked_here:
                verification_errors.append(f"Candidate {expl.candidate_id} (Rank {expl.rank}) missing why_ranked_here")
            if not expl.summary:
                verification_errors.append(f"Candidate {expl.candidate_id} (Rank {expl.rank}) missing summary")
            if len(expl.strengths) == 0:
                verification_errors.append(f"Candidate {expl.candidate_id} (Rank {expl.rank}) missing strengths")

        all_reqs = (
            expl.matched_requirements +
            expl.partial_requirements +
            expl.missing_required_requirements +
            expl.missing_preferred_requirements
        )
        for req_exp in all_reqs:
            if not req_exp.explanation:
                verification_errors.append(f"Candidate {expl.candidate_id} req {req_exp.requirement_id} has empty explanation")
            # Provenance checks
            for ev in req_exp.supporting_evidence:
                if not ev.evidence_text:
                    verification_errors.append(f"Empty evidence text in {expl.candidate_id}")
                if not ev.evidence_type:
                    verification_errors.append(f"Empty evidence type in {expl.candidate_id}")

    elapsed_time = time.time() - start_time

    print("\n" + "="*60)
    print("EXPLANATION SMOKE TEST REPORT")
    print("="*60)
    print(f"Resumes discovered: {len(all_files)}")
    print(f"Resumes parsed: {processed_count}")
    print(f"Parse crashes: {crash_count}")
    print(f"Candidates ranked: {len(ranked_results)}")
    print(f"Explanations generated: {len(explanations)}")
    print(f"Top 3 explanations verified: {top_3_count == min(3, len(ranked_results))}")
    print(f"Verification errors: {len(verification_errors)}")
    print(f"Total smoke test runtime: {elapsed_time:.2f}s")

    if verification_errors:
        print("\nErrors encountered:")
        for err in verification_errors[:10]:
            print(f"  - {err}")
    else:
        print("ALL VERIFICATIONS PASSED CLEANLY.")

    # 7. Print Sample Top-3 and Bottom-1 Explanations
    print("\n" + "-"*60)
    print("SAMPLE EXPLANATIONS")
    print("-"*60)
    for expl in explanations[:3]:
        print(f"\n[RANK {expl.rank}] Candidate: {expl.candidate_name or expl.candidate_id} | Score: {expl.overall_score:.1f}")
        print(f"Why Ranked Here:\n  {expl.why_ranked_here}")
        print(f"Summary:\n  {expl.summary}")
        print(f"Strengths ({len(expl.strengths)}):")
        for s in expl.strengths:
            print(f"  * {s}")
        if expl.missing_required_requirements:
            print(f"Missing Required ({len(expl.missing_required_requirements)}):")
            for m in expl.missing_required_requirements:
                print(f"  * {m.requirement_text}")
        print("Requirement Breakdowns:")
        all_reqs = expl.matched_requirements + expl.partial_requirements + expl.missing_required_requirements + expl.missing_preferred_requirements
        for rb in all_reqs:
            print(f"  - [{rb.verdict.value}] {rb.requirement_text[:50]}... -> {rb.explanation} ({rb.contribution_to_score:.1f} pts)")
            for ev in rb.supporting_evidence:
                print(f"      [Evidence ({ev.evidence_type})]: \"{ev.evidence_text[:60]}\" (page {ev.page_number or 'N/A'}, sec {ev.source_section or 'N/A'}, method={ev.match_method})")

    if len(explanations) > 3:
        bottom = explanations[-1]
        print(f"\n[RANK {bottom.rank}] Candidate: {bottom.candidate_name or bottom.candidate_id} | Score: {bottom.overall_score:.1f}")
        print(f"Why Ranked Here: {bottom.why_ranked_here}")
        print(f"Summary: {bottom.summary}")
        if bottom.missing_required_requirements:
            print(f"Missing Required ({len(bottom.missing_required_requirements)}):")
            for m in bottom.missing_required_requirements[:3]:
                print(f"  * {m.requirement_text}")

if __name__ == "__main__":
    main()
