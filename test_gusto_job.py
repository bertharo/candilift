#!/usr/bin/env python3
"""
Test with the actual Gusto job posting to see what skills are extracted
"""
import sys
import os
from typing import Dict, Any

# Add current directory to Python path
sys.path.insert(0, os.path.abspath('.'))

from analysis_engine import AnalysisEngine

def test_gusto_job():
    engine = AnalysisEngine()
    
    print("=== TESTING WITH ACTUAL GUSTO JOB POSTING ===")
    
    # The actual Gusto job description
    gusto_job_description = """
    Senior Product Manager, Core Experiences Platform
    
    About Gusto
    At Gusto, we're on a mission to grow the small business economy. We handle the hard stuff—like payroll, health insurance, 401(k)s, and HR—so owners can focus on their craft and customers. With teams in Denver, San Francisco, and New York, we're proud to support more than 400,000 small businesses across the country, and we're building a workplace that represents and celebrates the customers we serve.
    
    What Product Management is like at Gusto:
    We're looking for high-autonomy, entrepreneurial Product Managers to come build high-impact solutions for small businesses and their employees. We believe in high-ownership Product Managers who operate like business owners - owning an entire roadmap end to end and shipping product all the way from strategy through to the nitty gritty details.
    
    About the Team:
    The Core Experiences Platform teams encompass the foundational data models, APIs, and UX concepts (or "commons") that teams across Gusto leverage to build high quality, cohesive experiences at scale. We think globally about how to craft a thoughtful system of apps and experiences — considering the full stack — so that App teams can focus more locally on solving their unique jobs to be done.
    
    Here's what you'll do day-to-day:
    Ownership: Craft a holistic vision grounded and lead the long-term product strategy for how Gusto represents more complex companies in both our data models and product experiences.
    North Star: Your goal is to evolve Gusto's data model and product experience to unlock new business opportunities for companies with more complex tax reporting structures.
    Collaborate: Work closely with Design, Engineering, Data, and peer Product teams to drive the roadmap forward.
    Problem Framing & Research: Distill insights and data from key stakeholders, industry trends, competitive analysis, business and product metrics, and other sources to guide strategy.
    Roadmapping & Prioritization: Set goals and strategy for your domain then translate it into a roadmap, milestones, and requirements collaboratively to drive alignment and excitement with your cross-functional partners and stakeholders.
    Measure & Communicate: Define success metrics that reflect adoption, usage, and system health.
    
    Here's what we're looking for:
    5+ years of product management experience driving platforms and systems including experience with building 0-1 platforms with
    3+ years with data modeling and/or architecture experience
    Experience driving high growth of product from launch phase to scaled adoption
    Ability to set a strategy and translate to a roadmap & metrics with end-to-end execution
    Data and hypothesis driven, business-minded
    Experience collaborating with multiple stakeholders to build scalable platforms
    Creating and growing diverse and passionate product teams
    Zest for learning and first principles thinking
    """
    
    print("Job description preview:")
    print(gusto_job_description[:200] + "...")
    
    # Test job skills extraction
    job_skills = engine.job_analyzer.extract_required_skills(gusto_job_description)
    print(f"\nExtracted job skills: {job_skills}")
    
    # Check for problematic skills
    all_job_skills = []
    for category_skills in job_skills.values():
        all_job_skills.extend(category_skills)
    
    problematic_skills = [skill for skill in all_job_skills if skill.lower() in ['go', 'express', 'ai']]
    if problematic_skills:
        print(f"❌ FOUND PROBLEMATIC SKILLS: {problematic_skills}")
        print("These skills are being incorrectly extracted from the job description!")
    else:
        print(f"✅ No problematic skills found in job extraction")
    
    # Test with a resume
    resume_data = {
        'skills': ['Python', 'JavaScript', 'SQL', 'Product Management'],
        'experience': {'years_experience': 5, 'job_titles': ['Product Manager']},
        'format': {'has_contact_info': True, 'has_summary': True, 'has_experience': True, 'has_education': True, 'has_tables': False, 'has_images': False, 'has_headers_footers': False, 'total_lines': 20, 'word_count': 350}
    }
    
    # Create job data
    job_data = {
        'required_skills': job_skills,
        'requirements': {'years_experience_required': 5, 'seniority': 'senior'}
    }
    
    # Test the full analysis
    result = engine.analyze(
        resume_file_content=b"fake resume content",
        resume_filename="test.pdf",
        job_description=gusto_job_description,
        job_url=""
    )
    
    print(f"\nJob recommendations:")
    if result.get('job_recommendations'):
        for i, rec in enumerate(result['job_recommendations'], 1):
            print(f"  {i}. {rec['title']} - Skills: {rec['required_skills']}")
    
    # Check if Go, Express, AI appear in recommendations
    all_skills = []
    if result.get('job_recommendations'):
        for rec in result['job_recommendations']:
            all_skills.extend(rec.get('required_skills', []))
    
    problematic_skills = [skill for skill in all_skills if skill.lower() in ['go', 'express', 'ai']]
    if problematic_skills:
        print(f"\n❌ FOUND PROBLEMATIC SKILLS IN RECOMMENDATIONS: {problematic_skills}")
        print("This is the bug you're seeing!")
    else:
        print(f"\n✅ No problematic skills found in recommendations")
    
    print("\n=== GUSTO JOB TEST COMPLETE ===")

if __name__ == "__main__":
    test_gusto_job()
