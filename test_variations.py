#!/usr/bin/env python3
"""
Test the job recommendation variations
"""
import sys
import os
from typing import Dict, Any

# Add current directory to Python path
sys.path.insert(0, os.path.abspath('.'))

from analysis_engine import AnalysisEngine

def test_job_variations():
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
    
    # Job with specific skills
    job_data = {
        'required_skills': {
            'programming': ['Python', 'JavaScript', 'Java', 'Go'],
            'web': ['Node.js', 'Express'],
            'database': ['MongoDB'],
            'cloud': ['AWS', 'Docker'],
            'data': ['AI']
        },
        'optional_skills': {},
        'requirements': {
            'years_experience_required': 2,
            'seniority': 'mid-level'
        }
    }
    
    print("Testing job variations...")
    print(f"Resume skills: {resume_data['skills']}")
    
    # Get all job skills
    all_job_skills = set()
    for category_skills in job_data['required_skills'].values():
        all_job_skills.update(category_skills)
    print(f"All job skills: {list(all_job_skills)}")
    print()
    
    # Test entry-level skills
    entry_skills = engine._get_entry_level_skills(list(all_job_skills), set(resume_data['skills']))
    print(f"Entry-level skills: {entry_skills}")
    
    # Test match reasons for different skill sets
    print("\nTesting match reasons:")
    print(f"Similar role skills: {list(all_job_skills)}")
    print(f"Match reason: {engine._get_match_reason(70, resume_data['skills'], list(all_job_skills))}")
    
    print(f"Entry-level skills: {entry_skills}")
    print(f"Match reason: {engine._get_match_reason(70, resume_data['skills'], entry_skills)}")
    
    senior_skills = list(all_job_skills) + ['leadership', 'mentoring', 'architecture']
    print(f"Senior skills: {senior_skills}")
    print(f"Match reason: {engine._get_match_reason(50, resume_data['skills'], senior_skills)}")

if __name__ == "__main__":
    test_job_variations()
