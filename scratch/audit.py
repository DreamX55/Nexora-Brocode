import os
import zipfile
import hashlib
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath('backend'))

from app.services.document_parser import DocumentParser
from app.services.resume_analyzer.analyzer import ResumeAnalyzer

def main():
    ext_dir = Path("data/external_resumes")
    all_files = []
    for root, _, files in os.walk(ext_dir):
        for f in files:
            if not f.startswith('.'):
                all_files.append(Path(root) / f)
                
    unique_pdfs = [f for f in all_files if f.suffix.lower() == '.pdf']
    
    parser_results = []
    analyzer_results = []
    
    parser = DocumentParser()
    analyzer = ResumeAnalyzer()
    
    for pdf in unique_pdfs:
        try:
            doc = parser.parse_pdf(pdf)
            parser_results.append({
                "file": pdf.name,
                "success": True,
                "pages": len(doc.pages) if hasattr(doc, 'pages') else 0,
                "text_len": len(doc.raw_text) if hasattr(doc, 'raw_text') else (len(doc.text) if hasattr(doc, 'text') else 0),
                "sections": len(doc.sections) if hasattr(doc, 'sections') else 0,
                "doc": doc
            })
            
            try:
                profile = analyzer.analyze(doc)
                analyzer_results.append({
                    "file": pdf.name,
                    "success": True,
                    "name": profile.name,
                    "has_email": bool(profile.email),
                    "has_phone": bool(profile.phone),
                    "skills_count": len(profile.skills) if profile.skills else 0,
                    "experience_count": len(profile.experience) if profile.experience else 0,
                    "education_count": len(profile.education) if profile.education else 0,
                    "projects_count": len(profile.projects) if profile.projects else 0,
                    "cert_count": len(profile.certifications) if profile.certifications else 0
                })
            except Exception as ae:
                analyzer_results.append({
                    "file": pdf.name,
                    "success": False,
                    "error": str(ae)
                })
                
        except Exception as e:
            parser_results.append({
                "file": pdf.name,
                "success": False,
                "error": str(e)
            })
            
    parsed_ok = [r for r in parser_results if r["success"]]
    parsed_fail = [r for r in parser_results if not r["success"]]
    analyzed_ok = [r for r in analyzer_results if r["success"]]
    analyzed_fail = [r for r in analyzer_results if not r["success"]]
    
    print(f"Parser: Success={len(parsed_ok)} Fail={len(parsed_fail)}")
    print(f"Analyzer: Success={len(analyzed_ok)} Fail={len(analyzed_fail)}")
    
    if analyzed_ok:
        names = [r for r in analyzed_ok if r["name"]]
        print(f"Names extracted: {len(names)}/{len(analyzed_ok)}")
        skills = [r for r in analyzed_ok if r["skills_count"] > 0]
        print(f"Skills extracted: {len(skills)}/{len(analyzed_ok)}")
        exp = [r for r in analyzed_ok if r["experience_count"] > 0]
        print(f"Experience extracted: {len(exp)}/{len(analyzed_ok)}")
        edu = [r for r in analyzed_ok if r["education_count"] > 0]
        print(f"Education extracted: {len(edu)}/{len(analyzed_ok)}")
        cert = [r for r in analyzed_ok if r["cert_count"] > 0]
        print(f"Certifications extracted: {len(cert)}/{len(analyzed_ok)}")
        proj = [r for r in analyzed_ok if r["projects_count"] > 0]
        print(f"Projects extracted: {len(proj)}/{len(analyzed_ok)}")
        
    for pf in parsed_fail:
        print(f"Parse Fail: {pf['file']} - {pf['error']}")
    for af in analyzed_fail:
        print(f"Analyze Fail: {af['file']} - {af['error']}")

if __name__ == "__main__":
    main()
