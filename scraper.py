from sources import fetch_remoteok, fetch_github_india_internships
from scorer import score_job
from deduplicator import load_seen, save_seen, job_hash
from summarizer import summarize_jobs
from emailer import send_email
from sources import fetch_github_india_internships, fetch_greenhouse_internships

def is_valid_tech_internship(title, tags):
    title = title.lower()
    tags_text = " ".join(tags).lower()

    # ✅ MUST contain internship / fresher intent
    STUDENT_KEYWORDS = [
        "intern",
        "internship",
        "trainee",
        "graduate",
        "fresher",
        "entry",
        "junior"
    ]

    # ✅ MUST be a tech role
    TECH_KEYWORDS = [
        "software",
        "developer",
        "engineer",
        "engineering",
        "backend",
        "frontend",
        "full stack",
        "fullstack",
        "data",
        "machine learning",
        "ml",
        "ai",
        "artificial intelligence",
        "cloud",
        "devops",
        "site reliability",
        "sre",
        "security",
        "qa",
        "test",
        "automation"
    ]

    # ❌ BLOCK NON-TECH / BUSINESS / SUPPORT ROLES
    BLOCKLIST = [
        "support",
        "customer",
        "care",
        "content",
        "marketing",
        "sales",
        "clinical",
        "medical",
        "health",
        "operations",
        "recovery",
        "finance",
        "account",
        "representative",
        "manager",
        "director",
        "lead",
        "principal",
        "staff",
        "senior"
    ]

    if any(word in title for word in BLOCKLIST):
        return False

    student_match = any(word in title or word in tags_text for word in STUDENT_KEYWORDS)
    tech_match = any(word in title or word in tags_text for word in TECH_KEYWORDS)

    return student_match and tech_match

# 1. Fetch jobs
all_jobs = []

# Primary: Greenhouse (real company internships)
all_jobs.extend(fetch_greenhouse_internships())

# Secondary: GitHub curated internships
all_jobs.extend(fetch_github_india_internships())

# 2. Load seen jobs
seen = load_seen()
new_seen = set(seen)

ranked = []
all_scored = []

MIN_SCORE = 5

# 3. Score + filter
for job in all_jobs:
    title = job.get("title", "").strip()
    company = job.get("company", "").strip()
    tags = job.get("tags", [])
    location = job.get("location", "")
    url = job.get("url", "")

    if not title or not company:
        continue

    h = job_hash(title, company)
    if h in seen:
        continue

    score = score_job(job)
    all_scored.append((title, company, tags, score, url))

    if score >= MIN_SCORE and is_valid_tech_internship(title, tags):
        ranked.append((title, company, tags, url))
        new_seen.add(h)

# 4. Fallback (near-miss)
if not ranked and all_scored:
    print("No strong matches found — using near-miss recommendations")
    all_scored.sort(key=lambda x: x[3], reverse=True)
    ranked = [(j[0], j[1], j[2], j[4]) for j in all_scored[:5]]

# 5. Save state
save_seen(new_seen)

print("New relevant jobs found:", len(ranked))

# 6. Summarize + email
summary = summarize_jobs(ranked)
print("\nDAILY SUMMARY:\n")
print(summary)

send_email(summary)
