import re
import os
from typing import List, Dict, Optional
from pdfminer.high_level import extract_text
from docx import Document
import spacy
from models.resume_data import ResumeData, ContactInfo, Experience, Education

class ResumeParser:
    def __init__(self):
        # Load spaCy model for NLP processing
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Warning: spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
    
    def parse(self, file_path: str) -> ResumeData:
        """Parse resume from file path."""
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            text = self.parse_pdf(file_path)
        elif file_extension == '.docx':
            text = self.parse_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        return self.parse_text(text)
    
    def parse_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        try:
            return extract_text(file_path)
        except Exception as e:
            raise ValueError(f"Failed to parse PDF: {str(e)}")
    
    def parse_docx(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        try:
            doc = Document(file_path)
            text_parts = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_parts.append(paragraph.text.strip())
            
            return "\n".join(text_parts)
        except Exception as e:
            raise ValueError(f"Failed to parse DOCX: {str(e)}")
    
    def parse_text(self, text: str) -> ResumeData:
        """Parse resume text into structured data."""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Extract contact information
        contact_info = self._extract_contact_info(lines)
        
        # Extract sections
        sections = self._extract_sections(text)
        
        # Extract experience
        experience = self._extract_experience(sections.get('experience', ''))
        
        # Extract education
        education = self._extract_education(sections.get('education', ''))
        
        # Extract skills
        skills = self._extract_skills(sections.get('skills', ''))
        
        # Extract summary
        summary = sections.get('summary', '') or sections.get('objective', '')
        
        return ResumeData(
            contact_info=contact_info,
            summary=summary,
            experience=experience,
            education=education,
            skills=skills,
            raw_text=text,
            sections=sections
        )
    
    def _extract_contact_info(self, lines: List[str]) -> ContactInfo:
        """Extract contact information from resume lines."""
        contact = ContactInfo()
        
        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        # Phone pattern
        phone_pattern = r'(\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}'
        # LinkedIn pattern
        linkedin_pattern = r'(?:https?://)?(?:www\.)?linkedin\.com/in/[A-Za-z0-9_-]+/?'
        
        for line in lines[:10]:  # Check first 10 lines for contact info
            # Extract email
            email_match = re.search(email_pattern, line)
            if email_match and not contact.email:
                contact.email = email_match.group()
            
            # Extract phone
            phone_match = re.search(phone_pattern, line)
            if phone_match and not contact.phone:
                contact.phone = phone_match.group()
            
            # Extract LinkedIn
            linkedin_match = re.search(linkedin_pattern, line)
            if linkedin_match and not contact.linkedin:
                contact.linkedin = linkedin_match.group()
        
        # Name is typically the first non-empty line
        for line in lines[:5]:
            if line and not re.search(email_pattern, line) and not re.search(phone_pattern, line):
                if len(line.split()) <= 4:  # Likely a name
                    contact.name = line
                    break
        
        return contact
    
    def _extract_sections(self, text: str) -> Dict[str, str]:
        """Extract different sections from resume text."""
        sections = {}
        
        # Common section headers
        section_patterns = {
            'summary': r'(?:summary|profile|objective|about)\s*:?',
            'experience': r'(?:experience|work\s+history|employment|professional\s+experience)\s*:?',
            'education': r'(?:education|academic|qualifications)\s*:?',
            'skills': r'(?:skills|technical\s+skills|competencies|expertise)\s*:?',
            'certifications': r'(?:certifications|certificates|credentials)\s*:?',
            'projects': r'(?:projects|portfolio)\s*:?',
            'awards': r'(?:awards|honors|achievements)\s*:?'
        }
        
        # Split text into sections
        current_section = 'header'
        current_content = []
        
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line matches a section header
            section_found = False
            for section_name, pattern in section_patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    # Save previous section
                    if current_content:
                        sections[current_section] = '\n'.join(current_content)
                    
                    # Start new section
                    current_section = section_name
                    current_content = []
                    section_found = True
                    break
            
            if not section_found:
                current_content.append(line)
        
        # Save last section
        if current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    def _extract_experience(self, experience_text: str) -> List[Experience]:
        """Extract work experience from text."""
        experiences = []
        
        if not experience_text:
            return experiences
        
        # Split by common separators
        entries = re.split(r'\n\s*\n', experience_text)
        
        for entry in entries:
            if not entry.strip():
                continue
            
            lines = [line.strip() for line in entry.split('\n') if line.strip()]
            if not lines:
                continue
            
            # First line usually contains title and company
            title_company_line = lines[0]
            
            # Try to extract title and company
            # Common patterns: "Title at Company", "Title, Company", "Company - Title"
            title_company_match = re.match(r'(.+?)\s+(?:at|,|\-)\s+(.+)', title_company_line)
            
            if title_company_match:
                title = title_company_match.group(1).strip()
                company = title_company_match.group(2).strip()
            else:
                # Fallback: assume first part is title, rest is company
                parts = title_company_line.split()
                if len(parts) >= 2:
                    title = ' '.join(parts[:-1])
                    company = parts[-1]
                else:
                    title = title_company_line
                    company = "Unknown"
            
            # Extract dates (look for date patterns)
            dates = self._extract_dates(' '.join(lines))
            start_date, end_date, current = dates
            
            # Extract description (remaining lines)
            description = []
            for line in lines[1:]:
                # Skip date lines
                if not re.search(r'\d{4}|\d{1,2}/\d{4}', line):
                    description.append(line)
            
            experiences.append(Experience(
                company=company,
                title=title,
                start_date=start_date,
                end_date=end_date,
                current=current,
                description=description
            ))
        
        return experiences
    
    def _extract_education(self, education_text: str) -> List[Education]:
        """Extract education information from text."""
        education = []
        
        if not education_text:
            return education
        
        # Split by common separators
        entries = re.split(r'\n\s*\n', education_text)
        
        for entry in entries:
            if not entry.strip():
                continue
            
            lines = [line.strip() for line in entry.split('\n') if line.strip()]
            if not lines:
                continue
            
            # First line usually contains degree and institution
            degree_institution_line = lines[0]
            
            # Try to extract degree and institution
            # Common patterns: "Degree in Field, Institution", "Institution - Degree"
            degree_institution_match = re.match(r'(.+?)\s+(?:in|,|\-)\s+(.+)', degree_institution_line)
            
            if degree_institution_match:
                degree = degree_institution_match.group(1).strip()
                institution = degree_institution_match.group(2).strip()
            else:
                # Fallback: assume first part is degree, rest is institution
                parts = degree_institution_line.split()
                if len(parts) >= 2:
                    degree = ' '.join(parts[:-1])
                    institution = parts[-1]
                else:
                    degree = degree_institution_line
                    institution = "Unknown"
            
            # Extract graduation date
            dates = self._extract_dates(' '.join(lines))
            graduation_date = dates[1]  # End date
            
            education.append(Education(
                institution=institution,
                degree=degree,
                graduation_date=graduation_date
            ))
        
        return education
    
    def _extract_skills(self, skills_text: str) -> List[str]:
        """Extract skills from text."""
        if not skills_text:
            return []
        
        # Split by common separators
        skills = []
        
        # Handle comma-separated, semicolon-separated, or line-separated skills
        separators = [',', ';', '\n', '|']
        
        for separator in separators:
            if separator in skills_text:
                skills = [skill.strip() for skill in skills_text.split(separator) if skill.strip()]
                break
        
        if not skills:
            # Try bullet points
            skills = [skill.strip('- •*').strip() for skill in skills_text.split('\n') if skill.strip()]
        
        return [skill for skill in skills if skill and len(skill) > 1]
    
    def _extract_dates(self, text: str) -> tuple:
        """Extract start and end dates from text."""
        # Date patterns
        date_patterns = [
            r'(\d{4})\s*[-–]\s*(\d{4}|\b(?:present|current|now)\b)',
            r'(\d{1,2}/\d{4})\s*[-–]\s*(\d{1,2}/\d{4}|\b(?:present|current|now)\b)',
            r'(\d{4})\s*[-–]\s*(\d{4})',
            r'(\d{1,2}/\d{4})\s*[-–]\s*(\d{1,2}/\d{4})'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                start_date = match.group(1)
                end_date = match.group(2)
                current = end_date.lower() in ['present', 'current', 'now']
                return start_date, end_date if not current else None, current
        
        return None, None, False
