from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class ContactInfo(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    location: Optional[str] = None

class Experience(BaseModel):
    company: str
    title: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    current: bool = False
    description: List[str]
    location: Optional[str] = None

class Education(BaseModel):
    institution: str
    degree: str
    field: Optional[str] = None
    graduation_date: Optional[str] = None
    gpa: Optional[str] = None

class ResumeData(BaseModel):
    contact_info: ContactInfo
    summary: Optional[str] = None
    experience: List[Experience]
    education: List[Education]
    skills: List[str]
    certifications: List[str] = []
    projects: List[str] = []
    awards: List[str] = []
    raw_text: str
    sections: Dict[str, str]  # section_name -> content
    
    def get_all_text(self) -> str:
        """Get all text content from the resume."""
        text_parts = []
        
        if self.contact_info.name:
            text_parts.append(self.contact_info.name)
        if self.summary:
            text_parts.append(self.summary)
        
        for exp in self.experience:
            text_parts.append(f"{exp.title} at {exp.company}")
            text_parts.extend(exp.description)
        
        for edu in self.education:
            text_parts.append(f"{edu.degree} from {edu.institution}")
        
        text_parts.extend(self.skills)
        text_parts.extend(self.certifications)
        text_parts.extend(self.projects)
        text_parts.extend(self.awards)
        
        return " ".join(text_parts).lower()
