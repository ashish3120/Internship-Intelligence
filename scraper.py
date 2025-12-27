import requests
from deduplicator import load_seen, save_seen, job_hash

URL = "https://remoteok.com/api"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(URL, headers=headers)
jobs = response.json()[1:]

seen = load_seen()
new_seen = set(seen)

new_jobs = []

KEYWORDS = ["intern", "internship", "junior", "trainee", "student"]

for job in jobs:
    title = job.get("position", "")
    company = job.get("company", "")
    tags = [t.lower() for t in job.get("tags", [])]

    if any(k in title.lower() for k in KEYWORDS) or any(k in tags for k in KEYWORDS):
        h = job_hash(title, company)
        if h not in seen:
            new_jobs.append((title, company, tags))
            new_seen.add(h)

save_seen(new_seen)

print("New jobs found:", len(new_jobs))

for j in new_jobs[:5]:
    print("----")
    print("Title:", j[0])
    print("Company:", j[1])
    print("Tags:", j[2])
from summarizer import summarize_jobs

summary = summarize_jobs(new_jobs)
print("\nDAILY SUMMARY:\n")
print(summary)
