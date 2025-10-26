#!/usr/bin/env python3
"""
Debug what's actually happening with job parsing
"""
import sys
import os
from typing import Dict, Any

# Add current directory to Python path
sys.path.insert(0, os.path.abspath('.'))

from analysis_engine import AnalysisEngine

def debug_real_job_parsing():
    engine = AnalysisEngine()
    
    # Test with a job that DOES contain Go and Express (like your actual job)
    test_job_url = "https://example.com/job-posting"
    test_job_text = """
    Backend Developer Position
    
    We are looking for a Backend Developer with experience in:
    - Go programming language
    - Express.js framework
    - Node.js development
    - Python scripting
    - JavaScript development
    - MongoDB database
    - Docker containerization
    - AWS cloud services
    
    Requirements:
    - 3+ years of experience
    - Bachelor's degree in Computer Science
    - Strong problem-solving skills
    """
    
    print("Testing job parsing with Go and Express (like your actual job)...")
    print(f"Job text: {test_job_text[:200]}...")
    print()
    
    # Test skill extraction
    job_skills = engine.job_analyzer.extract_required_skills(test_job_text)
    print("Extracted job skills:")
    for category, skills in job_skills.items():
        print(f"  {category}: {skills}")
    print()
    
    # Test full analysis
    resume_data = {
        'skills': ['Python', 'JavaScript', 'SQL', 'React'],
        'experience': {'years_experience': 3, 'job_titles': ['Developer']},
        'format': {
            'has_contact_info': True,
            'has_summary': True,
            'has_experience': True,
            'has_education': True,
            'has_tables': False,
            'has_images': False,
            'has_headers_footers': False,
            'total_lines': 20,
            'word_count': 350
        }
    }
    
    job_data = {
        'required_skills': job_skills,
        'requirements': {
            'years_experience_required': 2,
            'seniority': 'mid-level'
        },
        'text': test_job_text[:500]
    }
    
    print("Testing job recommendations with REAL job data...")
    recommendations = engine._generate_job_recommendations(resume_data, job_data)
    
    print("Job Recommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['title']} - {rec['match_score']}% match")
        print(f"   Required Skills: {rec['required_skills']}")
        print(f"   Reason: {rec['match_reason']}")
        print()

if __name__ == "__main__":
    debug_real_job_parsing()
