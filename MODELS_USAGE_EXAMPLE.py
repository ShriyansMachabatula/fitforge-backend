"""
Example usage of User and Plan models
Shows how to create users, hash passwords, and create plans
"""

from datetime import datetime
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import User, Plan

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def create_user_example():
    """Example: Create a new user with hashed password"""
    db: Session = SessionLocal()

    try:
        # Create user with hashed password
        user = User(
            name="John Doe",
            email="john.doe@fitforge.com",
            hashed_password=hash_password("SecurePassword123!"),
            created_at=datetime.utcnow()
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        print(f"✅ Created user: {user}")
        return user

    except Exception as e:
        db.rollback()
        print(f"❌ Error creating user: {e}")
        raise
    finally:
        db.close()


def create_plan_example(user_id: int):
    """Example: Create a fitness plan for a user"""
    db: Session = SessionLocal()

    try:
        # Define the routine as a JSON structure
        routine = {
            "frequency": "3 days per week",
            "duration": "45 minutes",
            "exercises": [
                {
                    "name": "Squats",
                    "sets": 3,
                    "reps": 10,
                    "rest_seconds": 90
                },
                {
                    "name": "Bench Press",
                    "sets": 3,
                    "reps": 8,
                    "rest_seconds": 120
                },
                {
                    "name": "Deadlifts",
                    "sets": 3,
                    "reps": 5,
                    "rest_seconds": 180
                }
            ],
            "cardio": {
                "type": "running",
                "duration_minutes": 20,
                "days": ["Monday", "Wednesday", "Friday"]
            }
        }

        # Create plan
        plan = Plan(
            user_id=user_id,
            goals="Build strength and muscle mass. Lose 10 pounds in 3 months.",
            routine_json=routine,
            created_at=datetime.utcnow()
        )

        db.add(plan)
        db.commit()
        db.refresh(plan)

        print(f"✅ Created plan: {plan}")
        print(f"   Routine: {plan.routine_json}")
        return plan

    except Exception as e:
        db.rollback()
        print(f"❌ Error creating plan: {e}")
        raise
    finally:
        db.close()


def get_user_with_plans(user_id: int):
    """Example: Query user with all their plans"""
    db: Session = SessionLocal()

    try:
        user = db.query(User).filter(User.id == user_id).first()

        if user:
            print(f"👤 User: {user.name} ({user.email})")
            print(f"   Created: {user.created_at}")
            print(f"   Plans: {len(user.plans)}")

            for plan in user.plans:
                print(f"   - Plan {plan.id}: {plan.goals}")
                print(f"     Routine exercises: {len(plan.routine_json.get('exercises', []))}")

        return user

    finally:
        db.close()


def authenticate_user(email: str, password: str):
    """Example: Authenticate a user"""
    db: Session = SessionLocal()

    try:
        user = db.query(User).filter(User.email == email).first()

        if not user:
            print("❌ User not found")
            return None

        if not verify_password(password, user.hashed_password):
            print("❌ Invalid password")
            return None

        print(f"✅ User authenticated: {user.email}")
        return user

    finally:
        db.close()


if __name__ == "__main__":
    print("🏋️ FitForge Models Usage Example\n")

    # Example 1: Create a user
    print("1. Creating user...")
    user = create_user_example()

    # Example 2: Create a plan for the user
    print("\n2. Creating plan...")
    plan = create_plan_example(user.id)

    # Example 3: Query user with plans
    print("\n3. Querying user with plans...")
    get_user_with_plans(user.id)

    # Example 4: Authenticate user
    print("\n4. Authenticating user...")
    authenticate_user("john.doe@fitforge.com", "SecurePassword123!")
    authenticate_user("john.doe@fitforge.com", "WrongPassword")
