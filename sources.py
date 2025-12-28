import requests

HEADERS = {"User-Agent": "Mozilla/5.0"}


# -----------------------------
# SOURCE 1: RemoteOK (Remote jobs)
# -----------------------------
def fetch_remoteok():
    url = "https://remoteok.com/api"
    response = requests.get(url, headers=HEADERS)
    data = response.json()[1:]

    jobs = []
    for job in data:
        jobs.append({
            "title": job.get("position", ""),
            "company": job.get("company", ""),
            "tags": job.get("tags", []) + ["remote"],
            "location": "remote"
        })

    return jobs


# -----------------------------
# SOURCE 2: GitHub India Internships
# -----------------------------
def fetch_github_india_internships():
    url = "https://raw.githubusercontent.com/pittcsc/Summer2025-Internships/dev/README.md"
    response = requests.get(url, headers=HEADERS)
    text = response.text

    jobs = []
    for line in text.splitlines():
        if "|" in line and ("India" in line or "Remote" in line):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 4:
                jobs.append({
                    "title": parts[1],
                    "company": parts[2],
                    "tags": ["internship", "student"],
                    "location": parts[3]
                })

    return jobs
