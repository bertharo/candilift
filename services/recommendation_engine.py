from typing import List, Dict, Any
from models.analysis_result import (
    KeywordAnalysis, FormattingAnalysis, ImpactAnalysis, 
    Recommendation, RecommendationCategory, SeverityLevel
)

class RecommendationEngine:
    def __init__(self):
        # Recommendation templates with examples
        self.recommendation_templates = {
            'missing_keywords': {
                'title': 'Add Missing Keywords',
                'description': 'Include important keywords from the job description to improve ATS matching',
                'examples': {
                    'before': 'Managed cross-functional teams',
                    'after': 'Led cross-functional product development teams using Agile methodology'
                }
            },
            'weak_keywords': {
                'title': 'Strengthen Keyword Usage',
                'description': 'Improve how keywords are integrated into your experience descriptions',
                'examples': {
                    'before': 'Worked with data analysis',
                    'after': 'Performed advanced data analysis using Python and SQL to drive business insights'
                }
            },
            'formatting_issues': {
                'title': 'Fix Formatting Issues',
                'description': 'Resolve formatting problems that may prevent ATS parsing',
                'examples': {
                    'before': 'Complex table layouts and columns',
                    'after': 'Simple, linear text format with clear section headers'
                }
            },
            'impact_statements': {
                'title': 'Improve Impact Statements',
                'description': 'Add quantifiable results and stronger action verbs to demonstrate impact',
                'examples': {
                    'before': 'Responsible for managing projects',
                    'after': 'Led 5+ product launches that increased revenue by 25% and improved user engagement by 40%'
                }
            },
            'generic_phrases': {
                'title': 'Replace Generic Phrases',
                'description': 'Replace vague language with specific, action-oriented statements',
                'examples': {
                    'before': 'Helped with various tasks',
                    'after': 'Collaborated with engineering teams to deliver 3 major feature releases ahead of schedule'
                }
            },
            'structure_issues': {
                'title': 'Improve Resume Structure',
                'description': 'Optimize section organization and flow for better readability',
                'examples': {
                    'before': 'Scattered information without clear sections',
                    'after': 'Clear sections: Contact, Summary, Experience, Education, Skills'
                }
            }
        }
    
    def generate_recommendations(self, keyword_analysis: KeywordAnalysis,
                               formatting_analysis: FormattingAnalysis,
                               impact_analysis: ImpactAnalysis,
                               ats_score: float,
                               recruiter_score: float) -> List[Recommendation]:
        """Generate prioritized recommendations based on analysis results."""
        recommendations = []
        
        # Generate keyword recommendations
        recommendations.extend(self._generate_keyword_recommendations(keyword_analysis))
        
        # Generate formatting recommendations
        recommendations.extend(self._generate_formatting_recommendations(formatting_analysis))
        
        # Generate impact recommendations
        recommendations.extend(self._generate_impact_recommendations(impact_analysis))
        
        # Generate structure recommendations
        recommendations.extend(self._generate_structure_recommendations(formatting_analysis))
        
        # Generate score-based recommendations
        recommendations.extend(self._generate_score_based_recommendations(ats_score, recruiter_score))
        
        # Sort by priority score
        recommendations.sort(key=lambda x: x.priority_score, reverse=True)
        
        # Limit to top 10 recommendations
        return recommendations[:10]
    
    def _generate_keyword_recommendations(self, keyword_analysis: KeywordAnalysis) -> List[Recommendation]:
        """Generate keyword-related recommendations."""
        recommendations = []
        
        # Missing keywords recommendation
        if keyword_analysis.missing_keywords:
            missing_count = len(keyword_analysis.missing_keywords)
            severity = SeverityLevel.CRITICAL if missing_count > 10 else SeverityLevel.MAJOR
            
            recommendations.append(Recommendation(
                category=RecommendationCategory.KEYWORD,
                severity=severity,
                title="Add Missing Keywords",
                description=f"Include {missing_count} missing keywords from the job description: {', '.join(keyword_analysis.missing_keywords[:5])}{'...' if missing_count > 5 else ''}",
                before_example="Led product development initiatives",
                after_example="Led cross-functional product development initiatives using Agile methodology and data-driven decision making",
                priority_score=self._calculate_keyword_priority_score(missing_count, severity)
            ))
        
        # Weak keyword matches recommendation
        if keyword_analysis.weak_keywords:
            weak_count = len(keyword_analysis.weak_keywords)
            severity = SeverityLevel.MAJOR if weak_count > 5 else SeverityLevel.NICE_TO_HAVE
            
            recommendations.append(Recommendation(
                category=RecommendationCategory.KEYWORD,
                severity=severity,
                title="Strengthen Keyword Integration",
                description=f"Improve integration of {weak_count} keywords that appear weakly in your resume",
                before_example="Worked with various technologies",
                after_example="Developed scalable solutions using Python, AWS, and machine learning algorithms",
                priority_score=self._calculate_keyword_priority_score(weak_count, severity)
            ))
        
        # Low keyword density recommendation
        low_density_keywords = [kw for kw, density in keyword_analysis.keyword_density.items() if density < 0.5]
        if low_density_keywords:
            recommendations.append(Recommendation(
                category=RecommendationCategory.KEYWORD,
                severity=SeverityLevel.MAJOR,
                title="Increase Keyword Density",
                description=f"Increase frequency of important keywords: {', '.join(low_density_keywords[:3])}",
                before_example="Project management experience",
                after_example="Extensive project management experience leading cross-functional teams and delivering complex initiatives",
                priority_score=7.0
            ))
        
        return recommendations
    
    def _generate_formatting_recommendations(self, formatting_analysis: FormattingAnalysis) -> List[Recommendation]:
        """Generate formatting-related recommendations."""
        recommendations = []
        
        # Critical formatting issues
        critical_issues = [issue for issue in formatting_analysis.issues 
                          if issue.severity == SeverityLevel.CRITICAL]
        
        if critical_issues:
            for issue in critical_issues[:3]:  # Limit to top 3 critical issues
                recommendations.append(Recommendation(
                    category=RecommendationCategory.FORMATTING,
                    severity=SeverityLevel.CRITICAL,
                    title=f"Fix Critical Formatting Issue: {issue.issue_type.replace('_', ' ').title()}",
                    description=issue.description,
                    before_example="Complex table layout with multiple columns",
                    after_example="Simple, linear text format with clear section headers",
                    priority_score=9.0
                ))
        
        # Major formatting issues
        major_issues = [issue for issue in formatting_analysis.issues 
                       if issue.severity == SeverityLevel.MAJOR]
        
        if major_issues:
            for issue in major_issues[:2]:  # Limit to top 2 major issues
                recommendations.append(Recommendation(
                    category=RecommendationCategory.FORMATTING,
                    severity=SeverityLevel.MAJOR,
                    title=f"Improve Formatting: {issue.issue_type.replace('_', ' ').title()}",
                    description=issue.description,
                    before_example="Inconsistent date formats (2020, Jan 2021, 12/2022)",
                    after_example="Consistent date format (MM/YYYY) throughout",
                    priority_score=7.0
                ))
        
        # Header recommendations
        if not formatting_analysis.has_proper_headers:
            recommendations.append(Recommendation(
                category=RecommendationCategory.FORMATTING,
                severity=SeverityLevel.MAJOR,
                title="Use Standard Section Headers",
                description="Replace custom headers with ATS-friendly standard headers",
                before_example="Professional Background, Academic Credentials, Technical Proficiencies",
                after_example="Experience, Education, Skills",
                priority_score=6.0
            ))
        
        return recommendations
    
    def _generate_impact_recommendations(self, impact_analysis: ImpactAnalysis) -> List[Recommendation]:
        """Generate impact-related recommendations."""
        recommendations = []
        
        # Weak impact statements
        if impact_analysis.weak_bullets:
            weak_count = len(impact_analysis.weak_bullets)
            severity = SeverityLevel.MAJOR if weak_count > 5 else SeverityLevel.NICE_TO_HAVE
            
            recommendations.append(Recommendation(
                category=RecommendationCategory.IMPACT,
                severity=severity,
                title="Strengthen Impact Statements",
                description=f"Improve {weak_count} bullet points to better demonstrate your impact and achievements",
                before_example="Responsible for managing various projects and tasks",
                after_example="Led 8 cross-functional projects that delivered $2M in cost savings and improved efficiency by 35%",
                priority_score=self._calculate_impact_priority_score(weak_count, severity)
            ))
        
        # Generic phrases
        if impact_analysis.generic_phrases_found:
            generic_count = len(impact_analysis.generic_phrases_found)
            
            recommendations.append(Recommendation(
                category=RecommendationCategory.IMPACT,
                severity=SeverityLevel.MAJOR,
                title="Replace Generic Phrases",
                description=f"Replace {generic_count} generic phrases with specific, action-oriented language",
                before_example="Helped with various tasks and responsibilities",
                after_example="Collaborated with 5+ teams to streamline processes and reduce project delivery time by 20%",
                priority_score=8.0
            ))
        
        # Missing metrics
        bullets_without_metrics = [b for b in impact_analysis.weak_bullets if not b.has_metrics]
        if bullets_without_metrics:
            recommendations.append(Recommendation(
                category=RecommendationCategory.IMPACT,
                severity=SeverityLevel.MAJOR,
                title="Add Quantifiable Metrics",
                description=f"Add specific numbers and metrics to {len(bullets_without_metrics)} bullet points",
                before_example="Improved team performance and efficiency",
                after_example="Increased team productivity by 40% and reduced project delivery time from 6 weeks to 4 weeks",
                priority_score=7.5
            ))
        
        return recommendations
    
    def _generate_structure_recommendations(self, formatting_analysis: FormattingAnalysis) -> List[Recommendation]:
        """Generate structure-related recommendations."""
        recommendations = []
        
        # Low structure score
        if formatting_analysis.structure_score < 70:
            recommendations.append(Recommendation(
                category=RecommendationCategory.STRUCTURE,
                severity=SeverityLevel.MAJOR,
                title="Improve Resume Structure",
                description="Reorganize sections and content flow for better readability and ATS compatibility",
                before_example="Mixed content without clear section separation",
                after_example="Clear sections with consistent formatting: Contact, Summary, Experience, Education, Skills",
                priority_score=6.5
            ))
        
        # Inconsistent formatting
        if not formatting_analysis.has_consistent_formatting:
            recommendations.append(Recommendation(
                category=RecommendationCategory.STRUCTURE,
                severity=SeverityLevel.MAJOR,
                title="Ensure Consistent Formatting",
                description="Apply consistent formatting throughout the resume for professional appearance",
                before_example="Mixed fonts, sizes, and date formats throughout",
                after_example="Consistent font, size, and date format (MM/YYYY) throughout",
                priority_score=6.0
            ))
        
        return recommendations
    
    def _generate_score_based_recommendations(self, ats_score: float, recruiter_score: float) -> List[Recommendation]:
        """Generate recommendations based on overall scores."""
        recommendations = []
        
        # Low ATS score
        if ats_score < 60:
            recommendations.append(Recommendation(
                category=RecommendationCategory.KEYWORD,
                severity=SeverityLevel.CRITICAL,
                title="Critical: Improve ATS Compatibility",
                description=f"Your ATS score is {ats_score:.0f}/100. Focus on keyword optimization and formatting fixes to pass ATS filters.",
                before_example="Resume with poor keyword coverage and formatting issues",
                after_example="ATS-optimized resume with relevant keywords and clean formatting",
                priority_score=10.0
            ))
        
        # Low recruiter score
        if recruiter_score < 60:
            recommendations.append(Recommendation(
                category=RecommendationCategory.IMPACT,
                severity=SeverityLevel.CRITICAL,
                title="Critical: Enhance Recruiter Appeal",
                description=f"Your recruiter score is {recruiter_score:.0f}/100. Strengthen impact statements and achievements to impress human reviewers.",
                before_example="Generic bullet points without measurable impact",
                after_example="Quantified achievements with strong action verbs and specific results",
                priority_score=9.5
            ))
        
        # Score improvement suggestions
        if ats_score >= 60 and recruiter_score >= 60:
            recommendations.append(Recommendation(
                category=RecommendationCategory.IMPACT,
                severity=SeverityLevel.NICE_TO_HAVE,
                title="Optimize for Excellence",
                description="Your resume is good but can be optimized further for maximum impact and ATS compatibility.",
                before_example="Good resume with room for improvement",
                after_example="Excellent resume optimized for both ATS and human reviewers",
                priority_score=5.0
            ))
        
        return recommendations
    
    def _calculate_keyword_priority_score(self, count: int, severity: SeverityLevel) -> float:
        """Calculate priority score for keyword recommendations."""
        base_score = {
            SeverityLevel.CRITICAL: 9.0,
            SeverityLevel.MAJOR: 7.0,
            SeverityLevel.NICE_TO_HAVE: 4.0
        }[severity]
        
        # Increase score based on count
        if count > 10:
            return base_score + 1.0
        elif count > 5:
            return base_score + 0.5
        else:
            return base_score
    
    def _calculate_impact_priority_score(self, count: int, severity: SeverityLevel) -> float:
        """Calculate priority score for impact recommendations."""
        base_score = {
            SeverityLevel.CRITICAL: 9.0,
            SeverityLevel.MAJOR: 7.5,
            SeverityLevel.NICE_TO_HAVE: 5.0
        }[severity]
        
        # Increase score based on count
        if count > 8:
            return base_score + 1.0
        elif count > 4:
            return base_score + 0.5
        else:
            return base_score
