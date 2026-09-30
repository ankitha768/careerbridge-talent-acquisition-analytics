import json
from pathlib import Path

import pandas as pd
import streamlit as st

from app.models import Candidate, Job
from app.services.ranking import rank_jobs

st.set_page_config(
    page_title="CareerBridge — Talent Acquisition Analytics",
    page_icon="💼",
    layout="wide",
)

@st.cache_data
def load_jobs():
    path = Path(__file__).parent / "data" / "jobs.json"
    return json.loads(path.read_text(encoding="utf-8"))

jobs_data = load_jobs()

st.title("💼 CareerBridge")
st.caption("Talent acquisition analytics • explainable candidate-to-job matching")

with st.sidebar:
    st.header("Candidate profile")
    name = st.text_input("Name", value="Ankitha")
    skills_text = st.text_area(
        "Skills",
        value="Python, FastAPI, MySQL, Git, GCP",
        help="Separate skills with commas.",
    )
    experience = st.number_input(
        "Years of experience",
        min_value=0.0,
        max_value=30.0,
        value=1.0,
        step=0.5,
    )
    summary = st.text_area(
        "Profile summary",
        value="Backend-focused developer interested in cloud, automation and AI-assisted applications.",
    )
    run = st.button("Analyze matches", type="primary", use_container_width=True)

skills = [item.strip() for item in skills_text.split(",") if item.strip()]
candidate = Candidate(
    name=name.strip() or "Candidate",
    skills=skills,
    years_experience=experience,
    summary=summary,
)

jobs = [Job(**item) for item in jobs_data]
ranked = rank_jobs(candidate, jobs)

if run or "careerbridge_ran" not in st.session_state:
    st.session_state.careerbridge_ran = True

st.subheader("Match overview")
scores = pd.DataFrame(
    [
        {
            "Job": item["job"].title,
            "Company": item["job"].company,
            "Location": item["job"].location,
            "Match Score": item["score"],
            "Matched Skills": len(item["matched_skills"]),
            "Missing Skills": len(item["missing_skills"]),
        }
        for item in ranked
    ]
)
st.dataframe(
    scores.style.format({"Match Score": "{:.1f}"}),
    use_container_width=True,
    hide_index=True,
)

st.subheader("Match scores")
chart_data = scores.set_index("Job")["Match Score"].sort_values(ascending=True)
st.bar_chart(chart_data, height=280)

st.subheader("Explainable results")
for item in ranked:
    job = item["job"]
    with st.expander(f"{job.title} · {job.company} · {item['score']:.1f}%"):
        col1, col2, col3 = st.columns(3)
        col1.metric("Match score", f"{item['score']:.1f}%")
        col2.metric("Required experience", f"{job.min_experience:g} yrs")
        col3.metric("Candidate experience", f"{candidate.years_experience:g} yrs")

        st.write(item["explanation"])
        st.write("**Matched skills:**", ", ".join(item["matched_skills"]) or "None")
        st.write("**Missing skills:**", ", ".join(item["missing_skills"]) or "None")
        st.write(f"**Role:** {job.title} at {job.company} · {job.location}")
        st.write(job.description)

st.divider()
st.caption("Portfolio demo: uses the repository's sample jobs and transparent matching logic; no live job-site scraping is required for deployment.")
