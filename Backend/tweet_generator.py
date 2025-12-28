"""
Tweet Thread Generator using LangChain and OpenAI
Generates engaging tweet threads from topic descriptions

Updated for LangChain 1.x with modern message patterns
"""

import os
import json
import re
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

# LangChain imports (updated for v1.x)
from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage, HumanMessage, AIMessage
from config import settings

# Load environment variables
load_dotenv()


# ============================================
# Tweet Prompt Templates
# ============================================

TWEET_PROMPTS = {
    "professional": """You are a professional social media strategist. Create a professional and informative tweet thread.

Rules:
- Each tweet must be EXACTLY under 280 characters
- Create {tweet_count} tweets that flow naturally
- Use clear, professional language
- Focus on providing value and insights
- Add relevant hashtags only in the last tweet
- Return ONLY a valid JSON array of strings, nothing else

Topic: {topic}

Return format: ["Tweet 1 text here", "Tweet 2 text here", ...]""",

    "casual": """You are a friendly social media content creator. Create a casual and conversational tweet thread.

Rules:
- Each tweet must be EXACTLY under 280 characters
- Create {tweet_count} tweets that flow naturally
- Use friendly, conversational tone
- Include personal touches and relatability
- Add appropriate emojis sparingly (1-2 per tweet max)
- Return ONLY a valid JSON array of strings, nothing else

Topic: {topic}

Return format: ["Tweet 1 text here", "Tweet 2 text here", ...]""",

    "humorous": """You are a witty social media personality. Create an entertaining and humorous tweet thread.

Rules:
- Each tweet must be EXACTLY under 280 characters
- Create {tweet_count} tweets that flow naturally
- Use humor, wit, and clever observations
- Keep it lighthearted but informative
- Add relevant emojis to enhance humor
- Return ONLY a valid JSON array of strings, nothing else

Topic: {topic}

Return format: ["Tweet 1 text here", "Tweet 2 text here", ...]""",

    "engaging": """You are a social media expert specializing in engagement. Create a highly engaging tweet thread.

Rules:
- Each tweet must be EXACTLY under 280 characters
- Create {tweet_count} tweets that flow naturally
- Use hooks, curiosity gaps, and strong conclusions
- Make it shareable and thought-provoking
- Include strategic emojis for emphasis
- Return ONLY a valid JSON array of strings, nothing else

Topic: {topic}

Return format: ["Tweet 1 text here", "Tweet 2 text here", ...]""",

    "educational": """You are an educational content creator. Create an informative and educational tweet thread.

Rules:
- Each tweet must be EXACTLY under 280 characters
- Create {tweet_count} tweets that flow naturally
- Break down complex topics into simple explanations
- Use clear examples and analogies
- End with key takeaways or action items
- Return ONLY a valid JSON array of strings, nothing else

Topic: {topic}

Return format: ["Tweet 1 text here", "Tweet 2 text here", ...]"""
}


# ============================================
# Initialize Chat Model
# ============================================

def get_chat_model(temperature: float = 0.7):
    """
    Initialize and return chat model using init_chat_model
    
    This is the recommended way to initialize models in LangChain 1.x
    as it provides a unified interface across providers.

    Args:
        temperature: Model temperature (0.0 to 1.0)
                    Lower = more focused, Higher = more creative

    Returns:
        ChatModel instance
    """
    # Set API key in environment if not already set
    if settings.OPENAI_API_KEY and not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
    
    return init_chat_model(
        model="gpt-4o-mini",  # or "gpt-4o" for better quality
        model_provider="openai",
        temperature=temperature,
        max_tokens=1000
    )


# ============================================
# Tweet Generation Functions
# ============================================

def validate_tweet_length(tweet: str, max_length: int = 280) -> bool:
    """
    Validate if a tweet is within the character limit

    Args:
        tweet: Tweet text to validate
        max_length: Maximum allowed characters (default: 280)

    Returns:
        True if valid, False otherwise
    """
    return len(tweet) <= max_length


def add_thread_numbering(tweets: List[str]) -> List[str]:
    """
    Add thread numbering to tweets (1/n, 2/n, etc.)

    Args:
        tweets: List of tweet texts

    Returns:
        List of tweets with thread numbers added
    """
    total = len(tweets)
    numbered_tweets = []

    for i, tweet in enumerate(tweets, 1):
        # Add numbering at the beginning
        thread_number = f"[{i}/{total}] "

        # Check if adding numbering exceeds character limit
        if len(thread_number + tweet) <= 280:
            numbered_tweets.append(thread_number + tweet)
        else:
            # If it exceeds, try to trim the tweet
            max_tweet_length = 280 - len(thread_number)
            trimmed_tweet = tweet[:max_tweet_length-3] + "..."
            numbered_tweets.append(thread_number + trimmed_tweet)

    return numbered_tweets


def parse_tweet_response(response_text: str) -> List[str]:
    """
    Parse the LLM response to extract tweets

    Args:
        response_text: Raw response from LLM

    Returns:
        List of tweet strings

    Raises:
        ValueError: If response cannot be parsed
    """
    # Try to find JSON array in the response
    try:
        # First, try direct JSON parsing
        tweets = json.loads(response_text)
        if isinstance(tweets, list):
            return tweets
    except json.JSONDecodeError:
        pass

    # Try to extract JSON array using regex
    json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
    if json_match:
        try:
            tweets = json.loads(json_match.group(0))
            if isinstance(tweets, list):
                return tweets
        except json.JSONDecodeError:
            pass

    # If all parsing fails, raise error
    raise ValueError("Could not parse tweets from LLM response")


