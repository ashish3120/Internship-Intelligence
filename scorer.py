KEYWORDS = {
    "intern": 5,
    "internship": 5,
    "junior": 3,
    "student": 4,
    "trainee": 3,
    "entry": 3,
    "fresher": 4
}

def score_job(job):
    score = 0
    text = (job["title"] + " " + " ".join(job["tags"])).lower()

    for word, weight in KEYWORDS.items():
        if word in text:
            score += weight

    return score
