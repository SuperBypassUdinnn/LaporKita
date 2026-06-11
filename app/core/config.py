"""Configuration settings for the application."""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    PROJECT_NAME: str = "LaporKita"
    DATABASE_URL: str
    GEMINI_API_KEY: str
    FONNTE_TOKEN: str
    
    # ID WhatsApp Group untuk masing-masing dinas (e.g. 12036300000000@g.us)
    WA_GROUP_PU: str
    WA_GROUP_PDAM: str
    WA_GROUP_PERHUBUNGAN: str
    WA_GROUP_KEBERSIHAN: str
    WA_GROUP_SOSIAL: str
    WA_GROUP_KESEHATAN: str
    WA_GROUP_UMUM: str

    # Kredensial Administrator Portal Dinas (Hardcoded)
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

# Pemetaan kategori dinas dari Gemini AI ke Target ID Grup di Fonnte
# Memuat nilai langsung dari environment variables agar ID tidak terekspos.
DINAS_TARGET_MAPPING = {
    # Dinas PU
    "Dinas PU": settings.WA_GROUP_PU,
    "PU": settings.WA_GROUP_PU,
    
    # Dinas PDAM / PDAM
    "Dinas PDAM": settings.WA_GROUP_PDAM,
    "PDAM": settings.WA_GROUP_PDAM,
    
    # Dinas Perhubungan
    "Dinas Perhubungan": settings.WA_GROUP_PERHUBUNGAN,
    "Perhubungan": settings.WA_GROUP_PERHUBUNGAN,
    "Dishub": settings.WA_GROUP_PERHUBUNGAN,
    
    # Dinas Kebersihan
    "Dinas Kebersihan": settings.WA_GROUP_KEBERSIHAN,
    "Kebersihan": settings.WA_GROUP_KEBERSIHAN,
    
    # Dinas Sosial
    "Dinas Sosial": settings.WA_GROUP_SOSIAL,
    "Sosial": settings.WA_GROUP_SOSIAL,
    
    # Dinas Kesehatan
    "Dinas Kesehatan": settings.WA_GROUP_KESEHATAN,
    "Kesehatan": settings.WA_GROUP_KESEHATAN,
    
    # Default jika tidak ada yang cocok
    "Dinas Umum": settings.WA_GROUP_UMUM,
    "Tidak Diketahui": settings.WA_GROUP_UMUM
}

