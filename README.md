# FitForge Backend

Python backend API for FitForge - a fitness tracking and workout management platform.

## Purpose

Provides RESTful API endpoints for user authentication, workout tracking, exercise management, and fitness analytics.

## Tech Stack

- Python 3.11+
- Flask/FastAPI
- PostgreSQL
- SQLAlchemy

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/fitforge-backend.git
   cd fitforge-backend
   ```
2. **Create virtual environment**
   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
3. **Install dependencies**
   pip install -r requirements.txt
4. **Set up environment variables**
   cp .env.example .env
   # Edit .env with your configuration\*\*
5. **Run database migrations**
   flask db upgrade
6. **Start development server**
   python app.py

API will be available at http://localhost:5000

# Branches

    main - Production-ready code
    develop - Integration branch for features
    feature/* - Feature development branches
