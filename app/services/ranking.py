from app.models import Candidate, Job
from .matcher import match_candidate

def rank_jobs(candidate: Candidate, jobs: list[Job]):
    ranked=[]
    for job in jobs:
        score,matched,missing,explanation=match_candidate(candidate,job)
        ranked.append({"job":job,"score":score,"matched_skills":matched,"missing_skills":missing,"explanation":explanation})
    return sorted(ranked,key=lambda x:x["score"],reverse=True)
