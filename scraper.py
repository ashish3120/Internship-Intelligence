"""
scraper.py
-----------
Main orchestration pipeline for the Automated Internship Intelligence System.

Flow:
1. Fetch jobs from multiple India-relevant sources
2. Deduplicate previously seen jobs
3. Score jobs for early-career + India relevance
4. Apply fallback if data is sparse
5. Summarize using LLM
6. Email the daily report
"""

from sources import (
    fetch_remoteok,
    fetch_github_india_internships
)
from scorer import score_job
from deduplicator import load_seen, save_seen, job_hash
from summarizer import summarize_jobs
from emailer import send_email


# -----------------------------
# 1. COLLECT JOBS FROM SOURCES
# -----------------------------
all_jobs = []

try:
    all_jobs.extend(fetch_remoteok())
except Exception as e:
    print("RemoteOK fetch failed:", e)

try:
    all_jobs.extend(fetch_github_india_internships())
except Exception as e:
    print("GitHub India internships fetch failed:", e)


# -----------------------------
# 2. LOAD DEDUPLICATION STATE
# -----------------------------
seen = load_seen()
new_seen = set(seen)

ranked_jobs = []
all_scored_jobs = []

# -----------------------------
# 3. SCORE + FILTER JOBS
# -----------------------------
MIN_SCORE = 5  # higher threshold = better quality

for job in all_jobs:
    title = job.get("title", "").strip()
    company = job.get("company", "").strip()
    tags = job.get("tags", [])
    location = job.get("location", "")

    if not title or not company:
        continue

    job_id = job_hash(title, company)

    if job_id in seen:
        continue

    score = score_job(job)

    job_tuple = (title, company, tags, score, location)
    all_scored_jobs.append(job_tuple)

    if score >= MIN_SCORE:
        ranked_jobs.append(job_tuple)
        new_seen.add(job_id)


# -----------------------------
# 4. FALLBACK (NEAR-MISS LOGIC)
# -----------------------------
if not ranked_jobs and all_scored_jobs:
    print("No strong matches found — using near-miss recommendations")
    all_scored_jobs.sort(key=lambda x: x[3], reverse=True)
    ranked_jobs = all_scored_jobs[:5]  # top 5 closest matches


# -----------------------------
# 5. SAVE UPDATED STATE
# -----------------------------
save_seen(new_seen)


# -----------------------------
# 6. SUMMARIZE & EMAIL
# -----------------------------
print("New relevant jobs found:", len(ranked_jobs))

# summarizer expects (title, company, tags, score)
summary_input = [(j[0], j[1], j[2]) for j in ranked_jobs]

summary = summarize_jobs(summary_input)

print("\nDAILY SUMMARY:\n")
print(summary)

send_email(summary)
