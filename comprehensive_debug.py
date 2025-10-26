#!/usr/bin/env python3
"""
Comprehensive test to find where Go and Express are coming from
"""
import sys
import os
from typing import Dict, Any

# Add current directory to Python path
sys.path.insert(0, os.path.abspath('.'))

from analysis_engine import AnalysisEngine

def comprehensive_debug():
    engine = AnalysisEngine()
    
    # Test with a simple job that should NOT have Go or Express
    resume_data = {
        'skills': ['Python', 'JavaScript', 'SQL'],
        'experience': {'years_experience': 2, 'job_titles': ['Developer']},
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
    
    # Simple job with NO Go or Express
    job_data = {
        'required_skills': {
            'programming': ['Python', 'JavaScript'],
            'database': ['SQL']
        },
        'optional_skills': {},
        'requirements': {
            'years_experience_required': 2,
            'seniority': 'mid-level'
        }
    }
    
    print("=== COMPREHENSIVE DEBUG ===")
    print(f"Resume skills: {resume_data['skills']}")
    
    # Get all job skills
    all_job_skills = set()
    for category_skills in job_data['required_skills'].values():
        all_job_skills.update(category_skills)
    print(f"Job skills: {list(all_job_skills)}")
    print()
    
    # Test job title inference
    job_title = engine._infer_job_title(all_job_skills)
    print(f"Inferred job title: {job_title}")
    
    # Test entry-level skills
    entry_skills = engine._get_entry_level_skills(list(all_job_skills), set(resume_data['skills']))
    print(f"Entry-level skills: {entry_skills}")
    
    # Test most relevant skills
    relevant_skills = engine._get_most_relevant_skills(list(all_job_skills), set(resume_data['skills']))
    print(f"Most relevant skills: {relevant_skills}")
    print()
    
    # Test the full recommendation process
    print("=== FULL RECOMMENDATIONS ===")
    recommendations = engine._generate_job_recommendations(resume_data, job_data)
    
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['title']} - {rec['match_score']}% match")
        print(f"   Required Skills: {rec['required_skills']}")
        print(f"   Reason: {rec['match_reason']}")
        print()
    
    # Test with empty job data (fallback)
    print("=== FALLBACK TEST ===")
    empty_job_data = {
        'required_skills': {},
        'optional_skills': {},
        'requirements': {
            'years_experience_required': 2,
            'seniority': 'mid-level'
        }
    }
    
    fallback_recommendations = engine._generate_job_recommendations(resume_data, empty_job_data)
    
    for i, rec in enumerate(fallback_recommendations, 1):
        print(f"{i}. {rec['title']} - {rec['match_score']}% match")
        print(f"   Required Skills: {rec['required_skills']}")
        print(f"   Reason: {rec['match_reason']}")
        print()

if __name__ == "__main__":
    comprehensive_debug()
