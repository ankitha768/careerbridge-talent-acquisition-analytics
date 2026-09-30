import re
from app.models import Candidate, Job

def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9+#.-]+", " ", value.lower()).strip()

def match_candidate(candidate: Candidate, job: Job):
    candidate_skills={normalize(s) for s in candidate.skills}
    job_skills={normalize(s) for s in job.skills}
    matched=sorted(candidate_skills & job_skills)
    missing=sorted(job_skills-candidate_skills)
    skill_score=(len(matched)/len(job_skills)*70) if job_skills else 70
    experience_score=30 if candidate.years_experience >= job.min_experience else max(0, candidate.years_experience/job.min_experience*30) if job.min_experience else 30
    score=round(min(100, skill_score+experience_score),2)
    explanation=f"{len(matched)}/{len(job_skills)} required skills matched; experience requirement is {job.min_experience} years."
    return score, matched, missing, explanation
