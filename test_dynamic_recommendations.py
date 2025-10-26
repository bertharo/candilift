#!/usr/bin/env python3
"""
Test the new dynamic job recommendations
"""
import sys
import os
from typing import Dict, Any

# Add current directory to Python path
sys.path.insert(0, os.path.abspath('.'))

from analysis_engine import AnalysisEngine

def test_dynamic_job_recommendations():
    engine = AnalysisEngine()
    
    # Test with a job that has specific skills
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
    
    # Job with specific skills (like from a real job posting)
    job_data = {
        'required_skills': {
            'programming': ['Python', 'JavaScript', 'Express', 'Node.js'],
            'database': ['MongoDB', 'PostgreSQL'],
            'tools': ['Docker', 'AWS']
        },
        'optional_skills': {},
        'requirements': {
            'years_experience_required': 2,
            'seniority': 'mid-level'
        }
    }
    
    print("Testing dynamic job recommendations with specific job skills...")
    print(f"Resume skills: {resume_data['skills']}")
    print(f"Job skills: {job_data['required_skills']}")
    print()
    
    # Test the job recommendation function directly
    recommendations = engine._generate_job_recommendations(resume_data, job_data)
    
    print("Dynamic Job Recommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['title']} - {rec['match_score']}% match")
        print(f"   Description: {rec['description']}")
        print(f"   Required Skills: {rec['required_skills']}")
        print(f"   Reason: {rec['match_reason']}")
        print()
    
    # Test with no job skills (fallback to dynamic generic)
    print("Testing with no job skills (dynamic generic recommendations)...")
    empty_job_data = {
        'required_skills': {},
        'optional_skills': {},
        'requirements': {
            'years_experience_required': 2,
            'seniority': 'mid-level'
        }
    }
    
    generic_recommendations = engine._generate_job_recommendations(resume_data, empty_job_data)
    
    print("Dynamic Generic Job Recommendations:")
    for i, rec in enumerate(generic_recommendations, 1):
        print(f"{i}. {rec['title']} - {rec['match_score']}% match")
        print(f"   Description: {rec['description']}")
        print(f"   Required Skills: {rec['required_skills']}")
        print(f"   Reason: {rec['match_reason']}")
        print()

if __name__ == "__main__":
    test_dynamic_job_recommendations()
