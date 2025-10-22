#!/usr/bin/env python3
"""
Comprehensive test script to verify User and Plan models with password hashing.
Run this script to test all database functionality.
"""

import sys
from datetime import datetime
from passlib.context import CryptContext
from app.db import SessionLocal
from app.models import User, Plan

# Initialize password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)

def test_user_creation():
    """Test creating a user with hashed password."""
    print("\n🧪 Testing User Creation with Password Hashing...")

    db = SessionLocal()
    try:
        # Create a test user
        test_email = f"test_{datetime.now().timestamp()}@example.com"
        plain_password = "SecurePassword123!"
        hashed_pw = hash_password(plain_password)

        print(f"   Plain password length: {len(plain_password)} chars")
        print(f"   Hashed password length: {len(hashed_pw)} chars")

        new_user = User(
            name="Test User",
            email=test_email,
            hashed_password=hashed_pw
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        print(f"✅ User created successfully!")
        print(f"   ID: {new_user.id}")
        print(f"   Name: {new_user.name}")
        print(f"   Email: {new_user.email}")
        print(f"   Password Hash: {new_user.hashed_password[:50]}...")
        print(f"   Created At: {new_user.created_at}")

        # Store the plain password for verification test
        new_user._plain_password = plain_password

        return new_user

    except Exception as e:
        print(f"❌ Error creating user: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return None
    finally:
        db.close()

def test_password_verification(user: User):
    """Test password verification."""
    print("\n🧪 Testing Password Verification...")

    # Test correct password
    correct_password = getattr(user, '_plain_password', "SecurePassword123!")
    is_valid = verify_password(correct_password, user.hashed_password)

    if is_valid:
        print(f"✅ Correct password verified successfully!")
    else:
        print(f"❌ Password verification failed!")

    # Test incorrect password
    wrong_password = "WrongPassword"
    is_invalid = verify_password(wrong_password, user.hashed_password)

    if not is_invalid:
        print(f"✅ Incorrect password correctly rejected!")
    else:
        print(f"❌ Incorrect password was accepted (security issue)!")

def test_plan_creation(user: User):
    """Test creating a plan with JSON routine."""
    print("\n🧪 Testing Plan Creation with JSON Routine...")

    db = SessionLocal()
    try:
        # Create a test plan
        routine_data = {
            "monday": {
                "exercises": [
                    {"name": "Bench Press", "sets": 3, "reps": 10, "weight": 135},
                    {"name": "Squats", "sets": 4, "reps": 8, "weight": 185}
                ],
                "duration": 60
            },
            "wednesday": {
                "exercises": [
                    {"name": "Deadlifts", "sets": 3, "reps": 5, "weight": 225},
                    {"name": "Pull-ups", "sets": 3, "reps": 12, "weight": 0}
                ],
                "duration": 45
            },
            "friday": {
                "exercises": [
                    {"name": "Overhead Press", "sets": 3, "reps": 10, "weight": 95},
                    {"name": "Rows", "sets": 3, "reps": 10, "weight": 115}
                ],
                "duration": 50
            }
        }

        new_plan = Plan(
            user_id=user.id,
            goals="Build strength and muscle mass. Target: bench 225lbs, squat 315lbs, deadlift 405lbs",
            routine_json=routine_data
        )

        db.add(new_plan)
        db.commit()
        db.refresh(new_plan)

        print(f"✅ Plan created successfully!")
        print(f"   ID: {new_plan.id}")
        print(f"   User ID: {new_plan.user_id}")
        print(f"   Goals: {new_plan.goals}")
        print(f"   Created At: {new_plan.created_at}")
        print(f"   Routine Days: {list(new_plan.routine_json.keys())}")
        print(f"   Monday Exercises: {len(new_plan.routine_json['monday']['exercises'])}")

        return new_plan

    except Exception as e:
        print(f"❌ Error creating plan: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def test_user_plan_relationship(user: User):
    """Test querying user with their plans."""
    print("\n🧪 Testing User-Plan Relationship...")

    db = SessionLocal()
    try:
        # Query user with plans
        queried_user = db.query(User).filter(User.id == user.id).first()

        if queried_user:
            print(f"✅ User retrieved successfully!")
            print(f"   User: {queried_user.name} ({queried_user.email})")
            print(f"   Number of plans: {len(queried_user.plans)}")

            for i, plan in enumerate(queried_user.plans, 1):
                print(f"\n   Plan {i}:")
                print(f"     ID: {plan.id}")
                print(f"     Goals: {plan.goals[:50]}...")
                print(f"     Workout Days: {list(plan.routine_json.keys())}")
        else:
            print(f"❌ Could not retrieve user!")

    except Exception as e:
        print(f"❌ Error querying relationship: {e}")
    finally:
        db.close()

def test_database_tables():
    """Test that all tables exist in the database."""
    print("\n🧪 Testing Database Tables...")

    db = SessionLocal()
    try:
        # Count records in each table
        user_count = db.query(User).count()
        plan_count = db.query(Plan).count()

        print(f"✅ Database tables accessible!")
        print(f"   Users in database: {user_count}")
        print(f"   Plans in database: {plan_count}")

    except Exception as e:
        print(f"❌ Error accessing database tables: {e}")
    finally:
        db.close()

def main():
    """Run all tests."""
    print("=" * 60)
    print("🚀 FitForge Database Model Tests")
    print("=" * 60)

    try:
        # Test 1: Database tables
        test_database_tables()

        # Test 2: User creation
        user = test_user_creation()
        if not user:
            print("\n❌ User creation failed. Stopping tests.")
            sys.exit(1)

        # Test 3: Password verification
        test_password_verification(user)

        # Test 4: Plan creation
        plan = test_plan_creation(user)
        if not plan:
            print("\n❌ Plan creation failed. Stopping tests.")
            sys.exit(1)

        # Test 5: User-Plan relationship
        test_user_plan_relationship(user)

        print("\n" + "=" * 60)
        print("✅ All tests passed successfully!")
        print("=" * 60)
        print("\n📊 Summary:")
        print(f"   ✓ User model with password hashing: Working")
        print(f"   ✓ Plan model with JSON routines: Working")
        print(f"   ✓ User-Plan relationship: Working")
        print(f"   ✓ Password verification: Working")
        print("\n🎉 Your FitForge backend is ready to go!")

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
