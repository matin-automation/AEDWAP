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
http://127.0.0.1:8000
```
Swagger UI show all endpoints, test directly there.

## API Endpoints

Base URL: `http://127.0.0.1:8000`

### Root
| Method | Endpoint | Description |
|--------|----------|--------------|
| GET | `/` | health check |
| GET | `/docs` | Swagger UI |

### Vendors
| Method | Endpoint | Description |
|--------|----------|--------------|
| GET | `/vendors/` | list all vendors |
| GET | `/vendors/{vendor_id}` | get vendor by id |

### Purchase Orders
| Method | Endpoint | Description |
|--------|----------|--------------|
| GET | `/purchase-orders/` | list all purchase orders |
| GET | `/purchase-orders/{po_id}` | get purchase order by id |

### Invoices
| Method | Endpoint | Description |
|--------|----------|--------------|
| GET | `/invoices/` | list all invoices |
| GET | `/invoices/{invoice_id}` | get invoice by id |

### Invoice Items
| Method | Endpoint | Description |
|--------|----------|--------------|
| GET | `/invoice-items/` | list all invoice line items |
| GET | `/invoice-items/{item_id}` | get invoice item by id |

### Validations
| Method | Endpoint | Description |
|--------|----------|--------------|
| GET | `/validations/` | list all validation records |
| GET | `/validations/{validation_id}` | get validation by id |

### Workflow Tasks
| Method | Endpoint | Description |
|--------|----------|--------------|
| GET | `/workflow-tasks/` | list all workflow tasks |
| GET | `/workflow-tasks/{task_id}` | get workflow task by id |

### Approvals
| Method | Endpoint | Description |
|--------|----------|--------------|
| GET | `/approvals/` | list all approvals |
| GET | `/approvals/{approval_id}` | get approval by id |

> Note: `audit_logs` table has no endpoints yet — read-only trail, add later if needed.

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
