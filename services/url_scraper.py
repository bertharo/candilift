import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any
import re
from urllib.parse import urlparse
import time

class JobPostingScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Common job posting selectors for different platforms
        self.job_selectors = {
            'linkedin': [
                '.description__text',
                '.show-more-less-html__markup',
                '.jobs-description-content__text',
                '.jobs-box__html-content'
            ],
            'indeed': [
                '.jobsearch-jobDescriptionText',
                '#jobDescriptionText',
                '.jobsearch-jobDescriptionText'
            ],
            'glassdoor': [
                '.jobDescriptionContent',
                '.jobDescriptionContent .desc',
                '.jobDescriptionContent .jobDescription'
            ],
            'ziprecruiter': [
                '.jobDescriptionSection',
                '.jobDescriptionSection .jobDescription'
            ],
            'monster': [
                '.job-description',
                '.job-description .description'
            ],
            'generic': [
                '[class*="description"]',
                '[class*="job-description"]',
                '[class*="content"]',
                '[class*="details"]',
                'main',
                '.content',
                '.main-content'
            ]
        }
        
        # Title selectors
        self.title_selectors = [
            'h1',
            '.job-title',
            '[class*="title"]',
            '[class*="job-title"]',
            '.jobsearch-JobInfoHeader-title',
            '.jobs-unified-top-card__job-title'
        ]
        
        # Company selectors
        self.company_selectors = [
            '[class*="company"]',
            '[class*="employer"]',
            '.company-name',
            '.employer-name',
            '.jobs-unified-top-card__company-name'
        ]
    
    def scrape_job_posting(self, url: str) -> Dict[str, Any]:
        """
        Scrape job posting from URL and extract job description.
        
        Args:
            url: Job posting URL
            
        Returns:
            Dictionary containing job title, company, and description
        """
        try:
            # Validate URL
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                raise ValueError("Invalid URL format")
            
            # Add protocol if missing
            if not parsed_url.scheme:
                url = f"https://{url}"
            
            # Make request
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract job information
            job_info = {
                'url': url,
                'title': self._extract_title(soup),
                'company': self._extract_company(soup),
                'description': self._extract_description(soup, url),
                'platform': self._identify_platform(url)
            }
            
            return job_info
            
        except requests.RequestException as e:
            raise ValueError(f"Failed to fetch URL: {str(e)}")
        except Exception as e:
            raise ValueError(f"Failed to parse job posting: {str(e)}")
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract job title from HTML."""
        for selector in self.title_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text(strip=True)
                if text and len(text) > 3 and len(text) < 200:
                    return text
        
        # Fallback: look for h1 tags
        h1 = soup.find('h1')
        if h1:
            return h1.get_text(strip=True)
        
        return "Unknown Position"
    
    def _extract_company(self, soup: BeautifulSoup) -> str:
        """Extract company name from HTML."""
        for selector in self.company_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text(strip=True)
                if text and len(text) > 1 and len(text) < 100:
                    return text
        
        return "Unknown Company"
    
    def _extract_description(self, soup: BeautifulSoup, url: str) -> str:
        """Extract job description from HTML."""
        platform = self._identify_platform(url)
        
        # Try platform-specific selectors first
        if platform in self.job_selectors:
            for selector in self.job_selectors[platform]:
                description = self._extract_with_selector(soup, selector)
                if description:
                    return description
        
        # Try generic selectors
        for selector in self.job_selectors['generic']:
            description = self._extract_with_selector(soup, selector)
            if description:
                return description
        
        # Fallback: extract from main content
        main = soup.find('main')
        if main:
            return self._clean_text(main.get_text())
        
        # Last resort: extract from body
        body = soup.find('body')
        if body:
            return self._clean_text(body.get_text())
        
        return "Job description not found"
    
    def _extract_with_selector(self, soup: BeautifulSoup, selector: str) -> Optional[str]:
        """Extract text using CSS selector."""
        try:
            elements = soup.select(selector)
            for element in elements:
                text = self._clean_text(element.get_text())
                if self._is_valid_job_description(text):
                    return text
        except Exception:
            pass
        return None
    
    def _is_valid_job_description(self, text: str) -> bool:
        """Check if text looks like a valid job description."""
        if not text or len(text) < 100:
            return False
        
        # Check for job-related keywords
        job_keywords = [
            'responsibilities', 'requirements', 'qualifications', 'experience',
            'skills', 'education', 'benefits', 'salary', 'location', 'remote',
            'full-time', 'part-time', 'contract', 'permanent', 'position',
            'role', 'candidate', 'applicant', 'apply', 'job', 'career'
        ]
        
        text_lower = text.lower()
        keyword_count = sum(1 for keyword in job_keywords if keyword in text_lower)
        
        return keyword_count >= 3
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text."""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common unwanted elements
        unwanted_patterns = [
            r'Cookie Policy.*?Accept',
            r'Privacy Policy.*?Accept',
            r'Terms of Service.*?Accept',
            r'Subscribe to.*?newsletter',
            r'Follow us on.*?social',
            r'©.*?All rights reserved',
            r'Loading\.\.\.',
            r'Please enable JavaScript',
            r'This site uses cookies'
        ]
        
        for pattern in unwanted_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.DOTALL)
        
        return text.strip()
    
    def _identify_platform(self, url: str) -> str:
        """Identify the job platform from URL."""
        url_lower = url.lower()
        
        if 'linkedin.com' in url_lower:
            return 'linkedin'
        elif 'indeed.com' in url_lower:
            return 'indeed'
        elif 'glassdoor.com' in url_lower:
            return 'glassdoor'
        elif 'ziprecruiter.com' in url_lower:
            return 'ziprecruiter'
        elif 'monster.com' in url_lower:
            return 'monster'
        else:
            return 'generic'
    
    def extract_job_description_text(self, url: str) -> str:
        """
        Extract just the job description text from a URL.
        
        Args:
            url: Job posting URL
            
        Returns:
            Clean job description text
        """
        job_info = self.scrape_job_posting(url)
        return job_info['description']
