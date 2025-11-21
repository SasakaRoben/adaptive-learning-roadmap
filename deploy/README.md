# Deployment Guide 	6 Option A (Frontend on Vercel, Backend on Railway + Supabase Postgres)

This document explains how to deploy the Adaptive Learning Roadmap app using a split-hosting approach:
- Static frontend deployed to Vercel (or Netlify / GitHub Pages)
- Backend (FastAPI) deployed to Railway (or Fly) with a PostgreSQL database hosted on Supabase (or Railway Postgres)

This guide assumes you have a GitHub repo with the project and are using the `main` branch.

## 1. Prepare the backend

- Ensure `backend/requirements.txt` is up-to-date (it includes `uvicorn[standard]`).
- Add a `Procfile` in the repository root (created here) containing the Uvicorn start command that reads `$PORT`.

Procfile (already added to repo):
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## 2. Create a Postgres database (Supabase)

1. Sign up at https://supabase.com and create a new project (free tier available).
2. In the Supabase project, open `API` 	6 copy the `Connection string (Database URL)`.
3. Save the value 	6 you'll use it as `DATABASE_URL` in Railway (or directly in the backend `.env` for local testing).

Run the SQL schema files to create tables (example using `psql`):
```
# Replace <DATABASE_URL> with the Supabase connection string
psql "<DATABASE_URL>" -f backend/sql/learning_tables.sql
psql "<DATABASE_URL>" -f backend/sql/assessment_schema.sql
psql "<DATABASE_URL>" -f backend/sql/learning_resources.sql
psql "<DATABASE_URL>" -f backend/sql/user_registration.sql
```

Note: Inspect the SQL files for ordering or dependency issues and run them in the proper sequence.

## 3. Deploy backend to Railway

1. Create an account at https://railway.app and choose "Deploy from GitHub".
2. Connect your GitHub account and select the repository.
3. Configure environment variables in Railway project settings:
   - `DATABASE_URL` 	6 Supabase connection string (or Railway Postgres connection string)
   - `SECRET_KEY` 	6 a secure random string for JWT
   - `GEMINI_API_KEY` 	6 if you use Gemini for chatbot features
   - `GEMINI_MODEL` 	6 optional (e.g. `gemini-1.5-flash`)
4. Set the start command (Railway usually infers this) or use the `Procfile` above.
5. Deploy 	6 Railway will build the image and start the container.

After deployment, copy the Railway URL (e.g. `https://your-api.up.railway.app`) and test the health endpoint:
```
curl https://your-api.up.railway.app/
```

## 4. Deploy frontend to Vercel (static)

1. Go to https://vercel.com and import the GitHub repository as a new project.
2. Vercel will detect there is no framework build; set the root to the repository root and deploy as a static site.
3. In Vercel project settings add an environment variable `API_URL` (optional) pointing to your Railway API base URL.
4. Update `frontend/js/config.js` to read the env var when building, or rely on `window.APP_CONFIG` fallback.

Example `frontend/js/config.js` (already in repo):
```js
window.APP_CONFIG = {
  API_URL: (typeof process !== 'undefined' && process.env && process.env.API_URL) || 'https://your-api.up.railway.app'
};
```

Note: For GitHub Pages, you can host the static files directly from the repository.

## 5. CORS

Make sure `app.main` CORS settings allow your frontend origin (Vercel domain). Update `allow_origins` or `allow_origin_regex` accordingly.

## 6. Local testing

Run the backend locally with:
```bash
# from repo root
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then open the frontend `index.html` via a static server (e.g., VSCode Live Server or `python -m http.server`).

## 7. Troubleshooting
- If migrations fail, inspect SQL errors for missing tables or constraint order.
- Use Railway/Supabase dashboards for logs and query consoles.

---
If you'd like, I can: create a `Dockerfile`, or automate the SQL run steps via a small script. Tell me which extra artifacts you'd like me to add and I will implement them.
