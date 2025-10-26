#!/usr/bin/env python3
"""
Ultimate final test - check every possible scenario
"""
import sys
import os
from typing import Dict, Any

# Add current directory to Python path
sys.path.insert(0, os.path.abspath('.'))

from analysis_engine import AnalysisEngine

def ultimate_final_test():
    engine = AnalysisEngine()
    
    print("=== ULTIMATE FINAL TEST ===")
    
    resume_data = {
        'skills': ['Python', 'JavaScript', 'SQL'],
        'experience': {'years_experience': 3, 'job_titles': ['Developer']},
        'format': {'has_contact_info': True, 'has_summary': True, 'has_experience': True, 'has_education': True, 'has_tables': False, 'has_images': False, 'has_headers_footers': False, 'total_lines': 20, 'word_count': 350}
    }
    
    # Test 1: Job with NO Go/Express
    print("\n1. Job with NO Go/Express:")
    job_data = {
        'required_skills': {
            'programming': ['Python', 'JavaScript'],
            'database': ['SQL', 'PostgreSQL']
        },
        'requirements': {'years_experience_required': 2, 'seniority': 'mid-level'}
    }
    
    recommendations = engine._generate_job_recommendations(resume_data, job_data)
    print("Recommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec['title']} - Skills: {rec['required_skills']}")
    
    # Test 2: Empty job (fallback)
    print("\n2. Empty job (fallback):")
    empty_job = {
        'required_skills': {},
        'requirements': {'years_experience_required': 2, 'seniority': 'mid-level'}
    }
    
    fallback_recs = engine._generate_job_recommendations(resume_data, empty_job)
    print("Fallback recommendations:")
    for i, rec in enumerate(fallback_recs, 1):
        print(f"  {i}. {rec['title']} - Skills: {rec['required_skills']}")
    
    # Test 3: Check for any hardcoded Go/Express
    print("\n3. Checking for hardcoded Go/Express:")
    all_skills = []
    for rec in recommendations + fallback_recs:
        all_skills.extend(rec['required_skills'])
    
    unwanted = [skill for skill in all_skills if skill.lower() in ['go', 'express']]
    if unwanted:
        print(f"  ❌ FOUND: {unwanted}")
    else:
        print("  ✅ NO hardcoded Go/Express found")
    
    # Test 4: Test job title inference
    print("\n4. Testing job title inference:")
    test_skills = {'python', 'javascript', 'sql'}
    title = engine._infer_job_title(test_skills)
    print(f"  Skills: {test_skills} -> Title: {title}")
    
    # Test 5: Test entry-level skills
    print("\n5. Testing entry-level skills:")
    entry_skills = engine._get_entry_level_skills(['Python', 'JavaScript', 'SQL'], {'Python', 'JavaScript'})
    print(f"  Entry-level skills: {entry_skills}")
    
    # Test 6: Test most relevant skills
    print("\n6. Testing most relevant skills:")
    relevant_skills = engine._get_most_relevant_skills(['Python', 'JavaScript', 'SQL'], {'Python', 'JavaScript'})
    print(f"  Most relevant skills: {relevant_skills}")
    
    print("\n=== ULTIMATE TEST COMPLETE ===")

if __name__ == "__main__":
    ultimate_final_test()
