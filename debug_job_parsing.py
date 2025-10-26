#!/usr/bin/env python3
"""
Debug job parsing and recommendations
"""
import sys
import os
from typing import Dict, Any

# Add current directory to Python path
sys.path.insert(0, os.path.abspath('.'))

from analysis_engine import AnalysisEngine

def debug_job_parsing():
    engine = AnalysisEngine()
    
    # Test job URL scraping
    test_url = "https://example.com/job-posting"
    test_job_text = """
    We are looking for a Software Engineer with experience in:
    - Go programming language
    - Express.js framework
    - Node.js development
    - Python scripting
    - JavaScript frontend development
    - MongoDB database
    - Docker containerization
    - AWS cloud services
    
    Requirements:
    - 3+ years of experience
    - Bachelor's degree in Computer Science
    - Strong problem-solving skills
    """
    
    print("Testing job text parsing...")
    print(f"Job text: {test_job_text[:200]}...")
    print()
    
    # Test skill extraction
    job_skills = engine.job_analyzer.extract_required_skills(test_job_text)
    print("Extracted job skills:")
    for category, skills in job_skills.items():
        print(f"  {category}: {skills}")
    print()
    
    # Test job requirements
    job_requirements = engine.job_analyzer.extract_requirements(test_job_text)
    print("Extracted job requirements:")
    print(f"  Years required: {job_requirements['years_experience_required']}")
    print(f"  Education required: {job_requirements['education_required']}")
    print(f"  Seniority level: {job_requirements['seniority_level']}")
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
        'requirements': job_requirements,
        'text': test_job_text[:500]
    }
    
    print("Testing job recommendations with extracted data...")
    
    # Debug: Show what skills are being passed to recommendations
    all_job_skills = set()
    for category_skills in job_skills.values():
        all_job_skills.update(category_skills)
    print(f"All job skills: {list(all_job_skills)}")
    print(f"Resume skills: {resume_data['skills']}")
    
    # Debug: Test the skill prioritization
    print("\nTesting skill prioritization:")
    resume_skills_set = set(resume_data['skills'])
    relevant_skills = engine._get_most_relevant_skills(list(all_job_skills), resume_skills_set)
    print(f"Most relevant skills: {relevant_skills}")
    print()
    
    recommendations = engine._generate_job_recommendations(resume_data, job_data)
    
    print("Job Recommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['title']} - {rec['match_score']}% match")
        print(f"   Description: {rec['description']}")
        print(f"   Required Skills: {rec['required_skills']}")
        print(f"   Reason: {rec['match_reason']}")
        print()

if __name__ == "__main__":
    debug_job_parsing()
