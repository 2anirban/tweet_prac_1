# Authentication System Guide

Complete guide to understanding the authentication system in the Tweet Generator backend.

---

## Table of Contents

1. [Overview](#overview)
2. [File Structure](#file-structure)
3. [Password Hashing](#password-hashing)
4. [JWT Tokens](#jwt-tokens)
5. [Authentication Flow](#authentication-flow)
6. [API Endpoints](#api-endpoints)
7. [Using Authentication in Your App](#using-authentication-in-your-app)
8. [Testing Authentication](#testing-authentication)

---

## Overview

The authentication system provides:
- ✅ User registration with email and password
- ✅ Secure password hashing with bcrypt
- ✅ JWT (JSON Web Token) based authentication
- ✅ Protected routes that require authentication
- ✅ User profile access
- ✅ Token verification

**Security Features:**
- Passwords are hashed using bcrypt (never stored as plain text)
- JWT tokens expire after a configured time (default: 30 minutes)
- Tokens include user ID and email in the payload
- Protected routes verify token validity on every request

---

## File Structure

```
Backend/
├── utils/
│   ├── __init__.py
│   └── auth_utils.py          # Password hashing & JWT utilities
├── routers/
│   ├── __init__.py
│   └── auth.py                # Authentication endpoints
├── config.py                   # Settings (SECRET_KEY, ALGORITHM, etc.)
├── models.py                   # User model
└── schemas.py                  # UserCreate, UserLogin, Token schemas
```

---

## Password Hashing

### How It Works

Located in [utils/auth_utils.py](Backend/utils/auth_utils.py)

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

### Functions

#### 1. `hash_password(password: str) -> str`

Converts a plain text password into a secure hash.

```python
plain_password = "mypassword123"
hashed = hash_password(plain_password)
# Result: "$2b$12$KIXl.QEfY8x7yK5z..."
```

**When to use:**
- During user registration
- When user changes password

**Example:**
```python
# In registration endpoint
hashed_password = hash_password(user_data.password)
new_user = User(
    email=user_data.email,
    hashed_password=hashed_password  # Store hashed, not plain
)
```

#### 2. `verify_password(plain_password: str, hashed_password: str) -> bool`

Checks if a plain text password matches a hashed password.

```python
plain = "mypassword123"
hashed = "$2b$12$KIXl.QEfY8x7yK5z..."
is_valid = verify_password(plain, hashed)  # True if match
```

**When to use:**
- During login authentication
- When verifying user credentials

**Example:**
```python
# In login endpoint
user = get_user_by_email(db, email)
if not verify_password(password, user.hashed_password):
    raise HTTPException(status_code=401, detail="Invalid password")
```

### Why Bcrypt?

- **Slow by design**: Makes brute-force attacks impractical
- **Salted**: Each password gets a unique salt
- **Industry standard**: Widely trusted and tested
- **Adaptive**: Can increase complexity over time

---

## JWT Tokens

### What is JWT?

**JWT (JSON Web Token)** is a compact, URL-safe token format that contains:
1. **Header**: Token type and algorithm
2. **Payload**: User data (email, user_id, expiration)
3. **Signature**: Verification signature

**Example JWT:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIiwidXNlcl9pZCI6MSwiZXhwIjoxNjk5OTk5OTk5fQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

**Decoded payload:**
```json
{
  "sub": "user@example.com",
  "user_id": 1,
  "exp": 1699999999
}
```

### Functions

Located in [utils/auth_utils.py](Backend/utils/auth_utils.py)

#### 1. `create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str`

Creates a JWT token with user data.

```python
from datetime import timedelta

token = create_access_token(
    data={"sub": "user@example.com", "user_id": 1},
    expires_delta=timedelta(minutes=30)
)
```

**Parameters:**
- `data`: Dictionary with user information
  - `sub`: Subject (usually email or username)
  - `user_id`: User's database ID
- `expires_delta`: How long the token is valid (optional)

**Returns:** Encoded JWT token string

#### 2. `decode_access_token(token: str) -> Optional[dict]`

Decodes and verifies a JWT token.

```python
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
payload = decode_access_token(token)

if payload:
    email = payload.get("sub")
    user_id = payload.get("user_id")
else:
    # Token is invalid or expired
    print("Invalid token")
```

**Returns:**
- `dict`: Decoded payload if token is valid
- `None`: If token is invalid or expired

### Token Security

**Secret Key:**
```python
# In config.py
SECRET_KEY: str = "your-secret-key-here"  # Change this!
```

⚠️ **IMPORTANT:**
- Keep `SECRET_KEY` secret (use environment variables)
- Use a strong, random key (at least 32 characters)
- Never commit it to version control

**Generate a secure key:**
```bash
# Method 1: Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Method 2: OpenSSL
openssl rand -hex 32
```

---

## Authentication Flow

### 1. User Registration

```
User → POST /auth/register
{
  "username": "john",
  "email": "john@example.com",
  "password": "password123"
}

Backend:
1. Check if email/username exists
2. Hash password with bcrypt
3. Save user to database
4. Return user info (without password)

← Response:
{
  "id": 1,
  "username": "john",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00"
}
```

### 2. User Login

```
User → POST /auth/login
{
  "email": "john@example.com",
  "password": "password123"
}

Backend:
1. Find user by email
2. Verify password with bcrypt
3. Generate JWT token
4. Return token

← Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Accessing Protected Routes

```
User → GET /auth/me
Headers: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Backend:
1. Extract token from Authorization header
2. Decode and verify token
3. Get user from database
4. Check if user is active
5. Return user info

← Response:
{
  "id": 1,
  "username": "john",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00"
}
```

### Visual Flow Diagram

```
┌─────────────┐
│  Register   │
│  /register  │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  Hash Password      │
│  Save to Database   │
└──────┬──────────────┘
       │
       ▼
┌─────────────┐
│    Login    │
│   /login    │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  Verify Password    │
│  Generate JWT Token │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Store Token        │
│  (Frontend)         │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Protected Request  │
│  With Token Header  │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Verify Token       │
│  Get User           │
│  Return Response    │
└─────────────────────┘
```

---

## API Endpoints

### 1. POST /auth/register

**Register a new user**

**Request:**
```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "securepass123"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "username": "john",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

**Errors:**
- `400`: Email already registered
- `400`: Username already taken
- `422`: Validation error (weak password, invalid email, etc.)

---

### 2. POST /auth/login

**Login with email and password**

**Request:**
```json
{
  "email": "john@example.com",
  "password": "securepass123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errors:**
- `401`: Incorrect email or password
- `403`: User account is inactive

---

### 3. POST /auth/token

**OAuth2 compatible token endpoint (for Swagger UI)**

**Request (Form Data):**
```
username: john@example.com  (use email here)
password: securepass123
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Note:** This endpoint is used by FastAPI's Swagger UI (`/docs`) for authentication.

---

### 4. GET /auth/me

**Get current user profile (Protected)**

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "john",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

**Errors:**
- `401`: Invalid or missing token
- `403`: User account is inactive

---

### 5. GET /auth/verify

**Verify if token is valid (Protected)**

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Token is valid",
  "user_id": 1,
  "email": "john@example.com"
}
```

---

## Using Authentication in Your App

### Protecting Endpoints

To protect an endpoint, add the `get_current_active_user` dependency:

```python
from fastapi import APIRouter, Depends
from routers.auth import get_current_active_user
from models import User

router = APIRouter()

@router.get("/protected-route")
async def protected_route(current_user: User = Depends(get_current_active_user)):
    """
    This endpoint requires authentication
    Only users with valid JWT token can access it
    """
    return {
        "message": f"Hello {current_user.username}!",
        "user_id": current_user.id
    }
```

### Example: Tweet Generation with Auth

```python
from fastapi import APIRouter, Depends
from routers.auth import get_current_active_user
from models import User
from schemas import TweetGenerationRequest, TweetGenerationResponse

router = APIRouter()

@router.post("/tweets/generate", response_model=TweetGenerationResponse)
async def generate_tweets(
    request: TweetGenerationRequest,
    current_user: User = Depends(get_current_active_user),  # ← Requires auth
    db: Session = Depends(get_db)
):
    """
    Generate a tweet thread (requires authentication)
    """
    # current_user is automatically populated from JWT token

    # Generate tweets (your logic here)
    tweets = generate_tweet_thread(request.topic)

    # Save to database with user_id
    thread = TweetThread(
        user_id=current_user.id,  # ← From authenticated user
        topic=request.topic,
        thread_content=json.dumps(tweets),
        tweet_count=len(tweets)
    )
    db.add(thread)
    db.commit()

    return TweetGenerationResponse(
        tweets=tweets,
        tweet_count=len(tweets),
        topic=request.topic
    )
```

### Frontend Integration

**1. Register User:**
```javascript
const response = await fetch('http://localhost:8000/auth/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'john',
    email: 'john@example.com',
    password: 'securepass123'
  })
});
const user = await response.json();
```

**2. Login and Get Token:**
```javascript
const response = await fetch('http://localhost:8000/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'john@example.com',
    password: 'securepass123'
  })
});
const { access_token } = await response.json();

// Store token (e.g., localStorage)
localStorage.setItem('token', access_token);
```

**3. Use Token for Protected Requests:**
```javascript
const token = localStorage.getItem('token');

const response = await fetch('http://localhost:8000/auth/me', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
const user = await response.json();
```

---

## Testing Authentication

### Using Swagger UI (/docs)

1. Start your FastAPI server:
   ```bash
   cd Backend
   uvicorn main:app --reload
   ```

2. Open browser: `http://localhost:8000/docs`

3. **Register a user:**
   - Click on `POST /auth/register`
   - Click "Try it out"
   - Enter user data
   - Click "Execute"

4. **Login and get token:**
   - Click on `POST /auth/login`
   - Enter email and password
   - Copy the `access_token` from response

5. **Authorize in Swagger:**
   - Click the "Authorize" button (🔓) at the top
   - Paste token in the value field
   - Click "Authorize"

6. **Access protected endpoints:**
   - Try `GET /auth/me`
   - It should work now with your token

### Using cURL

**Register:**
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

**Login:**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

**Get User Profile:**
```bash
TOKEN="your-token-here"

curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Register
response = requests.post(f"{BASE_URL}/auth/register", json={
    "username": "john",
    "email": "john@example.com",
    "password": "securepass123"
})
print(response.json())

# Login
response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "john@example.com",
    "password": "securepass123"
})
token = response.json()["access_token"]

# Access protected route
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
print(response.json())
```

---

## Security Best Practices

### 1. Environment Variables

**Never hardcode secrets in code!**

```python
# ❌ BAD
SECRET_KEY = "my-secret-key-123"

# ✅ GOOD
from config import settings
SECRET_KEY = settings.SECRET_KEY  # Loaded from .env
```

**In .env file:**
```
SECRET_KEY=your-super-secret-key-here-generate-random
```

### 2. Strong SECRET_KEY

Generate a strong random key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Password Requirements

Enforce strong passwords (already configured in schemas.py):
```python
password: str = Field(..., min_length=8)
```

Consider adding:
- Uppercase and lowercase letters
- Numbers and special characters
- Password strength meter

### 4. Token Expiration

Tokens expire after 30 minutes by default. Adjust in [config.py](Backend/config.py):
```python
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Change as needed
```

### 5. HTTPS in Production

Always use HTTPS in production to prevent token interception.

### 6. Rate Limiting

Consider adding rate limiting to prevent brute-force attacks:
```python
from slowapi import Limiter

@router.post("/login")
@limiter.limit("5/minute")  # Max 5 login attempts per minute
def login(...):
    ...
```

---

## Common Issues and Solutions

### Issue 1: "Could not validate credentials"

**Cause:** Invalid or expired token

**Solution:**
- Check if token is being sent in headers
- Verify token hasn't expired
- Re-login to get a new token

### Issue 2: "Email already registered"

**Cause:** Trying to register with existing email

**Solution:**
- Use a different email
- Or implement "forgot password" functionality

### Issue 3: "Incorrect email or password"

**Cause:** Wrong credentials

**Solution:**
- Double-check email and password
- Ensure user has registered first

### Issue 4: Import errors

**Cause:** Circular imports or missing files

**Solution:**
- Ensure all `__init__.py` files exist
- Check import paths
- Restart the server

---

## Summary

✅ **Authentication system includes:**
- User registration with validation
- Secure password hashing (bcrypt)
- JWT token generation and verification
- Protected route middleware
- User profile access
- Token verification endpoint

✅ **Security features:**
- Passwords never stored as plain text
- Tokens expire after configured time
- Email and username uniqueness enforced
- Active user check on authentication

✅ **Ready to use:**
- Add `Depends(get_current_active_user)` to protect any route
- Frontend can store and use JWT tokens
- Works with FastAPI's Swagger UI

---

**Next Steps:**
1. Test all endpoints in Swagger UI
2. Integrate with tweet generation endpoints
3. Add frontend authentication
4. Consider adding refresh tokens for better UX

**Reference Files:**
- [routers/auth.py](Backend/routers/auth.py) - Authentication endpoints
- [utils/auth_utils.py](Backend/utils/auth_utils.py) - Password & JWT utilities
- [schemas.py](Backend/schemas.py) - Validation schemas
- [config.py](Backend/config.py) - Configuration settings
