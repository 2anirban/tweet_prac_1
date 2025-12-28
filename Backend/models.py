from database import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime



class User(Base):
    __tablename__="users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)  
    phone_number = Column(String, nullable=True)
    address = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)   
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    #Relationships
    tweets_threads = relationship("TweetThread",back_populates="user",cascade="all, delete-orphan")
    tweet_histories = relationship("TweetHistory",back_populates="user",cascade="all, delete-orphan")

class TweetThread(Base):
    __tablename__="tweet_threads"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic = Column(String, index=True, nullable=False)
    thread_content = Column(Text, nullable=False)  # JSON string of tweets
    tweet_count = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    #Relationships
    user = relationship("User", back_populates="tweets_threads")
    tweet_histories = relationship("TweetHistory", back_populates="tweet_thread", cascade="all, delete-orphan") 

class TweetHistory(Base):
    __tablename__ = "tweet_histories"

    id = Column(Integer, primary_key=True, index=True)
    thread_id = Column(Integer, ForeignKey('tweet_threads.id'), nullable=False)  # ForeignKey to TweetThread
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # ForeignKey to User
    generation_params = Column(Text, nullable=True)  # Storing as Text/JSON for simplicity (optional)
    processing_time = Column(Integer, nullable=True)  # Time in milliseconds (optional)
    status = Column(String, nullable=False)  # e.g., "success" or "failed"
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="tweet_histories")
    tweet_thread = relationship("TweetThread", back_populates="tweet_histories")

