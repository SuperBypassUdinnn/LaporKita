"""Configuration settings for the application."""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    PROJECT_NAME: str = "LaporKita"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:YOUR_PASSWORD@db.your-supabase-project.supabase.co:5432/postgres"
    GEMINI_API_KEY: str
    WA_ACCESS_TOKEN: str
    WA_PHONE_NUMBER_ID: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
