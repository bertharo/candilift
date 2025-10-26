#!/usr/bin/env python3
"""
Test what happens when job URL scraping fails
"""
import sys
import os
from typing import Dict, Any

# Add current directory to Python path
sys.path.insert(0, os.path.abspath('.'))

from analysis_engine import AnalysisEngine

def test_failed_job_scraping():
    engine = AnalysisEngine()
    
    # Test with empty job data (simulating failed URL scraping)
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
    
    # Empty job data (simulating failed scraping)
    job_data = {
        'required_skills': {},  # Empty - no skills extracted
        'optional_skills': {},
        'requirements': {
            'years_experience_required': 2,
            'seniority': 'mid-level'
        }
    }
    
    print("Testing fallback when job URL scraping fails...")
    print(f"Resume skills: {resume_data['skills']}")
    print(f"Job skills: {job_data['required_skills']} (empty)")
    print()
    
    # Test the fallback recommendations
    recommendations = engine._generate_job_recommendations(resume_data, job_data)
    
    print("Fallback Job Recommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['title']} - {rec['match_score']}% match")
        print(f"   Required Skills: {rec['required_skills']}")
        print(f"   Reason: {rec['match_reason']}")
        print()

if __name__ == "__main__":
    test_failed_job_scraping()
