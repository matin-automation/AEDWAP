# AEDWAP

## Problem Statement

Enterprise organizations process large volumes of invoices and other business documents manually.

Employees must extract information from documents, validate data against purchase orders, check business policies, obtain approvals, update enterprise systems, and maintain audit records.

This process is slow, error-prone, and difficult to scale.

This project builds an AI-powered document and workflow automation platform that automates these activities while routing uncertain cases to humans for review.

# AEDWAP — Backend Setup

## Prerequisites
- Python 3.12
- PostgreSQL running, DB created
- Git

## 1. Clone repo
```powershell
git clone <repo-url>
cd AEDWAP
```

## 2. Create virtual environment
```powershell
python -m venv venv
venv\Scripts\activate
```

## 3. Install dependencies
```powershell
cd backend
pip install -r requirements.txt
```

## 4. Environment variables
Create `.env` file inside `backend/` folder:

```
DATABASE_URL=postgresql://<user>:<password>@localhost:5432/<dbname>
```


## 5. Load database schema (first time only)
```powershell
psql -U <user> -d <dbname> -f ../database/schema.sql
psql -U <user> -d <dbname> -f ../database/seed_data.sql
```

## 6. Verify DB connection
```powershell
python test_db.py
```

## 7. Run API server
```powershell
uvicorn app.main:app --reload
```

## 8. Check it works
Open browser:
```
http://127.0.0.1:8000/docs
```
Swagger UI show all endpoints, test directly there.

## Project structure
```
backend/
├── app/
│   ├── main.py          — FastAPI entry point
│   ├── api/              — route handlers, one file per resource
│   ├── schemas/           — Pydantic request/response models
│   ├── core/
│   │   ├── config.py      — env settings
│   │   └── database.py    — DB engine + session
│   └── models/
│       └── models.py      — SQLAlchemy ORM models
├── test_db.py
└── requirements.txt
```

## Notes
- Never commit `.env` file — already in `.gitignore`.
- New endpoint = new file in `app/api/`, matching schema in `app/schemas/`, then register in `app/main.py` via `app.include_router(...)`.
