from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "LaporKita"
    DATABASE_URL: str = "sqlite+aiosqlite:///./laporkita.db"
    GEMINI_API_KEY: str
    WA_ACCESS_TOKEN: str
    WA_PHONE_NUMBER_ID: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
