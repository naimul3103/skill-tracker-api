
# 🚀 Developer Skill Tracker API

A comprehensive, production-style REST API built with **FastAPI** for tracking technical skills, proficiency levels, and daily learning journals. This project demonstrates advanced API design patterns, including resource linking, cross-resource validation, and data integrity enforcement.

## ✨ Features

- **Full CRUD Operations**: Complete Create, Read, Update, and Delete functionality for Skills and Journals.
- **Resource Linking (Foreign Keys)**: Link journal entries to specific skills using a `skill_id` reference.
- **Data Integrity (RESTRICT Pattern)**: Prevents the deletion of skills that have active journals linked to them, avoiding orphaned records.
- **Partial Updates**: Uses Pydantic's `exclude_unset=True` to allow updating specific fields without overwriting the rest of the resource.
- **Robust Data Validation**: Pydantic schemas enforce data types, string lengths, and value ranges (e.g., rating 1-10) automatically, returning `422 Unprocessable Entity` on bad data.
- **Professional Documentation**: Automatically generated, highly detailed Swagger UI and ReDoc endpoints with examples.

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Server**: Uvicorn (ASGI)
- **Validation**: Pydantic v2
- **Language**: Python 3.10+
- **Architecture**: Separation of Concerns (Routers, Schemas, Database layer)

---

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/naimul3103/skill-tracker-api.git
   cd skill-tracker-api
   ```


2. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   python -m pip install -r requirements.txt
   ```

## 🏃 Running the Application

Start the development server:

```bash
python -m uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## 📚 Interactive API Documentation

Once the server is running, visit:

- **Swagger UI** (Interactive testing): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc** (Alternative reference): [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---
## 🛣️ API Endpoints Overview

### Skills
- `POST /skills/` - Create a new skill
- `GET /skills/` - List all skills (filterable by `?category=Backend`)
- `GET /skills/{id}` - Get a specific skill
- `PUT /skills/{id}` - Update a skill
- `DELETE /skills/{id}` - Delete a skill (fails if linked journals exist)

### Journals
- `POST /journals/` - Create a journal entry (optionally link to a `skill_id`)
- `GET /journals/` - List journals (filterable by `?skill_id=1`)
- `GET /journals/{id}` - Get a specific journal
- `PUT /journals/{id}` - Update a journal
- `DELETE /journals/{id}` - Delete a journal


## 🏗️ Project Architecture

This project follows the **Separation of Concerns** principle to ensure maintainability:

```text
skill-tracker-api/
├── main.py              # App initialization, lifespan events, and router inclusion
├── schemas.py           # Pydantic models (Data shapes, validation rules, examples)
├── db.py                # Mock database layer (In production, replaced by SQL/NoSQL ORM)
└── routers/
    ├── __init__.py      # Package marker
    ├── skills.py        # Skill endpoints and business logic
    └── journals.py      # Journal endpoints and cross-resource validation
```

### Key Design Decisions

1. **Shared Database Layer (`db.py`)**: Instead of defining databases inside individual routers, we centralize them in `db.py`. This prevents circular imports and allows the Journals router to easily query the Skills database for validation.
2. **Pydantic v2 `exclude_unset=True`**: Used in `PUT` endpoints to ensure that if a client only sends `{"rating": 10}`, the server doesn't accidentally overwrite the `name` and `category` with `null`.
3. **RESTRICT Deletion**: Before deleting a skill, the API checks the `JOURNALS_DB` for dependencies. This prevents "orphaned" journal entries that point to non-existent skills.

## 📜 License

MIT License. Free to use and modify.
