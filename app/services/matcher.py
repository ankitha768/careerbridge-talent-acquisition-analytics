import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.models import Candidate, Job

def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9+#.-]+", " ", value.lower()).strip()

def match_candidate(candidate: Candidate, job: Job):
    candidate_skills={normalize(s) for s in candidate.skills}
    job_skills={normalize(s) for s in job.skills}
    matched=sorted(candidate_skills & job_skills)
    missing=sorted(job_skills-candidate_skills)

    skill_score=(len(matched)/len(job_skills)*60) if job_skills else 60
    candidate_text=" ".join(candidate.skills)+" "+candidate.summary
    job_text=" ".join(job.skills)+" "+job.title+" "+job.description
    semantic=cosine_similarity(
        TfidfVectorizer(stop_words="english").fit_transform([candidate_text, job_text])
    )[0,1] if candidate_text.strip() and job_text.strip() else 0
    semantic_score=round(semantic*20,2)
    experience_score=20 if candidate.years_experience >= job.min_experience else (candidate.years_experience/job.min_experience*20 if job.min_experience else 20)
    score=round(min(100, skill_score+semantic_score+experience_score),2)
    if not missing and candidate.years_experience >= job.min_experience:
        score=100.0
    explanation=f"{len(matched)}/{len(job_skills)} required skills matched; semantic profile similarity={semantic:.2f}; experience requirement={job.min_experience} years."
    return score, matched, missing, explanation
