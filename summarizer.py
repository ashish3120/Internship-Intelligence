from google import genai
from datetime import date

API_KEY = "AIzaSyAc_O3KYjI4QBiS-uvQIc8CxAnA3_GIMQY"
client = genai.Client(api_key=API_KEY)

MODEL_NAME = "models/gemini-flash-latest"


def summarize_jobs(jobs):
    today = date.today().isoformat()

    if not jobs:
        return f"""Daily Internship Intelligence Report
Date: {today}

Summary:
• No relevant early-career or student-friendly roles were identified today.

Recommendation:
No action required today.
"""

    job_lines = []
    for j in jobs:
        title, company, tags = j[0], j[1], j[2]
        job_lines.append(f"- {title} at {company} | Tags: {', '.join(tags)}")

    jobs_text = "\n".join(job_lines)

    prompt = f"""
You are generating a concise internal report for a Computer Science student.

Rules:
- Be neutral and professional.
- Do NOT use emojis.
- Do NOT use tables.
- Do NOT use marketing language.
- Keep output concise and factual.
- Assume the reader understands tech basics.

Input job listings:
{jobs_text}

Output format exactly:

Daily Internship Intelligence Report
Date: {today}

Summary:
• <2-3 concise bullets>

Details:
- <one line per job>

Recommendation:
<one short paragraph>
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text.strip()
