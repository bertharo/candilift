#!/usr/bin/env python3
"""
ATS Resume Reviewer - Main entry point
Run this script to start both backend and frontend servers
"""

import subprocess
import sys
import os
import time
import signal
from pathlib import Path

def run_backend():
    """Start the FastAPI backend server"""
    backend_dir = Path(__file__).parent / "backend"
    return subprocess.Popen([
        sys.executable, "main.py"
    ], cwd=backend_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def run_frontend():
    """Start the React frontend development server"""
    frontend_dir = Path(__file__).parent / "frontend"
    
    # Check if node_modules exists
    if not (frontend_dir / "node_modules").exists():
        print("Installing frontend dependencies...")
        subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
    
    return subprocess.Popen([
        "npm", "start"
    ], cwd=frontend_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def main():
    """Main function to start both servers"""
    print("🚀 Starting ATS Resume Reviewer...")
    
    # Start backend
    print("📡 Starting backend server...")
    backend_process = run_backend()
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    # Start frontend
    print("🎨 Starting frontend server...")
    frontend_process = run_frontend()
    
    print("\n✅ ATS Resume Reviewer is running!")
    print("📱 Frontend: http://localhost:3000")
    print("🔧 Backend API: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop both servers")
    
    try:
        # Wait for both processes
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("❌ Backend server stopped unexpectedly")
                break
            
            if frontend_process.poll() is not None:
                print("❌ Frontend server stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        
        # Terminate processes
        backend_process.terminate()
        frontend_process.terminate()
        
        # Wait for graceful shutdown
        try:
            backend_process.wait(timeout=5)
            frontend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            backend_process.kill()
            frontend_process.kill()
        
        print("✅ Servers stopped")

if __name__ == "__main__":
    main()
