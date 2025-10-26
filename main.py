"""
FastAPI main application for CandiLift MVP
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import uvicorn
import os
from contextlib import asynccontextmanager
from analysis_engine import AnalysisEngine
from report_generator import ReportGenerator, ResumeGenerator, FileService

# Initialize services
analysis_engine = AnalysisEngine()
report_generator = ReportGenerator()
resume_generator = ResumeGenerator()

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
        
        # Read file content
        file_content = await resume_file.read()
        
        # Perform real analysis
        print(f"Analyzing resume: {resume_file.filename}")
        print(f"Job description provided: {bool(job_description)}")
        print(f"Job URL provided: {bool(job_url)}")
        
        result = analysis_engine.analyze(
            resume_file_content=file_content,
            resume_filename=resume_file.filename,
            job_description=job_description,
            job_url=job_url
        )
        
        # Add debug info to response
        result['debug_info'] = {
            'filename': resume_file.filename,
            'file_size': len(file_content),
            'job_description_length': len(job_description),
            'job_url': job_url,
            'ats_platform': ats_platform
        }
        
        return result
        
    except Exception as e:
        print(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/download-report")
async def download_report(
    resume_file: UploadFile = File(...),
    job_description: str = Form(""),
    job_url: str = Form(""),
    ats_platform: str = Form("generic")
):
    """Generate and download PDF analysis report"""
    try:
        # Basic validation
        if not resume_file:
            raise HTTPException(status_code=400, detail="Resume file is required")
        
        if not job_description and not job_url:
            raise HTTPException(status_code=400, detail="Job description or URL is required")
        
        # Read file content
        file_content = await resume_file.read()
        
        # Perform analysis
        analysis_result = analysis_engine.analyze(
            resume_file_content=file_content,
            resume_filename=resume_file.filename,
            job_description=job_description,
            job_url=job_url
        )
        
        # Generate PDF report
        pdf_path = report_generator.generate_pdf_report(analysis_result)
        
        # Return file response
        return FileResponse(
            path=pdf_path,
            filename=f"candilift_report_{resume_file.filename}.pdf",
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment"}
        )
        
    except Exception as e:
        print(f"Report generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")


@app.post("/generate-resume")
async def generate_resume(
    resume_file: UploadFile = File(...),
    job_description: str = Form(""),
    job_url: str = Form(""),
    ats_platform: str = Form("generic")
):
    """Generate and download improved resume DOCX"""
    try:
        # Basic validation
        if not resume_file:
            raise HTTPException(status_code=400, detail="Resume file is required")
        
        if not job_description and not job_url:
            raise HTTPException(status_code=400, detail="Job description or URL is required")
        
        # Read file content
        file_content = await resume_file.read()
        
        # Perform analysis
        analysis_result = analysis_engine.analyze(
            resume_file_content=file_content,
            resume_filename=resume_file.filename,
            job_description=job_description,
            job_url=job_url
        )
        
        # Extract original resume text
        resume_text = analysis_engine.resume_analyzer.extract_text_from_file(
            file_content, resume_file.filename
        )
        
        # Generate improved resume
        docx_path = resume_generator.generate_improved_resume(
            resume_text, analysis_result
        )
        
        # Return file response
        return FileResponse(
            path=docx_path,
            filename=f"improved_resume_{resume_file.filename}.docx",
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": "attachment"}
        )
        
    except Exception as e:
        print(f"Resume generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Resume generation failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting CandiLift API on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)