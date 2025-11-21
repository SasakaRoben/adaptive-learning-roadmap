from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from urllib.parse import urlparse

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra='ignore')
    
    # Support both DATABASE_URL (for cloud platforms) and individual parameters (for local dev)
    DATABASE_URL: Optional[str] = None
    DATABASE_HOST: Optional[str] = "localhost"
    DATABASE_PORT: Optional[int] = 5432
    DATABASE_NAME: Optional[str] = "adaptive_learning"
    DATABASE_USER: Optional[str] = "postgres"
    DATABASE_PASSWORD: Optional[str] = ""
    
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: Optional[str] = "gemini-1.5-flash"
    CORS_ORIGINS: Optional[str] = None  # Comma-separated list of allowed origins
    
    @property
    def database_url(self) -> str:
        """Return DATABASE_URL if set, otherwise construct from individual parameters."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )
    
    def get_db_params(self) -> dict:
        """Parse DATABASE_URL or use individual parameters for psycopg connection."""
        if self.DATABASE_URL:
            parsed = urlparse(self.DATABASE_URL)
            return {
                "host": parsed.hostname,
                "port": parsed.port or 5432,
                "dbname": parsed.path.lstrip('/'),
                "user": parsed.username,
                "password": parsed.password,
            }
        return {
            "host": self.DATABASE_HOST,
            "port": self.DATABASE_PORT,
            "dbname": self.DATABASE_NAME,
            "user": self.DATABASE_USER,
            "password": self.DATABASE_PASSWORD,
        }

settings = Settings()