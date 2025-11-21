from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router
from app.api.assessment import router as assessment_router
from app.api.learning_path import router as learning_path_router
from app.api.chatbot import router as chatbot_router
from app.core.database import get_db_connection
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Adaptive Learning Roadmap API",
    description="Backend API for personalized learning roadmaps with progress tracking and AI recommendations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration - allows frontend to connect
# Default origins for development
default_origins = [
    "http://localhost:5500",      # Live Server default
    "http://127.0.0.1:5500",      # Live Server alternative
    "http://localhost:3000",      # React/Next.js default
    "http://localhost:8080",      # Alternative dev server
    "http://localhost",           # Docker frontend
]

# Add production origins from environment variable if set
cors_origins = default_origins.copy()
if settings.CORS_ORIGINS:
    # Parse comma-separated origins from environment
    additional_origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(',')]
    cors_origins.extend(additional_origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    # Allow any localhost/127.0.0.1 port during development
    allow_origin_regex=r"^http://(localhost|127\\.0\\.0\\.1)(:\\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(assessment_router)
app.include_router(learning_path_router)
app.include_router(chatbot_router)

# Health check endpoint
@app.get("/", tags=["health"])
async def root():
    """API health check endpoint"""
    return {
        "message": "Adaptive Learning Roadmap API is running",
        "version": "1.0.0",
        "status": "healthy"
    }


@app.on_event("startup")
async def on_startup():
    """Optional startup check to log DB connectivity without failing app startup."""
    try:
        conn = get_db_connection()
        conn.close()
        logger.info("Database connectivity check: OK")
    except Exception as e:
        # Log warning but do not crash the app; runtime routes will still attempt connections
        logger.warning(f"Database connectivity check failed: {e}")