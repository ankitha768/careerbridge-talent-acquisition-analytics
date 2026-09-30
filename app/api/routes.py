import json
from pathlib import Path
from fastapi import APIRouter, HTTPException
from app.models import Candidate, Job, MatchResponse
from app.services.matcher import match_candidate
from app.services.ranking import rank_jobs

router=APIRouter(prefix="/api/v1")
DATA=Path(__file__).resolve().parents[2]/"data/jobs.json"

def load_jobs():
    return [Job(**item) for item in json.loads(DATA.read_text(encoding="utf-8"))]

@router.get("/jobs")
def jobs():
    return load_jobs()

@router.post("/match/{job_id}", response_model=MatchResponse)
def match(job_id:str, candidate:Candidate):
    job=next((j for j in load_jobs() if j.id==job_id),None)
    if not job: raise HTTPException(status_code=404,detail="Job not found")
    score,matched,missing,explanation=match_candidate(candidate,job)
    return {"job_id":job.id,"candidate":candidate.name,"score":score,"matched_skills":matched,"missing_skills":missing,"explanation":explanation}

@router.post("/rank")
def rank(candidate:Candidate):
    return rank_jobs(candidate,load_jobs())
