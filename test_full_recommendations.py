#!/usr/bin/env python3
"""
Test the full job recommendations with different skills
"""
import sys
import os
from typing import Dict, Any

# Add current directory to Python path
sys.path.insert(0, os.path.abspath('.'))

from analysis_engine import AnalysisEngine

def test_full_recommendations():
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
    
    print("Testing full job recommendations...")
    print(f"Resume skills: {resume_data['skills']}")
    
    # Get all job skills
    all_job_skills = set()
    for category_skills in job_data['required_skills'].values():
        all_job_skills.update(category_skills)
    print(f"All job skills: {list(all_job_skills)}")
    
    # Debug: Test entry-level skills directly
    entry_skills = engine._get_entry_level_skills(list(all_job_skills), set(resume_data['skills']))
    print(f"Entry-level skills (direct): {entry_skills}")
    print()
    
    # Test the full job recommendation function
    recommendations = engine._generate_job_recommendations(resume_data, job_data)
    
    print("Job Recommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['title']} - {rec['match_score']}% match")
        print(f"   Description: {rec['description']}")
        print(f"   Required Skills: {rec['required_skills']}")
        print(f"   Reason: {rec['match_reason']}")
        print()

if __name__ == "__main__":
    test_full_recommendations()
