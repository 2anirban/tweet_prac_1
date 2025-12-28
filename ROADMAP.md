# Tweet Generator Backend - Development Roadmap

## Project Overview
A FastAPI backend that takes a topic description (couple of lines) and generates a comprehensive tweet thread using OpenAI API and LangChain.

---

## Phase 1: Project Setup & Configuration ⚙️

### 1.1 Environment Setup
- [x] Create project structure
- [ ] Set up virtual environment
- [ ] Install dependencies:
  - `fastapi`
  - `uvicorn[standard]`
  - `sqlalchemy`
  - `psycopg2-binary` (PostgreSQL) or `pymysql` (MySQL)
  - `python-dotenv`
  - `pydantic`
  - `pydantic-settings`
  - `openai`
  - `langchain`
  - `langchain-openai`
  - `python-jose[cryptography]` (for JWT)
  - `passlib[bcrypt]` (for password hashing)
  - `python-multipart`

### 1.2 Configuration ([config.py](Backend/config.py))
- [ ] Move Settings class from [database.py](Backend/database.py) to [config.py](Backend/config.py)
- [ ] Add environment variables:
  - `DATABASE_URL` (database connection string)
  - `OPENAI_API_KEY` (OpenAI API key)
  - `SECRET_KEY` (for JWT token generation)
  - `ALGORITHM` (JWT algorithm, e.g., HS256)
  - `ACCESS_TOKEN_EXPIRE_MINUTES`
  - `CORS_ORIGINS` (allowed origins for CORS)
- [ ] Create `.env.example` template
- [ ] Configure `.gitignore` to exclude `.env`

### 1.3 Database Setup ([database.py](Backend/database.py))
- [ ] Set up SQLAlchemy engine
- [ ] Create SessionLocal for database sessions
- [ ] Create Base class for models
- [ ] Implement `get_db()` dependency for FastAPI

---

## Phase 2: Database Models & Schemas 🗄️

### 2.1 Database Models ([models.py](Backend/models.py))
Define SQLAlchemy ORM models:

- [ ] **User Model**
  - `id` (Primary Key)
  - `email` (Unique)
  - `username` (Unique)
  - `hashed_password`
  - `is_active`
  - `created_at`
  - `updated_at`

- [ ] **TweetThread Model**
  - `id` (Primary Key)
  - `user_id` (Foreign Key to User)
  - `topic` (input topic/description)
  - `thread_content` (JSON/Text - generated tweets)
  - `tweet_count` (number of tweets in thread)
  - `created_at`
  - `updated_at`

- [ ] **TweetHistory Model** (Optional - for analytics)
  - `id` (Primary Key)
  - `thread_id` (Foreign Key to TweetThread)
  - `generation_params` (JSON - parameters used)
  - `processing_time` (float)
  - `status` (success/failed)

### 2.2 Pydantic Schemas ([schemas.py](Backend/schemas.py))
Define request/response schemas:

- [ ] **User Schemas**
  - `UserCreate` (registration)
  - `UserLogin` (authentication)
  - `UserResponse` (safe user data)
  - `Token` (JWT token response)

