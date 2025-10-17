"""
Database seeding script for FitForge.
Populates the database with sample data for development and testing.

Usage:
    python app/seed.py
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import User, Exercise, Workout, Run, ExerciseCategory


def seed_database(force=False):
    """Seed the database with sample data"""
    db: Session = SessionLocal()

    try:
        print("🌱 Starting database seeding...\n")

        # Check if data already exists
        existing_users = db.query(User).count()
        if existing_users > 0 and not force:
            print(f"⚠️  Database already contains {existing_users} user(s).")
            print("   Use --force to add more data anyway")
            print("   Use --clear to delete existing data first")
            return

        # Create sample user
        print("👤 Creating sample user...")
        user = User(
            email="john.doe@example.com",
            name="John Doe"
        )
        db.add(user)
        db.flush()  # Flush to get the user ID
        print(f"   ✅ Created user: {user.name} ({user.email})")

        # Create sample exercises
        print("\n💪 Creating sample exercises...")

        exercise1 = Exercise(
            name="Bench Press",
            category=ExerciseCategory.STRENGTH,
            description="A strength training exercise for the chest, shoulders, and triceps. Lie on a bench and press a weighted barbell upward."
        )
        db.add(exercise1)
        print(f"   ✅ Created exercise: {exercise1.name} ({exercise1.category.value})")

        exercise2 = Exercise(
            name="5K Run",
            category=ExerciseCategory.CARDIO,
            description="A 5-kilometer running workout for cardiovascular endurance and stamina building."
        )
        db.add(exercise2)
        print(f"   ✅ Created exercise: {exercise2.name} ({exercise2.category.value})")

        db.flush()

        # Create sample workout
        print("\n🏋️  Creating sample workout...")
        workout_date = datetime.utcnow() - timedelta(days=1)
        workout = Workout(
            user_id=user.id,
            date=workout_date,
            notes="Great chest day! Increased weight by 5 lbs on bench press. Felt strong and energized."
        )
        db.add(workout)
        print(f"   ✅ Created workout for {user.name} on {workout_date.strftime('%Y-%m-%d')}")

        # Create sample run
        print("\n🏃 Creating sample run...")
        run_date = datetime.utcnow() - timedelta(days=2)
        run = Run(
            user_id=user.id,
            distance_km=5.2,
            duration_seconds=1680,  # 28 minutes
            date=run_date
        )
        db.add(run)

        # Calculate pace
        pace_per_km = run.duration_seconds / run.distance_km / 60  # minutes per km
        print(f"   ✅ Created run: {run.distance_km}km in {run.duration_seconds // 60} minutes ({pace_per_km:.2f} min/km)")

        # Commit all changes
        db.commit()

        print("\n" + "="*50)
        print("✅ Database seeding completed successfully!")
        print("="*50)

        # Print summary
        print("\n📊 Summary:")
        print(f"   • Users: {db.query(User).count()}")
        print(f"   • Exercises: {db.query(Exercise).count()}")
        print(f"   • Workouts: {db.query(Workout).count()}")
        print(f"   • Runs: {db.query(Run).count()}")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Error during seeding: {e}")
        print("   All changes have been rolled back.")
        sys.exit(1)

    finally:
        db.close()
        print("\n🔒 Database connection closed.")


def clear_database():
    """Clear all data from the database (DESTRUCTIVE!)"""
    db: Session = SessionLocal()

    try:
        response = input("⚠️  This will DELETE all data from the database. Are you sure? (yes/no): ")
        if response.lower() != "yes":
            print("❌ Operation cancelled.")
            return

        print("🗑️  Clearing database...")

        # Delete in correct order (respecting foreign keys)
        runs_deleted = db.query(Run).delete()
        workouts_deleted = db.query(Workout).delete()
        exercises_deleted = db.query(Exercise).delete()
        users_deleted = db.query(User).delete()

        db.commit()

        print(f"✅ Deleted {runs_deleted} runs")
        print(f"✅ Deleted {workouts_deleted} workouts")
        print(f"✅ Deleted {exercises_deleted} exercises")
        print(f"✅ Deleted {users_deleted} users")
        print("\n✅ Database cleared successfully!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error clearing database: {e}")
        sys.exit(1)

    finally:
        db.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Database seeding script")
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear all data from the database (DESTRUCTIVE!)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force seeding even if data already exists"
    )

    args = parser.parse_args()

    if args.clear:
        clear_database()
    else:
        seed_database(force=args.force)
