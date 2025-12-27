import json
import os
import hashlib

FILE_PATH = "data/seen_jobs.json"

def load_seen():
    if not os.path.exists(FILE_PATH):
        return set()

    if os.path.getsize(FILE_PATH) == 0:
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
    unique_string = f"{title}_{company}"
    return hashlib.md5(unique_string.encode()).hexdigest()
