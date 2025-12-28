# Tweet Generator - Quick Start Guide

Get your Tweet Generator API up and running in minutes!

---

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

---

## Step 1: Set Up Virtual Environment

### Windows:
```bash
# Navigate to project directory
cd Prac

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

### macOS/Linux:
```bash
# Navigate to project directory
cd Prac

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

---

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI & Uvicorn (web framework)
- SQLAlchemy (database)
- LangChain & OpenAI (AI generation)
- Authentication libraries (JWT, bcrypt)
- And all other dependencies

---

## Step 3: Configure Environment Variables

1. **Copy the example environment file:**
   ```bash
   cp Backend/.env Backend/.env
   ```

2. **Edit `Backend/.env` and add your configuration:**
   ```env
   # Database (SQLite by default)
   DATABASE_URL=sqlite:///./test.db

   # OpenAI API Key (REQUIRED - Get from https://platform.openai.com/api-keys)
   OPENAI_API_KEY=sk-your-actual-openai-api-key-here

   # JWT Secret Key (Generate a random string)
   SECRET_KEY=your-super-secret-key-change-this-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30

   # CORS Origins (optional)
   # CORS_ORIGINS=http://localhost:3000,http://localhost:5173
   ```

3. **Generate a secure SECRET_KEY:**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
   Copy the output and use it as your `SECRET_KEY` in `.env`

---

## Step 4: Run the Application

### Development Server (with auto-reload):

```bash
cd Backend
python main.py
```

Or using uvicorn directly:

```bash
cd Backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see output like:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Creating database tables...
INFO:     Database tables created successfully
INFO:     Tweet Generator API started successfully
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

## Step 5: Test the API

### Option 1: Swagger UI (Recommended for beginners)

1. Open your browser and go to: `http://localhost:8000/docs`
2. You'll see the interactive API documentation

**Test the API:**

1. **Register a user:**
   - Click on `POST /api/auth/register`
   - Click "Try it out"
   - Fill in the request body:
     ```json
     {
       "username": "testuser",
       "email": "test@example.com",
       "password": "password123"
     }
     ```
   - Click "Execute"

2. **Login to get access token:**
   - Click on `POST /api/auth/login`
   - Fill in:
     ```json
     {
       "email": "test@example.com",
       "password": "password123"
     }
     ```
   - Click "Execute"
   - **Copy the `access_token` from the response**

3. **Authorize:**
   - Click the **"Authorize" 🔓 button** at the top right
   - Paste your token in the value field
   - Click "Authorize"
   - Click "Close"

4. **Generate tweets:**
   - Click on `POST /api/tweets/generate`
   - Click "Try it out"
   - Fill in:
     ```json
     {
       "topic": "The benefits of learning Python for data science",
       "tone": "educational",
       "max_tweets": 5
     }
     ```
   - Click "Execute"
   - See your generated tweet thread!

### Option 2: Using cURL

**Register:**
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

**Login:**
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

**Generate Tweets:**
```bash
TOKEN="your-token-here"

curl -X POST "http://localhost:8000/api/tweets/generate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "topic": "The benefits of learning Python for data science",
    "tone": "educational",
    "max_tweets": 5
  }'
```

### Option 3: Using Python

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Register
response = requests.post(f"{BASE_URL}/auth/register", json={
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
})
print("Registration:", response.json())

# Login
response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "test@example.com",
    "password": "password123"
})
token = response.json()["access_token"]
print("Token:", token)

# Generate Tweets
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(f"{BASE_URL}/tweets/generate",
    headers=headers,
    json={
        "topic": "The benefits of learning Python for data science",
        "tone": "educational",
        "max_tweets": 5
    }
)
tweets = response.json()
print("\nGenerated Tweets:")
for tweet in tweets["tweets"]:
    print(f"- {tweet}")
```

---

## Available Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get token
- `POST /api/auth/token` - OAuth2 token (for Swagger)
- `GET /api/auth/me` - Get current user info
- `GET /api/auth/verify` - Verify token

### Tweet Generation
- `POST /api/tweets/generate` - Generate tweet thread 🔒
- `GET /api/tweets/history` - Get user's tweet history 🔒
- `GET /api/tweets/{id}` - Get specific tweet thread 🔒
- `DELETE /api/tweets/{id}` - Delete tweet thread 🔒
- `GET /api/tweets/analytics/stats` - Get user statistics 🔒

### Health & Info
- `GET /` - API information
- `GET /api/health` - Health check
- `GET /api/tweets/health` - Service health

🔒 = Requires authentication

---

## Tweet Generation Options

### Tone Options:
- `professional` - Business content, formal
- `casual` - Conversational, friendly
- `humorous` - Witty and entertaining
- `engaging` - Maximum interaction
- `educational` - Teaching and explaining

### Parameters:
- `topic` - Your topic (10-500 characters)
- `tone` - Optional tone (default: engaging)
- `max_tweets` - Number of tweets (1-20, default: 5)

---

## Project Structure

```
Prac/
├── Backend/
│   ├── main.py                 # Main FastAPI app ✅
│   ├── config.py               # Configuration ✅
│   ├── database.py             # Database setup ✅
│   ├── models.py               # Database models ✅
│   ├── schemas.py              # Request/response schemas ✅
│   ├── tweet_generator.py      # AI tweet generation ✅
│   ├── routers/
│   │   ├── auth.py            # Authentication endpoints ✅
│   │   └── tweets.py          # Tweet endpoints ✅
│   └── utils/
│       └── auth_utils.py      # Password & JWT utilities ✅
├── .env                        # Environment variables
├── requirements.txt            # Dependencies ✅
└── README.md
```

---

## Common Issues & Solutions

### Issue 1: "Module not found"
**Solution:** Make sure you're in the Backend directory and venv is activated:
```bash
cd Backend
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
```

### Issue 2: "OpenAI API key not found"
**Solution:** Check that `OPENAI_API_KEY` is set in `Backend/.env`:
```bash
# View your .env file
cat Backend/.env

# Make sure it has: OPENAI_API_KEY=sk-...
```

### Issue 3: "Database error"
**Solution:** Delete the test database and restart:
```bash
cd Backend
rm test.db
python main.py
```

### Issue 4: "Port 8000 already in use"
**Solution:** Change the port:
```bash
uvicorn main:app --reload --port 8001
```

---

## Next Steps

1. ✅ **API is running** - Test all endpoints in Swagger UI
2. 📱 **Build a frontend** - Connect React/Vue/HTML frontend
3. 🚀 **Deploy** - Deploy to Heroku, AWS, or Google Cloud
4. 🎨 **Customize** - Add new tones, features, or integrations

---

## Documentation

- 📖 [ROADMAP.md](ROADMAP.md) - Development roadmap
- 🔐 [AUTH_GUIDE.md](AUTH_GUIDE.md) - Authentication system guide
- 🐦 [TWEET_GENERATOR_GUIDE.md](TWEET_GENERATOR_GUIDE.md) - Tweet generation guide
- 🗄️ [DATABASE_MODELS_GUIDE.md](DATABASE_MODELS_GUIDE.md) - Database models guide

---

## Support

Having issues? Check:
1. All dependencies are installed: `pip list`
2. Environment variables are set: `cat Backend/.env`
3. You're in the correct directory: `pwd`
4. Virtual environment is activated: Check for `(venv)` in terminal

---

## Production Deployment

For production deployment:
1. Use PostgreSQL instead of SQLite
2. Set strong SECRET_KEY
3. Enable HTTPS
4. Set proper CORS origins
5. Add rate limiting
6. Monitor logs and errors

See deployment guides for specific platforms.

---

**Enjoy generating tweets! 🐦✨**
