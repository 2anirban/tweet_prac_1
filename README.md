# 🐦 Tweet Generator API

> AI-powered tweet thread generator using FastAPI, LangChain, and OpenAI GPT models

Generate engaging, professional tweet threads from any topic with just one API call. Perfect for content creators, marketers, and social media managers.

---

## ✨ Features

- 🤖 **AI-Powered Generation** - Uses OpenAI's GPT models via LangChain
- 🎨 **5 Tone Options** - Professional, casual, humorous, engaging, educational
- 🔐 **Secure Authentication** - JWT-based user authentication with bcrypt password hashing
- 📊 **History & Analytics** - Track all generated threads with detailed statistics
- ⚡ **Fast & Reliable** - Optimized for performance with async operations
- 🔄 **Auto Thread Numbering** - Automatic [1/n], [2/n] formatting
- 📏 **Character Limit Validation** - Ensures all tweets are ≤280 characters
- 🗄️ **Database Persistence** - SQLAlchemy ORM with SQLite (easy PostgreSQL/MySQL migration)
- 📖 **Interactive Documentation** - Auto-generated Swagger UI and ReDoc

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd Prac
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

Create `Backend/.env`:
```env
DATABASE_URL=sqlite:///./test.db
OPENAI_API_KEY=sk-your-openai-api-key-here
SECRET_KEY=your-secret-key-here
```

### 3. Run the Server

```bash
cd Backend
python main.py
```

### 4. Open Swagger UI

Visit: `http://localhost:8000/docs`

**See [QUICK_START.md](QUICK_START.md) for detailed instructions.**

---

## 📖 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/register` | Register new user | ❌ |
| POST | `/api/auth/login` | Login and get JWT token | ❌ |
| GET | `/api/auth/me` | Get current user profile | ✅ |
| GET | `/api/auth/verify` | Verify token validity | ✅ |

### Tweet Generation

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/tweets/generate` | Generate tweet thread | ✅ |
| GET | `/api/tweets/history` | Get user's tweet history | ✅ |
| GET | `/api/tweets/{id}` | Get specific thread | ✅ |
| DELETE | `/api/tweets/{id}` | Delete thread | ✅ |
| GET | `/api/tweets/analytics/stats` | Get user statistics | ✅ |

### Health & Info

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | API information | ❌ |
| GET | `/api/health` | Health check | ❌ |

---

## 💡 Usage Examples

### Generate a Tweet Thread

```python
import requests

# Login
response = requests.post("http://localhost:8000/api/auth/login", json={
    "email": "user@example.com",
    "password": "password123"
})
token = response.json()["access_token"]

# Generate tweets
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(
    "http://localhost:8000/api/tweets/generate",
    headers=headers,
    json={
        "topic": "The future of artificial intelligence in healthcare",
        "tone": "professional",
        "max_tweets": 5
    }
)

tweets = response.json()
for tweet in tweets["tweets"]:
    print(tweet)
```

### Example Output

```
[1/5] AI is revolutionizing healthcare through predictive analytics,
personalized treatment plans, and automated diagnostics. Here's what you need to know.

[2/5] Predictive analytics helps identify high-risk patients before conditions worsen,
enabling preventive care and reducing hospital readmissions by up to 30%.

[3/5] Personalized medicine uses AI to analyze genetic data, creating treatment
plans tailored to individual patients' unique biological profiles.

[4/5] Automated diagnostic tools can detect diseases like cancer and diabetes
earlier than traditional methods, improving patient outcomes significantly.

[5/5] The future of healthcare lies in the synergy between human expertise and
AI capabilities. #HealthTech #AIinHealthcare
```

---

## 🎨 Available Tones

| Tone | Best For | Characteristics |
|------|----------|-----------------|
| **Professional** | Business content, industry insights | Clear, formal, value-focused |
| **Casual** | Personal stories, community building | Friendly, conversational, relatable |
| **Humorous** | Entertainment, viral content | Witty, lighthearted, engaging |
| **Engaging** | Maximum interaction, thought leadership | Hooks, curiosity gaps, shareable |
| **Educational** | Teaching, tutorials, explanations | Clear examples, structured learning |

---

## 🏗️ Architecture

```
┌─────────────┐
│   Client    │
│ (Frontend)  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│      FastAPI Application        │
│  ┌──────────────────────────┐   │
│  │  Authentication Router   │   │
│  │  (JWT, Password Hashing) │   │
│  └──────────────────────────┘   │
│  ┌──────────────────────────┐   │
│  │    Tweet Router          │   │
│  │  (Generation, History)   │   │
│  └──────────────────────────┘   │
└────────┬────────────────┬────────┘
         │                │
         ▼                ▼
