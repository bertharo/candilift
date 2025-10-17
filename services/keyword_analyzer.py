import re
from typing import List, Dict, Tuple
from collections import Counter
from models.resume_data import ResumeData
from models.job_data import JobData
from models.analysis_result import KeywordAnalysis, KeywordMatch
import spacy
from difflib import SequenceMatcher

class KeywordAnalyzer:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Warning: spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Keyword synonyms mapping
        self.synonyms = {
            'leadership': ['lead', 'led', 'leading', 'manage', 'managed', 'managing', 'direct', 'directed'],
            'management': ['manage', 'managed', 'managing', 'lead', 'led', 'leading', 'oversee', 'oversaw'],
            'development': ['develop', 'developed', 'developing', 'build', 'built', 'building', 'create', 'created'],
            'implementation': ['implement', 'implemented', 'implementing', 'deploy', 'deployed', 'deploying'],
            'analysis': ['analyze', 'analyzed', 'analyzing', 'assess', 'assessed', 'assessing', 'evaluate', 'evaluated'],
            'strategy': ['strategic', 'strategically', 'strategize', 'strategized', 'plan', 'planned', 'planning'],
            'improvement': ['improve', 'improved', 'improving', 'enhance', 'enhanced', 'enhancing', 'optimize', 'optimized'],
            'collaboration': ['collaborate', 'collaborated', 'collaborating', 'work with', 'worked with', 'partner', 'partnered'],
            'communication': ['communicate', 'communicated', 'communicating', 'present', 'presented', 'presenting'],
            'project': ['initiative', 'program', 'campaign', 'effort', 'undertaking'],
            'team': ['group', 'staff', 'personnel', 'crew', 'squad'],
            'business': ['company', 'organization', 'enterprise', 'firm', 'corporation'],
            'data': ['information', 'metrics', 'analytics', 'insights', 'statistics'],
            'technology': ['tech', 'system', 'platform', 'software', 'application'],
            'customer': ['client', 'user', 'consumer', 'buyer', 'stakeholder'],
            'revenue': ['sales', 'income', 'earnings', 'profit', 'growth'],
            'cost': ['expense', 'budget', 'spending', 'investment', 'savings'],
            'performance': ['efficiency', 'effectiveness', 'productivity', 'output', 'results'],
            'quality': ['excellence', 'standard', 'benchmark', 'best practice', 'optimization']
        }
        
        # Action verb strength mapping
        self.action_verb_strength = {
            'achieved': 10, 'accomplished': 10, 'delivered': 10, 'exceeded': 10, 'surpassed': 10,
            'led': 9, 'managed': 9, 'directed': 9, 'oversaw': 9, 'spearheaded': 9,
            'developed': 8, 'created': 8, 'built': 8, 'designed': 8, 'implemented': 8,
            'increased': 7, 'improved': 7, 'enhanced': 7, 'optimized': 7, 'streamlined': 7,
            'analyzed': 6, 'evaluated': 6, 'assessed': 6, 'researched': 6, 'investigated': 6,
            'collaborated': 5, 'coordinated': 5, 'facilitated': 5, 'supported': 5, 'assisted': 5,
            'helped': 3, 'worked on': 3, 'participated': 3, 'involved in': 2, 'responsible for': 2
        }
    
    def analyze(self, resume_data: ResumeData, job_data: JobData) -> KeywordAnalysis:
        """Analyze keyword gaps between resume and job description."""
        # Get all keywords from job description
        job_keywords = self._extract_job_keywords(job_data)
        
        # Get all text from resume
        resume_text = resume_data.get_all_text()
        
        # Analyze keyword matches
        missing_keywords, weak_keywords, strong_keywords = self._analyze_keyword_matches(
            job_keywords, resume_text, resume_data
        )
        
        # Calculate coverage score
        coverage_score = self._calculate_coverage_score(job_keywords, strong_keywords, weak_keywords)
        
        # Calculate keyword density
        keyword_density = self._calculate_keyword_density(job_keywords, resume_text)
        
        return KeywordAnalysis(
            coverage_score=coverage_score,
            missing_keywords=missing_keywords,
            weak_keywords=weak_keywords,
            strong_keywords=strong_keywords,
            keyword_density=keyword_density
        )
    
    def _extract_job_keywords(self, job_data: JobData) -> Dict[str, float]:
        """Extract and weight keywords from job description."""
        keywords = {}
        
        # Add required skills with high weight
        for skill in job_data.required_skills:
            keywords[skill.name.lower()] = skill.importance * 1.5
        
        # Add preferred skills with medium weight
        for skill in job_data.preferred_skills:
            keywords[skill.name.lower()] = skill.importance
        
        # Add key phrases with medium weight
        for phrase in job_data.key_phrases:
            keywords[phrase.lower()] = 6.0
        
        # Add title words with high weight
        title_words = job_data.title.lower().split()
        for word in title_words:
            if len(word) > 2:  # Skip short words
                keywords[word] = 8.0
        
        # Add words from responsibilities and qualifications
        for responsibility in job_data.responsibilities:
            words = self._extract_important_words(responsibility)
            for word in words:
                keywords[word] = keywords.get(word, 0) + 2.0
        
        for qualification in job_data.qualifications:
            words = self._extract_important_words(qualification)
            for word in words:
                keywords[word] = keywords.get(word, 0) + 3.0
        
        return keywords
    
    def _extract_important_words(self, text: str) -> List[str]:
        """Extract important words from text using NLP."""
        if not self.nlp:
            # Fallback: simple word extraction
            words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
            return [word for word in words if word not in {'the', 'and', 'for', 'with', 'this', 'that', 'from', 'into'}]
        
        doc = self.nlp(text)
        important_words = []
        
        for token in doc:
            # Include nouns, adjectives, and verbs
            if (token.pos_ in ['NOUN', 'ADJ', 'VERB'] and 
                not token.is_stop and 
                not token.is_punct and 
                len(token.text) > 2 and
                not token.is_space):
                important_words.append(token.lemma_.lower())
        
        return important_words
    
    def _analyze_keyword_matches(self, job_keywords: Dict[str, float], 
                                resume_text: str, resume_data: ResumeData) -> Tuple[List[str], List[KeywordMatch], List[KeywordMatch]]:
        """Analyze how well resume matches job keywords."""
        missing_keywords = []
        weak_keywords = []
        strong_keywords = []
        
        resume_lower = resume_text.lower()
        
        for keyword, importance in job_keywords.items():
            # Check for exact matches
            if keyword in resume_lower:
                location = self._find_keyword_location(keyword, resume_data)
                strength = self._calculate_keyword_strength(keyword, resume_lower)
                
                match = KeywordMatch(
                    keyword=keyword,
                    match_type="exact",
                    frequency_in_jd=1,  # Simplified
                    location_in_resume=location,
                    importance_score=importance
                )
                
                if strength >= 7:
                    strong_keywords.append(match)
                else:
                    weak_keywords.append(match)
            
            # Check for synonym matches
            elif keyword in self.synonyms:
                synonym_matches = self._find_synonym_matches(keyword, resume_lower)
                if synonym_matches:
                    location = self._find_keyword_location(synonym_matches[0], resume_data)
                    
                    match = KeywordMatch(
                        keyword=keyword,
                        match_type="synonym",
                        frequency_in_jd=1,
                        location_in_resume=location,
                        importance_score=importance * 0.8  # Slight penalty for synonyms
                    )
                    
                    strong_keywords.append(match)
                else:
                    missing_keywords.append(keyword)
            
            # Check for partial matches
            else:
                partial_match = self._find_partial_match(keyword, resume_lower)
                if partial_match:
                    location = self._find_keyword_location(partial_match, resume_data)
                    
                    match = KeywordMatch(
                        keyword=keyword,
                        match_type="partial",
                        frequency_in_jd=1,
                        location_in_resume=location,
                        importance_score=importance * 0.6  # Penalty for partial matches
                    )
                    
                    weak_keywords.append(match)
                else:
                    missing_keywords.append(keyword)
        
        return missing_keywords, weak_keywords, strong_keywords
    
    def _find_synonym_matches(self, keyword: str, resume_text: str) -> List[str]:
        """Find synonym matches for a keyword."""
        if keyword not in self.synonyms:
            return []
        
        matches = []
        for synonym in self.synonyms[keyword]:
            if synonym in resume_text:
                matches.append(synonym)
        
        return matches
    
    def _find_partial_match(self, keyword: str, resume_text: str) -> str:
        """Find partial matches for a keyword."""
        words = resume_text.split()
        
        for word in words:
            if len(word) > 3 and len(keyword) > 3:
                similarity = SequenceMatcher(None, keyword, word).ratio()
                if similarity > 0.8:
                    return word
        
        return None
    
    def _find_keyword_location(self, keyword: str, resume_data: ResumeData) -> str:
        """Determine where in the resume a keyword appears."""
        keyword_lower = keyword.lower()
        
        # Check title/name
        if resume_data.contact_info.name and keyword_lower in resume_data.contact_info.name.lower():
            return "title"
        
        # Check summary
        if resume_data.summary and keyword_lower in resume_data.summary.lower():
            return "summary"
        
        # Check experience
        for exp in resume_data.experience:
            if (keyword_lower in exp.title.lower() or 
                keyword_lower in exp.company.lower() or
                any(keyword_lower in desc.lower() for desc in exp.description)):
                return "experience"
        
        # Check skills
        if any(keyword_lower in skill.lower() for skill in resume_data.skills):
            return "skills"
        
        # Check education
        for edu in resume_data.education:
            if (keyword_lower in edu.degree.lower() or 
                keyword_lower in edu.institution.lower()):
                return "education"
        
        return "none"
    
    def _calculate_keyword_strength(self, keyword: str, resume_text: str) -> float:
        """Calculate the strength of a keyword match based on context."""
        # Count occurrences
        count = resume_text.count(keyword)
        
        # Find surrounding context
        strength = 5.0  # Base strength
        
        # Increase strength based on frequency
        if count > 3:
            strength += 2.0
        elif count > 1:
            strength += 1.0
        
        # Check for action verbs near the keyword
        words = resume_text.split()
        for i, word in enumerate(words):
            if keyword in word:
                # Check surrounding words for action verbs
                start = max(0, i - 3)
                end = min(len(words), i + 3)
                context = ' '.join(words[start:end])
                
                for action_verb, verb_strength in self.action_verb_strength.items():
                    if action_verb in context:
                        strength += verb_strength * 0.1
                        break
        
        return min(10.0, strength)
    
    def _calculate_coverage_score(self, job_keywords: Dict[str, float], 
                                strong_keywords: List[KeywordMatch], 
                                weak_keywords: List[KeywordMatch]) -> float:
        """Calculate overall keyword coverage score (0-100)."""
        if not job_keywords:
            return 100.0
        
        total_weight = sum(job_keywords.values())
        
        strong_weight = sum(match.importance_score for match in strong_keywords)
        weak_weight = sum(match.importance_score * 0.5 for match in weak_keywords)  # 50% weight for weak matches
        
        covered_weight = strong_weight + weak_weight
        
        coverage_percentage = (covered_weight / total_weight) * 100
        return min(100.0, coverage_percentage)
    
    def _calculate_keyword_density(self, job_keywords: Dict[str, float], resume_text: str) -> Dict[str, float]:
        """Calculate keyword density for important keywords."""
        word_count = len(resume_text.split())
        if word_count == 0:
            return {}
        
        density = {}
        for keyword in job_keywords.keys():
            count = resume_text.count(keyword)
            density[keyword] = (count / word_count) * 100
        
        return density
