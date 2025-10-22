"""
Pydantic schemas for request/response validation.
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


# ==================== Auth Schemas ====================

class UserRegisterRequest(BaseModel):
    """Schema for user registration request."""
    name: str = Field(..., min_length=1, max_length=255, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, max_length=100, description="User's password (min 8 characters)")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "password": "SecurePassword123!"
            }
        }


class UserLoginRequest(BaseModel):
    """Schema for user login request."""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "SecurePassword123!"
            }
        }


class TokenResponse(BaseModel):
    """Schema for authentication token response."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }


class UserResponse(BaseModel):
    """Schema for user data response."""
    id: int
    name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe",
                "email": "john.doe@example.com",
                "created_at": "2025-10-21T00:00:00"
            }
        }


class UserRegisterResponse(BaseModel):
    """Schema for successful registration response."""
    message: str
    user: UserResponse
    access_token: str
    token_type: str = "bearer"

    class Config:
        json_schema_extra = {
            "example": {
                "message": "User registered successfully",
                "user": {
                    "id": 1,
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "created_at": "2025-10-21T00:00:00"
                },
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }


# ==================== Plan Schemas ====================

class PlanGenerateRequest(BaseModel):
    """Schema for plan generation request."""
    goal: str = Field(..., description="Fitness goal: 'build muscle' or 'run faster'")
    days_per_week: int = Field(..., ge=1, le=7, description="Number of workout days per week (1-7)")
    run_days: int = Field(..., ge=0, le=7, description="Number of running days (0-7)")
    lift_days: int = Field(..., ge=0, le=7, description="Number of lifting days (0-7)")

    class Config:
        json_schema_extra = {
            "example": {
                "goal": "build muscle",
                "days_per_week": 5,
                "run_days": 2,
                "lift_days": 3
            }
        }


class PlanResponse(BaseModel):
    """Schema for plan response."""
    id: int
    user_id: int
    goals: str
    routine_json: dict
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
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
        }


# ==================== Error Schemas ====================

class ErrorResponse(BaseModel):
    """Schema for error responses."""
    detail: str

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Error message here"
            }
        }
