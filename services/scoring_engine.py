from typing import Dict, Any
from models.analysis_result import KeywordAnalysis, FormattingAnalysis, ImpactAnalysis

class ScoringEngine:
    def __init__(self):
        # Scoring weights for ATS score
        self.ats_weights = {
            'keyword_coverage': 0.5,      # 50% - Most important for ATS
            'formatting': 0.3,            # 30% - Critical for ATS parsing
            'structure': 0.2              # 20% - Important for organization
        }
        
        # Scoring weights for Recruiter score
        self.recruiter_weights = {
            'impact': 0.4,                # 40% - Most important for human readers
            'formatting': 0.25,           # 25% - Readability and professionalism
            'structure': 0.2,             # 20% - Organization and flow
            'keyword_relevance': 0.15     # 15% - Still important for matching
        }
        
        # Score thresholds
        self.score_thresholds = {
            'excellent': 85,
            'good': 70,
            'fair': 55,
            'poor': 40
        }
    
    def calculate_ats_score(self, keyword_analysis: KeywordAnalysis, 
                          formatting_analysis: FormattingAnalysis) -> float:
        """
        Calculate ATS compatibility score (0-100).
        
        ATS score focuses on:
        - Keyword coverage and matching
        - Formatting compatibility
        - Structure and organization
        """
        # Keyword coverage component (0-100)
        keyword_score = keyword_analysis.coverage_score
        
        # Formatting component (0-100)
        formatting_score = formatting_analysis.ats_compatibility_score
        
        # Structure component (0-100)
        structure_score = formatting_analysis.structure_score
        
        # Calculate weighted score
        ats_score = (
            keyword_score * self.ats_weights['keyword_coverage'] +
            formatting_score * self.ats_weights['formatting'] +
            structure_score * self.ats_weights['structure']
        )
        
        # Apply penalties for critical issues
        critical_issues = [issue for issue in formatting_analysis.issues 
                          if issue.severity.value == 'critical']
        
        if critical_issues:
            penalty = min(20, len(critical_issues) * 5)  # Max 20 point penalty
            ats_score -= penalty
        
        return max(0.0, min(100.0, ats_score))
    
    def calculate_recruiter_score(self, impact_analysis: ImpactAnalysis, 
                                formatting_analysis: FormattingAnalysis) -> float:
        """
        Calculate recruiter appeal score (0-100).
        
        Recruiter score focuses on:
        - Impact and achievements
        - Readability and formatting
        - Structure and flow
        - Overall presentation quality
        """
        # Impact component (0-100)
        impact_score = impact_analysis.impact_score
        
        # Formatting component (0-100) - weighted for readability
        formatting_score = self._calculate_readability_score(formatting_analysis)
        
        # Structure component (0-100)
        structure_score = formatting_analysis.structure_score
        
        # Keyword relevance component (0-100) - based on strong keyword matches
        keyword_relevance_score = self._calculate_keyword_relevance_score(impact_analysis)
        
        # Calculate weighted score
        recruiter_score = (
            impact_score * self.recruiter_weights['impact'] +
            formatting_score * self.recruiter_weights['formatting'] +
            structure_score * self.recruiter_weights['structure'] +
            keyword_relevance_score * self.recruiter_weights['keyword_relevance']
        )
        
        # Apply bonuses for excellent content
        if impact_analysis.impact_score >= 80:
            recruiter_score += 5  # Bonus for strong impact statements
        
        if formatting_analysis.has_consistent_formatting:
            recruiter_score += 3  # Bonus for consistent formatting
        
        return max(0.0, min(100.0, recruiter_score))
    
    def _calculate_readability_score(self, formatting_analysis: FormattingAnalysis) -> float:
        """Calculate readability score based on formatting analysis."""
        score = formatting_analysis.ats_compatibility_score
        
        # Bonus for proper headers
        if formatting_analysis.has_proper_headers:
            score += 10
        
        # Bonus for consistent formatting
        if formatting_analysis.has_consistent_formatting:
            score += 10
        
        # Penalty for major formatting issues
        major_issues = [issue for issue in formatting_analysis.issues 
                       if issue.severity.value == 'major']
        score -= len(major_issues) * 5
        
        return max(0.0, min(100.0, score))
    
    def _calculate_keyword_relevance_score(self, impact_analysis: ImpactAnalysis) -> float:
        """Calculate keyword relevance score based on impact analysis."""
        # This is a simplified calculation
        # In a real implementation, you'd analyze how well keywords are integrated
        # into impact statements rather than just listed
        
        total_bullets = len(impact_analysis.strong_bullets) + len(impact_analysis.weak_bullets)
        if total_bullets == 0:
            return 50.0  # Neutral score if no bullets
        
        # Higher score for more strong bullets with good integration
        strong_ratio = len(impact_analysis.strong_bullets) / total_bullets
        
        # Base score on ratio of strong bullets
        base_score = strong_ratio * 100
        
        # Bonus for bullets with metrics (indicates better keyword integration)
        bullets_with_metrics = sum(1 for bullet in impact_analysis.strong_bullets if bullet.has_metrics)
        if bullets_with_metrics > 0:
            metrics_bonus = (bullets_with_metrics / len(impact_analysis.strong_bullets)) * 10
            base_score += metrics_bonus
        
        return min(100.0, base_score)
    
    def get_score_grade(self, score: float) -> str:
        """Get letter grade for a score."""
        if score >= self.score_thresholds['excellent']:
            return 'A'
        elif score >= self.score_thresholds['good']:
            return 'B'
        elif score >= self.score_thresholds['fair']:
            return 'C'
        elif score >= self.score_thresholds['poor']:
            return 'D'
        else:
            return 'F'
    
    def get_score_description(self, score: float, score_type: str) -> str:
        """Get description for a score."""
        grade = self.get_score_grade(score)
        
        descriptions = {
            'A': {
                'ats': "Excellent ATS compatibility - your resume should pass most ATS filters",
                'recruiter': "Outstanding resume quality - highly likely to impress recruiters"
            },
            'B': {
                'ats': "Good ATS compatibility - minor improvements could optimize further",
                'recruiter': "Strong resume quality - should perform well with recruiters"
            },
            'C': {
                'ats': "Fair ATS compatibility - some improvements needed for better results",
                'recruiter': "Decent resume quality - room for improvement to stand out"
            },
            'D': {
                'ats': "Poor ATS compatibility - significant improvements needed",
                'recruiter': "Below average quality - substantial improvements recommended"
            },
            'F': {
                'ats': "Very poor ATS compatibility - major overhaul required",
                'recruiter': "Poor quality - complete revision recommended"
            }
        }
        
        return descriptions.get(grade, {}).get(score_type, "Score analysis not available")
    
    def get_improvement_priority(self, ats_score: float, recruiter_score: float) -> Dict[str, Any]:
        """Determine improvement priorities based on scores."""
        priorities = {
            'critical_issues': [],
            'high_priority': [],
            'medium_priority': [],
            'low_priority': []
        }
        
        # Critical issues (scores below 40)
        if ats_score < 40:
            priorities['critical_issues'].append("Fix critical ATS compatibility issues")
        
        if recruiter_score < 40:
            priorities['critical_issues'].append("Improve overall resume quality")
        
        # High priority (scores 40-60)
        if 40 <= ats_score < 60:
            priorities['high_priority'].append("Improve keyword coverage and formatting")
        
        if 40 <= recruiter_score < 60:
            priorities['high_priority'].append("Strengthen impact statements and achievements")
        
        # Medium priority (scores 60-80)
        if 60 <= ats_score < 80:
            priorities['medium_priority'].append("Optimize remaining formatting and structure issues")
        
        if 60 <= recruiter_score < 80:
            priorities['medium_priority'].append("Fine-tune content for better recruiter appeal")
        
        # Low priority (scores 80+)
        if ats_score >= 80:
            priorities['low_priority'].append("Minor ATS optimizations for perfection")
        
        if recruiter_score >= 80:
            priorities['low_priority'].append("Polish and refine for maximum impact")
        
        return priorities
