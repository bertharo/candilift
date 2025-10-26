#!/usr/bin/env python3
"""
Test the dynamic system fixes
"""
import sys
import os
from typing import Dict, Any

# Add current directory to Python path
sys.path.insert(0, os.path.abspath('.'))

from analysis_engine import AnalysisEngine

def test_dynamic_system():
    engine = AnalysisEngine()
    
    print("=== TESTING DYNAMIC SYSTEM FIXES ===")
    
    # Test 1: Dynamic job title inference
    print("\n1. Testing dynamic job title inference:")
    test_skills = {'python', 'javascript', 'react', 'node.js', 'sql'}
    title = engine._infer_job_title(test_skills)
    print(f"  Skills: {test_skills} -> Title: {title}")
    
    test_skills2 = {'html', 'css', 'javascript', 'react'}
    title2 = engine._infer_job_title(test_skills2)
    print(f"  Skills: {test_skills2} -> Title: {title2}")
    
    test_skills3 = {'kubernetes', 'docker', 'aws', 'terraform'}
    title3 = engine._infer_job_title(test_skills3)
    print(f"  Skills: {test_skills3} -> Title: {title3}")
    
    # Test 2: Dynamic generic recommendations
    print("\n2. Testing dynamic generic recommendations:")
    resume_data = {
        'skills': ['Python', 'JavaScript', 'React', 'SQL'],
        'experience': {'years_experience': 3, 'job_titles': ['Developer']},
        'format': {'has_contact_info': True, 'has_summary': True, 'has_experience': True, 'has_education': True, 'has_tables': False, 'has_images': False, 'has_headers_footers': False, 'total_lines': 20, 'word_count': 350}
    }
    
    empty_job_data = {
        'required_skills': {},
        'requirements': {'years_experience_required': 2, 'seniority': 'mid-level'}
    }
    
    recommendations = engine._generate_job_recommendations(resume_data, empty_job_data)
    print("  Dynamic recommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"    {i}. {rec['title']} - {rec['match_score']}% match")
        print(f"       Skills: {rec['required_skills']}")
        print(f"       Description: {rec['description']}")
        print(f"       Reason: {rec['match_reason']}")
    
    # Test 3: Dynamic skill analysis
    print("\n3. Testing dynamic skill analysis:")
    skill_analysis = engine._analyze_resume_skills({'python', 'javascript', 'react', 'sql'})
    print("  Skill analysis:")
    for role, info in skill_analysis.items():
        if info['skill_count'] > 0:
            print(f"    {role}: {info['skill_count']} skills - {info['title']}")
            print(f"      Description: {info['description']}")
            print(f"      Key skills: {info['key_skills']}")
    
    # Test 4: Dynamic entry-level skills
    print("\n4. Testing dynamic entry-level skills:")
    job_skills = ['Python', 'JavaScript', 'React', 'Kubernetes', 'Docker', 'AWS']
    resume_skills = {'Python', 'JavaScript'}
    entry_skills = engine._get_entry_level_skills(job_skills, resume_skills)
    print(f"  Job skills: {job_skills}")
    print(f"  Resume skills: {resume_skills}")
    print(f"  Entry-level skills: {entry_skills}")
    
    # Test 5: Dynamic most relevant skills
    print("\n5. Testing dynamic most relevant skills:")
    relevant_skills = engine._get_most_relevant_skills(job_skills, resume_skills)
    print(f"  Most relevant skills: {relevant_skills}")
    
    print("\n=== DYNAMIC SYSTEM TEST COMPLETE ===")

if __name__ == "__main__":
    test_dynamic_system()
