"""
Authentication routes for user registration and login.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db import get_db
from app.models import User
from app.schemas import (
    UserRegisterRequest,
    UserLoginRequest,
    UserRegisterResponse,
    TokenResponse,
    UserResponse,
    ErrorResponse
)
from app.security import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserRegisterResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "User successfully registered"},
        400: {"model": ErrorResponse, "description": "Invalid input or email already exists"},
    }
)
async def register_user(
    user_data: UserRegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user.

    **Process:**
    1. Validates email format and password strength
    2. Checks if email is already registered
    3. Hashes the password using bcrypt
    4. Saves user to database
    5. Generates JWT access token
    6. Returns user data and token

    **Returns:**
    - User information (id, name, email, created_at)
    - JWT access token
    - Token type (bearer)

    **Raises:**
    - 400: If email already exists or invalid input
    """
    # Check if user with this email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password
    hashed_pw = hash_password(user_data.password)

    # Create new user
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_pw
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create access token
    access_token = create_access_token(data={"sub": str(new_user.id)})

    # Return user data and token
    return UserRegisterResponse(
        message="User registered successfully",
        user=UserResponse.model_validate(new_user),
        access_token=access_token,
        token_type="bearer"
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Login successful"},
        401: {"model": ErrorResponse, "description": "Invalid credentials"},
    }
)
async def login_user(
    login_data: UserLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT token.

    **Process:**
    1. Validates email format
    2. Checks if user exists
    3. Verifies password using bcrypt
    4. Generates JWT access token
    5. Returns token

    **Returns:**
    - JWT access token
    - Token type (bearer)

    **Raises:**
    - 401: If email not found or password is incorrect

    **Usage:**
    After receiving the token, include it in subsequent requests:
    ```
    Authorization: Bearer <access_token>
    ```
    """
    # Find user by email
    user = db.query(User).filter(User.email == login_data.email).first()

    # Check if user exists
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify password
    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )


@router.get(
    "/me",
    response_model=UserResponse,
    responses={
        200: {"description": "Current user information"},
        401: {"model": ErrorResponse, "description": "Not authenticated or invalid token"},
    }
)
async def get_current_user(
    db: Session = Depends(get_db),
    # TODO: Add authentication dependency to extract user from JWT
):
    """
    Get current authenticated user information.

    **Note:** This endpoint will be fully functional once we add the
    authentication dependency middleware.

    **Returns:**
    - User information (id, name, email, created_at)

    **Raises:**
    - 401: If token is invalid or missing
    """
    # This is a placeholder - will be implemented with authentication dependency
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication dependency not yet implemented. Use /register or /login endpoints."
    )
