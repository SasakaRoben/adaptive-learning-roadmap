# 🚀 Deployment Guide

This guide provides multiple deployment options for the Adaptive Learning Roadmap application. Choose the method that best fits your needs.

## 📋 Table of Contents

- [Quick Start with Docker Compose](#quick-start-with-docker-compose)
- [Deploy to Railway + Vercel](#deploy-to-railway--vercel)
- [Deploy to Render](#deploy-to-render)
- [Deploy with Docker](#deploy-with-docker)
- [Environment Variables](#environment-variables)
- [Database Setup](#database-setup)
- [Troubleshooting](#troubleshooting)

---

## 🐳 Quick Start with Docker Compose

The easiest way to run the entire application locally.

### Prerequisites
- Docker and Docker Compose installed
- At least 2GB of free RAM

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/SasakaRoben/adaptive-learning-roadmap.git
   cd adaptive-learning-roadmap
   ```

2. **Create environment file**
   ```bash
   cp .env.production.example .env
   ```
   Edit `.env` and set your values, especially:
   - `SECRET_KEY` (generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
   - `GEMINI_API_KEY` (optional, for AI chatbot features)

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Database: localhost:5432

5. **Stop services**
   ```bash
   docker-compose down
   ```

---

## 🚂 Deploy to Railway + Vercel

Split deployment: Backend on Railway, Frontend on Vercel, Database on Supabase.

### Backend on Railway

1. **Create Railway Account**
   - Sign up at https://railway.app

2. **Create New Project**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

3. **Configure Environment Variables**
   Add these variables in Railway dashboard:
   ```
   SECRET_KEY=<generate-random-32-char-string>
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   GEMINI_API_KEY=<your-gemini-api-key>
   GEMINI_MODEL=gemini-1.5-flash
   DATABASE_URL=<your-supabase-connection-string>
   CORS_ORIGINS=https://your-frontend.vercel.app
   ```

4. **Deploy**
   - Railway will automatically detect the Procfile and deploy
   - Note your Railway URL (e.g., `https://your-app.up.railway.app`)

### Database on Supabase

1. **Create Supabase Project**
   - Sign up at https://supabase.com
   - Create a new project

2. **Get Connection String**
   - Go to Settings → Database
   - Copy the "Connection string" (URI format)
   - Use this as `DATABASE_URL` in Railway

3. **Run SQL Migrations**
   ```bash
   # Install psql if needed
   psql "<YOUR_SUPABASE_CONNECTION_STRING>" -f backend/sql/learning_tables.sql
   psql "<YOUR_SUPABASE_CONNECTION_STRING>" -f backend/sql/assessment_schema.sql
   psql "<YOUR_SUPABASE_CONNECTION_STRING>" -f backend/sql/learning_resources.sql
   psql "<YOUR_SUPABASE_CONNECTION_STRING>" -f backend/sql/user_registration.sql
   ```

### Frontend on Vercel

1. **Create Vercel Account**
   - Sign up at https://vercel.com

2. **Import Project**
   - Click "New Project" → Import from GitHub
   - Select your repository

3. **Configure Build Settings**
   - Framework Preset: Other
   - Root Directory: `frontend`
   - Build Command: (leave empty)
   - Output Directory: `.`

4. **Set Environment Variable**
   ```
   API_URL=https://your-railway-app.up.railway.app/api
   ```

5. **Deploy**
   - Vercel will automatically deploy your frontend
   - Note your Vercel URL

6. **Update CORS**
   - Go back to Railway
   - Update `CORS_ORIGINS` environment variable with your Vercel URL
   - Redeploy the backend

---

## 🎨 Deploy to Render

All-in-one platform for backend, database, and static frontend.

### Prerequisites
- Render account (https://render.com)
- GitHub repository

### Using Blueprint (Automatic)

1. **Push render.yaml to your repo**
   - The `render.yaml` file is already included

2. **Create New Blueprint**
   - Go to Render Dashboard
   - Click "New" → "Blueprint"
   - Connect your GitHub repository

3. **Configure Environment Variables**
   - Render will prompt for required variables
   - Add your `SECRET_KEY` and `GEMINI_API_KEY`

4. **Deploy**
   - Render will create all services automatically
   - Wait for deployment to complete

### Manual Setup

#### Backend Service

1. **Create Web Service**
   - New → Web Service
   - Connect GitHub repository
   - Name: `adaptive-learning-backend`
   - Environment: Python 3
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. **Environment Variables**
   Add all required variables (see [Environment Variables](#environment-variables))

#### Database

1. **Create PostgreSQL Database**
   - New → PostgreSQL
   - Name: `adaptive-learning-db`
   - Note the internal connection string

2. **Connect to Backend**
   - Copy the internal database URL
   - Add to backend as `DATABASE_URL` environment variable

3. **Run Migrations**
   - Use Render shell or connect via psql to run SQL files

#### Static Site (Frontend)

1. **Create Static Site**
   - New → Static Site
   - Connect GitHub repository
   - Root Directory: `frontend`
   - Build Command: (leave empty)
   - Publish Directory: `.`

2. **Set API URL**
   - Create a file `frontend/js/env.js`:
     ```javascript
     window.ENV = { API_URL: 'https://your-backend.onrender.com/api' };
     ```
   - Include it before `config.js` in your HTML files

---

## 🐋 Deploy with Docker

Deploy to any Docker-compatible host (AWS ECS, Google Cloud Run, DigitalOcean, etc.)

### Build Docker Image

```bash
docker build -t adaptive-learning-roadmap .
```

### Run Container

```bash
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:pass@host:5432/dbname" \
  -e SECRET_KEY="your-secret-key" \
  -e GEMINI_API_KEY="your-api-key" \
  -e CORS_ORIGINS="https://yourdomain.com" \
  adaptive-learning-roadmap
```

### Push to Registry

```bash
# Tag for your registry
docker tag adaptive-learning-roadmap your-registry/adaptive-learning-roadmap:latest

# Push
docker push your-registry/adaptive-learning-roadmap:latest
```

---

## 🔐 Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | JWT secret key (32+ chars) | Generate with Python command below |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration | `30` |
| `GEMINI_API_KEY` | Google Gemini API key for AI features | None |
| `GEMINI_MODEL` | Gemini model to use | `gemini-1.5-flash` |
| `CORS_ORIGINS` | Comma-separated allowed origins | Dev origins only |

### Generate SECRET_KEY

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Alternative Database Variables

Instead of `DATABASE_URL`, you can use individual parameters:

```bash
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=adaptive_learning
DATABASE_USER=postgres
DATABASE_PASSWORD=yourpassword
```

---

## 🗄️ Database Setup

### SQL Migration Order

Run these SQL files in order to set up the database:

1. `backend/sql/learning_tables.sql` - Core learning tables
2. `backend/sql/assessment_schema.sql` - Assessment system
3. `backend/sql/learning_resources.sql` - Learning resources
4. `backend/sql/user_registration.sql` - User management

### Using psql

```bash
psql "$DATABASE_URL" -f backend/sql/learning_tables.sql
psql "$DATABASE_URL" -f backend/sql/assessment_schema.sql
psql "$DATABASE_URL" -f backend/sql/learning_resources.sql
psql "$DATABASE_URL" -f backend/sql/user_registration.sql
```

### Using PostgreSQL Client

Connect to your database and run each SQL file manually.

---

## 🔧 Troubleshooting

### Backend Issues

**Database Connection Fails**
- Check `DATABASE_URL` format: `postgresql://user:pass@host:port/dbname`
- Verify database server is running and accessible
- Check firewall rules and security groups

**CORS Errors**
- Add your frontend URL to `CORS_ORIGINS` environment variable
- Format: `CORS_ORIGINS=https://domain1.com,https://domain2.com`
- Restart backend after updating

**Port Already in Use**
- Change port: `uvicorn app.main:app --port 8001`
- Or kill process using the port

### Frontend Issues

**API Not Connecting**
- Check browser console for errors
- Verify `API_URL` in config.js
- Ensure backend is running and accessible
- Check CORS settings on backend

**Static Files Not Loading**
- Verify file paths are correct
- Check web server configuration
- Clear browser cache

### Docker Issues

**Container Won't Start**
- Check logs: `docker-compose logs backend`
- Verify environment variables are set
- Ensure database is ready before backend starts

**Database Connection Refused**
- Wait for database to be fully ready
- Check database health: `docker-compose ps`
- Verify internal Docker network connectivity

### Platform-Specific

**Railway**
- Check build logs in Railway dashboard
- Verify Procfile is present and correct
- Ensure all environment variables are set

**Vercel**
- Check deployment logs
- Verify build settings match requirements
- Ensure `vercel.json` is properly configured

**Render**
- Check service logs
- Verify start command includes `cd backend`
- Ensure health check endpoint is accessible

---

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review logs for error messages

## 🔄 Updates

To update your deployment:

1. Pull latest changes
2. Rebuild Docker images (if using Docker)
3. Run any new database migrations
4. Restart services
5. Clear browser cache

---

## 📝 Notes

- Always use HTTPS in production
- Keep your `SECRET_KEY` secure and never commit it
- Regularly backup your database
- Monitor application logs
- Set up error tracking (Sentry, etc.)
- Configure proper database backups

---

**Happy Deploying! 🎉**
