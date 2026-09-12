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
from app.schemas.domain import (
    JobDescription,
    JDRequirement,
    RequirementCategory,
    RequirementPriority
)
import uuid

def main():
    start_time = time.time()
    ext_dir = Path("data/external_resumes")
    all_files = list(ext_dir.rglob("*.pdf"))
    
    # 1. Initialize services
    parser = DocumentParser()
    analyzer = ResumeAnalyzer()
    keyword_matcher = KeywordMatcher()
    embedding_model = LocalSentenceTransformerEmbeddingModel("all-MiniLM-L6-v2")
    semantic_matcher = SemanticMatcher(embedding_model)
    evaluator = RequirementEvaluator(keyword_matcher, semantic_matcher)
    scoring_engine = ScoringEngine(evaluator)
    ranking_service = RankingService(scoring_engine)
    
    # 2. Representative Job Description
    jd = JobDescription(
        jd_id="jd_fullstack_lead",
        raw_text="Fullstack Software Engineer JD",
        requirements=[
            JDRequirement(
                id="r1",
                requirement_text="Proficiency in Python or backend API development",
                category=RequirementCategory.SKILL,
                priority=RequirementPriority.REQUIRED,
                extracted_keywords=["Python", "API"]
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
                extracted_keywords=["AWS", "GCP"]
            )
        ]
    )
    
    processed_count = 0
    crash_count = 0
    candidates = []
    
    for pdf in all_files:
        if pdf.name.startswith('.'):
            continue
        try:
            doc = parser.parse_pdf(pdf)
            profile = analyzer.analyze(doc)
            candidates.append(profile)
            processed_count += 1
        except Exception as e:
            print(f"Crash parsing {pdf.name}: {e}")
            crash_count += 1
            
    # 3. Score and rank all candidates
    try:
        ranked_results = ranking_service.rank_candidates(jd, candidates)
        ranked_count = len(ranked_results)
        scores = [r.score.overall_score for r in ranked_results]
        min_score = min(scores) if scores else 0.0
        max_score = max(scores) if scores else 0.0
    except Exception as e:
        print(f"Crash ranking candidates: {e}")
        ranked_results = []
        ranked_count = 0
        min_score = 0.0
        max_score = 0.0
        crash_count += 1

    elapsed_time = time.time() - start_time
    print(f"Hybrid Smoke Test Results:")
    print(f"Resumes processed: {processed_count}")
    print(f"Crashes: {crash_count}")
    print(f"Candidates scored: {len(candidates)}")
    print(f"Candidates ranked: {ranked_count}")
    print(f"Score range: [{min_score:.2f}, {max_score:.2f}]")
    print(f"Runtime: {elapsed_time:.2f}s")
    if ranked_results:
        print("\nTop 3 Ranked Candidates:")
        for r in ranked_results[:3]:
            print(f"Rank {r.rank}: {r.candidate_name or r.candidate_id} - Score: {r.score.overall_score:.1f}")
        print("\nBottom 3 Ranked Candidates:")
        for r in ranked_results[-3:]:
            print(f"Rank {r.rank}: {r.candidate_name or r.candidate_id} - Score: {r.score.overall_score:.1f}")

if __name__ == "__main__":
    main()
