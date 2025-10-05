from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router

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

# Health check endpoint
@app.get("/", tags=["health"])
async def root():
    """API health check endpoint"""
    return {
        "message": "Adaptive Learning Roadmap API is running",
        "version": "1.0.0",
        "status": "healthy"
    }