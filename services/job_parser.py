import re
from typing import List, Dict, Tuple
from models.job_data import JobData, JobSkill, SkillType, SeniorityLevel

class JobDescriptionParser:
    def __init__(self):
        # Common technical skills and tools
        self.technical_skills = {
            'python', 'java', 'javascript', 'typescript', 'react', 'angular', 'vue', 'node.js',
            'sql', 'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform',
            'git', 'github', 'gitlab', 'jenkins', 'ci/cd', 'devops',
            'machine learning', 'ai', 'deep learning', 'nlp', 'computer vision',
            'tableau', 'power bi', 'excel', 'spreadsheet', 'analytics',
            'agile', 'scrum', 'kanban', 'jira', 'confluence'
        }
        
        # Soft skills
        self.soft_skills = {
            'leadership', 'management', 'communication', 'collaboration', 'teamwork',
            'problem solving', 'critical thinking', 'analytical', 'strategic thinking',
            'project management', 'stakeholder management', 'presentation',
            'mentoring', 'coaching', 'negotiation', 'influence'
        }
        
        # Seniority keywords
        self.seniority_keywords = {
            'entry': ['entry', 'junior', 'associate', 'intern', 'graduate'],
            'junior': ['junior', 'associate', 'coordinator', 'specialist'],
            'mid': ['mid', 'intermediate', 'analyst', 'coordinator'],
            'senior': ['senior', 'lead', 'principal', 'staff', 'expert'],
            'staff': ['staff', 'principal', 'architect', 'senior lead'],
            'principal': ['principal', 'architect', 'distinguished', 'fellow'],
            'executive': ['director', 'vp', 'vice president', 'c-level', 'executive', 'head of']
        }
        
        # Experience year patterns
        self.experience_patterns = [
            r'(\d+)[\+\-\s]*years?[\+\-\s]*(?:of\s+)?(?:experience|exp)',
            r'(\d+)[\+\-\s]*to\s+(\d+)\s+years?',
            r'(?:minimum|min|at least)\s+(\d+)\s+years?',
            r'(\d+)\+?\s*years?\s+(?:of\s+)?(?:experience|exp)'
        ]
    
    def parse(self, job_description: str) -> JobData:
        """Parse job description text into structured data."""
        text = job_description.lower()
        
        # Extract job title
        title = self._extract_job_title(job_description)
        
        # Extract skills
        required_skills, preferred_skills = self._extract_skills(text)
        
        # Determine seniority level
        seniority_level = self._determine_seniority_level(text)
        
        # Extract years of experience
        years_experience = self._extract_years_experience(text)
        
        # Extract key phrases
        key_phrases = self._extract_key_phrases(text)
        
        # Extract responsibilities and qualifications
        responsibilities, qualifications = self._extract_responsibilities_qualifications(job_description)
        
        return JobData(
            title=title,
            raw_text=job_description,
            required_skills=required_skills,
            preferred_skills=preferred_skills,
            seniority_level=seniority_level,
            years_experience=years_experience,
            key_phrases=key_phrases,
            responsibilities=responsibilities,
            qualifications=qualifications
        )
    
    def _extract_job_title(self, text: str) -> str:
        """Extract job title from job description."""
        lines = text.split('\n')
        
        # Look for title in first few lines
        for line in lines[:5]:
            line = line.strip()
            if line and len(line.split()) <= 8:  # Reasonable title length
                # Skip common headers
                if not any(header in line.lower() for header in ['job description', 'position', 'role']):
                    return line
        
        # Fallback: extract from common patterns
        title_patterns = [
            r'position:\s*(.+)',
            r'role:\s*(.+)',
            r'title:\s*(.+)',
            r'job:\s*(.+)'
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "Unknown Position"
    
    def _extract_skills(self, text: str) -> Tuple[List[JobSkill], List[JobSkill]]:
        """Extract required and preferred skills from job description."""
        required_skills = []
        preferred_skills = []
        
        # Split text into sections
        sections = self._split_into_sections(text)
        
        for section_name, section_text in sections.items():
            skills = self._identify_skills_in_text(section_text)
            
            # Determine if skills are required or preferred based on section
            is_required = any(keyword in section_name for keyword in [
                'required', 'must have', 'essential', 'mandatory', 'qualifications'
            ])
            is_preferred = any(keyword in section_name for keyword in [
                'preferred', 'nice to have', 'bonus', 'plus', 'advantage'
            ])
            
            for skill_name, skill_type in skills.items():
                # Count frequency in the entire text
                frequency = text.count(skill_name.lower())
                
                # Determine importance based on section and frequency
                importance = self._calculate_skill_importance(skill_name, frequency, section_name)
                
                job_skill = JobSkill(
                    name=skill_name,
                    skill_type=skill_type,
                    importance=importance,
                    frequency=frequency
                )
                
                if is_required:
                    required_skills.append(job_skill)
                elif is_preferred:
                    preferred_skills.append(job_skill)
                else:
                    # Default to required if not specified
                    required_skills.append(job_skill)
        
        return required_skills, preferred_skills
    
    def _split_into_sections(self, text: str) -> Dict[str, str]:
        """Split job description into sections."""
        sections = {}
        
        # Common section headers
        section_patterns = [
            r'(?:required|must have|essential|mandatory|qualifications?)\s*(?:skills?|experience)?\s*:?',
            r'(?:preferred|nice to have|bonus|plus|advantage)\s*(?:skills?|experience)?\s*:?',
            r'(?:responsibilities?|duties?|what you\'ll do)\s*:?',
            r'(?:requirements?|qualifications?)\s*:?',
            r'(?:skills?|technical skills?|competencies?)\s*:?',
            r'(?:experience|background)\s*:?',
            r'(?:education|academic)\s*:?'
        ]
        
        current_section = 'general'
        current_content = []
        
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line matches a section header
            section_found = False
            for pattern in section_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    # Save previous section
                    if current_content:
                        sections[current_section] = '\n'.join(current_content)
                    
                    # Start new section
                    current_section = line.lower()
                    current_content = []
                    section_found = True
                    break
            
            if not section_found:
                current_content.append(line)
        
        # Save last section
        if current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    def _identify_skills_in_text(self, text: str) -> Dict[str, SkillType]:
        """Identify skills mentioned in text and classify them."""
        skills = {}
        text_lower = text.lower()
        
        # Check technical skills
        for skill in self.technical_skills:
            if skill in text_lower:
                # Determine skill type
                if skill in {'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform'}:
                    skill_type = SkillType.TOOL
                elif skill in {'python', 'java', 'javascript', 'typescript', 'sql'}:
                    skill_type = SkillType.TECHNICAL_SKILL
                elif skill in {'react', 'angular', 'vue', 'node.js'}:
                    skill_type = SkillType.FRAMEWORK
                else:
                    skill_type = SkillType.HARD_SKILL
                
                skills[skill] = skill_type
        
        # Check soft skills
        for skill in self.soft_skills:
            if skill in text_lower:
                skills[skill] = SkillType.SOFT_SKILL
        
        # Look for other technical terms (programming languages, tools, etc.)
        tech_patterns = [
            r'\b(?:html|css|php|ruby|go|rust|c\+\+|c#|swift|kotlin)\b',
            r'\b(?:spring|django|flask|rails|express|laravel)\b',
            r'\b(?:tensorflow|pytorch|scikit-learn|pandas|numpy)\b',
            r'\b(?:salesforce|hubspot|slack|zoom|teams)\b'
        ]
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                skills[match] = SkillType.TECHNICAL_SKILL
        
        return skills
    
    def _calculate_skill_importance(self, skill_name: str, frequency: int, section_name: str) -> float:
        """Calculate importance score for a skill (0-10)."""
        importance = 5.0  # Base importance
        
        # Increase importance based on frequency
        if frequency > 3:
            importance += 2.0
        elif frequency > 1:
            importance += 1.0
        
        # Increase importance based on section
        if any(keyword in section_name for keyword in ['required', 'must have', 'essential']):
            importance += 2.0
        elif any(keyword in section_name for keyword in ['preferred', 'nice to have']):
            importance += 0.5
        
        # Increase importance for technical skills
        if skill_name.lower() in self.technical_skills:
            importance += 1.0
        
        return min(10.0, importance)
    
    def _determine_seniority_level(self, text: str) -> SeniorityLevel:
        """Determine seniority level from job description."""
        text_lower = text.lower()
        
        # Check for seniority keywords
        for level, keywords in self.seniority_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return SeniorityLevel(level)
        
        # Check for experience requirements
        years = self._extract_years_experience(text)
        if years:
            if years <= 2:
                return SeniorityLevel.ENTRY
            elif years <= 4:
                return SeniorityLevel.JUNIOR
            elif years <= 7:
                return SeniorityLevel.MID
            elif years <= 10:
                return SeniorityLevel.SENIOR
            else:
                return SeniorityLevel.STAFF
        
        # Default based on title
        if any(word in text_lower for word in ['director', 'vp', 'vice president', 'c-level']):
            return SeniorityLevel.EXECUTIVE
        elif any(word in text_lower for word in ['senior', 'lead', 'principal']):
            return SeniorityLevel.SENIOR
        elif any(word in text_lower for word in ['junior', 'associate', 'coordinator']):
            return SeniorityLevel.JUNIOR
        else:
            return SeniorityLevel.MID
    
    def _extract_years_experience(self, text: str) -> int:
        """Extract years of experience requirement."""
        text_lower = text.lower()
        
        for pattern in self.experience_patterns:
            match = re.search(pattern, text_lower)
            if match:
                if len(match.groups()) == 2:
                    # Range like "3-5 years"
                    return int(match.group(2))
                else:
                    # Single number like "5+ years"
                    return int(match.group(1))
        
        return None
    
    def _extract_key_phrases(self, text: str) -> List[str]:
        """Extract key phrases from job description."""
        key_phrases = []
        
        # Common key phrases in job descriptions
        phrase_patterns = [
            r'scenario planning',
            r'organizational design',
            r'stakeholder management',
            r'cross-functional',
            r'data-driven',
            r'strategic planning',
            r'product roadmap',
            r'user experience',
            r'business intelligence',
            r'change management',
            r'risk management',
            r'budget management',
            r'team leadership',
            r'project delivery',
            r'process improvement'
        ]
        
        for pattern in phrase_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                key_phrases.append(pattern)
        
        return key_phrases
    
    def _extract_responsibilities_qualifications(self, text: str) -> Tuple[List[str], List[str]]:
        """Extract responsibilities and qualifications sections."""
        responsibilities = []
        qualifications = []
        
        # Look for bullet points or numbered lists
        lines = text.split('\n')
        
        in_responsibilities = False
        in_qualifications = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for section headers
            if re.search(r'(?:responsibilities?|duties?|what you\'ll do)', line, re.IGNORECASE):
                in_responsibilities = True
                in_qualifications = False
                continue
            elif re.search(r'(?:requirements?|qualifications?)', line, re.IGNORECASE):
                in_qualifications = True
                in_responsibilities = False
                continue
            elif re.search(r'(?:preferred|nice to have)', line, re.IGNORECASE):
                in_responsibilities = False
                in_qualifications = False
                continue
            
            # Check if line is a bullet point
            if line.startswith(('•', '-', '*', '◦')) or re.match(r'^\d+\.', line):
                content = re.sub(r'^[•\-*\d\.\s]+', '', line).strip()
                
                if in_responsibilities:
                    responsibilities.append(content)
                elif in_qualifications:
                    qualifications.append(content)
        
        return responsibilities, qualifications
