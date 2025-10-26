#!/usr/bin/env python3
"""
Final comprehensive review - test ALL scenarios
"""
import sys
import os
from typing import Dict, Any

# Add current directory to Python path
sys.path.insert(0, os.path.abspath('.'))

from analysis_engine import AnalysisEngine

def final_comprehensive_review():
    engine = AnalysisEngine()
    
    print("=== FINAL COMPREHENSIVE REVIEW ===")
    
    # Test 1: Job with Go and Express (should show them if they're in the job)
    print("\n1. Testing job WITH Go and Express:")
    job_with_go_express = {
        'required_skills': {
            'programming': ['Go', 'Python', 'JavaScript'],
            'web': ['Express', 'Node.js'],
            'database': ['MongoDB']
        }
    }
    
    resume_data = {
        'skills': ['Python', 'JavaScript', 'SQL'],
        'experience': {'years_experience': 3, 'job_titles': ['Developer']},
        'format': {'has_contact_info': True, 'has_summary': True, 'has_experience': True, 'has_education': True, 'has_tables': False, 'has_images': False, 'has_headers_footers': False, 'total_lines': 20, 'word_count': 350}
    }
    
    job_data = {
        'required_skills': job_with_go_express['required_skills'],
        'requirements': {'years_experience_required': 2, 'seniority': 'mid-level'}
    }
    
    recommendations = engine._generate_job_recommendations(resume_data, job_data)
    print("Job recommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec['title']} - Skills: {rec['required_skills']}")
    
    # Test 2: Job WITHOUT Go and Express (should NOT show them)
    print("\n2. Testing job WITHOUT Go and Express:")
    job_without_go_express = {
        'required_skills': {
            'programming': ['Python', 'JavaScript'],
            'database': ['SQL', 'PostgreSQL']
        }
    }
    
    job_data2 = {
        'required_skills': job_without_go_express['required_skills'],
        'requirements': {'years_experience_required': 2, 'seniority': 'mid-level'}
    }
    
    recommendations2 = engine._generate_job_recommendations(resume_data, job_data2)
    print("Job recommendations:")
    for i, rec in enumerate(recommendations2, 1):
        print(f"  {i}. {rec['title']} - Skills: {rec['required_skills']}")
    
    # Test 3: Empty job data (fallback)
    print("\n3. Testing fallback with empty job data:")
    empty_job_data = {
        'required_skills': {},
        'requirements': {'years_experience_required': 2, 'seniority': 'mid-level'}
    }
    
    recommendations3 = engine._generate_job_recommendations(resume_data, empty_job_data)
    print("Fallback recommendations:")
    for i, rec in enumerate(recommendations3, 1):
        print(f"  {i}. {rec['title']} - Skills: {rec['required_skills']}")
    
    # Test 4: Check if Go/Express appear in any recommendations when they shouldn't
    print("\n4. Checking for unwanted Go/Express in recommendations:")
    all_skills = []
    for rec in recommendations2 + recommendations3:
        all_skills.extend(rec['required_skills'])
    
    unwanted_skills = [skill for skill in all_skills if skill.lower() in ['go', 'express']]
    if unwanted_skills:
        print(f"  ❌ FOUND UNWANTED SKILLS: {unwanted_skills}")
    else:
        print("  ✅ No unwanted Go/Express found in recommendations")
    
    print("\n=== REVIEW COMPLETE ===")

if __name__ == "__main__":
    final_comprehensive_review()
