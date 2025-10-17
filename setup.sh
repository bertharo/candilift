#!/bin/bash

# ATS Resume Reviewer Setup Script

echo "🚀 Setting up ATS Resume Reviewer..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.8+ and try again."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed. Please install Node.js 16+ and try again."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Download spaCy language model
echo "🧠 Downloading spaCy language model..."
python3 -m spacy download en_core_web_sm

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo "  python3 run.py"
echo ""
echo "Or start servers individually:"
echo "  Backend: cd backend && python3 main.py"
echo "  Frontend: cd frontend && npm start"
echo ""
echo "🌐 Application will be available at:"
echo "  Frontend: http://localhost:3000"
echo "  Backend API: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
