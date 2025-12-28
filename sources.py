"""
sources.py
-----------
Job sources for Internship Intelligence System

Includes:
- Greenhouse ATS (scalable, real companies)
- GitHub curated internships (fallback)
"""

import requests
from bs4 import BeautifulSoup
import re


# --------------------------------------------------
# GREENHOUSE ATS SCRAPER
# --------------------------------------------------
def fetch_greenhouse_company(company):
    """
    Fetch jobs from a single Greenhouse-powered company
    """

    url = f"https://boards.greenhouse.io/{company}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code != 200:
            return []
    except Exception:
        return []

    soup = BeautifulSoup(resp.text, "html.parser")

    jobs = []

    # Each job listing
    for job in soup.select("div.opening"):
        title_tag = job.find("a")
        location_tag = job.find("span", class_="location")

        if not title_tag:
            continue

        title = title_tag.text.strip()
        link = "https://boards.greenhouse.io" + title_tag["href"]
        location = location_tag.text.strip() if location_tag else "Unknown"

        # Normalize internship signals
        tags = []

        title_lower = title.lower()
        if "intern" in title_lower:
            tags.append("intern")
            tags.append("internship")

        # Add tech hints
        for kw in [
            "software", "engineer", "developer", "backend",
            "frontend", "full stack", "data", "machine learning",
            "ml", "ai", "cloud", "devops", "qa", "test", "security"
        ]:
            if kw in title_lower:
                tags.append(kw)

        jobs.append({
            "title": title,
            "company": company.title(),
            "location": location,
            "tags": tags,
            "url": link
        })

    return jobs


import requests
from bs4 import BeautifulSoup


def fetch_greenhouse_company(company):
    """
    Robust Greenhouse scraper (HTML changes safe)
    """

    url = f"https://boards.greenhouse.io/{company}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        resp = requests.get(url, headers=headers, timeout=20)
        if resp.status_code != 200:
            return []
    except Exception:
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    jobs = []

    # Greenhouse jobs are inside <section id="jobs">
    jobs_section = soup.find("section", id="jobs")
    if not jobs_section:
        return []

    for job in jobs_section.find_all("a", href=True):
        href = job["href"]
        title = job.get_text(strip=True)

        # Skip navigation / empty links
        if not title or "/jobs/" not in href:
            continue

        link = "https://boards.greenhouse.io" + href

        # Try to extract location
        location = "Unknown"
        parent = job.parent
        if parent:
            loc = parent.find("span", class_="location")
            if loc:
                location = loc.get_text(strip=True)

        jobs.append({
            "title": title,
            "company": company.title(),
            "location": location,
            "tags": [],  # filtering happens later
            "url": link
        })

    return jobs


def fetch_greenhouse_internships():
    """
    Fetch jobs from Greenhouse-powered companies
    (internship filtering happens downstream)
    """

    GREENHOUSE_COMPANIES = [
        "stripe",
        "airbnb",
        "atlassian",
        "uber",
        "shopify",
        "databricks",
        "snowflake",
    ]

    all_jobs = []

    for company in GREENHOUSE_COMPANIES:
        jobs = fetch_greenhouse_company(company)
        all_jobs.extend(jobs)

    return all_jobs


# --------------------------------------------------
# GITHUB CURATED INTERNSHIPS (FALLBACK)
# --------------------------------------------------
def fetch_github_india_internships():
    """
    Fetch curated internships from GitHub repositories
    """

    RAW_URL = (
        "https://raw.githubusercontent.com/pittcsc/"
        "Summer2026-Internships/main/README.md"
    )

    try:
        resp = requests.get(RAW_URL, timeout=15)
        if resp.status_code != 200:
            return []
    except Exception:
        return []

    jobs = []

    for line in resp.text.splitlines():
        # Match markdown internship links
        match = re.search(r"\[(.+?)\]\((https?://.+?)\)", line)
        if not match:
            continue

        title = match.group(1)
        url = match.group(2)

        if "intern" not in title.lower():
            continue

        jobs.append({
            "title": title,
            "company": "Various Companies",
            "location": "India / Remote",
            "tags": ["intern", "internship", "tech"],
            "url": url
        })

    return jobs
