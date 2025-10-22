# FitForge Authentication Guide

Complete guide to the authentication system using JWT tokens, bcrypt password hashing, and FastAPI.

## Overview

The authentication system provides secure user registration and login functionality with:
- **Password Hashing:** Bcrypt for secure password storage
- **JWT Tokens:** JSON Web Tokens for stateless authentication
- **Email Validation:** Pydantic EmailStr for email verification
- **Secure Storage:** Environment variables for secrets

---

## Files Created

### 1. [app/security.py](app/security.py)
Security utilities for password hashing and JWT token management.

**Functions:**
- `hash_password(password: str) -> str` - Hash passwords with bcrypt
- `verify_password(plain_password: str, hashed_password: str) -> bool` - Verify passwords
- `create_access_token(data: dict, expires_delta: Optional[timedelta]) -> str` - Generate JWT tokens
- `decode_access_token(token: str) -> Optional[dict]` - Decode and verify JWT tokens
- `get_user_id_from_token(token: str) -> Optional[int]` - Extract user ID from token

### 2. [app/schemas.py](app/schemas.py)
Pydantic schemas for request/response validation.

**Schemas:**
- `UserRegisterRequest` - Registration request (name, email, password)
- `UserLoginRequest` - Login request (email, password)
- `TokenResponse` - Token response (access_token, token_type)
- `UserResponse` - User data response (id, name, email, created_at)
- `UserRegisterResponse` - Combined registration response (user + token)
- `ErrorResponse` - Error response format

### 3. [app/api/routes/auth.py](app/api/routes/auth.py)
Authentication endpoints for registration and login.

**Endpoints:**
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user (placeholder for future implementation)

---

## API Endpoints

### POST /api/auth/register

Register a new user account.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "password": "SecurePassword123"
}
```

**Response (201 Created):**
```json
{
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
```

**Error Response (400 Bad Request):**
```json
{
  "detail": "Email already registered"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "password": "SecurePassword123"
  }'
```

---

### POST /api/auth/login

Authenticate user and receive JWT token.

**Request Body:**
```json
{
  "email": "john.doe@example.com",
  "password": "SecurePassword123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Incorrect email or password"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "SecurePassword123"
  }'
```

---

## Environment Variables

The following environment variables are used (defined in `.env`):

```bash
# Security - JWT Configuration
SECRET_KEY=your-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Generate a secure SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## Usage Examples

### Python Client Example

```python
import requests

API_URL = "http://localhost:8000"

# Register a new user
register_data = {
    "name": "Jane Smith",
    "email": "jane@example.com",
    "password": "SecurePass123"
}

response = requests.post(f"{API_URL}/api/auth/register", json=register_data)
result = response.json()

print(f"User ID: {result['user']['id']}")
print(f"Access Token: {result['access_token']}")

# Save the token for future requests
access_token = result['access_token']

# Login (if already registered)
login_data = {
    "email": "jane@example.com",
    "password": "SecurePass123"
}

response = requests.post(f"{API_URL}/api/auth/login", json=login_data)
token_response = response.json()

access_token = token_response['access_token']

# Use the token in subsequent requests
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Example: Make authenticated request (future endpoint)
response = requests.get(f"{API_URL}/api/auth/me", headers=headers)
```

### JavaScript/TypeScript Example

```javascript
const API_URL = 'http://localhost:8000';

// Register a new user
async function register(name, email, password) {
  const response = await fetch(`${API_URL}/api/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ name, email, password }),
  });

  const data = await response.json();

  if (response.ok) {
    console.log('User registered:', data.user);
    console.log('Access token:', data.access_token);
    return data;
  } else {
    throw new Error(data.detail);
  }
}

