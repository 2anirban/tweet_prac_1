"""
Tweet Generator Backend - Main Application
FastAPI application for generating tweet threads using LangChain and OpenAI
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import logging
import time

from database import engine  # Used by admin panel
from routers import auth, tweets
from config import settings
from admin import create_admin

# ============================================
# Configure Logging
# ============================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================
# Lifespan Events
# ============================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for startup and shutdown
    """
    # Startup
    logger.info("Starting Tweet Generator API...")

    # Database tables are now managed by Alembic migrations
    # To create/update tables, use: alembic upgrade head
    logger.info("Database ready (tables managed by Alembic)")

    logger.info("Tweet Generator API started successfully")

    yield

    # Shutdown
    logger.info("Shutting down Tweet Generator API...")
    logger.info("Tweet Generator API shut down complete")


# ============================================
# Initialize FastAPI Application
# ============================================

app = FastAPI(
    title="Tweet Generator API",
    description="""
    🐦 **Tweet Generator API** - AI-Powered Tweet Thread Generator

    Generate engaging tweet threads from any topic using OpenAI's GPT models and LangChain.

    ## Features

    * 🔐 **Secure Authentication** - JWT-based user authentication
    * 🤖 **AI-Powered Generation** - Uses OpenAI GPT models via LangChain
    * 🎨 **Multiple Tones** - Professional, casual, humorous, engaging, educational
    * 📊 **History & Analytics** - Track your tweet generation history
    * ⚡ **Fast & Reliable** - Optimized for performance

    ## Authentication

    Most endpoints require authentication. Use the `/auth/register` endpoint to create an account,
    then `/auth/login` to get an access token. Click the "Authorize" button to add your token.

    ## Rate Limits

    Please use the API responsibly. Rate limits may apply.
    """,
    version="1.0.0",
    contact={
        "name": "Tweet Generator Team",
        "email": "support@tweetgenerator.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)


# ============================================
# CORS Configuration
# ============================================

# Configure CORS
origins = settings.CORS_ORIGINS or [
    "http://localhost:3000",      # React default
    "http://localhost:5173",      # Vite default
    "http://localhost:8080",      # Vue default
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# Admin Panel Configuration
# ============================================

# Initialize admin panel (accessible at /admin)
admin = create_admin(app)
logger.info("Admin panel initialized at /admin")


# ============================================
# Request Logging Middleware
# ============================================

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Log all incoming requests
    """
    start_time = time.time()

    # Log request
    logger.info(f"Request: {request.method} {request.url.path}")

    # Process request
    response = await call_next(request)

    # Calculate processing time
    process_time = time.time() - start_time

    # Add custom header
    response.headers["X-Process-Time"] = str(process_time)

    # Log response
    logger.info(
        f"Response: {request.method} {request.url.path} "
        f"- Status: {response.status_code} "
        f"- Time: {process_time:.3f}s"
    )

    return response


# ============================================
# Exception Handlers
# ============================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle validation errors
    """
    logger.warning(f"Validation error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "message": "Validation error in request data"
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle general exceptions
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "message": "An unexpected error occurred. Please try again later."
        }
    )


# ============================================
# Include Routers
# ============================================

# Include authentication router
app.include_router(
    auth.router,
    prefix="/api",
    tags=["Authentication"]
)

# Include tweets router
app.include_router(
    tweets.router,
    prefix="/api",
    tags=["Tweets"]
)


# ============================================
# Root Endpoints
# ============================================

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - API information
    """
    return {
        "message": "Welcome to Tweet Generator API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/api/tweets/health"
    }


@app.get("/api/health", tags=["Health"])
async def api_health():
    """
    API health check endpoint
    """
    return {
        "status": "healthy",
        "service": "Tweet Generator API",
        "version": "1.0.0",
        "database": "connected"
    }


# ============================================
# Run Application
# ============================================

if __name__ == "__main__":
    import uvicorn

    logger.info("Starting development server...")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
