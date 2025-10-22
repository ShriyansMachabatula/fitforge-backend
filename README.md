# FitForge Backend

Python backend API for FitForge - a fitness tracking and workout management platform.

## Purpose

Provides RESTful API endpoints for user authentication, workout tracking, exercise management, and fitness analytics.

## Tech Stack

- **Python** 3.11+
- **FastAPI** - Modern, fast web framework
- **PostgreSQL 16** - Database
- **SQLAlchemy 2.0** - ORM with type hints
- **Docker** - PostgreSQL containerization
- **Pydantic** - Data validation
- **Passlib + Bcrypt** - Password hashing

## Quick Start

### Automated Setup (Recommended for New Team Members)

```bash
# Clone the repository
git clone https://github.com/yourusername/fitforge-backend.git
cd fitforge-backend

# Run the automated setup script
./setup.sh
```

The setup script will:
1. ✅ Check prerequisites (Python, Docker)
2. ✅ Create virtual environment
3. ✅ Install dependencies
4. ✅ Set up environment variables
5. ✅ Start PostgreSQL in Docker
6. ✅ Initialize database tables

### Manual Setup

If you prefer to set up manually:

#### 1. Prerequisites

- Python 3.9 or higher
- Docker Desktop
- Git

#### 2. Clone and Navigate

```bash
git clone https://github.com/yourusername/fitforge-backend.git
cd fitforge-backend
```

#### 3. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 5. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env if needed (default values work for local development)
```

#### 6. Start PostgreSQL Database

```bash
docker compose up -d
```

#### 7. Initialize Database

```bash
python -m app.scripts.create_db
```

#### 8. Start Development Server

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **API Base:** http://localhost:8000
- **Interactive Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Database Models

### User
- id, name, email, hashed_password, created_at
- Relationships: workouts, runs, plans

### Plan
- id, user_id, goals, routine_json (JSON), created_at
- Stores workout routines as JSON data

### Exercise
- id, name, category, description

### Workout
- id, user_id, date, notes

### Run
- id, user_id, distance_km, duration_seconds, date

See [DATABASE_MODELS_GUIDE.md](DATABASE_MODELS_GUIDE.md) for detailed documentation.

## API Endpoints

### Health & Status
- `GET /api/health` - Health check with database status

### Test Endpoints
- `GET /api/test` - Test endpoint with user count

### Coming Soon
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/plans` - Get user's plans
- `POST /api/plans` - Create new plan

See the interactive API documentation at http://localhost:8000/docs

## Development Commands

### Running the Server

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Database Operations

```bash
# Create tables
python -m app.scripts.create_db

# Reset database (DESTRUCTIVE!)
python -m app.scripts.create_db --reset --force

# Seed with sample data
python app/seed.py --force

# Clear all data
python app/seed.py --clear
```

### Testing

```bash
# Run comprehensive model tests
python test_models.py

# Run specific test
pytest tests/test_models.py

# Test API endpoints
curl http://localhost:8000/api/health
curl http://localhost:8000/api/test
```

### Docker Commands

```bash
# Start PostgreSQL
docker compose up -d

# Stop PostgreSQL
docker compose down

# View logs
docker logs fitforge-postgres

# Access PostgreSQL shell
docker exec -it fitforge-postgres psql -U admin -d fitforge

# View database tables
docker exec -it fitforge-postgres psql -U admin -d fitforge -c "\dt"
```

## Project Structure

```
fitforge-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── db.py                # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── api/
│   │   └── routes/
│   │       ├── health.py    # Health check endpoint
│   │       └── test.py      # Test endpoints
│   └── scripts/
│       └── create_db.py     # Database initialization
├── tests/                   # Test files
├── venv/                    # Virtual environment (not in git)
├── .env                     # Environment variables (not in git)
├── .env.example             # Environment template
├── .gitignore
├── requirements.txt         # Python dependencies
├── docker-compose.yml       # PostgreSQL container config
├── setup.sh                 # Automated setup script
├── test_models.py           # Comprehensive model tests
└── README.md
```

## Environment Variables

Key environment variables in `.env`:

```bash
# Database
DATABASE_URL=postgresql://admin:admin@127.0.0.1:5432/fitforge

# Application
DEBUG=false
HOST=0.0.0.0
PORT=8000

# Security (change for production!)
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

See `.env.example` for all available options.

## Testing Your Setup

After setup, verify everything works:

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Check database connection
python -c "from app.db import engine; print('✅ Database connected!' if engine else '❌ Failed')"

# 3. Run model tests
python test_models.py

# 4. Start server
uvicorn app.main:app --reload

# 5. In another terminal, test endpoints
curl http://localhost:8000/api/health
curl http://localhost:8000/api/test
```

All tests should pass with green checkmarks! ✅

## Common Issues

### Port 5432 already in use
```bash
# Stop local PostgreSQL
brew services stop postgresql  # macOS
sudo systemctl stop postgresql  # Linux

# Or change the port in docker-compose.yml
```

### Database connection failed
```bash
# Restart PostgreSQL container
docker compose down
docker compose up -d

# Wait a few seconds, then test
docker ps | grep fitforge-postgres
```

### Import errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Bcrypt compatibility issues
```bash
# Install specific compatible version
pip uninstall bcrypt
pip install bcrypt==4.0.1
```

## Documentation

- [DATABASE_MODELS_GUIDE.md](DATABASE_MODELS_GUIDE.md) - Database models and usage
- [MODELS_USAGE_EXAMPLE.py](MODELS_USAGE_EXAMPLE.py) - Code examples
- [VERIFICATION_COMPLETE.md](VERIFICATION_COMPLETE.md) - Setup verification guide
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [GIT_WORKFLOW.md](GIT_WORKFLOW.md) - Git workflow and conventions

## Contributing

1. Read [CONTRIBUTING.md](CONTRIBUTING.md)
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Run tests: `python test_models.py`
5. Commit: `git commit -m "feat: add your feature"`
6. Push: `git push origin feature/your-feature`
7. Create a Pull Request

See [GIT_WORKFLOW.md](GIT_WORKFLOW.md) for detailed Git conventions.

## Branch Strategy

- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - Feature development branches
- `bugfix/*` - Bug fix branches
- `hotfix/*` - Emergency production fixes

## Team Setup Checklist

For new team members:

- [ ] Install Python 3.9+
- [ ] Install Docker Desktop
- [ ] Clone repository
- [ ] Run `./setup.sh`
- [ ] Verify with `python test_models.py`
- [ ] Review `CONTRIBUTING.md`
- [ ] Set up IDE (VS Code recommended)
- [ ] Install recommended extensions (Python, Pylance, Docker)

## Support

If you encounter issues:

1. Check [Common Issues](#common-issues) section
2. Review [VERIFICATION_COMPLETE.md](VERIFICATION_COMPLETE.md)
3. Check existing GitHub issues
4. Create a new issue with:
   - Error message
   - Steps to reproduce
   - Environment details (OS, Python version)

## License

[Add your license here]

## Authors

FitForge Team

---

**Ready to build?** Run `./setup.sh` and start coding! 🚀
