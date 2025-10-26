"""
Resume and Job Description Analysis Engine for CandiLift
"""

import re
import tempfile
import os
from typing import Dict, List, Any, Optional
from pdfminer.high_level import extract_text
from docx import Document
import requests
from bs4 import BeautifulSoup


class ResumeAnalyzer:
    """Analyzes resume content and structure"""
    
    def __init__(self):
        self.skills_keywords = {
            'programming': ['python', 'javascript', 'java', 'c++', 'c#', 'go', 'rust', 'php', 'ruby', 'swift', 'kotlin'],
            'web': ['html', 'css', 'react', 'vue', 'angular', 'node.js', 'express', 'django', 'flask', 'spring'],
            'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins'],
            'data': ['pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'machine learning', 'ai'],
            'mobile': ['ios', 'android', 'react native', 'flutter', 'xamarin'],
            'tools': ['git', 'github', 'gitlab', 'jira', 'confluence', 'slack', 'figma', 'photoshop']
        }
    
    def extract_text_from_file(self, file_content: bytes, filename: str) -> str:
        """Extract text from PDF or DOCX file"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_file:
                temp_file.write(file_content)
                temp_file_path = temp_file.name
            
            # Extract text based on file type
            if filename.lower().endswith('.pdf'):
                text = extract_text(temp_file_path)
            elif filename.lower().endswith('.docx'):
                doc = Document(temp_file_path)
                text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
            else:
                text = file_content.decode('utf-8', errors='ignore')
            
            # Clean up temp file
            os.unlink(temp_file_path)
            return text
            
        except Exception as e:
            print(f"Error extracting text: {e}")
            return ""
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume text"""
        text_lower = text.lower()
        found_skills = []
        
        for category, skills in self.skills_keywords.items():
            for skill in skills:
                if skill in text_lower:
                    found_skills.append(skill.title())
        
        return list(set(found_skills))
    
    def extract_experience(self, text: str) -> Dict[str, Any]:
        """Extract work experience information"""
        # Look for years of experience patterns
        years_pattern = r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)'
        years_match = re.search(years_pattern, text.lower())
        
        # Look for job titles
        title_patterns = [
            r'(?:senior|sr\.?|lead|principal|staff)\s+(\w+)',
            r'(\w+)\s+(?:engineer|developer|manager|analyst|specialist)',
            r'(?:software|web|mobile|data|devops)\s+(\w+)'
        ]
        
        titles = []
        for pattern in title_patterns:
            matches = re.findall(pattern, text.lower())
            titles.extend([match.title() for match in matches])
        
        return {
            'years_experience': int(years_match.group(1)) if years_match else 0,
            'job_titles': list(set(titles))[:5]  # Top 5 unique titles
        }
    
    def analyze_format(self, text: str) -> Dict[str, Any]:
        """Analyze resume format and structure"""
        lines = text.split('\n')
        
        # Check for common ATS-friendly elements
        has_contact_info = any(keyword in text.lower() for keyword in ['email', 'phone', 'linkedin', '@'])
        has_summary = any(keyword in text.lower() for keyword in ['summary', 'objective', 'profile'])
        has_education = any(keyword in text.lower() for keyword in ['education', 'university', 'college', 'degree'])
        has_experience = any(keyword in text.lower() for keyword in ['experience', 'employment', 'work history'])
        
        # Check for problematic elements
        has_tables = '|' in text or '\t' in text
        has_images = '[image]' in text.lower() or 'figure' in text.lower()
        has_headers_footers = any(keyword in text.lower() for keyword in ['page', 'header', 'footer'])
        
        return {
            'has_contact_info': has_contact_info,
            'has_summary': has_summary,
            'has_education': has_education,
            'has_experience': has_experience,
            'has_tables': has_tables,
            'has_images': has_images,
            'has_headers_footers': has_headers_footers,
            'total_lines': len(lines),
            'word_count': len(text.split())
        }


