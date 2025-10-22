"""
Plan generation routes for creating personalized fitness plans.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User, Plan
from app.schemas import PlanGenerateRequest, PlanResponse, ErrorResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/plans", tags=["Plans"])


def generate_workout_plan(
    goal: str,
    days_per_week: int,
    run_days: int,
    lift_days: int
) -> dict:
    """
    Generate a workout plan based on user preferences.

    Args:
        goal: Fitness goal ('build muscle' or 'run faster')
        days_per_week: Total number of workout days per week
        run_days: Number of running days
        lift_days: Number of lifting days

    Returns:
        Dictionary mapping day names to workout descriptions
    """
    # Available days of the week
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Initialize the plan
    routine = {}

    # Track which days are assigned
    assigned_days = []

    # Build muscle focus - prioritize lifting
    if goal.lower() == "build muscle":
        # Lifting workouts
        lift_workouts = [
            "Upper Body - Chest & Triceps",
            "Lower Body - Legs & Glutes",
            "Back & Biceps",
            "Shoulders & Core",
            "Full Body Strength"
        ]

        # Assign lift days
        for i in range(min(lift_days, days_per_week)):
            if i < len(days):
                routine[days[i]] = lift_workouts[i % len(lift_workouts)]
                assigned_days.append(i)

        # Assign run days on remaining days
        run_day_index = 0
        for i in range(len(days)):
            if i not in assigned_days and run_day_index < run_days:
                routine[days[i]] = f"Run {3 + run_day_index}km - Recovery Pace"
                assigned_days.append(i)
                run_day_index += 1

    # Run faster focus - prioritize running
    elif goal.lower() == "run faster":
        # Running workouts
        run_workouts = [
            "Run 5km - Tempo Pace",
            "Run 8km - Easy Pace",
            "Interval Training - 400m Repeats",
            "Run 10km - Long Run",
            "Hill Sprints - Speed Work",
            "Run 6km - Recovery Run"
        ]

        # Assign run days
        for i in range(min(run_days, days_per_week)):
            if i < len(days):
                routine[days[i]] = run_workouts[i % len(run_workouts)]
                assigned_days.append(i)

        # Assign lift days on remaining days (for strength support)
        lift_day_index = 0
        lift_workouts_support = [
            "Lower Body Strength - Legs",
            "Core & Stability",
            "Upper Body Maintenance"
        ]
        for i in range(len(days)):
            if i not in assigned_days and lift_day_index < lift_days:
                routine[days[i]] = lift_workouts_support[lift_day_index % len(lift_workouts_support)]
                assigned_days.append(i)
                lift_day_index += 1

    # Default/other goals
    else:
        # Balanced approach
        workouts = [
            "Full Body Workout",
            "Run 5km",
            "Upper Body Strength",
            "Run 3km - Easy",
            "Lower Body Strength",
            "Active Recovery - Yoga/Stretching",
            "Sports or Cross-Training"
        ]

        for i in range(min(days_per_week, len(days))):
            routine[days[i]] = workouts[i % len(workouts)]

    # Add rest days if needed
    rest_day_count = 0
    for i, day in enumerate(days):
        if day not in routine and rest_day_count < (7 - days_per_week):
            routine[day] = "Rest Day"
            rest_day_count += 1

    return routine


@router.post(
    "/generate-plan",
    response_model=PlanResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Plan generated and saved successfully"},
        400: {"model": ErrorResponse, "description": "Invalid input"},
        401: {"model": ErrorResponse, "description": "Not authenticated"},
    }
)
async def generate_plan(
    plan_request: PlanGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate a personalized fitness plan based on user preferences.

    **Requires Authentication:** Include JWT token in Authorization header.

    **Request Body:**
    - goal: Fitness goal ('build muscle' or 'run faster')
    - days_per_week: Number of workout days per week (1-7)
    - run_days: Number of running days (0-7)
    - lift_days: Number of lifting days (0-7)

    **Process:**
    1. Validates user preferences
    2. Generates workout plan using simple logic
    3. Saves plan to database linked to current user
    4. Returns the generated plan

    **Returns:**
    - Plan with routine_json containing day-to-day workout schedule

    **Example Response:**
    ```json
    {
      "id": 1,
      "user_id": 1,
      "goals": "build muscle",
      "routine_json": {
        "Monday": "Upper Body - Chest & Triceps",
        "Wednesday": "Run 5km",
        "Friday": "Lower Body - Legs & Glutes"
      },
      "created_at": "2025-10-21T00:00:00"
    }
    ```
    """
    # Validate that run_days + lift_days doesn't exceed days_per_week
    if plan_request.run_days + plan_request.lift_days > plan_request.days_per_week:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Total workout days (run_days: {plan_request.run_days} + lift_days: {plan_request.lift_days}) cannot exceed days_per_week: {plan_request.days_per_week}"
        )

    # Generate the workout routine
    routine = generate_workout_plan(
        goal=plan_request.goal,
        days_per_week=plan_request.days_per_week,
        run_days=plan_request.run_days,
        lift_days=plan_request.lift_days
    )

    # Create goals description
    goals_description = f"{plan_request.goal} - {plan_request.days_per_week} days/week ({plan_request.lift_days} lift, {plan_request.run_days} run)"

    # Save plan to database
    new_plan = Plan(
        user_id=current_user.id,
        goals=goals_description,
        routine_json=routine
    )

    try:
        db.add(new_plan)
        db.commit()
        db.refresh(new_plan)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save plan: {str(e)}"
        )

    return PlanResponse.model_validate(new_plan)


@router.get(
    "/my-plans",
    response_model=list[PlanResponse],
    responses={
        200: {"description": "List of user's plans"},
        401: {"model": ErrorResponse, "description": "Not authenticated"},
    }
)
async def get_my_plans(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all fitness plans for the current authenticated user.

    **Requires Authentication:** Include JWT token in Authorization header.

    **Returns:**
    - List of all plans created by the current user
    """
    plans = db.query(Plan).filter(Plan.user_id == current_user.id).order_by(Plan.created_at.desc()).all()
    return [PlanResponse.model_validate(plan) for plan in plans]


@router.get(
    "/{plan_id}",
    response_model=PlanResponse,
    responses={
        200: {"description": "Plan details"},
        401: {"model": ErrorResponse, "description": "Not authenticated"},
        403: {"model": ErrorResponse, "description": "Not authorized to view this plan"},
        404: {"model": ErrorResponse, "description": "Plan not found"},
    }
)
async def get_plan(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific fitness plan by ID.

    **Requires Authentication:** Include JWT token in Authorization header.

    **Authorization:** Users can only view their own plans.

    **Returns:**
    - Plan details including routine_json
    """
    plan = db.query(Plan).filter(Plan.id == plan_id).first()

    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found"
        )

    # Check if user owns this plan
    if plan.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this plan"
        )

    return PlanResponse.model_validate(plan)


@router.delete(
    "/{plan_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Plan deleted successfully"},
        401: {"model": ErrorResponse, "description": "Not authenticated"},
        403: {"model": ErrorResponse, "description": "Not authorized to delete this plan"},
        404: {"model": ErrorResponse, "description": "Plan not found"},
    }
)
async def delete_plan(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a specific fitness plan.

    **Requires Authentication:** Include JWT token in Authorization header.

    **Authorization:** Users can only delete their own plans.

    **Returns:**
    - 204 No Content on success
    """
    plan = db.query(Plan).filter(Plan.id == plan_id).first()

    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found"
        )

    # Check if user owns this plan
    if plan.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this plan"
        )

    try:
        db.delete(plan)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete plan: {str(e)}"
        )

    return None
