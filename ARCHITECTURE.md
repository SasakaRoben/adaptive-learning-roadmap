# Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        DEPLOYMENT OPTIONS                                │
└─────────────────────────────────────────────────────────────────────────┘

OPTION 1: Docker Compose (Local/Self-Hosted)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                                                                           
    ┌──────────────┐         ┌──────────────┐         ┌──────────────┐  
    │   Browser    │────────▶│    Nginx     │────────▶│   Backend    │  
    │              │         │  (Frontend)  │         │   FastAPI    │  
    └──────────────┘         └──────────────┘         └──────┬───────┘  
                                    │                         │          
                                    │                         │          
                                    └─────────┬───────────────┘          
                                              │                           
                                              ▼                           
                                     ┌──────────────┐                    
                                     │  PostgreSQL  │                    
                                     │   Database   │                    
                                     └──────────────┘                    
                                                                           
    All services run in Docker containers with internal networking

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


OPTION 2: Cloud Split (Railway + Vercel + Supabase)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                                                                           
    ┌──────────────┐         ┌──────────────┐         ┌──────────────┐  
    │   Browser    │────────▶│   Vercel     │────────▶│   Railway    │  
    │              │         │  (Frontend)  │   API   │  (Backend)   │  
    └──────────────┘         └──────────────┘         └──────┬───────┘  
                                                              │          
                                                              │          
                                                              ▼          
                                                     ┌──────────────┐   
                                                     │  Supabase    │   
                                                     │ (PostgreSQL) │   
                                                     └──────────────┘   
                                                                          
    Frontend: Static hosting on Vercel (CDN)
    Backend: Docker container on Railway
    Database: Managed PostgreSQL on Supabase

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


OPTION 3: Render (All-in-One)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                                                                           
    ┌──────────────┐         ┌──────────────┐         ┌──────────────┐  
    │   Browser    │────────▶│   Render     │────────▶│   Render     │  
    │              │         │ (Static Site)│         │ (Web Service)│  
    └──────────────┘         └──────────────┘         └──────┬───────┘  
                                                              │          
                                                              │          
                                                              ▼          
                                                     ┌──────────────┐   
                                                     │   Render     │   
                                                     │ (PostgreSQL) │   
                                                     └──────────────┘   
                                                                          
    All services managed by Render (one platform)
    Deploy using render.yaml blueprint

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


CONFIGURATION FILES MAPPING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

File                      Used For
─────────────────────────────────────────────────────────────────────────
docker-compose.yml        Local Docker deployment (all-in-one)
Dockerfile                Docker image build (backend)
nginx.conf                Frontend reverse proxy config
─────────────────────────────────────────────────────────────────────────
vercel.json               Vercel frontend deployment
Procfile                  Railway/Heroku backend deployment
─────────────────────────────────────────────────────────────────────────
render.yaml               Render blueprint (all services)
─────────────────────────────────────────────────────────────────────────
.env.production.example   Environment variables template
init-db.sh                Database initialization script
quickstart.sh             Local development setup
─────────────────────────────────────────────────────────────────────────


ENVIRONMENT VARIABLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Required:
  DATABASE_URL              PostgreSQL connection string
  SECRET_KEY                JWT secret (32+ characters)

Optional:
  GEMINI_API_KEY           Google Gemini API for AI features
  GEMINI_MODEL             Model name (default: gemini-1.5-flash)
  CORS_ORIGINS             Comma-separated allowed origins
  ALGORITHM                JWT algorithm (default: HS256)
  ACCESS_TOKEN_EXPIRE_MIN  Token expiration (default: 30)

Alternative to DATABASE_URL (for local development):
  DATABASE_HOST
  DATABASE_PORT
  DATABASE_NAME
  DATABASE_USER
  DATABASE_PASSWORD


DEPLOYMENT COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Docker Compose:
  $ docker-compose up -d                # Start all services
  $ docker-compose logs -f              # View logs
  $ docker-compose down                 # Stop services

Docker Manual:
  $ docker build -t adaptive-learning . # Build image
  $ docker run -p 8000:8000 [image]     # Run container

Database Setup:
  $ ./init-db.sh                        # Initialize database

Local Development:
  $ ./quickstart.sh                     # Interactive setup

Generate Secret Key:
  $ python -c "import secrets; print(secrets.token_urlsafe(32))"


For detailed instructions, see DEPLOYMENT.md
```
