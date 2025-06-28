from typing import List, Dict, Set
from app.models import ParsedResume, ParsedJobDescription

class GapAnalyzer:
    def analyze(
        self,
        parsed_resume: ParsedResume,
        parsed_jd: ParsedJobDescription,
        similar_resumes: List[Dict]
    ) -> Dict:
        """Analyze gaps between resume and job description"""
        
        current_skills = set(skill.lower() for skill in parsed_resume.skills)
        required_skills = set(skill.lower() for skill in parsed_jd.required_skills)
        preferred_skills = set(skill.lower() for skill in parsed_jd.preferred_skills)
        
        # Skills from similar successful resumes
        common_skills = self._extract_common_skills_from_similar(similar_resumes)
        
        gaps = {
            'missing_skills': list(required_skills - current_skills),
            'missing_preferred': list(preferred_skills - current_skills),
            'missing_from_similar': list(common_skills - current_skills),
            'current_skills': list(current_skills),
            'match_percentage': self._calculate_match_percentage(
                current_skills, 
                required_skills, 
                preferred_skills
            ),
            'keyword_coverage': self._calculate_keyword_coverage(
                parsed_resume,
                parsed_jd.keywords
            )
        }
        
        return gaps
    
    def _extract_common_skills_from_similar(
        self, 
        similar_resumes: List[Dict]
    ) -> Set[str]:
        """Extract skills that appear in multiple similar resumes"""
        skill_counts = {}
        
        for resume_data in similar_resumes:
            sections = resume_data.get('relevant_sections', {})
            skills = sections.get('matching_skills', [])
            
            for skill_line in skills:
                # Simple skill extraction - can be improved
                words = skill_line.lower().split()
                for word in words:
                    if len(word) > 3:
                        skill_counts[word] = skill_counts.get(word, 0) + 1
        
        # Return skills that appear in at least 2 resumes
        return {
            skill for skill, count in skill_counts.items() 
            if count >= 2
        }
    
    def _calculate_match_percentage(
        self,
        current_skills: Set[str],
        required_skills: Set[str],
        preferred_skills: Set[str]
    ) -> float:
        """Calculate overall match percentage"""
        if not required_skills:
            return 100.0
        
        required_match = len(current_skills & required_skills) / len(required_skills)
        preferred_match = len(current_skills & preferred_skills) / len(preferred_skills) if preferred_skills else 0
        
        # Weight: 70% required, 30% preferred
        return round((required_match * 0.7 + preferred_match * 0.3) * 100, 1)
    
    def _calculate_keyword_coverage(
        self,
        parsed_resume: ParsedResume,
        jd_keywords: List[str]
    ) -> Dict[str, int]:
        """Calculate how many JD keywords appear in resume"""
        resume_text = self._get_resume_text(parsed_resume).lower()
        
        coverage = {
            'total_keywords': len(jd_keywords),
            'found_keywords': 0,
            'missing_keywords': []
        }
        
        for keyword in jd_keywords:
            if keyword.lower() in resume_text:
                coverage['found_keywords'] += 1
            else:
                coverage['missing_keywords'].append(keyword)
        
        coverage['coverage_percentage'] = round(
            (coverage['found_keywords'] / coverage['total_keywords']) * 100
            if coverage['total_keywords'] > 0 else 0
        )
        
        return coverage
    
    def _get_resume_text(self, parsed_resume: ParsedResume) -> str:
        """Combine all resume sections into single text"""
        texts = []
        
        # Add skills
        texts.extend(parsed_resume.skills)
        
        # Add projects
        texts.extend([p['description'] for p in parsed_resume.projects])
        
        # Add experience
        texts.extend([e['description'] for e in parsed_resume.experience])
        
        return ' '.join(texts)