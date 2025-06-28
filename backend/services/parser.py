import re
from typing import List, Dict
from app.models import ParsedResume, ParsedJobDescription

class ResumeParser:
    def __init__(self):
        self.section_patterns = {
            'projects': r'(?i)(projects?|portfolio)',
            'experience': r'(?i)(experience|work history|employment)',
            'skills': r'(?i)(skills?|technical skills|technologies)',
            'education': r'(?i)(education|academic)'
        }
    
    def parse(self, resume_text: str) -> ParsedResume:
        """Parse resume text into structured format"""
        sections = self._extract_sections(resume_text)
        
        return ParsedResume(
            projects=self._parse_projects(sections.get('projects', '')),
            skills=self._parse_skills(sections.get('skills', '')),
            experience=self._parse_experience(sections.get('experience', '')),
            education=self._parse_education(sections.get('education', ''))
        )
    
    def _extract_sections(self, text: str) -> Dict[str, str]:
        """Extract major sections from resume"""
        sections = {}
        lines = text.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            # Check if line is a section header
            for section, pattern in self.section_patterns.items():
                if re.search(pattern, line):
                    if current_section:
                        sections[current_section] = '\n'.join(current_content)
                    current_section = section
                    current_content = []
                    break
            else:
                if current_section:
                    current_content.append(line)
        
        # Add last section
        if current_section:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    def _parse_projects(self, text: str) -> List[Dict[str, str]]:
        """Extract project descriptions as bullet points"""
        projects = []
        
        # Split by bullet points or numbered lists
        bullets = re.findall(r'[•\-\*]\s*(.+)', text)
        
        for bullet in bullets:
            projects.append({
                'description': bullet.strip(),
                'type': 'project_point'
            })
        
        return projects
    
    def _parse_skills(self, text: str) -> List[str]:
        """Extract skills from skills section"""
        # Common patterns: comma-separated, bullet points, categories
        skills = []
        
        # Remove common words
        text = re.sub(r'(?i)(languages?|frameworks?|tools?|technologies):', '', text)
        
        # Extract comma-separated values
        if ',' in text:
            skills.extend([s.strip() for s in text.split(',') if s.strip()])
        else:
            # Extract from bullet points
            skills.extend(re.findall(r'[•\-\*]\s*(.+)', text))
        
        return [s.strip() for s in skills if len(s.strip()) > 1]
    
    def _parse_experience(self, text: str) -> List[Dict[str, str]]:
        """Parse work experience section"""
        experiences = []
        # Similar to projects - extract bullet points
        bullets = re.findall(r'[•\-\*]\s*(.+)', text)
        
        for bullet in bullets:
            experiences.append({
                'description': bullet.strip(),
                'type': 'experience_point'
            })
        
        return experiences
    
    def _parse_education(self, text: str) -> List[Dict[str, str]]:
        """Parse education section"""
        # Basic implementation - can be enhanced
        return [{'description': text.strip()}] if text.strip() else []


class JobDescriptionParser:
    def __init__(self):
        self.tech_keywords = self._load_tech_keywords()
    
    def _load_tech_keywords(self) -> set:
        """Load common tech keywords"""
        return {
            # Languages
            'python', 'java', 'javascript', 'typescript', 'go', 'rust', 'c++',
            'ruby', 'scala', 'kotlin', 'swift', 'r', 'sql',
            
            # Frameworks
            'react', 'angular', 'vue', 'django', 'flask', 'spring', 'express',
            'fastapi', 'rails', 'laravel', 'nextjs', 'nodejs',
            
            # Tools & Platforms
            'aws', 'gcp', 'azure', 'docker', 'kubernetes', 'jenkins', 'git',
            'terraform', 'ansible', 'ci/cd', 'microservices', 'rest', 'graphql',
            
            # Databases
            'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch',
            'cassandra', 'dynamodb', 'firebase',
            
            # Concepts
            'agile', 'scrum', 'devops', 'tdd', 'clean code', 'solid',
            'design patterns', 'distributed systems', 'scalability'
        }
    
    def parse(self, job_description: str) -> ParsedJobDescription:
        """Parse job description to extract key information"""
        jd_lower = job_description.lower()
        
        return ParsedJobDescription(
            required_skills=self._extract_required_skills(job_description),
            preferred_skills=self._extract_preferred_skills(job_description),
            responsibilities=self._extract_responsibilities(job_description),
            keywords=self._extract_keywords(jd_lower)
        )
    
    def _extract_required_skills(self, text: str) -> List[str]:
        """Extract required skills from JD"""
        skills = []
        
        # Look for patterns like "Required:", "Must have:", etc.
        patterns = [
            r'(?i)required:?\s*([^\.]+)',
            r'(?i)must have:?\s*([^\.]+)',
            r'(?i)requirements:?\s*([^\.]+)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                # Extract individual skills
                skills.extend(self._extract_skills_from_text(match))
        
        return list(set(skills))
    
    def _extract_preferred_skills(self, text: str) -> List[str]:
        """Extract nice-to-have skills"""
        skills = []
        
        patterns = [
            r'(?i)preferred:?\s*([^\.]+)',
            r'(?i)nice to have:?\s*([^\.]+)',
            r'(?i)bonus:?\s*([^\.]+)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                skills.extend(self._extract_skills_from_text(match))
        
        return list(set(skills))
    
    def _extract_skills_from_text(self, text: str) -> List[str]:
        """Extract individual skills from a text block"""
        skills = []
        text_lower = text.lower()
        
        # Check for known tech keywords
        for keyword in self.tech_keywords:
            if keyword in text_lower:
                skills.append(keyword)
        
        return skills
    
    def _extract_responsibilities(self, text: str) -> List[str]:
        """Extract job responsibilities"""
        resp = []
        
        # Look for bullet points or numbered lists
        bullets = re.findall(r'[•\-\*]\s*(.+)', text)
        resp.extend(bullets)
        
        # Look for numbered items
        numbered = re.findall(r'\d+\.\s*(.+)', text)
        resp.extend(numbered)
        
        return [r.strip() for r in resp if r.strip()]
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract all technical keywords from JD"""
        keywords = []
        
        for keyword in self.tech_keywords:
            if keyword in text:
                keywords.append(keyword)
        
        # Extract years of experience
        exp_matches = re.findall(r'(\d+)\+?\s*years?', text)
        for match in exp_matches:
            keywords.append(f"{match}+ years")
        
        return keywords