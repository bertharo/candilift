import re
from typing import List, Dict
from models.resume_data import ResumeData
from models.analysis_result import FormattingAnalysis, FormattingIssue, SeverityLevel

class FormattingChecker:
    def __init__(self):
        # ATS-compatible section headers
        self.ats_headers = {
            'contact', 'contact information', 'personal information',
            'summary', 'profile', 'objective', 'about',
            'experience', 'work experience', 'employment', 'professional experience',
            'education', 'academic background', 'qualifications',
            'skills', 'technical skills', 'competencies', 'expertise',
            'certifications', 'certificates', 'credentials',
            'projects', 'portfolio',
            'awards', 'honors', 'achievements',
            'publications', 'publications and presentations',
            'languages', 'language skills'
        }
        
        # Problematic formatting elements
        self.problematic_elements = {
            'tables': r'<table|<td|<tr|<th',
            'columns': r'column|multicol|float:\s*(left|right)',
            'text_boxes': r'text\s*box|textbox',
            'headers_footers': r'header|footer',
            'images': r'<img|image|photo|picture',
            'charts': r'chart|graph|diagram',
            'shapes': r'shape|drawing|object',
            'special_chars': r'[^\x00-\x7F]',  # Non-ASCII characters
            'complex_formatting': r'font-family|font-size|color:|background:'
        }
        
        # Date format patterns
        self.date_patterns = [
            r'\d{1,2}/\d{4}',  # MM/YYYY
            r'\d{4}',          # YYYY
            r'\d{1,2}-\d{4}',  # MM-YYYY
            r'\d{1,2}\.\d{4}', # MM.YYYY
            r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{4}',  # Month YYYY
            r'\d{1,2}\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{4}'  # DD Month YYYY
        ]
    
    def check(self, resume_data: ResumeData) -> FormattingAnalysis:
        """Check resume formatting for ATS compatibility."""
        issues = []
        
        # Check for problematic elements
        issues.extend(self._check_problematic_elements(resume_data.raw_text))
        
        # Check section structure
        issues.extend(self._check_section_structure(resume_data))
        
        # Check header formatting
        issues.extend(self._check_headers(resume_data))
        
        # Check date formatting
        issues.extend(self._check_date_formatting(resume_data))
        
        # Check contact information formatting
        issues.extend(self._check_contact_formatting(resume_data))
        
        # Check overall structure
        issues.extend(self._check_overall_structure(resume_data))
        
        # Calculate scores
        ats_compatibility_score = self._calculate_ats_compatibility_score(issues)
        structure_score = self._calculate_structure_score(resume_data)
        
        # Check for proper headers and consistent formatting
        has_proper_headers = self._has_proper_headers(resume_data)
        has_consistent_formatting = self._has_consistent_formatting(resume_data)
        
        return FormattingAnalysis(
            ats_compatibility_score=ats_compatibility_score,
            issues=issues,
            structure_score=structure_score,
            has_proper_headers=has_proper_headers,
            has_consistent_formatting=has_consistent_formatting
        )
    
    def _check_problematic_elements(self, text: str) -> List[FormattingIssue]:
        """Check for ATS-problematic elements."""
        issues = []
        
        for element_type, pattern in self.problematic_elements.items():
            if re.search(pattern, text, re.IGNORECASE):
                severity = SeverityLevel.CRITICAL if element_type in ['tables', 'columns', 'text_boxes'] else SeverityLevel.MAJOR
                
                issues.append(FormattingIssue(
                    issue_type=element_type,
                    description=f"Found {element_type.replace('_', ' ')} which may not be parsed correctly by ATS",
                    severity=severity,
                    location="document",
                    suggestion=f"Remove or replace {element_type.replace('_', ' ')} with plain text formatting"
                ))
        
        return issues
    
    def _check_section_structure(self, resume_data: ResumeData) -> List[FormattingIssue]:
        """Check if resume has proper section structure."""
        issues = []
        
        # Check for required sections
        required_sections = ['contact', 'experience', 'education']
        missing_sections = []
        
        for section in required_sections:
            if not self._has_section(resume_data, section):
                missing_sections.append(section)
        
        if missing_sections:
            issues.append(FormattingIssue(
                issue_type="missing_sections",
                description=f"Missing required sections: {', '.join(missing_sections)}",
                severity=SeverityLevel.CRITICAL,
                location="document",
                suggestion="Add the missing sections to improve ATS compatibility"
            ))
        
        # Check section order
        section_order_issues = self._check_section_order(resume_data)
        issues.extend(section_order_issues)
        
        return issues
    
    def _check_headers(self, resume_data: ResumeData) -> List[FormattingIssue]:
        """Check if headers are properly formatted."""
        issues = []
        
        # Check for non-standard headers
        non_standard_headers = []
        for section_name in resume_data.sections.keys():
            if section_name.lower() not in self.ats_headers:
                non_standard_headers.append(section_name)
        
        if non_standard_headers:
            issues.append(FormattingIssue(
                issue_type="non_standard_headers",
                description=f"Non-standard section headers found: {', '.join(non_standard_headers)}",
                severity=SeverityLevel.MAJOR,
                location="headers",
                suggestion="Use standard section headers like 'Experience', 'Education', 'Skills' for better ATS parsing"
            ))
        
        # Check for missing section separators
        if not self._has_section_separators(resume_data.raw_text):
            issues.append(FormattingIssue(
                issue_type="missing_separators",
                description="Section headers may not be clearly separated",
                severity=SeverityLevel.MAJOR,
                location="headers",
                suggestion="Add clear spacing or formatting between sections"
            ))
        
        return issues
    
    def _check_date_formatting(self, resume_data: ResumeData) -> List[FormattingIssue]:
        """Check date formatting consistency."""
        issues = []
        
        all_dates = []
        
        # Extract dates from experience
        for exp in resume_data.experience:
            if exp.start_date:
                all_dates.append(exp.start_date)
            if exp.end_date:
                all_dates.append(exp.end_date)
        
        # Extract dates from education
        for edu in resume_data.education:
            if edu.graduation_date:
                all_dates.append(edu.graduation_date)
        
        # Check date format consistency
        date_formats = set()
        for date in all_dates:
            for pattern in self.date_patterns:
                if re.match(pattern, date, re.IGNORECASE):
                    date_formats.add(pattern)
                    break
        
        if len(date_formats) > 2:  # Too many different formats
            issues.append(FormattingIssue(
                issue_type="inconsistent_date_format",
                description="Multiple date formats found throughout the resume",
                severity=SeverityLevel.MAJOR,
                location="dates",
                suggestion="Use consistent date format (e.g., MM/YYYY or Month YYYY) throughout the resume"
            ))
        
        return issues
    
    def _check_contact_formatting(self, resume_data: ResumeData) -> List[FormattingIssue]:
        """Check contact information formatting."""
        issues = []
        contact = resume_data.contact_info
        
        # Check for missing essential contact info
        missing_contact = []
        if not contact.email:
            missing_contact.append("email")
        if not contact.phone:
            missing_contact.append("phone")
        
        if missing_contact:
            issues.append(FormattingIssue(
                issue_type="missing_contact_info",
                description=f"Missing contact information: {', '.join(missing_contact)}",
                severity=SeverityLevel.CRITICAL,
                location="contact",
                suggestion="Add missing contact information for better recruiter access"
            ))
        
        # Check email format
        if contact.email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', contact.email):
            issues.append(FormattingIssue(
                issue_type="invalid_email_format",
                description=f"Email format appears invalid: {contact.email}",
                severity=SeverityLevel.CRITICAL,
                location="contact",
                suggestion="Use a standard email format (e.g., name@domain.com)"
            ))
        
        return issues
    
    def _check_overall_structure(self, resume_data: ResumeData) -> List[FormattingIssue]:
        """Check overall resume structure."""
        issues = []
        
        # Check resume length
        word_count = len(resume_data.raw_text.split())
        if word_count < 200:
            issues.append(FormattingIssue(
                issue_type="too_short",
                description="Resume appears too short (less than 200 words)",
                severity=SeverityLevel.MAJOR,
                location="document",
                suggestion="Add more detail to experience and skills sections"
            ))
        elif word_count > 1000:
            issues.append(FormattingIssue(
                issue_type="too_long",
                description="Resume appears too long (more than 1000 words)",
                severity=SeverityLevel.MAJOR,
                location="document",
                suggestion="Consider condensing content to focus on most relevant information"
            ))
        
        # Check for excessive formatting
        if len(re.findall(r'[*_#]+', resume_data.raw_text)) > 20:
            issues.append(FormattingIssue(
                issue_type="excessive_formatting",
                description="Excessive use of formatting characters (asterisks, underscores, etc.)",
                severity=SeverityLevel.MAJOR,
                location="document",
                suggestion="Use minimal formatting for better ATS compatibility"
            ))
        
        return issues
    
    def _has_section(self, resume_data: ResumeData, section_name: str) -> bool:
        """Check if resume has a specific section."""
        section_keywords = {
            'contact': ['contact', 'personal', 'information'],
            'experience': ['experience', 'work', 'employment'],
            'education': ['education', 'academic', 'qualifications']
        }
        
        if section_name not in section_keywords:
            return True
        
        text = resume_data.raw_text.lower()
        return any(keyword in text for keyword in section_keywords[section_name])
    
    def _check_section_order(self, resume_data: ResumeData) -> List[FormattingIssue]:
        """Check if sections are in recommended order."""
        issues = []
        
        # Recommended order: Contact, Summary, Experience, Education, Skills
        section_order = ['contact', 'summary', 'experience', 'education', 'skills']
        
        # This is a simplified check - in a real implementation, you'd parse the actual order
        # For now, we'll just check if experience comes before education (common mistake)
        text = resume_data.raw_text.lower()
        
        exp_pos = text.find('experience')
        edu_pos = text.find('education')
        
        if exp_pos != -1 and edu_pos != -1 and edu_pos < exp_pos:
            issues.append(FormattingIssue(
                issue_type="section_order",
                description="Education section appears before Experience section",
                severity=SeverityLevel.NICE_TO_HAVE,
                location="structure",
                suggestion="Consider placing Experience before Education for better flow"
            ))
        
        return issues
    
    def _has_section_separators(self, text: str) -> bool:
        """Check if sections have clear separators."""
        # Look for common section separators
        separators = [r'\n\s*\n', r'\n-+\n', r'\n=+\n', r'\n\*\s*\n']
        
        for separator in separators:
            if re.search(separator, text):
                return True
        
        return False
    
    def _has_proper_headers(self, resume_data: ResumeData) -> bool:
        """Check if resume has proper section headers."""
        standard_headers_found = 0
        total_sections = len(resume_data.sections)
        
        for section_name in resume_data.sections.keys():
            if section_name.lower() in self.ats_headers:
                standard_headers_found += 1
        
        return standard_headers_found >= 3  # At least 3 standard sections
    
    def _has_consistent_formatting(self, resume_data: ResumeData) -> bool:
        """Check if resume has consistent formatting."""
        # Check date format consistency
        date_formats = set()
        
        for exp in resume_data.experience:
            if exp.start_date:
                for pattern in self.date_patterns:
                    if re.match(pattern, exp.start_date, re.IGNORECASE):
                        date_formats.add(pattern)
                        break
        
        return len(date_formats) <= 1  # Consistent date format
    
    def _calculate_ats_compatibility_score(self, issues: List[FormattingIssue]) -> float:
        """Calculate ATS compatibility score based on issues."""
        if not issues:
            return 100.0
        
        score = 100.0
        
        for issue in issues:
            if issue.severity == SeverityLevel.CRITICAL:
                score -= 20
            elif issue.severity == SeverityLevel.MAJOR:
                score -= 10
            else:  # NICE_TO_HAVE
                score -= 5
        
        return max(0.0, score)
    
    def _calculate_structure_score(self, resume_data: ResumeData) -> float:
        """Calculate structure score based on resume organization."""
        score = 0.0
        
        # Check for required sections
        required_sections = ['contact', 'experience', 'education']
        for section in required_sections:
            if self._has_section(resume_data, section):
                score += 25
        
        # Check for additional sections
        additional_sections = ['skills', 'summary']
        for section in additional_sections:
            if self._has_section(resume_data, section):
                score += 10
        
        # Check for proper headers
        if self._has_proper_headers(resume_data):
            score += 15
        
        # Check for consistent formatting
        if self._has_consistent_formatting(resume_data):
            score += 15
        
        return min(100.0, score)
