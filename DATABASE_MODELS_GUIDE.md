# FitForge Database Models Guide

Complete guide for User and Plan models with database setup.

---

## 📋 Database Schema

### User Model
```python
class User(Base):
    __tablename__ = "users"

    id: int                    # Primary key (auto-increment)
    name: str                  # User's full name
    email: str                 # Unique email (indexed)
    hashed_password: str       # Bcrypt hashed password
    created_at: datetime       # Account creation timestamp

    # Relationships
    plans: List[Plan]          # User's fitness plans
    workouts: List[Workout]    # User's workouts
    runs: List[Run]           # User's running sessions
```

### Plan Model
```python
class Plan(Base):
    __tablename__ = "plans"

    id: int                    # Primary key (auto-increment)
    user_id: int               # Foreign key to User (CASCADE delete)
    goals: str                 # Text description of fitness goals
    routine_json: dict         # JSON object with workout routine
    created_at: datetime       # Plan creation timestamp

    # Relationships
    user: User                 # Associated user
```

---

## 🗄️ Database Setup (db.py)

### Key Features:
- ✅ **Environment-based configuration** - DATABASE_URL from .env
- ✅ **Connection pooling** - pool_pre_ping for reliability
- ✅ **SQLAlchemy 2.0** - Modern declarative style with Mapped types
- ✅ **Auto-close sessions** - get_db() dependency with cleanup
- ✅ **Debug mode** - SQL echo when DEBUG=true

### Configuration:
```python
# .env file
DATABASE_URL=postgresql://admin:admin@localhost:5432/fitforge
DEBUG=false
```

### Initialize Database:
```bash
# Create all tables
python -m app.scripts.create_db

# Or in Python
from app.db import create_tables
create_tables()
```

---

## 📊 Models Files

### models.py
Located at: `app/models.py`

**Models included:**
1. ✅ **User** - Authentication and profile (with hashed_password)
2. ✅ **Plan** - Fitness plans with JSON routines
3. ✅ **Exercise** - Exercise catalog
4. ✅ **Workout** - Workout sessions
5. ✅ **Run** - Running activity tracking

### db.py
Located at: `app/db.py`

**Functions:**
- `get_db()` - FastAPI dependency for database sessions
- `create_tables()` - Create all tables
- `drop_tables()` - Drop all tables (dev only)

**Configuration:**
- Loads environment variables from .env
- Creates SQLAlchemy engine with connection pooling
- Provides Base class for all models

---

## 💻 Usage Examples

### 1. Create a User with Hashed Password

```python
from passlib.context import CryptContext
from app.models import User
from app.db import SessionLocal

# Setup password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = SessionLocal()

# Create user
user = User(
    name="Jane Smith",
    email="jane@example.com",
    hashed_password=pwd_context.hash("MySecurePassword123!"),
)

db.add(user)
db.commit()
db.refresh(user)
db.close()
```

### 2. Create a Fitness Plan with JSON Routine

```python
from app.models import Plan

db = SessionLocal()

# Define workout routine as JSON
routine = {
    "frequency": "4 days per week",
    "duration": "60 minutes",
    "exercises": [
        {
            "name": "Squats",
            "sets": 4,
            "reps": 8,
            "weight_kg": 80,
            "rest_seconds": 90
        },
        {
            "name": "Bench Press",
            "sets": 4,
            "reps": 8,
            "weight_kg": 60,
            "rest_seconds": 120
        }
    ],
    "cardio": {
        "type": "cycling",
        "duration_minutes": 20,
        "intensity": "moderate"
    }
}

# Create plan
plan = Plan(
    user_id=user.id,
    goals="Build muscle and improve cardiovascular fitness",
    routine_json=routine
)

db.add(plan)
db.commit()
db.close()
```

### 3. Query User with Plans

```python
from app.models import User

db = SessionLocal()

# Get user with all plans
user = db.query(User).filter(User.email == "jane@example.com").first()

print(f"User: {user.name}")
print(f"Plans: {len(user.plans)}")

for plan in user.plans:
    print(f"  - {plan.goals}")
    print(f"    Exercises: {len(plan.routine_json['exercises'])}")

db.close()
```

