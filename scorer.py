KEYWORDS = {
    "intern": 5,
    "internship": 5,
    "junior": 3,
    "student": 4,
    "trainee": 3,
    "entry": 3,
    "fresher": 4,
    "engineer": 2,
    "developer": 2
}

INDIA_LOCATIONS = [
    "india", "bangalore", "bengaluru", "hyderabad",
    "pune", "chennai", "noida", "gurgaon",
    "delhi", "remote"
]


def score_job(job):
    score = 0
    text = (job["title"] + " " + " ".join(job["tags"])).lower()
    location = job.get("location", "").lower()

    for word, weight in KEYWORDS.items():
        if word in text:
            score += weight

    for city in INDIA_LOCATIONS:
        if city in location:
            score += 4

    return score
