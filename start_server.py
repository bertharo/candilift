#!/usr/bin/env python3
"""
Simple startup script for Render
"""
import os
import sys

# Ensure we're in the right directory
print(f"Current working directory: {os.getcwd()}")
print(f"Files in current directory: {os.listdir('.')}")

# Try to import and run the app
try:
    from main import app
    import uvicorn
    
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting server on port {port}")
    
    uvicorn.run(app, host="0.0.0.0", port=port)
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
