"""Configuration settings for the application."""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "LaporKita"
    DATABASE_URL: str
    GEMINI_API_KEY: str
    FONNTE_TOKEN: str
    
    WA_GROUP_PU: str
    WA_GROUP_PDAM: str
    WA_GROUP_PERHUBUNGAN: str
    WA_GROUP_KEBERSIHAN: str
    WA_GROUP_SOSIAL: str
    WA_GROUP_KESEHATAN: str
    WA_GROUP_UMUM: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

DINAS_TARGET_MAPPING = {
    "Dinas PU": settings.WA_GROUP_PU,
    "Dinas PDAM": settings.WA_GROUP_PDAM,
    "Dinas Perhubungan": settings.WA_GROUP_PERHUBUNGAN,
    "Dinas Kebersihan": settings.WA_GROUP_KEBERSIHAN,
    "Dinas Sosial": settings.WA_GROUP_SOSIAL,
    "Dinas Kesehatan": settings.WA_GROUP_KESEHATAN,
    "Dinas Umum": settings.WA_GROUP_UMUM,
    "Tidak Diketahui": settings.WA_GROUP_UMUM
}