┌────────────────┐  ┌─────────────┐
│   SQLAlchemy   │  │  LangChain  │
│   (Database)   │  │   + OpenAI  │
│   - Users      │  │  (AI Engine)│
│   - Threads    │  └─────────────┘
│   - History    │
└────────────────┘
```

---

## 📁 Project Structure

```
Prac/
├── Backend/
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration settings
│   ├── database.py             # Database connection
│   ├── models.py               # SQLAlchemy ORM models
│   ├── schemas.py              # Pydantic validation schemas
│   ├── tweet_generator.py      # LangChain + OpenAI logic
│   ├── routers/
│   │   ├── auth.py            # Authentication endpoints
│   │   └── tweets.py          # Tweet generation endpoints
│   └── utils/
│       └── auth_utils.py      # JWT & password utilities
│
├── .env                        # Environment variables (not in git)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── QUICK_START.md             # Quick start guide
├── ROADMAP.md                 # Development roadmap
├── AUTH_GUIDE.md              # Authentication guide
├── TWEET_GENERATOR_GUIDE.md   # Tweet generator guide
└── DATABASE_MODELS_GUIDE.md   # Database models guide
```

---

## 🔧 Technologies

### Backend
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### AI/ML
- **LangChain** - LLM application framework
- **OpenAI GPT** - Language model
- **langchain-openai** - OpenAI integration

### Security
- **python-jose** - JWT tokens
- **passlib** - Password hashing (bcrypt)
- **CORS** - Cross-origin resource sharing

### Database
- **SQLite** - Default (development)
- **PostgreSQL** - Production (optional)
- **MySQL** - Production (optional)

---

## 📊 Database Schema

### User
- `id` - Primary key
- `email` - Unique email
- `username` - Unique username
- `hashed_password` - Bcrypt hash
- `is_active` - Account status
- `created_at` - Registration date
- `updated_at` - Last update

### TweetThread
- `id` - Primary key
- `user_id` - Foreign key to User
- `topic` - Input topic
- `thread_content` - JSON array of tweets
- `tweet_count` - Number of tweets
- `created_at` - Generation date
- `updated_at` - Last update

### TweetHistory
- `id` - Primary key
- `thread_id` - Foreign key to TweetThread
- `user_id` - Foreign key to User
- `generation_params` - Generation parameters (JSON)
- `processing_time` - Time in milliseconds
- `status` - success/failed
- `created_at` - Record date

---

## 🔐 Security Features

- ✅ **Password Hashing** - Bcrypt with salt
- ✅ **JWT Authentication** - Token-based auth
- ✅ **Token Expiration** - 30 minutes default
- ✅ **Input Validation** - Pydantic schemas
- ✅ **SQL Injection Protection** - SQLAlchemy ORM
- ✅ **CORS Configuration** - Configurable origins
- ✅ **Email Validation** - EmailStr type
- ✅ **Protected Routes** - Dependency injection

---

## 🧪 Testing

### Manual Testing (Swagger UI)
1. Visit `http://localhost:8000/docs`
2. Try the endpoints interactively
3. Use the "Authorize" button for protected routes

### Python Testing
```python
# Test tweet generator
cd Backend
python tweet_generator.py
```

### API Testing (cURL)
See [QUICK_START.md](QUICK_START.md) for cURL examples.

---

## 🚢 Deployment

### Environment Variables (Production)
```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
OPENAI_API_KEY=sk-your-production-key
SECRET_KEY=very-long-random-secure-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=https://yourdomain.com
```

### Docker Deployment
```bash
# Build image
docker build -t tweet-generator .

# Run container
docker run -p 8000:8000 --env-file .env tweet-generator
```

### Platform-Specific Guides
- **Heroku** - See deployment docs
- **AWS** - Use Elastic Beanstalk or ECS
- **Google Cloud** - Use App Engine or Cloud Run
- **Azure** - Use App Service

---

## 📈 Performance

- **Average Response Time**: ~2-3 seconds for tweet generation
- **Concurrent Requests**: Supports async operations
- **Database**: Optimized with indexes
- **Caching**: Ready for Redis integration
- **Rate Limiting**: Configurable (future feature)

---

## 🛠️ Development

### Run in Development Mode
```bash
cd Backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Database Migrations (Alembic)
```bash
# Initialize
alembic init migrations

# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```

### Code Formatting
```bash
# Install formatter
pip install black

# Format code
black Backend/
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [QUICK_START.md](QUICK_START.md) | Get started in 5 minutes |
| [ROADMAP.md](ROADMAP.md) | Development roadmap |
| [AUTH_GUIDE.md](AUTH_GUIDE.md) | Authentication system |
| [TWEET_GENERATOR_GUIDE.md](TWEET_GENERATOR_GUIDE.md) | Tweet generation |
| [DATABASE_MODELS_GUIDE.md](DATABASE_MODELS_GUIDE.md) | Database models |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- **FastAPI** - For the amazing web framework
- **LangChain** - For LLM application framework
- **OpenAI** - For GPT models
- **SQLAlchemy** - For the robust ORM

---

## 📧 Contact

For support or questions:
- Email: support@tweetgenerator.com
- GitHub Issues: [Create an issue](https://github.com/yourusername/tweet-generator/issues)

---

**Built with ❤️ using FastAPI, LangChain, and OpenAI**

**Star ⭐ this repository if you find it helpful!**
