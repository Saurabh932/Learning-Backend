"""
This file is used to load environment variables (like DATABASE_URL)
from the .env file using Pydantic's BaseSettings.
This keeps credentials secure and configurable for each environment.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # The database connection URL (e.g. postgresql+asyncpg://user:pass@host/db)
    DATABASE_URL: str
    JWT_SECRET : str
    JWT_ALGORITHM : str
    REDIS_HOST : str = "localhost"
    REDIS_PORT : int = 6379
    
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM : str
    MAIL_PORT : int
    MAIL_SERVER : str
    MAIL_FROM_NAME : str
    MAIL_STARTTLS : bool = True
    MAIL_SSL_TLS : bool = False
    USE_CREDENTIALS : bool = True
    VALIDATE_CERTS : bool = True
    
    DOMAIN : str
    
    
    # Configuration for where to read the environment file from
    model_config = SettingsConfigDict(
        env_file="src/.env",  # Path to .env file
        extra="ignore"        # Ignore any extra env vars not defined here
    )


# Create a single config object to import and use anywhere in the app
config = Settings()
# print(config.DATABASE_URL)  # Uncomment to verify the env variable is being read
