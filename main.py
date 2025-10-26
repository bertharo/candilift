"""
FastAPI main application for CandiLift MVP
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting CandiLift API...")
    
    # Create exports directory if it doesn't exist
    os.makedirs("exports", exist_ok=True)
    
    yield
    
    # Shutdown
    print("🛑 Shutting down CandiLift API...")


app = FastAPI(
    title="CandiLift API",
    description="MVP for resume analysis and optimization",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "candilift-api"}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "CandiLift API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/healthz"
    }

@app.post("/analyze")
async def analyze_resume(
    resume_file: UploadFile = File(...),
    job_description: str = Form(""),
    job_url: str = Form(""),
    ats_platform: str = Form("generic")
):
    """Analyze resume against job description"""
    try:
        # Basic validation
        if not resume_file:
            raise HTTPException(status_code=400, detail="Resume file is required")
        
        if not job_description and not job_url:
            raise HTTPException(status_code=400, detail="Job description or URL is required")
        
        # Mock response for now
        result = {
            "ats_score": 78,
            "recruiter_score": 85,
            "score_drivers": [
                {
                    "component": "Keyword Matching",
                    "score": 82,
                    "explanation": "Good keyword alignment with job requirements"
                },
                {
                    "component": "Format Compliance", 
                    "score": 75,
                    "explanation": "Resume format is mostly ATS-friendly"
                },
                {
                    "component": "Experience Relevance",
                    "score": 88,
                    "explanation": "Strong relevant experience demonstrated"
                }
            ],
            "recommendations": [
                {
                    "category": "Skills Enhancement",
                    "description": "Add more specific technical skills mentioned in the job description",
                    "estimated_lift": 12,
                    "example": "Instead of 'experienced with databases', use '5+ years PostgreSQL, MongoDB'"
                },
                {
                    "category": "Quantify Achievements",
                    "description": "Add more metrics and numbers to your accomplishments",
                    "estimated_lift": 8,
                    "example": "Increased team productivity by 25% through process optimization"
                }
            ],
            "gap_analysis": {
                "missing_skills": ["Python", "Machine Learning", "AWS"],
                "present_skills": ["JavaScript", "React", "Node.js", "SQL"]
            }
        }
        
        return result
        
    except Exception as e:
        print(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)