### 4. Authenticate User

```python
def authenticate_user(email: str, password: str):
    db = SessionLocal()

    user = db.query(User).filter(User.email == email).first()
    db.close()

    if not user:
        return None

    if not pwd_context.verify(password, user.hashed_password):
        return None

    return user
```

---

## 🔐 Password Hashing

### Install Dependencies:
```bash
pip install passlib[bcrypt]
```

### Setup:
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
hashed = pwd_context.hash("MyPassword123")

# Verify password
is_valid = pwd_context.verify("MyPassword123", hashed)
```

---

## 📦 JSON Routine Structure

Example routine_json structure for Plan model:

```json
{
  "frequency": "3-5 days per week",
  "duration": "45-60 minutes",
  "program_type": "strength_training",
  "exercises": [
    {
      "name": "Squats",
      "type": "compound",
      "muscle_groups": ["legs", "glutes"],
      "sets": 4,
      "reps": 8,
      "weight_kg": 100,
      "rest_seconds": 120,
      "notes": "Focus on depth"
    },
    {
      "name": "Bench Press",
      "type": "compound",
      "muscle_groups": ["chest", "triceps"],
      "sets": 4,
      "reps": 8,
      "weight_kg": 80,
      "rest_seconds": 120
    }
  ],
  "cardio": {
    "type": "HIIT",
    "duration_minutes": 20,
    "days": ["Monday", "Wednesday", "Friday"],
    "intensity": "high"
  },
  "rest_days": ["Sunday"],
  "progression": {
    "increase_weight_by": 2.5,
    "every_n_weeks": 2
  }
}
```

---

## 🗃️ Database Migrations (Optional - Alembic)

### Setup Alembic:
```bash
pip install alembic
alembic init alembic
```

### Configure:
Edit `alembic.ini`:
```ini
sqlalchemy.url = postgresql://admin:admin@localhost:5432/fitforge
```

### Create Migration:
```bash
alembic revision --autogenerate -m "Add User and Plan models"
alembic upgrade head
```

---

## 🔧 FastAPI Integration

### Use in Routes:
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User, Plan

router = APIRouter()

@router.post("/users")
async def create_user(
    name: str,
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    hashed_pwd = pwd_context.hash(password)

    user = User(
        name=name,
        email=email,
        hashed_password=hashed_pwd
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"id": user.id, "email": user.email}

@router.get("/users/{user_id}/plans")
async def get_user_plans(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.plans
```

---

## 📋 Complete Setup Checklist

1. ✅ **Install dependencies**
   ```bash
   pip install sqlalchemy psycopg2-binary python-dotenv passlib[bcrypt]
   ```

2. ✅ **Configure environment**
   ```bash
   # .env
   DATABASE_URL=postgresql://admin:admin@localhost:5432/fitforge
   ```

3. ✅ **Start PostgreSQL**
   ```bash
   docker compose up -d
   ```

4. ✅ **Create tables**
   ```bash
   python -m app.scripts.create_db
   ```

5. ✅ **Verify tables**
   ```bash
   docker exec fitforge-postgres psql -U admin -d fitforge -c "\dt"
   ```

   Expected output:
   ```
   users
   plans
   exercises
   workouts
   runs
   ```

---

## 🎯 Summary

✅ **User Model:** Includes id, name, email, hashed_password, created_at
✅ **Plan Model:** Includes id, user_id, goals, routine_json, created_at
✅ **Database Setup:** Environment-based configuration with connection pooling
✅ **Password Security:** Bcrypt hashing with passlib
✅ **JSON Storage:** Flexible routine_json field for workout data
✅ **Relationships:** User ↔ Plans with cascade delete
✅ **FastAPI Ready:** get_db() dependency for route injection

**All models are production-ready with proper types, indexes, and relationships!** 🚀

---

## 📚 Additional Resources

- **Example Code:** `MODELS_USAGE_EXAMPLE.py`
- **Database Setup:** `app/db.py`
- **Models:** `app/models.py`
- **Environment Guide:** `ENV_COMMANDS.md`
- **Verification:** Run `./verify.sh` to check everything
