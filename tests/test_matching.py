from app.models import Candidate, Job
from app.services.matcher import match_candidate

def test_skill_match():
    candidate=Candidate(name="Test",skills=["Python","FastAPI"],years_experience=1)
    job=Job(id="1",title="Backend",company="X",skills=["Python","FastAPI"],min_experience=1)
    score,matched,missing,_=match_candidate(candidate,job)
    assert score==100
    assert len(matched)==2
    assert missing==[]
