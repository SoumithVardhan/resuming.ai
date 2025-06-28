from pydantic import BaseModel
from typing import List, Dict, Optional

class ResumePoint(BaseModel):
    original_point: str
    enhanced_point: str

class EnhancementRequest(BaseModel):
    resume_text: str
    job_description: str

class EnhancementResponse(BaseModel):
    enhanced_resume_points: List[ResumePoint]
    recommendations: List[str]

class ParsedResume(BaseModel):
    projects: List[Dict[str, str]]
    skills: List[str]
    experience: List[Dict[str, str]]
    education: Optional[List[Dict[str, str]]] = []

class ParsedJobDescription(BaseModel):
    required_skills: List[str]
    preferred_skills: List[str]
    responsibilities: List[str]
    keywords: List[str]