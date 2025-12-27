import google.generativeai as genai

genai.configure(api_key="AIzaSyAiIL44HifQ9Fttn0yau9LbKSXpeZH3rZ4")

def summarize_jobs(jobs):
    if not jobs:
        return "No new relevant early-career roles found today."

    text = ""
    for j in jobs:
        text += f"Title: {j[0]}, Company: {j[1]}, Tags: {j[2]}\n"

    prompt = f"""
    You are a career assistant for a Computer Science student.
    Summarize the following job listings into a short daily report.
    Focus on student and early-career relevance.

    {text}
    """

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

    return response.text
