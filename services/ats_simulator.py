import re
import random
import time
from typing import Dict, List, Tuple, Any
from models.resume_data import ResumeData
from models.job_data import JobData
from models.analysis_result import AnalysisResult, KeywordAnalysis, FormattingAnalysis, ImpactAnalysis

class ATSSimulator:
    """
    Simulates real ATS behavior and scoring patterns.
    This makes the analysis feel more authentic and realistic.
    """
    
    def __init__(self):
        # Real ATS platforms and their characteristics
        self.ats_platforms = {
            'workday': {
                'name': 'Workday',
                'keyword_weight': 0.6,
                'formatting_weight': 0.3,
                'structure_weight': 0.1,
                'strict_parsing': True,
                'favors_simple_format': True
            },
            'greenhouse': {
                'name': 'Greenhouse',
                'keyword_weight': 0.5,
                'formatting_weight': 0.25,
                'structure_weight': 0.25,
                'strict_parsing': False,
                'favors_simple_format': False
            },
            'lever': {
                'name': 'Lever',
                'keyword_weight': 0.55,
                'formatting_weight': 0.2,
                'structure_weight': 0.25,
                'strict_parsing': False,
                'favors_simple_format': True
            },
            'bamboohr': {
                'name': 'BambooHR',
                'keyword_weight': 0.4,
                'formatting_weight': 0.4,
                'structure_weight': 0.2,
                'strict_parsing': True,
                'favors_simple_format': True
            },
            'icims': {
                'name': 'iCIMS',
                'keyword_weight': 0.65,
                'formatting_weight': 0.2,
                'structure_weight': 0.15,
                'strict_parsing': True,
                'favors_simple_format': True
            }
        }
        
        # ATS parsing quirks and behaviors
        self.ats_quirks = {
            'header_parsing': {
                'workday': ['summary', 'experience', 'education', 'skills'],
                'greenhouse': ['summary', 'experience', 'education', 'skills', 'certifications'],
                'lever': ['summary', 'experience', 'education', 'skills'],
                'bamboohr': ['summary', 'experience', 'education', 'skills', 'awards'],
                'icims': ['summary', 'experience', 'education', 'skills']
            },
            'keyword_matching': {
                'exact_match_bonus': 1.2,
                'synonym_penalty': 0.8,
                'case_sensitive': False,
                'stemming_enabled': True
            },
            'formatting_penalties': {
                'tables': -15,
                'columns': -10,
                'images': -20,
                'special_chars': -5,
                'complex_formatting': -8
            }
        }
    
    def simulate_ats_analysis(self, resume_data: ResumeData, job_data: JobData, 
                            platform: str = None) -> Dict[str, Any]:
        """
        Simulate real ATS analysis with platform-specific behavior.
        """
        if not platform:
            platform = random.choice(list(self.ats_platforms.keys()))
        
        ats_config = self.ats_platforms[platform]
        
        # Simulate processing time (like real ATS)
        processing_steps = [
            "Parsing resume structure...",
            "Extracting contact information...",
            "Analyzing work experience...",
            "Matching keywords...",
            "Checking formatting compatibility...",
            "Calculating ATS score...",
            "Generating recommendations..."
        ]
        
        # Simulate realistic processing delays (reduced for better UX)
        # Temporarily disabled for debugging
        # for step in processing_steps:
        #     time.sleep(random.uniform(0.05, 0.1))
        
        # Perform platform-specific analysis
        analysis_result = self._perform_platform_analysis(resume_data, job_data, ats_config)
        
        # Add ATS-specific insights
        analysis_result['ats_platform'] = ats_config['name']
        analysis_result['processing_time'] = random.uniform(2.5, 4.2)
        analysis_result['ats_quirks'] = self._identify_ats_quirks(resume_data, ats_config)
        
        return analysis_result
    
    def _perform_platform_analysis(self, resume_data: ResumeData, job_data: JobData, 
                                 ats_config: Dict) -> Dict[str, Any]:
        """Perform analysis specific to the ATS platform."""
        
        # Keyword analysis with platform-specific weighting
        keyword_score = self._calculate_ats_keyword_score(resume_data, job_data, ats_config)
        
        # Formatting analysis with platform-specific rules
        formatting_score = self._calculate_ats_formatting_score(resume_data, ats_config)
        
        # Structure analysis
        structure_score = self._calculate_ats_structure_score(resume_data, ats_config)
        
        # Calculate weighted ATS score
        ats_score = (
            keyword_score * ats_config['keyword_weight'] +
            formatting_score * ats_config['formatting_weight'] +
            structure_score * ats_config['structure_weight']
        )
        
        # Apply platform-specific adjustments
        ats_score = self._apply_platform_adjustments(ats_score, resume_data, ats_config)
        
        return {
            'ats_score': min(100, max(0, ats_score)),
            'keyword_score': keyword_score,
            'formatting_score': formatting_score,
            'structure_score': structure_score,
            'platform_weights': {
                'keyword': ats_config['keyword_weight'],
                'formatting': ats_config['formatting_weight'],
                'structure': ats_config['structure_weight']
            }
        }
    
    def _calculate_ats_keyword_score(self, resume_data: ResumeData, job_data: JobData, 
                                   ats_config: Dict) -> float:
        """Calculate keyword score with ATS-specific matching rules."""
        resume_text = resume_data.get_all_text().lower()
        job_keywords = [skill.name.lower() for skill in job_data.required_skills + job_data.preferred_skills]
        
        # ATS keyword matching is often more strict
        exact_matches = 0
        partial_matches = 0
        
        for keyword in job_keywords:
            if keyword in resume_text:
                exact_matches += 1
            elif any(word in resume_text for word in keyword.split()):
                partial_matches += 0.5
        
        # Calculate base score
        total_keywords = len(job_keywords)
        if total_keywords == 0:
            return 100.0
        
        base_score = ((exact_matches + partial_matches) / total_keywords) * 100
        
        # Apply ATS-specific adjustments
        if ats_config['strict_parsing']:
            # Penalize partial matches more heavily
            base_score = exact_matches / total_keywords * 100 + partial_matches / total_keywords * 50
        
        return min(100, base_score)
    
    def _calculate_ats_formatting_score(self, resume_data: ResumeData, ats_config: Dict) -> float:
        """Calculate formatting score based on ATS compatibility."""
        base_score = 100.0
        text = resume_data.raw_text
        
        # Check for ATS-problematic elements
        penalties = self.ats_quirks['formatting_penalties']
        
        if re.search(r'<table|<td|<tr|<th', text, re.IGNORECASE):
            base_score += penalties['tables']
        
        if re.search(r'column|multicol|float:\s*(left|right)', text, re.IGNORECASE):
            base_score += penalties['columns']
        
        if re.search(r'<img|image|photo|picture', text, re.IGNORECASE):
            base_score += penalties['images']
        
        if re.search(r'[^\x00-\x7F]', text):
            base_score += penalties['special_chars']
        
        if re.search(r'font-family|font-size|color:|background:', text, re.IGNORECASE):
            base_score += penalties['complex_formatting']
        
        # Platform-specific formatting preferences
        if ats_config['favors_simple_format']:
            # Bonus for simple, clean formatting
            if not re.search(r'[^\w\s\.\,\;\:\!\?\-\(\)]', text):
                base_score += 5
        
        return min(100, max(0, base_score))
    
    def _calculate_ats_structure_score(self, resume_data: ResumeData, ats_config: Dict) -> float:
        """Calculate structure score based on ATS parsing requirements."""
        score = 0.0
        max_score = 100.0
        
        # Check for required sections
        required_sections = self.ats_quirks['header_parsing'].get(
            list(self.ats_platforms.keys())[0], 
            ['summary', 'experience', 'education', 'skills']
        )
        
        found_sections = 0
        for section in required_sections:
            if section in resume_data.sections:
                found_sections += 1
        
        # Section completeness (40 points)
        section_score = (found_sections / len(required_sections)) * 40
        score += section_score
        
        # Contact information (20 points)
        contact = resume_data.contact_info
        contact_score = 0
        if contact.name:
            contact_score += 5
        if contact.email:
            contact_score += 5
        if contact.phone:
            contact_score += 5
        if contact.location:
            contact_score += 5
        score += contact_score
        
        # Experience formatting (20 points)
        if resume_data.experience:
            exp_score = min(20, len(resume_data.experience) * 5)
            score += exp_score
        
        # Skills section (10 points)
        if resume_data.skills:
            skills_score = min(10, len(resume_data.skills) * 0.5)
            score += skills_score
        
        # Education (10 points)
        if resume_data.education:
            score += 10
        
        return min(100, score)
    
    def _apply_platform_adjustments(self, score: float, resume_data: ResumeData, 
                                  ats_config: Dict) -> float:
        """Apply platform-specific adjustments to the score."""
        adjusted_score = score
        
        # Workday is known for being strict with formatting
        if ats_config['name'] == 'Workday':
            if self._has_complex_formatting(resume_data.raw_text):
                adjusted_score -= 10
        
        # Greenhouse is more lenient with modern formats
        elif ats_config['name'] == 'Greenhouse':
            if self._has_modern_formatting(resume_data.raw_text):
                adjusted_score += 5
        
        # iCIMS heavily weights keywords
        elif ats_config['name'] == 'iCIMS':
            keyword_density = self._calculate_keyword_density(resume_data)
            if keyword_density > 0.05:  # 5% keyword density
                adjusted_score += 8
        
        return adjusted_score
    
    def _has_complex_formatting(self, text: str) -> bool:
        """Check if resume has complex formatting that ATS might struggle with."""
        complex_patterns = [
            r'<table|<td|<tr|<th',
            r'column|multicol',
            r'font-family|font-size|color:',
            r'<img|image|photo',
            r'[^\x00-\x7F]'  # Non-ASCII characters
        ]
        
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in complex_patterns)
    
    def _has_modern_formatting(self, text: str) -> bool:
        """Check if resume has modern but ATS-friendly formatting."""
        modern_patterns = [
            r'##\s+',  # Markdown headers
            r'\*\*.*?\*\*',  # Bold text
            r'^\s*[-•]\s+',  # Bullet points
        ]
        
        return any(re.search(pattern, text, re.MULTILINE) for pattern in modern_patterns)
    
    def _calculate_keyword_density(self, resume_data: ResumeData) -> float:
        """Calculate keyword density in the resume."""
        text = resume_data.get_all_text()
        words = text.split()
        if not words:
            return 0.0
        
        # Count common resume keywords
        resume_keywords = [
            'experience', 'skills', 'education', 'project', 'management',
            'development', 'analysis', 'leadership', 'team', 'results',
            'achieved', 'improved', 'increased', 'developed', 'created'
        ]
        
        keyword_count = sum(1 for word in words if word.lower() in resume_keywords)
        return keyword_count / len(words)
    
    def _identify_ats_quirks(self, resume_data: ResumeData, ats_config: Dict) -> List[str]:
        """Identify specific quirks or issues with this ATS platform."""
        quirks = []
        
        if ats_config['strict_parsing']:
            if self._has_complex_formatting(resume_data.raw_text):
                quirks.append(f"{ats_config['name']} has strict parsing rules and may struggle with complex formatting")
        
        if ats_config['favors_simple_format']:
            if not self._has_modern_formatting(resume_data.raw_text):
                quirks.append(f"{ats_config['name']} works best with simple, clean formatting")
        
        # Check for missing required sections
        required_sections = self.ats_quirks['header_parsing'].get(
            list(self.ats_platforms.keys())[0], 
            ['summary', 'experience', 'education', 'skills']
        )
        
        missing_sections = [s for s in required_sections if s not in resume_data.sections]
        if missing_sections:
            quirks.append(f"Missing sections that {ats_config['name']} typically looks for: {', '.join(missing_sections)}")
        
        return quirks
    
    def get_ats_platform_recommendations(self, platform: str) -> List[str]:
        """Get specific recommendations for a particular ATS platform."""
        recommendations = {
            'workday': [
                "Use simple, linear formatting without tables or columns",
                "Include clear section headers: Summary, Experience, Education, Skills",
                "Avoid special characters and complex formatting",
                "Focus on exact keyword matches rather than synonyms"
            ],
            'greenhouse': [
                "Greenhouse is more flexible with modern formatting",
                "Include a strong summary section",
                "Use bullet points for experience descriptions",
                "Include relevant certifications if applicable"
            ],
            'lever': [
                "Lever works well with clean, professional formatting",
                "Focus on quantifiable achievements in experience",
                "Include skills section with relevant keywords",
                "Keep formatting simple but modern"
            ],
            'bamboohr': [
                "BambooHR is strict about formatting - avoid tables and columns",
                "Use standard section headers",
                "Include contact information clearly at the top",
                "Focus on clear, readable text formatting"
            ],
            'icims': [
                "iCIMS heavily weights keyword matching",
                "Include as many relevant keywords as possible",
                "Use standard resume sections",
                "Avoid complex formatting that might confuse parsing"
            ]
        }
        
        return recommendations.get(platform, [
            "Use standard resume formatting",
            "Include clear section headers",
            "Focus on keyword optimization",
            "Avoid complex formatting elements"
        ])
