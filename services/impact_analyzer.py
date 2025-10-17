import re
from typing import List, Dict, Tuple
from models.resume_data import ResumeData
from models.analysis_result import ImpactAnalysis, ImpactBullet

class ImpactAnalyzer:
    def __init__(self):
        # Simple verb detection without spaCy
        self.nlp = None
        
        # Strong action verbs that indicate impact
        self.strong_action_verbs = {
            'achieved', 'accomplished', 'delivered', 'exceeded', 'surpassed', 'outperformed',
            'increased', 'improved', 'enhanced', 'optimized', 'streamlined', 'accelerated',
            'reduced', 'decreased', 'minimized', 'eliminated', 'saved', 'cut',
            'grew', 'expanded', 'scaled', 'launched', 'initiated', 'established',
            'led', 'managed', 'directed', 'oversaw', 'spearheaded', 'championed',
            'developed', 'created', 'built', 'designed', 'implemented', 'executed',
            'analyzed', 'evaluated', 'assessed', 'researched', 'identified', 'discovered'
        }
        
        # Weak action verbs that lack impact
        self.weak_action_verbs = {
            'helped', 'assisted', 'supported', 'worked on', 'participated', 'involved',
            'responsible for', 'in charge of', 'tasked with', 'assigned to',
            'helped with', 'contributed to', 'part of', 'member of'
        }
        
        # Generic phrases that lack specificity
        self.generic_phrases = {
            'responsible for', 'involved in', 'participated in', 'worked on',
            'helped with', 'assisted with', 'contributed to', 'part of',
            'member of', 'tasked with', 'assigned to', 'in charge of',
            'duties included', 'responsibilities included', 'worked with'
        }
        
        # Metric patterns
        self.metric_patterns = [
            r'\d+%',  # Percentage
            r'\$\d+(?:,\d{3})*(?:\.\d{2})?[kKmMbB]?',  # Currency
            r'\d+(?:,\d{3})*(?:\.\d+)?',  # Numbers with commas
            r'\d+(?:\.\d+)?[x×]',  # Multipliers
            r'(?:first|second|third|top|bottom)\s+\d+',  # Rankings
            r'\d+\s*(?:people|employees|users|customers|clients)',  # Counts
            r'(?:increased|decreased|improved|reduced)\s+by\s+\d+%',  # Change percentages
        ]
        
        # Impact indicators
        self.impact_indicators = {
            'revenue', 'profit', 'sales', 'growth', 'efficiency', 'productivity',
            'cost', 'savings', 'time', 'quality', 'satisfaction', 'engagement',
            'retention', 'acquisition', 'conversion', 'performance', 'results',
            'outcome', 'impact', 'success', 'achievement', 'milestone'
        }
    
    def analyze(self, resume_data: ResumeData) -> ImpactAnalysis:
        """Analyze impact statements in resume."""
        # Extract all bullet points from experience
        all_bullets = self._extract_bullet_points(resume_data)
        
        # Analyze each bullet point
        strong_bullets = []
        weak_bullets = []
        generic_phrases_found = []
        
        for bullet_text in all_bullets:
            bullet_analysis = self._analyze_bullet_point(bullet_text)
            
            if bullet_analysis['strength_score'] >= 6:
                strong_bullets.append(ImpactBullet(
                    text=bullet_text,
                    has_metrics=bullet_analysis['has_metrics'],
                    has_action_verb=bullet_analysis['has_action_verb'],
                    strength_score=bullet_analysis['strength_score'],
                    suggestion=bullet_analysis['suggestion']
                ))
            else:
                weak_bullets.append(ImpactBullet(
                    text=bullet_text,
                    has_metrics=bullet_analysis['has_metrics'],
                    has_action_verb=bullet_analysis['has_action_verb'],
                    strength_score=bullet_analysis['strength_score'],
                    suggestion=bullet_analysis['suggestion']
                ))
            
            # Collect generic phrases
            generic_phrases_found.extend(bullet_analysis['generic_phrases'])
        
        # Calculate overall impact score
        impact_score = self._calculate_impact_score(strong_bullets, weak_bullets)
        
        # Generate improvement suggestions
        improvement_suggestions = self._generate_improvement_suggestions(strong_bullets, weak_bullets)
        
        return ImpactAnalysis(
            impact_score=impact_score,
            strong_bullets=strong_bullets,
            weak_bullets=weak_bullets,
            generic_phrases_found=list(set(generic_phrases_found)),
            improvement_suggestions=improvement_suggestions
        )
    
    def _extract_bullet_points(self, resume_data: ResumeData) -> List[str]:
        """Extract all bullet points from resume."""
        bullets = []
        
        # Extract from experience descriptions
        for exp in resume_data.experience:
            bullets.extend(exp.description)
        
        # Extract from other sections that might have bullets
        for section_content in resume_data.sections.values():
            # Look for bullet points in section content
            lines = section_content.split('\n')
            for line in lines:
                line = line.strip()
                if line and (line.startswith(('•', '-', '*', '◦')) or re.match(r'^\d+\.', line)):
                    # Remove bullet point markers
                    clean_line = re.sub(r'^[•\-*\d\.\s]+', '', line).strip()
                    if clean_line:
                        bullets.append(clean_line)
        
        return bullets
    
    def _analyze_bullet_point(self, bullet_text: str) -> Dict:
        """Analyze a single bullet point for impact."""
        bullet_lower = bullet_text.lower()
        
        # Check for action verbs
        has_action_verb = False
        has_strong_verb = False
        action_verb_strength = 0
        
        if self.nlp:
            doc = self.nlp(bullet_text)
            for token in doc:
                if token.pos_ == 'VERB' and token.lemma_.lower() in self.strong_action_verbs:
                    has_action_verb = True
                    has_strong_verb = True
                    action_verb_strength = 8
                    break
                elif token.pos_ == 'VERB' and token.lemma_.lower() in self.weak_action_verbs:
                    has_action_verb = True
                    action_verb_strength = 3
                    break
        else:
            # Fallback without spaCy
            words = bullet_lower.split()
            for word in words:
                if word in self.strong_action_verbs:
                    has_action_verb = True
                    has_strong_verb = True
                    action_verb_strength = 8
                    break
                elif word in self.weak_action_verbs:
                    has_action_verb = True
                    action_verb_strength = 3
                    break
        
        # Check for metrics
        has_metrics = any(re.search(pattern, bullet_text) for pattern in self.metric_patterns)
        
        # Check for impact indicators
        has_impact_indicators = any(indicator in bullet_lower for indicator in self.impact_indicators)
        
        # Check for generic phrases
        generic_phrases = [phrase for phrase in self.generic_phrases if phrase in bullet_lower]
        
        # Calculate strength score
        strength_score = 0
        
        if has_strong_verb:
            strength_score += 4
        elif has_action_verb:
            strength_score += 2
        
        if has_metrics:
            strength_score += 3
        
        if has_impact_indicators:
            strength_score += 2
        
        if generic_phrases:
            strength_score -= 2
        
        # Generate suggestion
        suggestion = self._generate_bullet_suggestion(bullet_text, has_metrics, has_strong_verb, generic_phrases)
        
        return {
            'has_metrics': has_metrics,
            'has_action_verb': has_action_verb,
            'strength_score': max(0, min(10, strength_score)),
            'generic_phrases': generic_phrases,
            'suggestion': suggestion
        }
    
    def _generate_bullet_suggestion(self, bullet_text: str, has_metrics: bool, has_strong_verb: bool, generic_phrases: List[str]) -> str:
        """Generate improvement suggestion for a bullet point."""
        suggestions = []
        
        if not has_strong_verb:
            suggestions.append("Start with a strong action verb (e.g., 'Led', 'Achieved', 'Increased')")
        
        if not has_metrics:
            suggestions.append("Add quantifiable results or metrics")
        
        if generic_phrases:
            suggestions.append(f"Replace generic phrases like '{generic_phrases[0]}' with specific actions")
        
        if not suggestions:
            return "This bullet point is well-structured with strong impact indicators."
        
        return " | ".join(suggestions)
    
    def _calculate_impact_score(self, strong_bullets: List[ImpactBullet], weak_bullets: List[ImpactBullet]) -> float:
        """Calculate overall impact score."""
        total_bullets = len(strong_bullets) + len(weak_bullets)
        if total_bullets == 0:
            return 0.0
        
        # Weight strong bullets more heavily
        strong_weight = len(strong_bullets) * 1.5
        weak_weight = len(weak_bullets) * 0.5
        
        total_weight = strong_weight + weak_weight
        
        if total_weight == 0:
            return 0.0
        
        # Calculate percentage of strong content
        strong_percentage = (strong_weight / total_weight) * 100
        
        # Base score on percentage of strong bullets
        impact_score = min(100.0, strong_percentage * 1.2)  # Boost for having strong content
        
        # Additional scoring based on bullet quality
        if strong_bullets:
            avg_strength = sum(bullet.strength_score for bullet in strong_bullets) / len(strong_bullets)
            impact_score += (avg_strength - 6) * 2  # Bonus for high-quality strong bullets
        
        return min(100.0, max(0.0, impact_score))
    
    def _generate_improvement_suggestions(self, strong_bullets: List[ImpactBullet], weak_bullets: List[ImpactBullet]) -> List[str]:
        """Generate overall improvement suggestions."""
        suggestions = []
        
        if len(weak_bullets) > len(strong_bullets):
            suggestions.append("Focus on adding more impact-driven bullet points with quantifiable results")
        
        weak_bullets_without_metrics = [b for b in weak_bullets if not b.has_metrics]
        if weak_bullets_without_metrics:
            suggestions.append("Add specific metrics and numbers to demonstrate your impact")
        
        weak_bullets_without_verbs = [b for b in weak_bullets if not b.has_action_verb]
        if weak_bullets_without_verbs:
            suggestions.append("Start bullet points with strong action verbs to show leadership and initiative")
        
        if not suggestions:
            suggestions.append("Your bullet points effectively demonstrate impact and achievements")
        
        # Add specific suggestions based on common patterns
        suggestions.extend([
            "Use the STAR method (Situation, Task, Action, Result) to structure your accomplishments",
            "Include specific numbers, percentages, and dollar amounts when possible",
            "Focus on outcomes and results rather than just responsibilities",
            "Use power verbs like 'Led', 'Achieved', 'Increased', 'Improved', 'Delivered'"
        ])
        
        return suggestions[:5]  # Limit to top 5 suggestions
