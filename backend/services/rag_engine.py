import numpy as np
from typing import List, Dict
import faiss
import pickle
from anthropic import Anthropic
import os
from app.models import ParsedResume, ParsedJobDescription

class RAGEngine:
    def __init__(self):
        self.anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.index = None
        self.reference_resumes = []
        self.embeddings_cache = {}
    
    async def initialize(self):
        """Initialize FAISS index with reference resumes"""
        # Load reference resumes
        self.reference_resumes = self._load_reference_resumes()
        
        # Generate embeddings for reference resumes
        embeddings = []
        for resume in self.reference_resumes:
            embedding = await self._generate_embedding(resume['text'])
            embeddings.append(embedding)
            self.embeddings_cache[resume['id']] = embedding
        
        # Create FAISS index
        dimension = len(embeddings[0])
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings).astype('float32'))
    
    def _load_reference_resumes(self) -> List[Dict]:
        """Load 10 high-quality technical resumes"""
        resumes = []
        resume_dir = "app/data/reference_resumes"
        
        for i, filename in enumerate(os.listdir(resume_dir)[:10]):
            with open(os.path.join(resume_dir, filename), 'r') as f:
                resumes.append({
                    'id': f'resume_{i}',
                    'text': f.read(),
                    'filename': filename
                })
        
        return resumes
    
    async def _generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding using Claude"""
        # Note: In production, you'd use a dedicated embedding model
        # This is a simplified approach for demonstration
        
        prompt = f"""
        Analyze this resume and extract key technical concepts, skills, and patterns.
        Represent it as a list of 384 numerical features (0-1 scale) covering:
        - Technical skills presence and depth
        - Experience level indicators
        - Project complexity
        - Industry alignment
        
        Resume:
        {text[:2000]}  # Truncate for API limits
        
        Return only comma-separated numbers.
        """
        
        response = self.anthropic.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Parse response to get embedding
        # In production, use a proper embedding model
        embedding_str = response.content[0].text.strip()
        embedding = [float(x) for x in embedding_str.split(',')[:384]]
        
        # Pad or truncate to ensure consistent dimension
        if len(embedding) < 384:
            embedding.extend([0.0] * (384 - len(embedding)))
        
        return np.array(embedding[:384])
    
    async def find_similar_resumes(
        self, 
        parsed_resume: ParsedResume, 
        parsed_jd: ParsedJobDescription,
        k: int = 3
    ) -> List[Dict]:
        """Find k most similar resumes using FAISS"""
        # Create query embedding combining resume and JD
        query_text = self._create_query_text(parsed_resume, parsed_jd)
        query_embedding = await self._generate_embedding(query_text)
        
        # Search in FAISS
        distances, indices = self.index.search(
            np.array([query_embedding]).astype('float32'), 
            k
        )
        
        # Return similar resumes with scores
        similar_resumes = []
        for idx, distance in zip(indices[0], distances[0]):
            similar_resumes.append({
                'resume': self.reference_resumes[idx],
                'similarity_score': 1 / (1 + distance),  # Convert distance to similarity
                'relevant_sections': self._extract_relevant_sections(
                    self.reference_resumes[idx]['text'],
                    parsed_jd.keywords
                )
            })
        
        return similar_resumes
    
    def _create_query_text(
        self, 
        resume: ParsedResume, 
        jd: ParsedJobDescription
    ) -> str:
        """Create query text combining resume and JD for embedding"""
        skills = ' '.join(resume.skills)
        projects = ' '.join([p['description'] for p in resume.projects[:3]])
        jd_keywords = ' '.join(jd.keywords)
        required_skills = ' '.join(jd.required_skills)
        
        return f"""
        Current Skills: {skills}
        Projects: {projects}
        Target Role Requirements: {required_skills}
        Key Technologies: {jd_keywords}
        """
    
    def _extract_relevant_sections(
        self, 
        resume_text: str, 
        keywords: List[str]
    ) -> Dict[str, List[str]]:
        """Extract sections from reference resume relevant to JD keywords"""
        relevant_sections = {
            'matching_skills': [],
            'relevant_projects': [],
            'useful_patterns': []
        }
        
        lines = resume_text.split('\n')
        
        for line in lines:
            line_lower = line.lower()
            # Check if line contains relevant keywords
            for keyword in keywords:
                if keyword.lower() in line_lower:
                    if any(indicator in line_lower for indicator in ['built', 'developed', 'created', 'implemented']):
                        relevant_sections['relevant_projects'].append(line.strip())
                    elif any(indicator in line_lower for indicator in ['skills', 'technologies', 'tools']):
                        relevant_sections['matching_skills'].append(line.strip())
                    else:
                        relevant_sections['useful_patterns'].append(line.strip())
                    break
        
        return relevant_sections