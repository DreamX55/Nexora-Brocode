import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath('backend'))
from app.services.document_parser import DocumentParser
from app.services.resume_analyzer.analyzer import ResumeAnalyzer

def main():
    ext_dir = Path("data/external_resumes")
    all_files = list(ext_dir.rglob("*.pdf"))
    
    parser = DocumentParser()
    analyzer = ResumeAnalyzer()
    
    for pdf in all_files:
        if pdf.name.startswith('.'): continue
        doc = parser.parse_pdf(pdf)
        profile = analyzer.analyze(doc)
        if len(profile.skills) == 0:
            print(f"Missing skills: {pdf.name}")
        if len(profile.education) == 0:
            print(f"Missing education: {pdf.name}")

if __name__ == "__main__":
    main()
