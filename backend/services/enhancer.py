from typing import List, Dict
from anthropic import Anthropic
import os
from app.models import ParsedResume, ParsedJobDescription, ResumePoint

class ResumeEnhancer:
    def __init__(self):
        self.anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    async def enhance_points(
        self,
        parsed_resume: ParsedResume,
        parsed_jd: ParsedJobDescription,
        similar_resumes: List[Dict],
        gaps: Dict
    ) -> List[ResumePoint]:
        """Enhance resume bullet points with relevant keywords"""
        enhanced_points = []
        
        # Focus on project descriptions as requested
        for project in parsed_resume.projects[:5]:  # Limit to top 5 projects
            enhanced = await self._enhance_single_point(
                project['description'],
                parsed_jd,
                similar_resumes,
                gaps
            )
            
            enhanced_points.append(ResumePoint(
                original_point=project['description'],
                enhanced_point=enhanced
            ))
        
        return enhanced_points
    
    async def _enhance_single_point(
        self,
        original_point: str,
        parsed_jd: ParsedJobDescription,
        similar_resumes: List[Dict],
        gaps: Dict
    ) -> str:
        """Enhance a single bullet point using Claude"""
        
        # Gather context from similar resumes
        similar_patterns = self._extract_enhancement_patterns(similar_resumes)
        
        prompt = f"""
        Enhance this resume bullet point by naturally incorporating relevant keywords and skills from the job description.
        
        Original bullet point:
        {original_point}
        
        Job Description Keywords:
        - Required: {', '.join(parsed_jd.required_skills)}
        - Keywords: {', '.join(parsed_jd.keywords[:10])}
        
        Missing skills to potentially incorporate:
        {', '.join(gaps.get('missing_skills', [])[:5])}
        
        Patterns from successful resumes:
        {similar_patterns}
        
        Rules:
        1. Keep the core achievement/work intact
        2. Only add keywords that make logical sense
        3. Don't force keywords that don't fit
        4. Maintain professional tone
        5. Keep it under 2 lines
        6. Use action verbs
        7. Include metrics if possible
        
        Return only the enhanced bullet point, nothing else.
        """
        
        response = self.anthropic.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text.strip()
    
    def _extract_enhancement_patterns(self, similar_resumes: List[Dict]) -> str:
        """Extract useful patterns from similar resumes"""
        patterns = []
        
        for resume_data in similar_resumes[:2]:  # Top 2 similar resumes
            relevant = resume_data.get('relevant_sections', {})
            
            # Extract strong action verbs and structures
            for project in relevant.get('relevant_projects', [])[:3]:
                if len(project) > 20:  # Meaningful bullets only
                    patterns.append(f"- {project}")
        
        return '\n'.join(patterns) if patterns else "No specific patterns found"
    
    async def generate_recommendations(
        self,
        gaps: Dict,
        similar_resumes: List[Dict],
        parsed_jd: ParsedJobDescription
    ) -> List[str]:
        """Generate recommendations based on gap analysis"""
        
        # Compile insights from similar resumes
        common_skills = self._extract_common_skills(similar_resumes)
        missing_critical = set(parsed_jd.required_skills) - set(gaps.get('current_skills', []))
        
        prompt = f"""
        Generate 3-5 specific, actionable recommendations for improving this resume based on:
        
        Critical missing skills from JD:
        {', '.join(missing_critical)}
        
        Skills commonly found in similar successful resumes:
        {', '.join(common_skills[:10])}
        
        JD emphasis areas:
        {', '.join(parsed_jd.keywords[:8])}
        
        Provide recommendations that are:
        1. Specific and actionable
        2. Based on the JD requirements
        3. Informed by patterns in successful resumes
        4. Realistic to implement
        
        Format: Return as a simple list, one recommendation per line.
        Focus on skills, experiences, or projects they could add or highlight.
        """
        
        response = self.anthropic.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Parse response into list
        recommendations = [
            line.strip() 
            for line in response.content[0].text.strip().split('\n')
            if line.strip() and not line.strip().startswith('#')
        ]
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    def _extract_common_skills(self, similar_resumes: List[Dict]) -> List[str]:
        """Extract commonly occurring skills from similar resumes"""
        skill_frequency = {}
        
        for resume_data in similar_resumes:
            skills = resume_data.get('relevant_sections', {}).get('matching_skills', [])
            
            for skill_line in skills:
                # Extract individual skills from lines
                words = skill_line.lower().split()
                for word in words:
                    if len(word) > 2 and word.isalnum():
                        skill_frequency[word] = skill_frequency.get(word, 0) + 1
        
        # Sort by frequency
        common_skills = sorted(
            skill_frequency.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        return [skill[0] for skill in common_skills[:15]]