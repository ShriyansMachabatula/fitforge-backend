from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.routes import health, test, auth, plan
from app.db import engine, Base
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    Runs database initialization on startup.
    """
    # Startup: Initialize database tables
    logger.info("🚀 Starting FitForge Backend API...")
    logger.info("📊 Initializing database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables initialized successfully!")
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")

    yield

    # Shutdown: Cleanup if needed
    logger.info("👋 Shutting down FitForge Backend API...")


app = FastAPI(
    title="FitForge Backend API",
    description="Fitness tracking and workout management API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware - Configure allowed origins for frontend
origins = [
    "http://localhost:3000",      # TanStack Start dev server
    "http://localhost:5173",      # Vite default dev server
    "http://127.0.0.1:3000",      # Alternative localhost
    "http://127.0.0.1:5173",      # Alternative localhost
]

# Add origins from environment variable (comma-separated)
if os.getenv("ALLOWED_ORIGINS"):
    origins.extend(os.getenv("ALLOWED_ORIGINS").split(","))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(test.router, prefix="/api", tags=["test"])
app.include_router(auth.router, prefix="/api", tags=["authentication"])
app.include_router(plan.router, prefix="/api", tags=["plans"])

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - API status and navigation."""
    return {
        "message": "FitForge API is running",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "health": "/api/health",
            "auth": {
                "register": "/api/auth/register",
                "login": "/api/auth/login"
            },
            "plans": {
                "generate": "/api/plans/generate-plan",
                "my_plans": "/api/plans/my-plans"
            }
        }
    }