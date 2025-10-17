from pydantic import BaseModel
from typing import List, Dict, Optional
from enum import Enum

class SkillType(str, Enum):
    HARD_SKILL = "hard_skill"
    SOFT_SKILL = "soft_skill"
    TECHNICAL_SKILL = "technical_skill"
    TOOL = "tool"
    FRAMEWORK = "framework"

class JobSkill(BaseModel):
    name: str
    skill_type: SkillType
    importance: float  # 0-10
    frequency: int  # how many times mentioned in JD

class SeniorityLevel(str, Enum):
    ENTRY = "entry"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    STAFF = "staff"
    PRINCIPAL = "principal"
    EXECUTIVE = "executive"

class JobData(BaseModel):
    title: str
    company: Optional[str] = None
    raw_text: str
    required_skills: List[JobSkill]
    preferred_skills: List[JobSkill]
    seniority_level: SeniorityLevel
    years_experience: Optional[int] = None
    key_phrases: List[str]
    responsibilities: List[str]
    qualifications: List[str]
    
    def get_all_keywords(self) -> List[str]:
        """Get all keywords from the job description."""
        keywords = []
        
        for skill in self.required_skills + self.preferred_skills:
            keywords.extend(skill.name.lower().split())
        
        keywords.extend([phrase.lower() for phrase in self.key_phrases])
        
        # Add title words
        keywords.extend(self.title.lower().split())
        
        return list(set(keywords))  # Remove duplicates
    
    def get_skill_names(self) -> List[str]:
        """Get all skill names as a list."""
        return [skill.name.lower() for skill in self.required_skills + self.preferred_skills]
