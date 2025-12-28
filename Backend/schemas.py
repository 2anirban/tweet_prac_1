# ### 2.2 Pydantic Schemas ([schemas.py](Backend/schemas.py))
# Define request/response schemas:

# - [ ] **User Schemas**
#   - `UserCreate` (registration)
#   - `UserLogin` (authentication)
#   - `UserResponse` (safe user data)
#   - `Token` (JWT token response)

# - [ ] **Tweet Schemas**
#   - `TweetGenerationRequest` (topic, optional params)
#   - `TweetGenerationResponse` (generated thread)
#   - `TweetThreadResponse` (thread with metadata)
#   - `TweetHistoryResponse` (user's tweet history)


from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

# ============================================
# User Schemas
# ============================================

class UserCreate(BaseModel):
    """Schema for user registration"""
    username: str = Field(..., min_length=3, max_length=50, description="Username (3-50 characters)")
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8, description="Password (minimum 8 characters)")


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema for safe user data (never expose password!)"""
    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)  # Enables ORM mode for SQLAlchemy


# ============================================
# Authentication Schemas
# ============================================

class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for JWT token payload (decoded token)"""
    email: Optional[str] = None
    user_id: Optional[int] = None


# ============================================
# Tweet Generation Schemas
# ============================================

class TweetGenerationRequest(BaseModel):
    """Schema for tweet generation request"""
    topic: str = Field(..., min_length=10, max_length=500, description="Topic description (10-500 characters)")
    # Optional parameters for customization (future enhancements)
    tone: Optional[str] = Field(None, description="Tone: professional, casual, humorous, etc.")
    max_tweets: Optional[int] = Field(5, ge=1, le=20, description="Maximum number of tweets in thread")


class TweetGenerationResponse(BaseModel):
    """Schema for generated tweet thread (immediate response)"""
    tweets: List[str] = Field(..., description="List of tweets in the thread")
    tweet_count: int = Field(..., description="Number of tweets generated")
    topic: str = Field(..., description="Original topic")


# ============================================
# Tweet Thread Schemas (Database Records)
# ============================================

class TweetThreadBase(BaseModel):
    """Base schema for TweetThread"""
    topic: str
    tweet_count: int


class TweetThreadCreate(TweetThreadBase):
    """Schema for creating a tweet thread in database"""
    thread_content: str  # JSON string of tweets
    user_id: int


class TweetThreadResponse(BaseModel):
    """Schema for tweet thread response (from database)"""
    id: int
    user_id: int
    topic: str
    tweets: List[str] = Field(..., description="Parsed tweets from thread_content")
    tweet_count: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm_with_parsed_tweets(cls, db_thread):
        """Custom constructor to parse thread_content JSON"""
        import json
        tweets = json.loads(db_thread.thread_content) if db_thread.thread_content else []
        return cls(
            id=db_thread.id,
            user_id=db_thread.user_id,
            topic=db_thread.topic,
            tweets=tweets,
            tweet_count=db_thread.tweet_count,
            created_at=db_thread.created_at,
            updated_at=db_thread.updated_at
        )


# ============================================
# Tweet History Schemas
# ============================================

class TweetHistoryResponse(BaseModel):
    """Schema for individual tweet history record"""
    id: int
    thread_id: int
    user_id: int
    status: str
    processing_time: Optional[int] = None
    generation_params: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserTweetHistoryResponse(BaseModel):
    """Schema for user's complete tweet history"""
    threads: List[TweetThreadResponse]
    total_count: int
    page: int = 1
    page_size: int = 10
    