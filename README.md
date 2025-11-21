# adaptive-learning-roadmap

**Project:** Adaptive Learning Roadmap — a full-stack app that delivers personalized learning paths, progress tracking, assessments, and AI-powered recommendations.

**What it does**
- **Personalized Roadmaps:** Presents topics organized by level and prerequisites.
- **Assessments:** Weighted scoring to place learners and measure progress.
- **Resources:** Curated learning resources linked to topics (one resource per topic).
- **AI Assistance:** Chatbot/quiz generation integrated with Google Gemini (configurable via env).

**Tech Stack**
- **Backend:** `FastAPI`, Python (Pydantic, Uvicorn)
- **Database:** `PostgreSQL` (schemas and SQL seeds are in `backend/sql/`)
- **ORM/DB driver:** `psycopg[binary]` (psycopg v3)
- **Frontend:** Static HTML/CSS/Vanilla JS in `frontend/`
- **AI:** `google-generativeai` (Gemini) used in `app/services/chatbot.py`

**Repository Layout**
- **`backend/`**: FastAPI app, CRUD, schemas, services, and SQL files.
- **`frontend/`**: Static pages and JS under `frontend/js/` and styles under `frontend/css/`.
- **`deploy/`**: Deployment notes and instructions.

**Getting Started (Local)**
- **Prerequisites:** `python 3.11+`, `postgresql` (or use Supabase), `node` not required for static frontend.
- **Install backend deps:**
	```bash
	pip install -r requirements.txt
	```
- **Run backend locally:**
	```bash
	# from repo root
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
	# or from backend/ directory:
	# cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
	```
- **Serve frontend locally:** Use VSCode Live Server or a simple static server:
	```bash
	# from frontend/ directory
	python -m http.server 5500
	```

**Environment Variables**
- **Backend `.env` (example in `backend/.env.example`)**
	- `DATABASE_URL` : PostgreSQL connection string
	- `SECRET_KEY` : JWT secret
	- `GEMINI_API_KEY` : (optional) Gemini API key for chatbot
	- `GEMINI_MODEL` : (optional) model name, e.g. `gemini-1.5-flash`

**Database (SQL files)**
- Schema and seed scripts are in `backend/sql/`.
- Run them with `psql` or the Supabase SQL editor. Example:
	```bash
	psql "<DATABASE_URL>" -f backend/sql/learning_tables.sql
	psql "<DATABASE_URL>" -f backend/sql/assessment_schema.sql
	psql "<DATABASE_URL>" -f backend/sql/learning_resources.sql
	psql "<DATABASE_URL>" -f backend/sql/user_registration.sql
	```

**Deployment (Option A — recommended)**
- **Frontend:** Deploy static site on `Vercel` (or Netlify/GitHub Pages). Set `API_URL` env in Vercel to your backend URL.
- **Backend:** Deploy on `Railway` (or Fly). Use `Procfile`/`start.sh` or Docker. Provide environment variables listed above.
- **Database:** Use Supabase (free tier) or Railway Postgres and run the SQL scripts.

**Troubleshooting & Notes**
- If Vercel reports "No fastapi entrypoint found", the repo contains `api/index.py` to expose the FastAPI app for Vercel serverless functions. If you prefer a split deploy (frontend static + backend on Railway), you can remove the serverless entrypoint.
- For Python 3.13 compatibility and buildpacks, a top-level `requirements.txt` is included for build detection.
- Avoid committing real secrets — use platform secrets / environment variables.

**Contributing**
- Fork the repo, create a topic branch, open a pull request with tests or a clear description of changes.

**License**
- MIT (or adjust as appropriate)

---
For detailed deployment steps see `deploy/README.md`.
