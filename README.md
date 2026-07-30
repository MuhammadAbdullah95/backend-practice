# 🚀 Backend Practice

A hands-on FastAPI backend project built from scratch to learn modern backend development practices.

## What I'm Building & Learning

| Concept | Implementation |
|---------|---------------|
| **FastAPI** | REST API framework with automatic OpenAPI docs |
| **CRUD Operations** | Full Create, Read, Update, Delete on items |
| **SQLite + SQLAlchemy** | ORM-based database with models and migrations |
| **Authentication** | JWT-based auth (register/login) with bcrypt password hashing |
| **Project Structure** | Modular layout — models, schemas, CRUD, API routes, config, security |
| **Dependency Injection** | FastAPI's `Depends` for DB sessions and auth |
| **Environment Config** | `.env`-driven settings via `core/config.py` |
| **Security** | Secure password hashing, JWT tokens, bearer auth |

## Project Structure

```
backend_app/
├── main.py              # App entry point
├── database.py          # SQLAlchemy engine & session
├── core/
│   ├── config.py        # Settings (SECRET_KEY, DB URL, etc.)
│   └── security.py      # Password hashing, JWT encode/decode
├── models/              # SQLAlchemy ORM models (User, Item)
├── schemas/             # Pydantic request/response schemas
├── crud/                # Database operation layer
└── api/
    ├── deps.py          # Shared dependencies (get_current_user)
    └── v1/
        ├── auth.py      # Register, Login, Me
        └── items.py     # Items CRUD endpoints
```

## Quick Start

```bash
uv sync
uv run uvicorn backend_app.main:app --reload
```

- **API Docs:** http://localhost:8000/docs
- **Register:** `POST /api/v1/register`
- **Login:** `POST /api/v1/login`
- **Items CRUD:** `POST/GET/PUT/DELETE /api/v1/items`
