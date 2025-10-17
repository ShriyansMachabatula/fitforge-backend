from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import health, test
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title="FitForge Backend API",
    description="Fitness tracking and workout management API",
    version="1.0.0"
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

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "FitForge Backend API",
        "docs": "/docs",
        "health": "/api/health",
        "test": "/api/test"
    }