import json
import os
import hashlib

os.makedirs("data", exist_ok=True)
FILE_PATH = "data/seen_jobs.json"

def load_seen():
    if not os.path.exists(FILE_PATH) or os.path.getsize(FILE_PATH) == 0:
        return set()
    try:
        with open(FILE_PATH, "r") as f:
            return set(json.load(f))
    except json.JSONDecodeError:
        return set()

def save_seen(seen):
    with open(FILE_PATH, "w") as f:
        json.dump(list(seen), f)

def job_hash(title, company):
    return hashlib.md5(f"{title}_{company}".encode()).hexdigest()
