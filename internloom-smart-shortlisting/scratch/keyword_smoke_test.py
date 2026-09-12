import os
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.abspath('backend'))
from app.services.document_parser import DocumentParser
from app.services.resume_analyzer.analyzer import ResumeAnalyzer
from app.services.keyword_matcher import KeywordMatcher
from app.schemas.domain import JDRequirement, RequirementCategory
import uuid

def main():
    start_time = time.time()
    ext_dir = Path("data/external_resumes")
    all_files = list(ext_dir.rglob("*.pdf"))
    
    parser = DocumentParser()
    analyzer = ResumeAnalyzer()
    matcher = KeywordMatcher()
    
    # Representative test requirements for keyword smoke test
    reqs = [
        JDRequirement(
            id=str(uuid.uuid4()),
            requirement_text="Proficiency in Python and backend services",
            category=RequirementCategory.SKILL,
            extracted_keywords=["Python", "backend"]
        ),
        JDRequirement(
            id=str(uuid.uuid4()),
            requirement_text="Experience with SQL or relational databases",
            category=RequirementCategory.SKILL,
            extracted_keywords=["SQL", "PostgreSQL", "MySQL"]
        ),
        JDRequirement(
            id=str(uuid.uuid4()),
            requirement_text="Cloud infrastructure using AWS or Docker",
            category=RequirementCategory.SKILL,
            extracted_keywords=["AWS", "Docker"]
        )
    ]
    
    processed_count = 0
    crash_count = 0
    empty_profile_count = 0
    total_valid_files = 0
    
    for pdf in all_files:
        if pdf.name.startswith('.'):
            continue
        total_valid_files += 1
        
        try:
            doc = parser.parse_pdf(pdf)
            profile = analyzer.analyze(doc)
            
            # Check if profile is empty / invalid
            has_content = bool(
                profile.skill_details or
                profile.experience or
                profile.projects or
                profile.education
            )
            if not has_content:
                empty_profile_count += 1
                
            # Run keyword matcher against all test requirements
            for req in reqs:
                results = matcher.evaluate_requirement(req, profile)
                # Verify that provenance fields and results are cleanly accessible
                for r in results:
                    _ = r.matched_keyword
                    _ = r.match_type
                    _ = r.lexical_score
                    _ = r.source_text
                    
            processed_count += 1
            
        except Exception as e:
            print(f"Crash on {pdf.name}: {e}")
            crash_count += 1
            
    elapsed_time = time.time() - start_time
    print(f"Keyword Smoke Test Results:")
    print(f"Processed: {processed_count}/{total_valid_files}")
    print(f"Crashes: {crash_count}")
    print(f"Empty/Invalid profiles: {empty_profile_count}")
    print(f"Execution time: {elapsed_time:.2f}s")

if __name__ == "__main__":
    main()
