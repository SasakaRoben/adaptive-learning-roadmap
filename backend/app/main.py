from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router
from app.api.assessment import router as assessment_router
from app.api.learning_path import router as learning_path_router

app = FastAPI(
    title="Adaptive Learning Roadmap API",
    description="Backend API for personalized learning roadmaps with progress tracking and AI recommendations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration - allows frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(assessment_router)
app.include_router(learning_path_router)

# Health check endpoint
@app.get("/", tags=["health"])
async def root():
    """API health check endpoint"""
    return {
        "message": "Adaptive Learning Roadmap API is running",
        "version": "1.0.0",
        "status": "healthy"
    }