from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.models import EnhancementRequest, EnhancementResponse
from app.services.parser import ResumeParser, JobDescriptionParser
from app.services.rag_engine import RAGEngine
from app.services.enhancer import ResumeEnhancer
from app.services.analyzer import GapAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Resume Enhancement API")

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
resume_parser = ResumeParser()
jd_parser = JobDescriptionParser()
rag_engine = RAGEngine()
enhancer = ResumeEnhancer()
gap_analyzer = GapAnalyzer()

@app.on_event("startup")
async def startup_event():
    """Initialize FAISS index with reference resumes"""
    logger.info("Initializing RAG engine...")
    await rag_engine.initialize()
    logger.info("RAG engine initialized successfully")

@app.post("/enhance", response_model=EnhancementResponse)
async def enhance_resume(request: EnhancementRequest):
    """Main endpoint for resume enhancement"""
    try:
        # Parse inputs
        parsed_resume = resume_parser.parse(request.resume_text)
        parsed_jd = jd_parser.parse(request.job_description)
        
        # Find similar resumes using RAG
        similar_resumes = await rag_engine.find_similar_resumes(
            parsed_resume, 
            parsed_jd
        )
        
        # Analyze gaps
        gaps = gap_analyzer.analyze(
            parsed_resume, 
            parsed_jd, 
            similar_resumes
        )
        
        # Enhance resume points
        enhanced_points = await enhancer.enhance_points(
            parsed_resume,
            parsed_jd,
            similar_resumes,
            gaps
        )
        
        # Generate recommendations
        recommendations = await enhancer.generate_recommendations(
            gaps,
            similar_resumes,
            parsed_jd
        )
        
        return EnhancementResponse(
            enhanced_resume_points=enhanced_points,
            recommendations=recommendations
        )
        
    except Exception as e:
        logger.error(f"Enhancement failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
