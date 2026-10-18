````markdown
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
   git clone https://github.com/yourusername/skill-tracker-api.git
   cd skill-tracker-api
   ```
````

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

## 🛣️ API Reference

### 1. Skills Endpoints (`/skills`)

#### `POST /skills/` - Create a new skill

Creates a new skill in the tracker.

- **Request Body**:
  ```json
  {
    "name": "FastAPI",
    "category": "Backend",
    "rating": 8
  }
  ```
- **Success Response**: `201 Created`
- **Error Responses**: `422 Unprocessable Entity` (if validation fails, e.g., rating > 10).

#### `GET /skills/` - List all skills

Returns a list of all skills.

- **Query Parameters**:
  - `category` (optional, string): Filter skills by category (e.g., `?category=Backend`).
- **Success Response**: `200 OK` - Returns an array of Skill objects.

#### `GET /skills/{skill_id}` - Get a specific skill

- **Path Parameters**: `skill_id` (integer)
- **Success Response**: `200 OK`
- **Error Responses**: `404 Not Found` (if the skill does not exist).

#### `PUT /skills/{skill_id}` - Update a skill

Partially or fully updates a skill. You only need to send the fields you want to change.

- **Request Body** (Example):
  ```json
  {
    "rating": 10
  }
  ```
- **Success Response**: `200 OK`
- **Error Responses**: `404 Not Found`, `422 Unprocessable Entity`.

#### `DELETE /skills/{skill_id}` - Delete a skill

Deletes a skill. **Important:** Uses the RESTRICT pattern. If any journals are linked to this skill, the deletion will be blocked.

- **Success Response**: `204 No Content`
- **Error Responses**:
  - `404 Not Found`
  - `400 Bad Request`: "Cannot delete skill because X journal(s) are linked to it."

---

### 2. Journals Endpoints (`/journals`)

#### `POST /journals/` - Create a new journal entry

Creates a learning journal entry. Can optionally be linked to an existing skill via `skill_id`.

- **Request Body**:
  ```json
  {
    "title": "Learned Pydantic validation",
    "content": "Today I learned how Pydantic automatically validates request bodies.",
    "skill_id": 1
  }
  ```
- **Success Response**: `201 Created`
- **Error Responses**:
  - `422 Unprocessable Entity` (invalid data types/length)
  - `400 Bad Request` (if `skill_id` is provided but the skill does not exist).

#### `GET /journals/` - List all journals

Returns a list of all journal entries.

- **Query Parameters**:
  - `skill_id` (optional, integer): Filter journals linked to a specific skill (e.g., `?skill_id=1`).
- **Success Response**: `200 OK`

#### `GET /journals/{journal_id}` - Get a specific journal

- **Path Parameters**: `journal_id` (integer)
- **Success Response**: `200 OK`
- **Error Responses**: `404 Not Found`

#### `PUT /journals/{journal_id}` - Update a journal

Partially or fully updates a journal entry. If you change the `skill_id`, it will validate that the new skill exists.

- **Success Response**: `200 OK`
- **Error Responses**: `404 Not Found`, `400 Bad Request` (invalid skill_id), `422 Unprocessable Entity`.

#### `DELETE /journals/{journal_id}` - Delete a journal

Deletes a journal entry. This does not affect the linked skill.

- **Success Response**: `204 No Content`
- **Error Responses**: `404 Not Found`

---

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

```

---

### Phase 6 Assessment (Final Review)

You have the README, you have the `.gitignore` strategy, and you are ready for GitHub!

To officially close out this project and move to the next major topic in your FastAPI journey, I need you to answer the **5 review questions** from my previous message. This ensures the logic is locked in your brain before we move on.

**Just reply with your answers to these 5 questions:**

1. **Why did we use `exclude_unset=True` in our `PUT` (update) endpoints?** What bad thing would happen if we didn't use it?
2. **Why does our `JournalCreate` schema have `skill_id: Optional[int]` instead of just `skill_id: int`?**
3. **Explain the "RESTRICT" logic we added to the `DELETE /skills/{id}` endpoint.** Why did we check the `JOURNALS_DB` before deleting the skill?
4. **What is the purpose of the `db.py` file?** Why didn't we just keep the `SKILLS_DB` dictionary inside `routers/skills.py`?
5. **If a client sends a JSON request with `"rating": 15` to `POST /skills/`, what status code will FastAPI return automatically, and why?**

Once you answer these, you will have officially mastered this consolidation project, and we will plan our next big learning step!
```
# skill-tracker-api
# skill-tracker-api
