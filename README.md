# 📌 Internship Intelligence

Automated **Tech Internship Tracking & Alert System**  
Built in Python — Scalable ATS Scraping, Rule-based Filtering, and Clean Email Delivery

---

## 🧠 Project Overview

**Internship Intelligence** is a backend automation system that:

✅ Scrapes internship and entry-level roles from scalable ATS platforms (e.g., Greenhouse)  
✅ Filters listings for **tech internships and fresher roles**  
✅ Deduplicates previously sent listings  
✅ Sends daily professional email alerts with links to internship applications

This project solves a real problem: **finding high-quality tech internships in India and remote**, with minimal noise and no unsafe scraping.

---

## 🚀 Features

✔ ATS-based scraping (Greenhouse) — covers thousands of tech companies  
✔ GitHub curated internship fallback  
✔ Rule-based tech internship filtering  
✔ Scoring and near-miss recommendation  
✔ Deduplication across runs  
✔ Daily email notifications  
✔ Clear, clean professional format

---

## 🧱 Architecture
sources.py → Fetch job data from Greenhouse + GitHub
scorer.py → Assign relevance scores
deduplicator.py → Persistent seen jobs state
scraper.py → Orchestration and filtering pipeline
summarizer.py → Formats final email content
emailer.py → Sends email using SMTP
scheduler.py → Runs scraper daily


Each module has a **single responsibility**, following clean backend design principles.

---

## 🔍 Data Sources

### 1️⃣ Greenhouse ATS (Primary Source)
- Covers **thousands of tech companies**
- Public, structured career pages
- No login, no unsafe scraping
- Internship filtering applied downstream

### 2️⃣ GitHub Curated Internship Lists (Fallback)
- Community-maintained internship repositories
- Used when ATS listings are sparse
- Ensures quality baseline

> ⚠️ Internship availability is seasonal.  
> Some days may legitimately have **zero results**.

---

## 🧠 Filtering Logic

A role is included only if it satisfies:

### ✅ Internship / Fresher intent
- `intern`, `internship`, `trainee`, `junior`, `graduate`, `fresher`

### ✅ Technical relevance
- Software, Backend, Frontend, Data, ML, AI, Cloud, DevOps, QA, Security

### ❌ Excluded roles
- Support, Sales, Marketing, Finance, Healthcare, Management, Senior roles

This ensures **high signal, low noise**.

---