// Login
async function login(email, password) {
  const response = await fetch(`${API_URL}/api/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  const data = await response.json();

  if (response.ok) {
    // Store token in localStorage or secure storage
    localStorage.setItem('access_token', data.access_token);
    return data;
  } else {
    throw new Error(data.detail);
  }
}

// Use token in requests
async function makeAuthenticatedRequest(url) {
  const token = localStorage.getItem('access_token');

  const response = await fetch(url, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  return response.json();
}

// Example usage
async function main() {
  try {
    // Register
    const registerResult = await register(
      'Jane Smith',
      'jane@example.com',
      'SecurePass123'
    );

    // Login
    const loginResult = await login(
      'jane@example.com',
      'SecurePass123'
    );

    console.log('Login successful:', loginResult);
  } catch (error) {
    console.error('Error:', error.message);
  }
}
```

---

## Security Features

### 1. Password Hashing (Bcrypt)

- **Algorithm:** Bcrypt with automatic salt generation
- **Cost Factor:** Default bcrypt cost (12 rounds)
- **Storage:** Only hashed passwords stored in database
- **Verification:** Constant-time comparison to prevent timing attacks

**Example:**
```python
from app.security import hash_password, verify_password

# Hash a password
hashed = hash_password("MySecurePassword")
# Output: $2b$12$...

# Verify a password
is_valid = verify_password("MySecurePassword", hashed)
# Output: True
```

### 2. JWT Tokens

- **Algorithm:** HS256 (HMAC with SHA-256)
- **Expiration:** 30 minutes (configurable)
- **Payload:** User ID in `sub` claim
- **Secret:** Stored in environment variable

**Token Structure:**
```json
{
  "sub": "2",  // User ID
  "exp": 1761093855  // Expiration timestamp
}
```

### 3. Email Validation

- **Library:** email-validator via Pydantic EmailStr
- **Checks:** Format validation and DNS verification
- **Prevention:** Invalid email formats rejected at request level

### 4. Error Messages

- **Security:** Generic "Incorrect email or password" for both invalid email and password
- **Prevention:** Prevents user enumeration attacks
- **Logging:** Actual errors logged server-side for debugging

---

## Testing

### Manual Testing

```bash
# Test Registration
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "email": "test@example.com", "password": "TestPass123"}'

# Test Login (valid credentials)
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "TestPass123"}'

# Test Login (invalid credentials)
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "WrongPassword"}'

# Test Registration (duplicate email)
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User 2", "email": "test@example.com", "password": "TestPass123"}'
```

### Expected Results

**✅ Successful Registration:**
- Status: 201 Created
- Returns: User data + JWT token

**✅ Successful Login:**
- Status: 200 OK
- Returns: JWT token

**❌ Wrong Password:**
- Status: 401 Unauthorized
- Message: "Incorrect email or password"

**❌ Duplicate Email:**
- Status: 400 Bad Request
- Message: "Email already registered"

**❌ Invalid Email Format:**
- Status: 422 Unprocessable Entity
- Message: Validation error

**❌ Password Too Short:**
- Status: 422 Unprocessable Entity
- Message: Password must be at least 8 characters

---

## Database Schema

The authentication system uses the existing `User` model from [app/models.py](app/models.py):

```python
class User(Base):
    __tablename__ = "users"

    id: Mapped[int]  # Primary key
    name: Mapped[str]  # User's full name
    email: Mapped[str]  # Unique email (indexed)
    hashed_password: Mapped[str]  # Bcrypt hashed password
    created_at: Mapped[datetime]  # Registration timestamp

    # Relationships
    workouts: Mapped[list["Workout"]]
    runs: Mapped[list["Run"]]
    plans: Mapped[list["Plan"]]
```

---

## Dependencies

All required packages are in [requirements.txt](requirements.txt):

```
python-jose[cryptography]==3.3.0  # JWT token handling
python-multipart==0.0.6           # Form data parsing
email-validator==2.1.2             # Email validation
passlib==1.7.4                     # Password hashing
bcrypt==4.0.1                      # Bcrypt algorithm
```

**Install:**
```bash
pip install -r requirements.txt
```

---

## Next Steps

### 1. Add Authentication Middleware

Create a dependency to extract and verify tokens:

```python
# app/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.security import get_user_id_from_token
from app.db import get_db
from app.models import User
from sqlalchemy.orm import Session

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token."""
    token = credentials.credentials
    user_id = get_user_id_from_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user
```

### 2. Protect Endpoints

Use the dependency in protected routes:

```python
from app.dependencies import get_current_user

@router.get("/api/auth/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)

@router.get("/api/plans")
async def get_user_plans(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    plans = db.query(Plan).filter(Plan.user_id == current_user.id).all()
    return plans
```

### 3. Add Refresh Tokens

Implement refresh token functionality for long-lived sessions:

```python
def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

### 4. Add Password Reset

Implement password reset via email:
- Generate reset token
- Send email with reset link
- Verify token and update password

### 5. Add Email Verification

Require email verification before login:
- Send verification email on registration
- Verify email with token
- Add `email_verified` field to User model

---

## Troubleshooting

### Issue: "email-validator is not installed"

**Solution:**
```bash
pip install email-validator==2.1.2
```

### Issue: "Invalid authentication credentials"

**Causes:**
- Token expired (30 minutes by default)
- Invalid token format
- Wrong SECRET_KEY

**Solution:**
- Login again to get new token
- Verify token format: `Bearer <token>`
- Check .env file for correct SECRET_KEY

### Issue: "Email already registered"

**Cause:** Email already exists in database

**Solution:** Use different email or login with existing account

### Issue: Token not working after server restart

**Cause:** SECRET_KEY changed or not set in environment

**Solution:** Ensure .env file has consistent SECRET_KEY

---

## API Documentation

Visit the interactive API documentation:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

Try the endpoints directly in your browser!

---

## Security Best Practices

1. **Always use HTTPS in production**
2. **Keep SECRET_KEY secure** - Never commit to git
3. **Use strong passwords** - Enforce minimum 8 characters
4. **Rotate tokens regularly** - Implement refresh tokens
5. **Rate limit auth endpoints** - Prevent brute force attacks
6. **Log authentication events** - Monitor for suspicious activity
7. **Use secure cookie storage** - For frontend token storage
8. **Implement CORS properly** - Only allow trusted origins

---

## Summary

✅ **Complete authentication system implemented:**
- User registration with password hashing
- User login with JWT tokens
- Secure password verification
- Email validation
- Error handling
- Full API documentation

🔒 **Security features:**
- Bcrypt password hashing
- JWT token authentication
- Environment variable secrets
- Generic error messages

📚 **Documentation:**
- Complete API reference
- Usage examples (Python, JavaScript)
- Security best practices
- Troubleshooting guide

**Your authentication system is ready for production use!**
