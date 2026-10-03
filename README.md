# SkillMatch

**Find internships and jobs that match your skills.**

SkillMatch is a student-focused internship & job discovery platform that matches
students to opportunities based on skills, education, location, and preferences —
and shows a precise **Skill Match %** for every listing, powered by a pure-Python
matching algorithm (no external AI API required).

---

## Problem Statement

Students apply to internships and jobs blindly — scanning long requirement lists
manually, with no clear sense of how well they actually fit a role, and no way to
track what they've applied to.

## Solution

SkillMatch builds one profile per student (skills, education, projects, resume,
preferences) and matches it against a database of opportunities using a transparent
formula:

```
Match % = (Matched Required Skills / Total Required Skills) × 100
```

Every opportunity clearly shows ✅ matched skills and ❌ missing skills, a skill-gap
breakdown, and a direct link to the official application page.

---

## Features

- Skill-based matching engine with match %, labels (Excellent / Good / Partial / Low
  Match) and visual progress bars
- Student registration/login (hashed passwords, session auth via Flask-Login)
- Editable student profile: education, career preferences, skills, multiple
  projects, resume upload (PDF)
- Rule-based Resume Skill Analyzer (works without any AI API)
- Recommended-for-you dashboard, ranked by match %, work mode, location, stipend
- Search & filter (keyword, skill, type, work mode, location, stipend range) with
  sorting (match, latest, stipend, deadline)
- Save/bookmark opportunities
- Application tracker with statuses (Saved → Applied → Shortlisted → Interview →
  Selected/Rejected) and stats
- Full admin panel: CRUD for opportunities, companies, skills; view students and
  applications; dashboard stats
- Optional AI module hook (`AI_ENABLED` in `.env`) — the core app works fully
  without it

## Tech Stack

| Layer     | Technology                                   |
|-----------|-----------------------------------------------|
| Frontend  | HTML5, CSS3 (custom, dark UI), Jinja2         |
| Backend   | Python 3, Flask, Flask-Login, Flask-SQLAlchemy|
| Database  | MySQL (via PyMySQL)                           |
| Auth      | Werkzeug password hashing + server sessions   |

## Architecture

```
Browser → Flask routes (auth / student / admin / main)
             → services/matching.py  (pure-Python skill match engine)
             → SQLAlchemy models     → MySQL
```

## Database Schema

See [`database/schema.sql`](database/schema.sql) for full DDL. Core tables:
`users`, `student_profiles`, `skills`, `student_skills`, `projects`, `companies`,
`opportunities`, `opportunity_skills`, `saved_opportunities`, `applications` —
normalized with foreign keys and indexes. [`database/seed.sql`](database/seed.sql)
has the equivalent raw-SQL sample data.

---

## Installation

```bash
# 1. Clone / unzip the project, then:
cd SkillMatch
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## MySQL Database Setup

```sql
-- In your MySQL client:
CREATE DATABASE skillmatch CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Then copy the environment template and fill in your MySQL credentials:

```bash
cp .env.example .env
# edit .env: DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, SECRET_KEY
```

### Environment Variables (`.env.example`)

```
SECRET_KEY=change-this-to-a-random-secret-key
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=skillmatch
UPLOAD_FOLDER=uploads/resumes
MAX_CONTENT_LENGTH=5242880
AI_API_KEY=
AI_ENABLED=False
```

### Create tables + sample data

Easiest path — one command creates all tables and seeds skills, companies,
sample opportunities, and demo accounts:

```bash
python init_db.py
```

(Equivalent manual path: run `database/schema.sql` then `database/seed.sql`
directly against MySQL with the `mysql` CLI or a GUI client.)

## How to Run

```bash
flask --app app run --debug
# or simply:
python app.py
```

Visit **http://127.0.0.1:5000**

## Test Login Credentials (Demo)

| Role    | Email                     | Password     |
|---------|----------------------------|--------------|
| Admin   | admin@skillmatch.com       | Admin@123    |
| Student | student@skillmatch.com     | Student@123  |

---

## Project Structure

