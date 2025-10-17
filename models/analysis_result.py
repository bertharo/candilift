from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

class SeverityLevel(str, Enum):
    CRITICAL = "critical"
    MAJOR = "major"
    NICE_TO_HAVE = "nice_to_have"

class RecommendationCategory(str, Enum):
    KEYWORD = "keyword"
    FORMATTING = "formatting"
    IMPACT = "impact"
    STRUCTURE = "structure"

class KeywordMatch(BaseModel):
    keyword: str
    match_type: str  # "exact", "synonym", "missing", "weak"
    frequency_in_jd: int
    location_in_resume: str  # "title", "summary", "experience", "skills", "none"
    importance_score: float

class KeywordAnalysis(BaseModel):
    coverage_score: float  # 0-100
    missing_keywords: List[str]
    weak_keywords: List[KeywordMatch]
    strong_keywords: List[KeywordMatch]
    keyword_density: Dict[str, float]

class FormattingIssue(BaseModel):
    issue_type: str
    description: str
    severity: SeverityLevel
    location: str
    suggestion: str

class FormattingAnalysis(BaseModel):
    ats_compatibility_score: float  # 0-100
    issues: List[FormattingIssue]
    structure_score: float  # 0-100
    has_proper_headers: bool
    has_consistent_formatting: bool

class ImpactBullet(BaseModel):
    text: str
    has_metrics: bool
    has_action_verb: bool
    strength_score: float  # 0-10
    suggestion: Optional[str] = None

class ImpactAnalysis(BaseModel):
    impact_score: float  # 0-100
    strong_bullets: List[ImpactBullet]
    weak_bullets: List[ImpactBullet]
    generic_phrases_found: List[str]
    improvement_suggestions: List[str]

class Recommendation(BaseModel):
    category: RecommendationCategory
    severity: SeverityLevel
    title: str
    description: str
    before_example: Optional[str] = None
    after_example: Optional[str] = None
    priority_score: float  # 0-10

class AnalysisResult(BaseModel):
    resume_filename: str
    analysis_timestamp: datetime
    ats_score: float  # 0-100
    recruiter_score: float  # 0-100
    keyword_analysis: KeywordAnalysis
    formatting_analysis: FormattingAnalysis
    impact_analysis: ImpactAnalysis
    recommendations: List[Recommendation]
    # ATS Simulation fields
    ats_platform: Optional[str] = None
    processing_time: Optional[float] = None
    ats_quirks: Optional[List[str]] = None
    platform_weights: Optional[Dict[str, float]] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
