from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import Dict, List, Optional
import os
import sys
import tempfile
import json
from datetime import datetime

# Add the parent directory to Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from services.resume_parser import ResumeParser
from services.job_parser import JobDescriptionParser
from services.keyword_analyzer import KeywordAnalyzer
from services.formatting_checker import FormattingChecker
from services.impact_analyzer import ImpactAnalyzer
from services.scoring_engine import ScoringEngine
from services.recommendation_engine import RecommendationEngine
from services.url_scraper import JobPostingScraper
from services.ats_simulator import ATSSimulator
from models.analysis_result import AnalysisResult

app = FastAPI(title="ATS Resume Reviewer", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://rats-lilac.vercel.app",  # Vercel frontend
        "https://*.vercel.app"  # Any Vercel subdomain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
resume_parser = ResumeParser()
job_parser = JobDescriptionParser()
keyword_analyzer = KeywordAnalyzer()
formatting_checker = FormattingChecker()
impact_analyzer = ImpactAnalyzer()
scoring_engine = ScoringEngine()
recommendation_engine = RecommendationEngine()
url_scraper = JobPostingScraper()
ats_simulator = ATSSimulator()

@app.get("/")
async def root():
    return {"message": "ATS Resume Reviewer API", "version": "1.0.0"}

@app.get("/test")
async def test_ats():
    """Test endpoint to debug ATS simulator"""
    try:
        from models.resume_data import ResumeData, ContactInfo
        from models.job_data import JobData, JobSkill, SkillType
        
        # Create test data
        resume_data = ResumeData(
            raw_text="John Doe\nSoftware Engineer\nPython, JavaScript",
            contact_info=ContactInfo(name="John Doe", email="john@email.com"),
            sections={"summary": "Software Engineer", "experience": "Tech Corp"},
            experience=[],
            education=[],
            skills=[]
        )
        
        job_data = JobData(
            title="Software Engineer",
            company="Tech Corp",
            raw_text="Python developer needed",
            required_skills=[JobSkill(name="Python", skill_type=SkillType.TECHNICAL_SKILL, importance=8.0, frequency=3)],
            preferred_skills=[],
            seniority_level="mid",
            years_experience=3,
            key_phrases=["Python", "Software Engineer"],
            responsibilities=["Develop applications", "Write code"],
            qualifications=["Bachelor's degree", "3+ years experience"]
        )
        
        # Test ATS simulator
        ats_result = ats_simulator.simulate_ats_analysis(resume_data, job_data, "workday")
        return {"status": "success", "ats_result": ats_result}
        
    except Exception as e:
        import traceback
        return {"status": "error", "error": str(e), "traceback": traceback.format_exc()}

@app.post("/analyze")
async def analyze_resume(
    resume_file: UploadFile = File(...),
    job_description: str = "",
    job_description_file: Optional[UploadFile] = File(None),
    job_url: Optional[str] = None,
    ats_platform: Optional[str] = None
):
    """
    Analyze a resume against a job description for ATS compliance and optimization.
    """
    try:
        # Debug: Log what we received
        print(f"DEBUG - Received parameters:")
        print(f"  resume_file: {resume_file.filename if resume_file else 'None'}")
        print(f"  job_description: '{job_description}'")
        print(f"  job_description_file: {job_description_file.filename if job_description_file else 'None'}")
        print(f"  job_url: '{job_url}'")
        print(f"  ats_platform: '{ats_platform}'")
        
        # Validate file types
        if not resume_file.filename or not resume_file.filename.lower().endswith(('.pdf', '.docx')):
            raise HTTPException(status_code=400, detail="Resume must be PDF or DOCX format")
        
        # Check if file is empty
        content = await resume_file.read()
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Resume file is empty")
        
        # Reset file pointer for processing
        await resume_file.seek(0)
        
        # Parse job description
        if job_url:
            # Extract job description from URL
            try:
                job_info = url_scraper.scrape_job_posting(job_url)
                job_description = job_info['description']
                if not job_description.strip():
                    raise HTTPException(status_code=400, detail="Could not extract job description from URL")
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Failed to scrape job posting: {str(e)}")
        elif job_description_file:
            if not job_description_file.filename.lower().endswith(('.pdf', '.docx', '.txt')):
                raise HTTPException(status_code=400, detail="Job description file must be PDF, DOCX, or TXT format")
            job_description = await parse_job_description_file(job_description_file)
        
        if not job_description or not job_description.strip():
            raise HTTPException(status_code=400, detail="Job description is required (provide text, file, or URL)")
        
        # Save resume to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{resume_file.filename.split('.')[-1]}") as temp_file:
            content = await resume_file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Parse resume
            resume_data = resume_parser.parse(temp_file_path)
            
            # Parse job description
            job_data = job_parser.parse(job_description)
            
            # Perform ATS simulation analysis
            ats_analysis = ats_simulator.simulate_ats_analysis(resume_data, job_data, ats_platform)
            
            # Perform detailed analysis
            keyword_analysis = keyword_analyzer.analyze(resume_data, job_data)
            formatting_analysis = formatting_checker.check(resume_data)
            impact_analysis = impact_analyzer.analyze(resume_data)
            
            # Calculate additional scores
            recruiter_score = scoring_engine.calculate_recruiter_score(impact_analysis, formatting_analysis)
            
            # Generate recommendations
            recommendations = recommendation_engine.generate_recommendations(
                keyword_analysis, formatting_analysis, impact_analysis, 
                ats_analysis['ats_score'], recruiter_score
            )
            
            # Add ATS-specific recommendations
            if ats_platform:
                ats_recommendations = ats_simulator.get_ats_platform_recommendations(ats_platform)
                for rec_text in ats_recommendations:
                    recommendations.append({
                        'category': 'ats_platform',
                        'severity': 'major',
                        'title': f'{ats_analysis["ats_platform"]} Optimization',
                        'description': rec_text,
                        'priority_score': 7.0
                    })
            
            # Create analysis result with ATS simulation data
            result = AnalysisResult(
                resume_filename=resume_file.filename,
                analysis_timestamp=datetime.now(),
                ats_score=ats_analysis['ats_score'],
                recruiter_score=recruiter_score,
                keyword_analysis=keyword_analysis,
                formatting_analysis=formatting_analysis,
                impact_analysis=impact_analysis,
                recommendations=recommendations,
                # Add ATS simulation data
                ats_platform=ats_analysis.get('ats_platform', 'Generic ATS'),
                processing_time=ats_analysis.get('processing_time', 0),
                ats_quirks=ats_analysis.get('ats_quirks', []),
                platform_weights=ats_analysis.get('platform_weights', {})
            )
            
            return result.dict()
            
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)
            
    except HTTPException as e:
        # Re-raise HTTP exceptions as-is
        raise e
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in analysis: {error_details}")  # Log the full error
        print(f"Exception type: {type(e).__name__}")
        print(f"Exception message: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

async def parse_job_description_file(file: UploadFile) -> str:
    """Parse job description from uploaded file."""
    content = await file.read()
    
    if file.filename.lower().endswith('.txt'):
        return content.decode('utf-8')
    elif file.filename.lower().endswith(('.pdf', '.docx')):
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')[-1]}") as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            if file.filename.lower().endswith('.pdf'):
                return resume_parser.parse_pdf(temp_file_path)
            else:
                return resume_parser.parse_docx(temp_file_path)
        finally:
            os.unlink(temp_file_path)
    else:
        raise HTTPException(status_code=400, detail="Unsupported job description file format")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
