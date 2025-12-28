# Tweet Generator Guide

Complete guide to understanding the LangChain-powered tweet thread generator.

---

## Table of Contents

1. [Overview](#overview)
2. [How It Works](#how-it-works)
3. [Tweet Tones](#tweet-tones)
4. [Core Functions](#core-functions)
5. [Usage Examples](#usage-examples)
6. [API Integration](#api-integration)
7. [Testing](#testing)
8. [Customization](#customization)

---

## Overview

The tweet generator uses **LangChain** and **OpenAI's GPT** to create engaging tweet threads from topic descriptions.

**Key Features:**
- ✅ 5 different tone options (professional, casual, humorous, engaging, educational)
- ✅ Automatic 280-character limit validation
- ✅ Thread numbering (1/n, 2/n, etc.)
- ✅ Customizable tweet count (1-20 tweets)
- ✅ JSON response parsing
- ✅ Error handling and validation

**Technology Stack:**
- **LangChain**: Framework for LLM applications
- **OpenAI GPT-4o-mini**: Language model (can use GPT-4 for better quality)
- **Python**: Core programming language

---

## How It Works

### High-Level Flow

```
User Topic Input
      ↓
Select Tone & Parameters
      ↓
Format Prompt Template
      ↓
Send to OpenAI via LangChain
      ↓
Receive JSON Response
      ↓
Parse & Validate Tweets
      ↓
Add Thread Numbering
      ↓
Return Tweet Thread
```

### Detailed Process

1. **Input Validation**
   - Topic must be at least 10 characters
   - Tweet count must be 1-20
   - Tone must be valid (defaults to "engaging")

2. **Prompt Construction**
   - Select appropriate prompt template based on tone
   - Inject topic and tweet count into template
   - Create system and human messages

3. **LLM Invocation**
   - Initialize ChatOpenAI model
   - Send messages to OpenAI API
   - Receive response with tweet thread

4. **Response Processing**
   - Parse JSON array from response
   - Validate each tweet is ≤280 characters
   - Trim tweets that are too long

5. **Thread Formatting**
   - Add thread numbering [1/n], [2/n], etc.
   - Ensure numbering doesn't exceed character limit

6. **Return Result**
   - Return dictionary with tweets, count, tone, and topic

---

## Tweet Tones

### 1. Professional

**Best for:** Business content, industry insights, thought leadership

**Characteristics:**
- Clear, professional language
- Focus on value and insights
- Hashtags only in last tweet
- Formal tone

**Example Topic:** "The impact of AI on healthcare industry"

**Sample Output:**
```
[1/5] AI is transforming healthcare delivery through predictive analytics,
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

### 2. Casual

**Best for:** Personal stories, relatable content, community building

**Characteristics:**
- Friendly, conversational tone
- Personal touches and relatability
- 1-2 emojis per tweet max
- Natural flow

**Example Topic:** "Tips for working from home productively"

**Sample Output:**
```
[1/5] Working from home can be amazing... or a total disaster 😅
Here are the things I learned the hard way about staying productive at home.

[2/5] Set up a dedicated workspace. I used to work from my couch and wondered
why my back hurt all the time. Your future self will thank you! 💼

[3/5] Get dressed in the morning. Yes, really. Pajamas all day sounds fun but
it tricks your brain into "lazy mode." Even jeans make a difference.

[4/5] Take actual lunch breaks away from your desk. I know it's tempting to
eat while working, but your productivity (and digestion) need that break.

[5/5] Set boundaries with family/roommates. A closed door = do not disturb.
Make it clear when you're "at work" even though you're home.
```

---

### 3. Humorous

**Best for:** Entertainment, viral content, lighthearted topics

**Characteristics:**
- Wit and clever observations
- Lighthearted but informative
- Strategic use of humor
- Engaging emojis

**Example Topic:** "Why programmers love coffee so much"

**Sample Output:**
```
[1/5] Let me explain the programmer-coffee relationship in terms you'll understand:
coffee is basically the compiler for human brains ☕👨‍💻

[2/5] Before coffee: "Why isn't this working?"
After coffee: *realizes I forgot a semicolon* "Ah yes, of course" 🤦‍♂️

[3/5] Fun fact: The best code is written between the 2nd and 4th cup of coffee.
Before that? Spaghetti code. After that? Also spaghetti code, but faster.

[4/5] Coffee doesn't actually solve bugs. It just makes you THINK you can solve
them. Which, surprisingly, is enough to actually solve them. Psychology is weird.

[5/5] In conclusion: programmers don't have a coffee addiction, we have a
"staying conscious during meetings" requirement 😴💻
```

---

### 4. Engaging

**Best for:** Maximum interaction, thought leadership, viral potential

**Characteristics:**
- Hooks and curiosity gaps
- Shareable and thought-provoking
- Strong conclusions
- Strategic emphasis

**Example Topic:** "The future of remote work"

**Sample Output:**
```
[1/5] Remote work isn't just a trend. It's a complete reimagining of how work
happens. And most companies are getting it totally wrong. Here's why 🧵

[2/5] Companies think remote work = office work from home. Wrong. It's an
entirely different system that requires new tools, processes, and mindsets.

[3/5] The winners? Companies building async-first cultures. Not "flexible hours"
but true asynchronous collaboration across time zones. Game changer 🚀

[4/5] The losers? Companies forcing "camera on" in every meeting and tracking
mouse movements. They're speedrunning employee burnout.

[5/5] The future belongs to companies that understand this: trust your team to
deliver results, not hours. Output > activity. Always. What's your take? 💭
```

---

### 5. Educational

**Best for:** Teaching, tutorials, explaining complex topics

**Characteristics:**
- Clear explanations
- Examples and analogies
- Structured information
- Actionable takeaways

**Example Topic:** "How blockchain works"

**Sample Output:**
```
[1/5] Let's break down how blockchain actually works, without the jargon.
Think of it like a shared Google Doc that everyone can see but no one can erase.

[2/5] Every "block" is a container of transactions. Think of it like a page
in a ledger. Once the page is full, it gets locked and linked to the previous page.

[3/5] The "chain" part? Each block contains a unique fingerprint (hash) of the
previous block. Change one block, and all the fingerprints change. Tampering = obvious.

[4/5] Why is it secure? Because thousands of computers have identical copies.
To fake a transaction, you'd need to change 51% of all copies simultaneously. Nearly impossible.

[5/5] Key takeaways:
• Decentralized = no single point of failure
• Transparent = everyone sees everything
• Immutable = can't change history
This is why it's revolutionary for trust.
```

---

## Core Functions

### 1. `generate_tweet_thread()`

**Main function** to generate tweet threads.

```python
def generate_tweet_thread(
    topic: str,
    tone: Optional[str] = "engaging",
    max_tweets: int = 5,
    add_numbering: bool = True,
    temperature: float = 0.7
) -> Dict[str, any]:
```

**Parameters:**
- `topic`: Topic description (min 10 characters)
- `tone`: One of: professional, casual, humorous, engaging, educational
- `max_tweets`: Number of tweets to generate (1-20)
- `add_numbering`: Add [1/n] style numbering
- `temperature`: Creativity level (0.0-1.0)
  - 0.0 = Very focused and deterministic
  - 0.7 = Balanced (default)
  - 1.0 = Very creative and random

**Returns:**
```python
{
    "tweets": ["Tweet 1...", "Tweet 2...", ...],
    "tweet_count": 5,
    "tone": "engaging",
    "topic": "Original topic"
}
```

**Example:**
```python
result = generate_tweet_thread(
    topic="The benefits of learning Python for beginners",
    tone="educational",
    max_tweets=5,
    add_numbering=True,
    temperature=0.7
)

print(result["tweets"])
# ["[1/5] Let's talk about...", "[2/5] First benefit...", ...]
```

---

### 2. `generate_simple_thread()`

**Simplified wrapper** for quick tweet generation with defaults.

```python
def generate_simple_thread(topic: str) -> List[str]:
```

**Parameters:**
- `topic`: Topic description

**Returns:**
- List of tweet strings

**Example:**
```python
tweets = generate_simple_thread("Why Python is great for data science")
for tweet in tweets:
    print(tweet)
```

---

### 3. `validate_tweet_length()`

Checks if a tweet is within Twitter's 280-character limit.

```python
def validate_tweet_length(tweet: str, max_length: int = 280) -> bool:
```

**Example:**
```python
tweet = "This is my tweet content"
if validate_tweet_length(tweet):
    print("Valid tweet!")
else:
    print("Too long!")
```

---

### 4. `add_thread_numbering()`

Adds thread numbering to tweets.

```python
def add_thread_numbering(tweets: List[str]) -> List[str]:
```

**Example:**
```python
tweets = ["First tweet", "Second tweet", "Third tweet"]
numbered = add_thread_numbering(tweets)
# Result: ["[1/3] First tweet", "[2/3] Second tweet", "[3/3] Third tweet"]
```

---

### 5. `parse_tweet_response()`

Parses LLM response to extract tweet array.

```python
def parse_tweet_response(response_text: str) -> List[str]:
```

**Handles various response formats:**
- Direct JSON array: `["Tweet 1", "Tweet 2"]`
- JSON with surrounding text: `Here are the tweets: ["Tweet 1", "Tweet 2"]`
- Malformed responses (raises ValueError)

---

## Usage Examples

### Example 1: Basic Usage

```python
from tweet_generator import generate_tweet_thread

# Generate a professional thread
result = generate_tweet_thread(
    topic="The importance of cybersecurity in modern business",
    tone="professional",
    max_tweets=5
)

for tweet in result["tweets"]:
    print(tweet)
    print(f"Length: {len(tweet)}")
    print("-" * 50)
```

### Example 2: Custom Parameters

```python
# More creative, casual thread
result = generate_tweet_thread(
    topic="My journey learning to code at 40",
    tone="casual",
    max_tweets=7,
    add_numbering=True,
    temperature=0.9  # More creative
)
```

### Example 3: Without Numbering

```python
# Generate without thread numbers (good for standalone tweets)
result = generate_tweet_thread(
    topic="Quick tips for better sleep",
    tone="educational",
    max_tweets=3,
    add_numbering=False  # No [1/n] numbering
)
```

### Example 4: Error Handling

```python
try:
    result = generate_tweet_thread(
        topic="AI",  # Too short!
        tone="professional",
        max_tweets=5
    )
except ValueError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"Generation error: {e}")
```

---

## API Integration

### In FastAPI Endpoint

```python
from fastapi import APIRouter, Depends, HTTPException
from tweet_generator import generate_tweet_thread
from schemas import TweetGenerationRequest, TweetGenerationResponse
from routers.auth import get_current_active_user
from models import User

router = APIRouter()

@router.post("/tweets/generate", response_model=TweetGenerationResponse)
async def generate_tweets(
    request: TweetGenerationRequest,
    current_user: User = Depends(get_current_active_user)
):
    try:
        # Generate tweets
        result = generate_tweet_thread(
            topic=request.topic,
            tone=request.tone or "engaging",
            max_tweets=request.max_tweets or 5,
            add_numbering=True,
            temperature=0.7
        )

        # Save to database
        import json
        thread = TweetThread(
            user_id=current_user.id,
            topic=request.topic,
            thread_content=json.dumps(result["tweets"]),
            tweet_count=result["tweet_count"]
        )
        db.add(thread)
        db.commit()

        # Return response
        return TweetGenerationResponse(
            tweets=result["tweets"],
            tweet_count=result["tweet_count"],
            topic=result["topic"]
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")
```

---

## Testing

### Manual Testing

Run the test function directly:

```bash
cd Backend
python tweet_generator.py
```

This will test multiple tones and display results.

### Custom Testing

```python
from tweet_generator import generate_tweet_thread

# Test your own topic
topic = "Your topic here"

result = generate_tweet_thread(
    topic=topic,
    tone="engaging",
    max_tweets=5
)

print(f"Topic: {result['topic']}")
print(f"Tone: {result['tone']}")
print(f"Tweet Count: {result['tweet_count']}\n")

for i, tweet in enumerate(result['tweets'], 1):
    print(f"Tweet {i}:")
    print(tweet)
    print(f"Characters: {len(tweet)}/280")
    print()
```

---

## Customization

### 1. Add New Tone

Edit `TWEET_PROMPTS` in [tweet_generator.py](Backend/tweet_generator.py):

```python
TWEET_PROMPTS = {
    # ... existing tones ...

    "motivational": """You are an inspirational speaker. Create a motivational tweet thread.

Rules:
- Each tweet must be EXACTLY under 280 characters
- Create {tweet_count} tweets that flow naturally
- Use inspirational and empowering language
- Include calls to action
- Add motivational emojis
- Return ONLY a valid JSON array of strings, nothing else

Topic: {topic}

Return format: ["Tweet 1 text here", "Tweet 2 text here", ...]"""
}
```

### 2. Change Model

In `get_chat_model()`:

```python
return ChatOpenAI(
    model="gpt-4",  # Use GPT-4 for better quality (more expensive)
    # or "gpt-3.5-turbo" for faster/cheaper
    temperature=temperature,
    openai_api_key=settings.OPENAI_API_KEY,
    max_tokens=1000
)
```

### 3. Adjust Character Limit

Modify `validate_tweet_length()`:

```python
def validate_tweet_length(tweet: str, max_length: int = 280):
    # Change max_length default to your desired limit
    return len(tweet) <= max_length
```

### 4. Custom Numbering Format

Modify `add_thread_numbering()`:

```python
# Current format: [1/5]
thread_number = f"[{i}/{total}] "

# Alternative format: (1/5)
thread_number = f"({i}/{total}) "

# Alternative format: 1️⃣ / 5️⃣
thread_number = f"{i}️⃣ / {total}️⃣ "

# Alternative format: Tweet 1 of 5:
thread_number = f"Tweet {i} of {total}: "
```

---

## Configuration

### Environment Variables

Make sure these are set in your `.env` file:

```env
OPENAI_API_KEY=sk-your-api-key-here
```

### Cost Considerations

**GPT-4o-mini** (default):
- ~$0.15 per 1M input tokens
- ~$0.60 per 1M output tokens
- Very cost-effective for tweet generation

**GPT-4**:
- ~$30 per 1M input tokens
- ~$60 per 1M output tokens
- Better quality, but 200x more expensive

**Estimate per thread:**
- GPT-4o-mini: ~$0.001 per thread
- GPT-4: ~$0.20 per thread

---

## Common Issues

### Issue 1: "Could not parse tweets from LLM response"

**Cause:** LLM didn't return valid JSON

**Solution:**
- Check if your OpenAI API key is valid
- Try lowering the temperature (more focused responses)
- Check the prompt template formatting

### Issue 2: Tweets too long

**Cause:** LLM generated tweets over 280 characters

**Solution:**
- The code automatically trims them
- But you can make the prompt stricter:
  ```python
  - Each tweet must be STRICTLY under 250 characters (to leave room for numbering)
  ```

### Issue 3: Import errors

**Cause:** Missing LangChain packages

**Solution:**
```bash
pip install langchain langchain-openai langchain-core
```

---

## Summary

✅ **Complete tweet generator with:**
- 5 tone options
- Automatic validation
- Thread numbering
- Error handling
- Easy customization

✅ **Production-ready features:**
- Character limit enforcement
- JSON parsing with fallbacks
- Comprehensive error handling
- Flexible parameters

✅ **Easy to use:**
```python
result = generate_tweet_thread("Your topic here")
tweets = result["tweets"]
```

---

**Next Steps:**
1. Test with different topics and tones
2. Integrate into your FastAPI endpoints
3. Add to database with user authentication
4. Deploy and start generating tweets!

**Reference:**
- [tweet_generator.py](Backend/tweet_generator.py) - Main implementation
- [ROADMAP.md](ROADMAP.md) - Project roadmap
- [AUTH_GUIDE.md](AUTH_GUIDE.md) - Authentication guide
