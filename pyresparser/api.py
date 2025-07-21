from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .resume_parser import ResumeParser
from .utils import extract_skills
from .ats_scorer import get_detailed_ats_score
import tempfile
import shutil
import os
import spacy

app = FastAPI()

# Load the spaCy model once when the application starts
nlp = spacy.load('en_core_web_sm')

# Allow CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/parse")
async def parse_resume(
    file: UploadFile = File(...), 
    job_description: str = Form("")
):
    # Save uploaded file to a temp location
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
    try:
        data = ResumeParser(tmp_path).get_extracted_data()

        job_skills = set()
        if job_description:
            # Extract skills from the job description
            doc = nlp(job_description)
            noun_chunks = list(doc.noun_chunks)
            job_skills = set([skill.lower() for skill in extract_skills(doc, noun_chunks)])
            
        # Get the detailed ATS score
        ats_score_details = get_detailed_ats_score(data, job_skills)
        data['ats_score'] = ats_score_details
        
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        os.remove(tmp_path) 