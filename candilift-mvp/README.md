# CandiLift MVP

A comprehensive web application for analyzing resumes against job descriptions with AI-powered scoring, gap analysis, and tailored resume generation.

## 🚀 Features

- **Resume Parsing**: Extract structured data from PDF, DOCX, and text inputs
- **Job Description Analysis**: Parse requirements and extract must-have vs nice-to-have skills
- **Explainable Scoring**: 7-component scoring system with detailed drivers
- **Gap Analysis**: Identify missing requirements with visual highlighting
- **Fix Recommendations**: AI-powered suggestions with estimated score improvements
- **Resume Variants**: Generate tailored resumes for different focus areas
- **Real-time Analysis**: Fast processing with immediate feedback

## 🏗️ Architecture

### Monorepo Structure
```
candilift-mvp/
├── api/                    # FastAPI backend
│   ├── routers/           # API endpoints
│   ├── core/              # Core business logic
│   ├── config/            # Configuration files
│   ├── tests/             # Test suites
│   ├── seeds/             # Sample data
│   └── scripts/           # CLI tools
└── web/                   # Next.js frontend
    ├── app/               # App Router pages
    ├── components/        # React components
    ├── lib/               # Utilities and types
    └── prisma/            # Database schema
```

### Tech Stack
- **Backend**: FastAPI, Python 3.11, SQLite, Pydantic
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, Prisma
- **Parsing**: pdfminer.six, python-docx, BeautifulSoup
- **Scoring**: Custom rule-based engine with explainable drivers
- **Generation**: python-docx for resume variants

## 📊 Scoring Components

| Component | Weight | Description |
|-----------|--------|-------------|
| Must-Have Coverage | 40% | Coverage of required skills/experience |
| Experience & Seniority | 20% | Relevant experience and seniority match |
| Skills Depth | 15% | Contextual use and quantified evidence |
| Impact Signals | 10% | Metrics and measurable achievements |
| ATS Parseability | 5% | Format and structure compliance |
| Language Quality | 5% | Action verbs and concise writing |
| Logistics | 5% | Location and remote work compatibility |

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### Backend Setup

1. **Install dependencies**:
   ```bash
   cd api
   pip install -r requirements.txt
   ```

2. **Run the API server**:
   ```bash
   uvicorn main:app --reload
   ```
   
   API will be available at `http://localhost:8000`
   - API docs: `http://localhost:8000/docs`
   - Health check: `http://localhost:8000/healthz`

### Frontend Setup

1. **Install dependencies**:
   ```bash
   cd web
   npm install
   ```

2. **Set up database**:
   ```bash
   npx prisma generate
   npx prisma db push
   ```

3. **Run the development server**:
   ```bash
   npm run dev
   ```
   
   Frontend will be available at `http://localhost:3000`

### Environment Variables

Create `.env.local` in the web directory:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Optional: Set `OPENAI_API_KEY` for LLM features:
```bash
OPENAI_API_KEY=your_openai_api_key
```

## 📝 API Endpoints

### Parse Endpoints
- `POST /parse/resume` - Parse resume from file or text
- `POST /parse/job` - Parse job description from text or URL
- `GET /parse/resume/preview` - Preview resume parsing
- `GET /parse/job/preview` - Preview job parsing

### Score Endpoints
- `POST /score/` - Score resume against job description
- `POST /score/recommend` - Get fix recommendations
- `GET /score/components` - Get scoring components info
- `GET /score/sample` - Get sample score response

### Generate Endpoints
- `POST /generate/resume` - Generate resume variants
- `GET /generate/variants` - Get available variant types
- `GET /generate/sample` - Get sample generation response

## 🧪 Testing

### Backend Tests
```bash
cd api
pytest tests/
```

### Frontend Tests
```bash
cd web
npm test
```

### CLI Testing
```bash
cd api
python scripts/batch_score.py create-sample
python scripts/batch_score.py score --input sample_pairs.csv --output results.csv
```

## 📊 Sample Data

The application includes sample resumes and job descriptions:

- **Resume 1**: Senior Software Engineer (Alex Chen)
- **Resume 2**: Product Manager (Sarah Johnson)  
- **Resume 3**: Data Scientist (Michael Rodriguez)

- **Job 1**: Senior Software Engineer at TechCorp
- **Job 2**: Senior Product Manager at GrowthCo
- **Job 3**: Senior Data Scientist at AI Solutions

## 🔧 Configuration

### Scoring Weights
Edit `api/config/scoring.yaml` to adjust component weights and thresholds.

### Skills Ontology
Edit `api/config/skills.json` to add new skills, aliases, and domains.

### Resume Variants
Modify `api/core/docx_export.py` to customize resume generation templates.

## 📈 Usage Examples

### 1. Parse Resume
```bash
curl -X POST "http://localhost:8000/parse/resume" \
  -F "file=@resume.pdf"
```

### 2. Parse Job Description
```bash
curl -X POST "http://localhost:8000/parse/job" \
  -F "text_content=Looking for Python developer with 3+ years experience..."
```

### 3. Score Resume
```bash
curl -X POST "http://localhost:8000/score/" \
  -H "Content-Type: application/json" \
  -d '{"resume": {...}, "job": {...}}'
```

### 4. Generate Variants
```bash
curl -X POST "http://localhost:8000/generate/resume" \
  -H "Content-Type: application/json" \
  -d '{"resume": {...}, "job": {...}, "variant_types": ["platform", "growth"]}'
```

## 🎯 Sample Score Response

```json
{
  "overall": 75.5,
  "components": {
    "must_haves": {
      "score": 32.0,
      "max": 40,
      "drivers": [
        {"label": "Covered: Python", "delta": 5, "evidence": ["Found Python experience"]},
        {"label": "Missing: Kubernetes", "delta": -5, "evidence": ["No Kubernetes experience found"]}
      ]
    },
    "experience": {
      "score": 16.0,
      "max": 20,
      "drivers": [
        {"label": "Seniority match", "delta": 8, "evidence": ["Title aligns with requirements"]}
      ]
    }
  },
  "matches": [
    {"jd_item": "Python", "resume_spans": [0, 1, 2]}
  ],
  "gaps": [
    {"jd_item": "Kubernetes", "reason": "missing"}
  ]
}
```

## 🔍 Troubleshooting

### Common Issues

1. **Port conflicts**: Change ports in `uvicorn` and `npm run dev` commands
2. **File parsing errors**: Ensure files are valid PDF/DOCX format
3. **API connection**: Check CORS settings and API URL configuration
4. **Database issues**: Run `npx prisma db push` to sync schema

### Debug Mode

Enable debug logging:
```bash
export LOG_LEVEL=DEBUG
uvicorn main:app --reload --log-level debug
```

## 🚀 Deployment

### Backend (Render)
1. Connect GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel)
1. Connect GitHub repository
2. Set framework preset: Next.js
3. Set build command: `npm run build`
4. Set output directory: `.next`

## 📚 Development

### Adding New Features

1. **New scoring component**: Add to `core/scoring.py` and update weights
2. **New resume variant**: Add to `core/docx_export.py` and update variants list
3. **New API endpoint**: Add to appropriate router in `routers/`
4. **New UI component**: Add to `web/components/` and update pages

### Code Style

- **Python**: Black formatter, flake8 linter
- **TypeScript**: ESLint with Next.js config
- **Commits**: Conventional commit messages

## 📄 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For questions or issues:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the API documentation at `/docs`

---

**Built with ❤️ for better candidate success**
