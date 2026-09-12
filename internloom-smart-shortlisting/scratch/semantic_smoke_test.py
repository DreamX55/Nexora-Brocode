import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath('backend'))
from app.services.document_parser import DocumentParser
from app.services.resume_analyzer.analyzer import ResumeAnalyzer
from app.services.semantic_matcher import LocalSentenceTransformerEmbeddingModel, SemanticMatcher
from app.schemas.domain import JDRequirement, RequirementCategory
import uuid

def main():
    ext_dir = Path("data/external_resumes")
    all_files = list(ext_dir.rglob("*.pdf"))
    
    parser = DocumentParser()
    analyzer = ResumeAnalyzer()
    
    # Load model and matcher
    model = LocalSentenceTransformerEmbeddingModel("all-MiniLM-L6-v2")
    matcher = SemanticMatcher(model)
    
    req = JDRequirement(
        id=str(uuid.uuid4()),
        requirement_text="Experience with Python and backend development",
        category=RequirementCategory.EXPERIENCE,
        is_required=True
    )
    
    success_count = 0
    crash_count = 0
    total = len(all_files)
    
    for pdf in all_files:
        if pdf.name.startswith('.'):
            total -= 1
            continue
            
        try:
            doc = parser.parse_pdf(pdf)
            profile = analyzer.analyze(doc)
            
            results = matcher.evaluate_requirement(req, profile)
            # Just verifying no crash and provenance is accessible
            for r in results:
                _ = r.similarity_score
                _ = r.source_text
            success_count += 1
            
        except Exception as e:
            print(f"Crash on {pdf.name}: {e}")
            crash_count += 1
            
    print(f"Smoke Test Results: Processed={success_count}/{total}, Crashes={crash_count}")
    
if __name__ == "__main__":
    main()