```
SkillMatch/
├── app.py                  # App factory + entry point
├── config.py                # Config from .env
├── init_db.py                # One-command DB init + seed
├── requirements.txt
├── .env.example
├── database/
│   ├── schema.sql            # Raw MySQL DDL
│   └── seed.sql               # Raw MySQL sample data
├── models/__init__.py        # SQLAlchemy models
├── routes/                    # auth, student, admin, main blueprints
├── services/matching.py      # Core skill-matching algorithm
├── templates/                 # Jinja2 templates (+ admin/, partials/)
├── static/css/style.css      # Dark UI theme
├── uploads/resumes/           # Uploaded resume PDFs
└── tests/test_matching.py    # Unit tests for the matching engine
```

## Important Note on Sample Data

All companies, opportunities and "Apply Now" links seeded by `init_db.py` /
`seed.sql` are **sample/demo data** built for this hackathon demo — they are
marked `is_sample = True` and are not verified live postings. Replace them with
real, verified opportunities before any production use.

---

## Hackathon Presentation Explanation

SkillMatch solves a problem every student on this team has personally faced:
sorting through internship listings with no idea whether their skills are a fit
until after filling out a full application. The matching engine is intentionally
simple and explainable — a direct percentage of overlapping required skills — so
judges and users alike can trust exactly why a match score is what it is, with no
opaque AI black box required for the core feature to work.

## 2-Minute Project Pitch

"Every year, thousands of students apply to internships they're not qualified for,
and skip ones they actually match — because nobody tells them their fit *before*
they apply. SkillMatch fixes that. Students build one profile — skills, projects,
resume — and instantly see a Skill Match % for every internship and job, with
exactly which skills they have and which they're missing. It's not just a job
board; it's a personalized skill gap report attached to every listing, that also
tracks their applications from 'Saved' to 'Selected'. And recruiters get a
lightweight admin panel to post and manage roles. We built the whole matching
engine in pure Python — no external AI dependency — so it's fast, explainable,
and free to run."

## Possible Judge Questions and Answers

**Q: How is the match percentage calculated — is it AI?**
A: No — it's a transparent formula: matched required skills ÷ total required
skills × 100. This makes it explainable and doesn't depend on an external API or
its cost/availability.

**Q: What happens if a student has more skills than required?**
A: Extra skills don't lower the score — only how many *required* skills are
covered matters, matching real-world screening.

**Q: How would you prevent fake or duplicate opportunity listings?**
A: The admin panel is the only way to add listings today; a production version
would add company verification workflows and duplicate-detection on
(company + title + apply_url).

**Q: Is the resume analyzer really AI-free?**
A: Yes — it's rule-based: it extracts the student's stated skills, compares them
against skills requested across all listed opportunities, and returns rule-based
suggestions (add projects, add GitHub, learn X). An optional AI module hook exists
in config but isn't required.

**Q: How do you handle security?**
A: Passwords are hashed with Werkzeug (never stored in plaintext), sessions via
Flask-Login, parameterized queries via SQLAlchemy (no raw SQL injection surface),
server-side PDF-only + file-size validation on resume uploads, and secrets are
kept in `.env` (never committed, never sent to the frontend).

**Q: What was the hardest part to build?**
A: Designing the matching + ranking logic so it stays simple to explain to a judge
in one sentence, while still factoring in work mode, location and stipend
preferences for the "Recommended For You" ordering.

## Future Improvements

- Real AI-powered resume parsing (skill extraction from unstructured PDF text)
- Recruiter accounts with their own posting dashboard (vs. admin-only)
- Email notifications on deadline reminders and new matching opportunities
- Skill trend analytics across the whole opportunity database
- Duplicate-listing detection and company verification workflow
- Public API for college placement cells to bulk-import listings

## How to Deploy

- **Backend + DB**: any host with Python 3.11+ and MySQL (Railway, Render,
  PythonAnywhere, or a VPS). Set the `.env` variables as environment variables in
  the host's dashboard instead of a committed `.env` file.
- Run `pip install -r requirements.txt`, then `python init_db.py` once against the
  production MySQL instance, then serve with a WSGI server:
  ```bash
  pip install gunicorn
  gunicorn -w 4 -b 0.0.0.0:8000 app:app
  ```
- Put Nginx (or the host's built-in proxy) in front of Gunicorn for TLS.
- Store uploaded resumes on persistent storage (or S3-compatible storage) rather
  than local disk if deploying to an ephemeral filesystem host.

## Team Members

- _Add your team members here before presenting._