def generate_tweet_thread(
    topic: str,
    tone: Optional[str] = "engaging",
    max_tweets: int = 5,
    add_numbering: bool = True,
    temperature: float = 0.7
) -> Dict[str, Any]:
    """
    Generate a tweet thread on a given topic using LangChain and OpenAI

    Args:
        topic: The topic/description for the tweet thread
        tone: Tone of the thread (professional, casual, humorous, engaging, educational)
        max_tweets: Maximum number of tweets to generate (1-20)
        add_numbering: Whether to add thread numbering (1/n, 2/n, etc.)
        temperature: Model temperature for creativity (0.0-1.0)

    Returns:
        Dictionary with:
            - tweets: List of generated tweet texts
            - tweet_count: Number of tweets generated
            - tone: Tone used
            - topic: Original topic

    Raises:
        ValueError: If invalid parameters or generation fails
        Exception: If OpenAI API call fails
    """
    # Validate inputs
    if not topic or len(topic.strip()) < 10:
        raise ValueError("Topic must be at least 10 characters long")

    if max_tweets < 1 or max_tweets > 20:
        raise ValueError("max_tweets must be between 1 and 20")

    # Get the appropriate prompt template
    tone = tone.lower() if tone else "engaging"
    if tone not in TWEET_PROMPTS:
        tone = "engaging"  # Default to engaging if invalid tone

    prompt_template = TWEET_PROMPTS[tone]

    # Initialize the model
    model = get_chat_model(temperature=temperature)

    try:
        # Create messages using modern LangChain message objects
        # SystemMessage: Sets the model's behavior and context
        # HumanMessage: The user's request
        messages = [
            SystemMessage(content=prompt_template.format(
                topic=topic,
                tweet_count=max_tweets
            )),
            HumanMessage(content=f"Generate a {max_tweets}-tweet thread about: {topic}")
        ]

        # Invoke the model - returns AIMessage
        response = model.invoke(messages)

        # Access the text content from AIMessage
        # In LangChain 1.x, you can use .text property or .content
        response_text = response.text if hasattr(response, 'text') else response.content

        # Parse the response
        tweets = parse_tweet_response(response_text)

        # Validate tweet lengths
        valid_tweets = []
        for tweet in tweets:
            if validate_tweet_length(tweet):
                valid_tweets.append(tweet)
            else:
                # Trim tweet if it's too long
                valid_tweets.append(tweet[:277] + "...")

        # Add thread numbering if requested
        if add_numbering and len(valid_tweets) > 1:
            valid_tweets = add_thread_numbering(valid_tweets)

        # Ensure we don't exceed max_tweets
        if len(valid_tweets) > max_tweets:
            valid_tweets = valid_tweets[:max_tweets]

        return {
            "tweets": valid_tweets,
            "tweet_count": len(valid_tweets),
            "tone": tone,
            "topic": topic
        }

    except Exception as e:
        raise Exception(f"Failed to generate tweets: {str(e)}")


def generate_simple_thread(topic: str) -> List[str]:
    """
    Simple wrapper to generate a tweet thread with default settings

    Args:
        topic: The topic for the tweet thread

    Returns:
        List of tweet strings
    """
    result = generate_tweet_thread(topic)
    return result["tweets"]


# ============================================
# Alternative: Using Dictionary Format
# ============================================

def generate_tweet_thread_dict_format(
    topic: str,
    tone: Optional[str] = "engaging",
    max_tweets: int = 5,
    temperature: float = 0.7
) -> Dict[str, Any]:
    """
    Alternative implementation using OpenAI chat completions format (dict messages)
    
    LangChain 1.x supports both message objects and dictionary format.
    This shows the dictionary approach for compatibility with existing code.
    """
    tone = tone.lower() if tone else "engaging"
    if tone not in TWEET_PROMPTS:
        tone = "engaging"

    prompt_template = TWEET_PROMPTS[tone]
    model = get_chat_model(temperature=temperature)

    # Using dictionary format instead of message objects
    messages = [
        {
            "role": "system",
            "content": prompt_template.format(topic=topic, tweet_count=max_tweets)
        },
        {
            "role": "user", 
            "content": f"Generate a {max_tweets}-tweet thread about: {topic}"
        }
    ]

    response = model.invoke(messages)
    response_text = response.text if hasattr(response, 'text') else response.content
    tweets = parse_tweet_response(response_text)

    return {
        "tweets": tweets[:max_tweets],
        "tweet_count": len(tweets[:max_tweets]),
        "tone": tone,
        "topic": topic
    }


# ============================================
# Testing Function
# ============================================

def test_tweet_generator():
    """
    Test function to verify tweet generation works
    """
    print("Testing Tweet Generator (LangChain 1.x)...")
    print("=" * 60)

    test_topic = "The importance of learning Python for data science and machine learning in 2024"

    print(f"\nTopic: {test_topic}\n")

    # Test different tones
    tones = ["professional", "casual", "engaging"]

    for tone in tones:
        print(f"\n{'='*50}")
        print(f"Tone: {tone.upper()}")
        print('='*50)

        try:
            result = generate_tweet_thread(
                topic=test_topic,
                tone=tone,
                max_tweets=5,
                add_numbering=True
            )

            for tweet in result["tweets"]:
                print(f"\n{tweet}")
                print(f"Length: {len(tweet)} characters")

            print(f"\nTotal tweets: {result['tweet_count']}")

        except Exception as e:
            print(f"Error: {e}")


# ============================================
# Main Execution
# ============================================

if __name__ == "__main__":
    # Run test if executed directly
    test_tweet_generator()