- [ ] **Tweet Schemas**
  - `TweetGenerationRequest` (topic, optional params)
  - `TweetGenerationResponse` (generated thread)
  - `TweetThreadResponse` (thread with metadata)
  - `TweetHistoryResponse` (user's tweet history)

---

## Phase 3: Authentication & Security 🔐

### 3.1 Create Auth Router
- [ ] Create `routers/` directory
- [ ] Create `routers/auth.py`

### 3.2 Implement Auth Features
- [ ] User registration endpoint (`POST /auth/register`)
- [ ] User login endpoint (`POST /auth/login`)
- [ ] Password hashing with bcrypt
- [ ] JWT token generation
- [ ] Token verification dependency (`get_current_user`)
- [ ] Protected route decorator

---

## Phase 4: Tweet Generation Core 🤖

### 4.1 LangChain Integration ([tweet_generator.py](Backend/tweet_generator.py))

- [ ] **Set up OpenAI LLM**
  ```python
  - Initialize ChatOpenAI with API key
  - Configure model (gpt-4, gpt-3.5-turbo)
  - Set temperature and max_tokens
  ```

- [ ] **Create Tweet Generation Chain**
  - Design prompt template for tweet thread generation
  - Define system prompt (Twitter best practices, character limits, etc.)
  - Create user prompt template (topic input)
  - Build LangChain chain (PromptTemplate → LLM → OutputParser)

- [ ] **Tweet Thread Logic**
  - Split long content into tweet-sized chunks (280 chars)
  - Add thread numbering (1/n, 2/n, etc.)
  - Ensure coherent flow between tweets
  - Add relevant hashtags
  - Include call-to-action in final tweet

- [ ] **Advanced Features** (Optional)
  - Tone customization (professional, casual, humorous)
  - Thread length control (short/medium/long)
  - Keyword/hashtag suggestions
  - Content refinement iterations

### 4.2 Error Handling
- [ ] Handle OpenAI API errors (rate limits, invalid requests)
- [ ] Handle LangChain exceptions
- [ ] Implement retry logic with exponential backoff
- [ ] Log errors for debugging

---

## Phase 5: API Endpoints 🚀

### 5.1 Create Tweet Router
- [ ] Create `routers/tweets.py`

### 5.2 Implement Endpoints

- [ ] **POST `/api/tweets/generate`** (Protected)
  - Accept topic description
  - Validate input (min/max length)
  - Call tweet_generator service
  - Save to database
  - Return generated thread

- [ ] **GET `/api/tweets/history`** (Protected)
  - Fetch user's tweet generation history
  - Pagination support
  - Sorting by date

- [ ] **GET `/api/tweets/{thread_id}`** (Protected)
  - Retrieve specific tweet thread
  - Verify ownership

- [ ] **DELETE `/api/tweets/{thread_id}`** (Protected)
  - Delete tweet thread
  - Verify ownership

- [ ] **GET `/api/health`** (Public)
  - Health check endpoint
  - Return service status

---

## Phase 6: Main Application Setup 📦

### 6.1 Configure FastAPI App ([main.py](Backend/main.py))

- [ ] Initialize FastAPI application
- [ ] Add metadata (title, description, version)
- [ ] Configure CORS middleware
- [ ] Include routers (auth, tweets)
- [ ] Add startup event (create database tables)
- [ ] Add exception handlers
- [ ] Configure logging

### 6.2 Middleware & Dependencies
- [ ] Rate limiting middleware (optional)
- [ ] Request logging middleware
- [ ] Error handling middleware

---

## Phase 7: Testing & Validation ✅

### 7.1 Unit Tests
- [ ] Test database models
- [ ] Test Pydantic schemas
- [ ] Test tweet_generator functions
- [ ] Test authentication logic

### 7.2 Integration Tests
- [ ] Test API endpoints
- [ ] Test database operations
- [ ] Test OpenAI integration
- [ ] Test error scenarios

### 7.3 Manual Testing
- [ ] Test with Swagger UI (`/docs`)
- [ ] Test with Postman/Thunder Client
- [ ] Verify token authentication
- [ ] Test edge cases (empty input, very long input, special characters)

---

## Phase 8: Optimization & Polish ⚡

### 8.1 Performance
- [ ] Add database indexes
- [ ] Implement caching (Redis - optional)
- [ ] Optimize LangChain prompts
- [ ] Add request timeout handling

### 8.2 Documentation
- [ ] Add docstrings to all functions
- [ ] Update API documentation
- [ ] Create API usage examples
- [ ] Document environment variables

### 8.3 Security Hardening
- [ ] Implement request validation
- [ ] Add rate limiting per user
- [ ] Sanitize user inputs
- [ ] Add API key rotation mechanism

---

## Phase 9: Deployment Preparation 🚢

### 9.1 Production Setup
- [ ] Create `requirements.txt`
- [ ] Set up production database
- [ ] Configure environment variables for production
- [ ] Set up logging to file/service

### 9.2 Containerization (Optional)
- [ ] Create `Dockerfile`
- [ ] Create `docker-compose.yml`
- [ ] Test Docker build

### 9.3 Deployment
- [ ] Deploy to cloud platform (AWS/GCP/Azure/Heroku)
- [ ] Set up CI/CD pipeline (GitHub Actions)
- [ ] Configure SSL/HTTPS
- [ ] Set up monitoring and alerts

---

## Project Structure

```
Prac/
├── Backend/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app initialization
│   ├── config.py               # Configuration & environment variables
│   ├── database.py             # Database connection & session
│   ├── models.py               # SQLAlchemy ORM models
│   ├── schemas.py              # Pydantic schemas
│   ├── tweet_generator.py      # LangChain + OpenAI logic
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py            # Authentication endpoints
│   │   └── tweets.py          # Tweet generation endpoints
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── auth_utils.py      # JWT & password utilities
│   │   └── validators.py      # Input validation helpers
│   └── tests/
│       ├── __init__.py
│       ├── test_auth.py
│       └── test_tweets.py
├── .env                        # Environment variables (not in git)
├── .env.example               # Template for .env
├── .gitignore
├── requirements.txt
├── ROADMAP.md                 # This file
└── README.md
```

---

## Dependencies List

Create `requirements.txt`:
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
python-dotenv==1.0.0
pydantic==2.5.3
pydantic-settings==2.1.0
openai==1.10.0
langchain==0.1.5
langchain-openai==0.0.5
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
```

---

## Next Steps

1. **Start with Phase 1**: Set up your virtual environment and install dependencies
2. **Configure `.env`**: Add your OpenAI API key and database credentials
3. **Follow the roadmap sequentially**: Each phase builds on the previous one
4. **Test frequently**: Validate each component before moving to the next phase

---

## Estimated Timeline

- **Phase 1-2**: 1-2 days (Setup & Models)
- **Phase 3**: 1 day (Authentication)
- **Phase 4**: 2-3 days (Core tweet generation logic)
- **Phase 5-6**: 1-2 days (API endpoints & main app)
- **Phase 7**: 1-2 days (Testing)
- **Phase 8-9**: 1-2 days (Optimization & Deployment)

**Total: ~7-14 days** depending on experience and complexity

---

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

---

**Happy Coding!** 🎉
