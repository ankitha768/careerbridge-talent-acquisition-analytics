from pydantic import BaseModel, Field

class Candidate(BaseModel):
    name: str
    skills: list[str] = Field(default_factory=list)
    years_experience: float = 0
    summary: str = ""

class Job(BaseModel):
    id: str
    title: str
    company: str
    skills: list[str] = Field(default_factory=list)
    min_experience: float = 0
    location: str = "Remote"
    description: str = ""

class MatchResponse(BaseModel):
    job_id: str
    candidate: str
    score: float
    matched_skills: list[str]
    missing_skills: list[str]
    explanation: str