class JobAnalyzer:
    """Analyzes job description content"""
    
    def __init__(self):
        self.skills_keywords = {
            'programming': ['python', 'javascript', 'java', 'c++', 'c#', 'go', 'rust', 'php', 'ruby', 'swift', 'kotlin'],
            'web': ['html', 'css', 'react', 'vue', 'angular', 'node.js', 'express', 'django', 'flask', 'spring'],
            'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins'],
            'data': ['pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'machine learning', 'ai'],
            'mobile': ['ios', 'android', 'react native', 'flutter', 'xamarin'],
            'tools': ['git', 'github', 'gitlab', 'jira', 'confluence', 'slack', 'figma', 'photoshop']
        }
    
    def scrape_job_url(self, url: str) -> str:
        """Scrape job description from URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Try to find job description content
            job_content = soup.find('div', class_=re.compile(r'job|description|content', re.I))
            if not job_content:
                job_content = soup.find('main')
            if not job_content:
                job_content = soup.find('body')
            
            return job_content.get_text() if job_content else soup.get_text()
            
        except Exception as e:
            print(f"Error scraping URL {url}: {e}")
            return ""
    
    def extract_required_skills(self, text: str) -> Dict[str, List[str]]:
        """Extract required skills from job description"""
        text_lower = text.lower()
        required_skills = {}
        
        for category, skills in self.skills_keywords.items():
            category_skills = []
            for skill in skills:
                if skill in text_lower:
                    category_skills.append(skill.title())
            if category_skills:
                required_skills[category] = category_skills
        
        return required_skills
    
    def extract_requirements(self, text: str) -> Dict[str, Any]:
        """Extract job requirements and qualifications"""
        text_lower = text.lower()
        
        # Extract years of experience required
        years_pattern = r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)'
        years_match = re.search(years_pattern, text_lower)
        
        # Extract education requirements
        education_keywords = ['bachelor', 'master', 'phd', 'degree', 'university', 'college']
        education_required = any(keyword in text_lower for keyword in education_keywords)
        
        # Extract seniority level
        seniority_keywords = {
            'entry': ['entry', 'junior', 'associate', 'intern'],
            'mid': ['mid', 'intermediate', 'experienced'],
            'senior': ['senior', 'sr', 'lead', 'principal', 'staff'],
            'executive': ['director', 'vp', 'cto', 'ceo', 'manager', 'head']
        }
        
        seniority_level = 'mid'  # default
        for level, keywords in seniority_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                seniority_level = level
                break
        
        return {
            'years_experience_required': int(years_match.group(1)) if years_match else 0,
            'education_required': education_required,
            'seniority_level': seniority_level
        }


class ScoringEngine:
    """Calculates ATS and recruiter scores"""
    
    def calculate_ats_score(self, resume_data: Dict, job_data: Dict) -> Dict[str, Any]:
        """Calculate ATS compatibility score"""
        score = 0
        max_score = 100
        drivers = []
        
        # Format compliance (30 points)
        format_score = 0
        if resume_data['format']['has_contact_info']:
            format_score += 10
        if resume_data['format']['has_summary']:
            format_score += 10
        if resume_data['format']['has_experience']:
            format_score += 10
        if not resume_data['format']['has_tables']:
            format_score += 5
        if not resume_data['format']['has_images']:
            format_score += 5
        
        score += format_score
        drivers.append({
            'component': 'Format Compliance',
            'score': format_score,
            'explanation': f"Resume format is {'mostly' if format_score >= 20 else 'partially'} ATS-friendly"
        })
        
        # Keyword matching (40 points)
        resume_skills = set(resume_data['skills'])
        job_skills = set()
        for category_skills in job_data['required_skills'].values():
            job_skills.update(category_skills)
        
        if job_skills:
            keyword_match_ratio = len(resume_skills.intersection(job_skills)) / len(job_skills)
            keyword_score = min(40, int(keyword_match_ratio * 40))
        else:
            keyword_score = 20
        
        score += keyword_score
        drivers.append({
            'component': 'Keyword Matching',
            'score': keyword_score,
            'explanation': f"{len(resume_skills.intersection(job_skills))} of {len(job_skills)} required skills found"
        })
        
        # Experience relevance (30 points)
        resume_years = resume_data['experience']['years_experience']
        job_years = job_data['requirements']['years_experience_required']
        
        if job_years == 0:
            exp_score = 25  # No specific requirement
        elif resume_years >= job_years:
            exp_score = 30  # Meets or exceeds requirement
        elif resume_years >= job_years * 0.7:
            exp_score = 20  # Close to requirement
        else:
            exp_score = 10  # Below requirement
        
        score += exp_score
        drivers.append({
            'component': 'Experience Relevance',
            'score': exp_score,
            'explanation': f"{resume_years} years experience vs {job_years} required"
        })
        
        return {
            'score': min(score, max_score),
            'drivers': drivers
        }
    
    def calculate_recruiter_score(self, resume_data: Dict, job_data: Dict) -> Dict[str, Any]:
        """Calculate recruiter appeal score"""
        score = 0
        max_score = 100
        drivers = []
        
        # Content quality (40 points)
        word_count = resume_data['format']['word_count']
        if word_count >= 400:
            content_score = 40
        elif word_count >= 300:
            content_score = 30
        elif word_count >= 200:
            content_score = 20
        else:
            content_score = 10
        
        score += content_score
        drivers.append({
            'component': 'Content Quality',
            'score': content_score,
            'explanation': f"Resume has {word_count} words - {'good' if word_count >= 300 else 'could be more detailed'}"
        })
        
        # Skills alignment (35 points)
        resume_skills = set(resume_data['skills'])
        job_skills = set()
        for category_skills in job_data['required_skills'].values():
            job_skills.update(category_skills)
        
        if job_skills:
            skills_ratio = len(resume_skills.intersection(job_skills)) / len(job_skills)
            skills_score = int(skills_ratio * 35)
        else:
            skills_score = 20
        
        score += skills_score
        drivers.append({
            'component': 'Skills Alignment',
            'score': skills_score,
            'explanation': f"Strong alignment with job requirements" if skills_score >= 25 else "Some skills match job requirements"
        })
        
        # Professional presentation (25 points)
        presentation_score = 0
        if resume_data['format']['has_summary']:
            presentation_score += 10
        if resume_data['format']['has_education']:
            presentation_score += 10
        if resume_data['format']['word_count'] >= 300:
            presentation_score += 5
        
        score += presentation_score
        drivers.append({
            'component': 'Professional Presentation',
            'score': presentation_score,
            'explanation': f"Resume presents {'well' if presentation_score >= 20 else 'adequately'} professionally"
        })
        
        return {
            'score': min(score, max_score),
            'drivers': drivers
        }


class RecommendationEngine:
    """Generates actionable recommendations"""
    
    def generate_recommendations(self, resume_data: Dict, job_data: Dict, scores: Dict) -> List[Dict[str, Any]]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Skills gap analysis
        resume_skills = set(resume_data['skills'])
        job_skills = set()
        for category_skills in job_data['required_skills'].values():
            job_skills.update(category_skills)
        
        missing_skills = job_skills - resume_skills
        if missing_skills:
            recommendations.append({
                'category': 'Skills Enhancement',
                'description': f"Add {len(missing_skills)} missing skills mentioned in the job description",
                'estimated_lift': min(15, len(missing_skills) * 3),
                'example': f"Consider adding: {', '.join(list(missing_skills)[:3])}"
            })
        
        # Experience gap
        resume_years = resume_data['experience']['years_experience']
        job_years = job_data['requirements']['years_experience_required']
        
        if resume_years < job_years and job_years > 0:
            recommendations.append({
                'category': 'Experience Enhancement',
                'description': f"Highlight relevant experience to bridge the {job_years - resume_years} year gap",
                'estimated_lift': 10,
                'example': "Emphasize transferable skills and quantify achievements with metrics"
            })
        
        # Format improvements
        if resume_data['format']['has_tables']:
            recommendations.append({
                'category': 'Format Optimization',
                'description': "Remove tables and use standard formatting for better ATS compatibility",
                'estimated_lift': 8,
                'example': "Convert table-based layouts to standard bullet points"
            })
        
        if not resume_data['format']['has_summary']:
            recommendations.append({
                'category': 'Content Enhancement',
                'description': "Add a professional summary section to highlight key qualifications",
                'estimated_lift': 12,
                'example': "Include 2-3 sentences summarizing your experience and value proposition"
            })
        
        # Content length
        word_count = resume_data['format']['word_count']
        if word_count < 300:
            recommendations.append({
                'category': 'Content Expansion',
                'description': "Expand resume content to provide more detail about your experience",
                'estimated_lift': 10,
                'example': "Add more bullet points under each role with quantified achievements"
            })
        
        return recommendations[:5]  # Return top 5 recommendations


class AnalysisEngine:
    """Main analysis engine that coordinates all components"""
    
    def __init__(self):
        self.resume_analyzer = ResumeAnalyzer()
        self.job_analyzer = JobAnalyzer()
        self.scoring_engine = ScoringEngine()
        self.recommendation_engine = RecommendationEngine()
    
    def analyze(self, resume_file_content: bytes, resume_filename: str, 
                job_description: str = "", job_url: str = "") -> Dict[str, Any]:
        """Perform complete analysis"""
        
        # Extract job description text
        if job_url:
            job_text = self.job_analyzer.scrape_job_url(job_url)
        else:
            job_text = job_description
        
        # Analyze resume
        resume_text = self.resume_analyzer.extract_text_from_file(resume_file_content, resume_filename)
        resume_skills = self.resume_analyzer.extract_skills(resume_text)
        resume_experience = self.resume_analyzer.extract_experience(resume_text)
        resume_format = self.resume_analyzer.analyze_format(resume_text)
        
        resume_data = {
            'skills': resume_skills,
            'experience': resume_experience,
            'format': resume_format,
            'text': resume_text[:500]  # First 500 chars for debugging
        }
        
        # Analyze job description
        job_skills = self.job_analyzer.extract_required_skills(job_text)
        job_requirements = self.job_analyzer.extract_requirements(job_text)
        
        job_data = {
            'required_skills': job_skills,
            'requirements': job_requirements,
            'text': job_text[:500]  # First 500 chars for debugging
        }
        
        # Calculate scores
        ats_result = self.scoring_engine.calculate_ats_score(resume_data, job_data)
        recruiter_result = self.scoring_engine.calculate_recruiter_score(resume_data, job_data)
        
        # Generate recommendations
        recommendations = self.recommendation_engine.generate_recommendations(
            resume_data, job_data, {'ats': ats_result, 'recruiter': recruiter_result}
        )
        
        # Gap analysis
        resume_skills_set = set(resume_skills)
        job_skills_set = set()
        for category_skills in job_skills.values():
            job_skills_set.update(category_skills)
        
        gap_analysis = {
            'missing_skills': list(job_skills_set - resume_skills_set),
            'present_skills': list(resume_skills_set.intersection(job_skills_set))
        }
        
        # Calculate likelihood of hearing back with domain fit assessment
        likelihood_result = self._calculate_likelihood_score(
            ats_result['score'], 
            recruiter_result['score'], 
            resume_data, 
            job_data
        )
        
        return {
            'ats_score': ats_result['score'],
            'recruiter_score': recruiter_result['score'],
            'likelihood_score': likelihood_result['score'],
            'likelihood_explanation': likelihood_result['explanation'],
            'likelihood_improvements': likelihood_result['improvements'],
            'domain_fit': likelihood_result['domain_fit'],
            'score_drivers': ats_result['drivers'] + recruiter_result['drivers'],
            'recommendations': recommendations,
            'gap_analysis': gap_analysis,
            'debug_info': {
                'resume_text_preview': resume_text[:200],
                'job_text_preview': job_text[:200],
                'resume_skills_found': resume_skills,
                'job_skills_found': job_skills
            }
        }
    
    def _calculate_likelihood_score(self, ats_score: int, recruiter_score: int, resume_data: Dict, job_data: Dict) -> Dict[str, Any]:
        """Calculate realistic likelihood with domain fit assessment and improvement suggestions"""
        
        # Weighted combination: ATS (60%) + Recruiter (40%)
        weighted_score = (ats_score * 0.6) + (recruiter_score * 0.4)
        
        # Domain fit assessment
        domain_fit = self._assess_domain_fit(resume_data, job_data)
        
        # Apply harsh market reality factors
        market_adjustment = 0.15  # Only 15% of theoretical score due to extreme competition
        competition_penalty = 0.8  # 80% penalty for typical job market competition
        
        # Apply domain fit penalty if poor match
        if domain_fit['fit_level'] == 'poor':
            domain_penalty = 0.5  # 50% penalty for poor domain fit
        elif domain_fit['fit_level'] == 'moderate':
            domain_penalty = 0.8  # 20% penalty for moderate fit
        else:
            domain_penalty = 1.0  # No penalty for good fit
        
        final_score = int(weighted_score * market_adjustment * competition_penalty * domain_penalty)
        final_score = min(final_score, 25)  # Cap at realistic maximum
        
        # Generate explanations and improvements
        explanation, improvements = self._generate_likelihood_feedback(final_score, domain_fit, resume_data, job_data)
        
        return {
            'score': final_score,
            'explanation': explanation,
            'improvements': improvements,
            'domain_fit': domain_fit
        }
    
    def _assess_domain_fit(self, resume_data: Dict, job_data: Dict) -> Dict[str, Any]:
        """Assess how well the candidate's background matches the job domain"""
        
        resume_skills = set(resume_data['skills'])
        job_skills = set()
        for category_skills in job_data['required_skills'].values():
            job_skills.update(category_skills)
        
        # Calculate skill overlap
        skill_overlap = len(resume_skills.intersection(job_skills))
        total_job_skills = len(job_skills)
        
        if total_job_skills == 0:
            overlap_ratio = 0
        else:
            overlap_ratio = skill_overlap / total_job_skills
        
        # Assess experience level match
        resume_years = resume_data['experience']['years_experience']
        job_years = job_data['requirements']['years_experience_required']
        
        # Determine fit level
        if overlap_ratio >= 0.7 and resume_years >= job_years * 0.8:
            fit_level = 'good'
            fit_description = "Strong domain alignment with relevant skills and experience"
        elif overlap_ratio >= 0.4 and resume_years >= job_years * 0.5:
            fit_level = 'moderate'
            fit_description = "Some relevant skills but may need additional experience or training"
        else:
            fit_level = 'poor'
            fit_description = "Limited domain alignment - consider roles more closely matching your background"
        
        return {
            'fit_level': fit_level,
            'description': fit_description,
            'skill_overlap_ratio': overlap_ratio,
            'skill_overlap_count': skill_overlap,
            'total_job_skills': total_job_skills,
            'experience_match': resume_years >= job_years * 0.8 if job_years > 0 else True
        }
    
    def _generate_likelihood_feedback(self, score: int, domain_fit: Dict, resume_data: Dict, job_data: Dict) -> tuple:
        """Generate explanation and improvement suggestions for likelihood score"""
        
        # Base explanation
        if score >= 20:
            explanation = "Above average chance, but still low. Even excellent resumes face 100+ competitors per role."
        elif score >= 15:
            explanation = "Below average chance. Most applications get no response due to overwhelming competition."
        elif score >= 10:
            explanation = "Very low chance. Significant improvements needed to stand out from hundreds of applicants."
        elif score >= 5:
            explanation = "Minimal chance. Resume needs major improvements to be competitive in today's market."
        else:
            explanation = "Extremely low chance. Resume likely won't pass initial screening in competitive market."
        
        # Add domain fit context
        if domain_fit['fit_level'] == 'poor':
            explanation += f" Additionally, {domain_fit['description'].lower()}"
        elif domain_fit['fit_level'] == 'moderate':
            explanation += f" Note: {domain_fit['description'].lower()}"
        
        # Generate specific improvements
        improvements = []
        
        # Domain fit improvements
        if domain_fit['fit_level'] == 'poor':
            improvements.append({
                'category': 'Domain Alignment',
                'suggestion': 'Consider applying to roles that better match your current skills and experience',
                'impact': 'High - Better fit roles will have much higher response rates',
                'alternative': 'Look for jobs in your current domain or adjacent fields'
            })
        
        # Skill gap improvements
        missing_skills = job_data['required_skills']
        if missing_skills:
            top_missing = []
            for category, skills in missing_skills.items():
                top_missing.extend(skills[:2])  # Top 2 from each category
            
            if top_missing:
                improvements.append({
                    'category': 'Skills Development',
                    'suggestion': f'Learn or highlight: {", ".join(top_missing[:3])}',
                    'impact': 'Medium - Adding key skills can significantly improve your chances',
                    'alternative': 'Take online courses or projects to demonstrate these skills'
                })
        
        # Experience improvements
        resume_years = resume_data['experience']['years_experience']
        job_years = job_data['requirements']['years_experience_required']
        
        if resume_years < job_years and job_years > 0:
            improvements.append({
                'category': 'Experience Gap',
                'suggestion': f'Highlight transferable experience and quantify achievements',
                'impact': 'Medium - Show how your experience applies to this role',
                'alternative': 'Consider entry-level or mid-level positions in this field'
            })
        
        # Format improvements
        if not resume_data['format']['has_summary']:
            improvements.append({
                'category': 'Resume Format',
                'suggestion': 'Add a professional summary highlighting relevant experience',
                'impact': 'Low-Medium - Helps recruiters quickly understand your fit',
                'alternative': 'Use the summary to bridge domain gaps'
            })
        
        return explanation, improvements
