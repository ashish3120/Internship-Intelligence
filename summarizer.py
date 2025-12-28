from datetime import date

def summarize_jobs(jobs):
    today = date.today().strftime("%d %b %Y")

    if not jobs:
        return f"""Subject: Tech Internships Update – {today}

Hi,

No new tech internships or fresher roles were found today.

Please check again tomorrow.

Best,
Internship Intelligence System
"""

    lines = []
    for i, (title, company, tags, url) in enumerate(jobs, start=1):
        location = "Remote" if "remote" in " ".join(tags).lower() else "India"
        lines.append(
            f"{i}. {title} – {company} ({location})\n   Apply: {url}"
        )

    body = "\n\n".join(lines)

    return f"""Subject: New Tech Internships & Fresher Roles – {today}

Hi,

Here are the latest tech internship and entry-level opportunities you can apply for today:

{body}

That’s all for today.

Best,  
Internship Intelligence System
"""
