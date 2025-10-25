"""
FastAPI main application for CandiLift MVP
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from contextlib import asynccontextmanager

from routers import parse, score, generate


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
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(parse.router, prefix="/parse", tags=["parsing"])
app.include_router(score.router, prefix="/score", tags=["scoring"])
app.include_router(generate.router, prefix="/generate", tags=["generation"])


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


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )