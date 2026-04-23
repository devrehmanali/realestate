# Real Estate Assistant Backend (FastAPI)

A professional, modular monolith backend for an AI-powered real estate assistant.

## Features
- **Modular Monolith**: Separated domains for `Properties`, `Assistant`, and `Conversations`.
- **Persistent Chat Context**: Remembers user filters (city, budget, type) across messages using PostgreSQL.
- **FastAPI Core**: High performance, type-safe validation with Pydantic, and automatic Swagger docs.
- **Database**: SQLAlchemy with support for complex filtering and relationship management.

---

## 📂 Project Structure

```text
/backend
├── app/
│   ├── core/              # Shared DB config, settings
│   ├── modules/
│   │   ├── properties/    # Property models, service, & router
│   │   ├── assistant/     # AI Logic & Intent Processor
│   │   └── conversations/ # Chat history & Context persistence
│   └── main.py            # FastAPI Entry Point
├── alembic/               # Database migrations
├── tests/                 # Pytest suite
├── .env                   # Configuration
└── requirements.txt       # Dependencies
```

---

## 🚀 Setup Instructions

### 1. Prerequisites
- Python 3.11+
- PostgreSQL server (running)

### 2. Environment Setup
Create a `.env` file in the `backend/` directory:
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/realestate
PROJECT_NAME="Real Estate Assistant"
```

### 3. Installation
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Database Migrations
Initialize and run migrations (requires PostgreSQL to be up):
```bash
# Initialize alembic if not already (completed in scaffold)
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 5. Running the API
```bash
uvicorn app.main:app --reload
```
View the interactive documentation at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🛠 API Endpoints Summary

### 🤖 Assistant
- `POST /api/v1/assistant/chat`: Core chat endpoint. Remembers context via `session_id`.

### 🏠 Properties
- `GET /api/v1/properties/`: Search listings with filters.
- `POST /api/v1/properties/seed`: Populate initial demo data.

### 💬 Conversations
- `GET /api/v1/conversations/{session_id}`: Retrieve chat history and current filter state.

---

## 💡 AI Assistant Logic (Intent Extraction)
The assistant uses an `IntentProcessor` to extract filters (Location, Price, Bedroom count) from natural language. If a key filter is missing, it dynamically generates a **Clarifying Question** before recommending properties, as per the design requirements.
