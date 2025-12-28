


# ### 1.2 Configuration ([config.py](Backend/config.py))
# - [ ] Move Settings class from [database.py](Backend/database.py) to [config.py](Backend/config.py)
# - [ ] Add environment variables:
#   - `DATABASE_URL` (database connection string)
#   - `OPENAI_API_KEY` (OpenAI API key)
#   - `SECRET_KEY` (for JWT token generation)
#   - `ALGORITHM` (JWT algorithm, e.g., HS256)
#   - `ACCESS_TOKEN_EXPIRE_MINUTES`
#   - `CORS_ORIGINS` (allowed origins for CORS)

from pydantic_settings import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"
    OPENAI_API_KEY: str = "Your OpenAI API Key"
    SECRET_KEY: str = "YourSecretKey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CORS_ORIGINS: Optional[List[str]] = None

    class Config:
        env_file = ".env"
        case_sensitive = True

# Create a single instance to be used throughout the app
settings = Settings()