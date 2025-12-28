"""
Tweet Router
Handles tweet generation, history, and management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import time

from database import get_db
from models import User, TweetThread, TweetHistory
from schemas import (
    TweetGenerationRequest,
    TweetGenerationResponse,
    TweetThreadResponse,
    UserTweetHistoryResponse,
    TweetHistoryResponse
)
from routers.auth import get_current_active_user
from tweet_generator import generate_tweet_thread

# Create router
router = APIRouter(
    prefix="/tweets",
    tags=["Tweets"]
)


# ============================================
# Tweet Generation Endpoint
# ============================================

@router.post("/generate", response_model=TweetGenerationResponse, status_code=status.HTTP_201_CREATED)
async def generate_tweets(
    request: TweetGenerationRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Generate a tweet thread from a topic (requires authentication)

    - **topic**: Topic description (10-500 characters)
    - **tone**: Optional tone (professional, casual, humorous, engaging, educational)
    - **max_tweets**: Optional max number of tweets (1-20, default: 5)

    Returns the generated tweet thread
    """
    try:
        # Start timer for processing time
        start_time = time.time()

        # Generate tweet thread using LangChain + OpenAI
        result = generate_tweet_thread(
            topic=request.topic,
            tone=request.tone or "engaging",
            max_tweets=request.max_tweets or 5,
            add_numbering=True,
            temperature=0.7
        )

        # Calculate processing time
        processing_time = int((time.time() - start_time) * 1000)  # milliseconds

        # Save tweet thread to database
        thread_content = json.dumps(result["tweets"])
        db_thread = TweetThread(
            user_id=current_user.id,
            topic=request.topic,
            thread_content=thread_content,
            tweet_count=result["tweet_count"]
        )
        db.add(db_thread)
        db.commit()
        db.refresh(db_thread)

        # Save generation history
        generation_params = json.dumps({
            "tone": result["tone"],
            "max_tweets": request.max_tweets or 5,
            "temperature": 0.7
        })

        history_record = TweetHistory(
            thread_id=db_thread.id,
            user_id=current_user.id,
            generation_params=generation_params,
            processing_time=processing_time,
            status="success"
        )
        db.add(history_record)
        db.commit()

        # Return response
        return TweetGenerationResponse(
            tweets=result["tweets"],
            tweet_count=result["tweet_count"],
            topic=result["topic"]
        )

    except ValueError as e:
        # Validation errors from tweet_generator
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Log error and save failed history
        try:
            history_record = TweetHistory(
                thread_id=None,
                user_id=current_user.id,
                generation_params=json.dumps({"error": str(e)}),
                processing_time=0,
                status="failed"
            )
            db.add(history_record)
            db.commit()
        except:
            pass  # Don't fail if history save fails

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Tweet generation failed: {str(e)}"
        )


# ============================================
# Tweet History Endpoints
# ============================================

@router.get("/history", response_model=UserTweetHistoryResponse)
async def get_user_tweet_history(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get user's tweet generation history with pagination (requires authentication)

    - **page**: Page number (starts at 1)
    - **page_size**: Number of items per page (1-100)

    Returns paginated list of tweet threads
    """
    # Calculate offset
    offset = (page - 1) * page_size

    # Query user's tweet threads
    threads = db.query(TweetThread)\
        .filter(TweetThread.user_id == current_user.id)\
        .order_by(TweetThread.created_at.desc())\
        .offset(offset)\
        .limit(page_size)\
        .all()

    # Get total count
    total_count = db.query(TweetThread)\
        .filter(TweetThread.user_id == current_user.id)\
        .count()

    # Parse threads (convert thread_content JSON to list)
    parsed_threads = [
        TweetThreadResponse.from_orm_with_parsed_tweets(thread)
        for thread in threads
    ]

    return UserTweetHistoryResponse(
        threads=parsed_threads,
        total_count=total_count,
        page=page,
        page_size=page_size
    )


# ============================================
# Single Tweet Thread Endpoints
# ============================================

@router.get("/{thread_id}", response_model=TweetThreadResponse)
async def get_tweet_thread(
    thread_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific tweet thread by ID (requires authentication)

    - **thread_id**: ID of the tweet thread

    Returns the tweet thread if it exists and belongs to the user
    """
    # Query the thread
    thread = db.query(TweetThread)\
        .filter(TweetThread.id == thread_id)\
        .first()

    # Check if thread exists
    if not thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tweet thread with ID {thread_id} not found"
        )

    # Verify ownership
    if thread.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this tweet thread"
        )

    # Return parsed thread
    return TweetThreadResponse.from_orm_with_parsed_tweets(thread)


@router.delete("/{thread_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tweet_thread(
    thread_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a tweet thread by ID (requires authentication)

    - **thread_id**: ID of the tweet thread to delete

    Returns 204 No Content on success
    """
    # Query the thread
    thread = db.query(TweetThread)\
        .filter(TweetThread.id == thread_id)\
        .first()

    # Check if thread exists
    if not thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tweet thread with ID {thread_id} not found"
        )

    # Verify ownership
    if thread.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this tweet thread"
        )

    # Delete the thread (cascade will delete related history records)
    db.delete(thread)
    db.commit()

    return None  # 204 No Content


# ============================================
# Analytics Endpoints
# ============================================

@router.get("/analytics/stats", response_model=dict)
async def get_user_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get user's tweet generation statistics (requires authentication)

    Returns statistics about the user's tweet generation activity
    """
    # Total threads generated
    total_threads = db.query(TweetThread)\
        .filter(TweetThread.user_id == current_user.id)\
        .count()

    # Total tweets generated
    total_tweets = db.query(TweetThread)\
        .filter(TweetThread.user_id == current_user.id)\
        .with_entities(TweetThread.tweet_count)\
        .all()
    total_tweet_count = sum(count[0] for count in total_tweets)

    # Success/failure counts
    total_generations = db.query(TweetHistory)\
        .filter(TweetHistory.user_id == current_user.id)\
        .count()

    successful_generations = db.query(TweetHistory)\
        .filter(TweetHistory.user_id == current_user.id)\
        .filter(TweetHistory.status == "success")\
        .count()

    failed_generations = db.query(TweetHistory)\
        .filter(TweetHistory.user_id == current_user.id)\
        .filter(TweetHistory.status == "failed")\
        .count()

    # Average processing time
    avg_processing_time_result = db.query(TweetHistory)\
        .filter(TweetHistory.user_id == current_user.id)\
        .filter(TweetHistory.status == "success")\
        .with_entities(TweetHistory.processing_time)\
        .all()

    if avg_processing_time_result:
        valid_times = [t[0] for t in avg_processing_time_result if t[0] is not None]
        avg_processing_time = sum(valid_times) / len(valid_times) if valid_times else 0
    else:
        avg_processing_time = 0

    return {
        "total_threads": total_threads,
        "total_tweets": total_tweet_count,
        "total_generations": total_generations,
        "successful_generations": successful_generations,
        "failed_generations": failed_generations,
        "success_rate": round(successful_generations / total_generations * 100, 2) if total_generations > 0 else 0,
        "avg_processing_time_ms": round(avg_processing_time, 2)
    }


# ============================================
# Health Check Endpoint
# ============================================

@router.get("/health", response_model=dict, tags=["Health"])
async def health_check():
    """
    Health check endpoint (public)

    Returns the service status
    """
    return {
        "status": "healthy",
        "service": "Tweet Generator API",
        "version": "1.0.0"
    }
