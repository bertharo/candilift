# ATS Resume Reviewer

A comprehensive tool that analyzes resumes against job descriptions to identify gaps in ATS compliance, keyword optimization, structure, and impact. Provides prioritized, actionable feedback to improve resume likelihood of passing ATS filters and impressing human recruiters.

## Features

- **Resume Parsing**: Supports PDF and DOCX formats with intelligent text extraction
- **Job Description Analysis**: Extracts keywords, skills, and requirements
- **Keyword Gap Analysis**: Identifies missing and weak keyword matches with weighting
- **ATS Formatting Check**: Validates compatibility with Applicant Tracking Systems
- **Impact Analysis**: Uses NLP to analyze bullet points for measurable outcomes
- **Dual Scoring**: Separate ATS compatibility and recruiter appeal scores
- **Prioritized Recommendations**: Actionable suggestions with before/after examples

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Download spaCy language model:
```bash
python -m spacy download en_core_web_sm
```

3. Start the FastAPI server:
```bash
cd backend
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the React development server:
```bash
npm start
```

The application will be available at `http://localhost:3000`

## API Endpoints

### POST /analyze
Analyze a resume against a job description.

**Parameters:**
- `resume_file` (file): Resume in PDF or DOCX format
- `job_description` (string): Job description text (optional if file provided)
- `job_description_file` (file): Job description file in PDF, DOCX, or TXT format (optional)

**Response:**
```json
{
  "resume_filename": "resume.pdf",
  "analysis_timestamp": "2024-01-01T12:00:00Z",
  "ats_score": 85.5,
  "recruiter_score": 78.2,
  "keyword_analysis": {
    "coverage_score": 82.0,
    "missing_keywords": ["python", "machine learning"],
    "strong_keywords": [...],
    "weak_keywords": [...]
  },
  "formatting_analysis": {
    "ats_compatibility_score": 90.0,
    "structure_score": 85.0,
    "issues": [...]
  },
  "impact_analysis": {
    "impact_score": 75.0,
    "strong_bullets": [...],
    "weak_bullets": [...]
  },
  "recommendations": [...]
}
```

### GET /health
Health check endpoint.

## Architecture

### Backend (FastAPI + Python)
- **Resume Parser**: Extracts text from PDF/DOCX using pdfminer.six and python-docx
- **Job Parser**: Analyzes job descriptions for keywords and requirements
- **Keyword Analyzer**: Performs gap analysis with synonym matching and weighting
- **Formatting Checker**: Validates ATS compatibility and structure
- **Impact Analyzer**: Uses NLP to evaluate bullet point strength
- **Scoring Engine**: Calculates ATS and recruiter scores
- **Recommendation Engine**: Generates prioritized improvement suggestions

### Frontend (React + Tailwind CSS)
- **File Upload**: Drag-and-drop interface for resume and job description
- **Results Dashboard**: Comprehensive analysis results with tabbed interface
- **Score Visualization**: Color-coded scores with grade indicators
- **Recommendations**: Prioritized suggestions with before/after examples

## Scoring System

### ATS Score (0-100)
- **Keyword Coverage (50%)**: How well resume matches job description keywords
- **Formatting (30%)**: ATS compatibility and parsing issues
- **Structure (20%)**: Section organization and header recognition

### Recruiter Score (0-100)
- **Impact (40%)**: Measurable outcomes and strong action verbs
- **Formatting (25%)**: Readability and professional appearance
- **Structure (20%)**: Content organization and flow
- **Keyword Relevance (15%)**: Strategic keyword integration

## Recommendation Categories

- **Critical**: Issues that severely impact ATS compatibility
- **Major**: Significant improvements that enhance resume quality
- **Nice-to-have**: Minor optimizations for perfection

## Development

### Project Structure
```
ATS Reviewer/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── models/                 # Data models
│   └── services/               # Business logic
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   └── services/           # API client
│   └── public/
├── requirements.txt            # Python dependencies
└── README.md
```

### Adding New Features

1. **Backend**: Add new services in `services/` directory
2. **Frontend**: Create components in `src/components/`
3. **API**: Extend endpoints in `main.py`

### Testing

Run backend tests:
```bash
cd backend
python -m pytest
```

Run frontend tests:
```bash
cd frontend
npm test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions, please open a GitHub issue or contact the development team.
