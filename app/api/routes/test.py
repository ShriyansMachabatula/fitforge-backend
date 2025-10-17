from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User
import logging

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/test")
async def test_endpoint(db: Session = Depends(get_db)):
    """
    Test endpoint to verify database connectivity and query functionality.
    Returns the count of users and details of the first user.
    """
    logger.info("🧪 Test endpoint called - querying database...")

    try:
        # Count total users
        user_count = db.query(User).count()
        logger.info(f"📊 Found {user_count} user(s) in database")

        # Get first user
        first_user = db.query(User).first()

        if first_user:
            logger.info(f"👤 First user: {first_user.name} ({first_user.email})")

            response = {
                "ok": True,
                "db_user_count": user_count,
                "first_user": {
                    "id": first_user.id,
                    "name": first_user.name,
                    "email": first_user.email
                }
            }
        else:
            logger.warning("⚠️  No users found in database")

            response = {
                "ok": True,
                "db_user_count": 0,
                "first_user": None
            }

        logger.info("✅ Test endpoint completed successfully")
        return response

    except Exception as e:
        logger.error(f"❌ Error in test endpoint: {str(e)}", exc_info=True)
        return {
            "ok": False,
            "error": str(e),
            "db_user_count": 0,
            "first_user": None
        }
