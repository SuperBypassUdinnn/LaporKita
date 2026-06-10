"""Configuration settings for the application."""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    PROJECT_NAME: str = "LaporKita"
    DATABASE_URL: str
    GEMINI_API_KEY: str
    FONNTE_TOKEN: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

# Pemetaan kategori dinas dari Gemini AI ke Target ID/Tag Grup di Fonnte
# Gunakan identifier yang future-proof: bisa diisi dengan tag contact group Fonnte
# atau ID WhatsApp Group spesifik (misal: "12036300000000@g.us").
DINAS_TARGET_MAPPING = {
    "Dinas PU": "grup_dinas_pu",
    "Dinas PDAM": "grup_dinas_pdam",
    "Dinas Perhubungan": "grup_dinas_perhubungan",
    "Dinas Kebersihan": "grup_dinas_kebersihan",
    "Dinas Sosial": "grup_dinas_sosial",
    "Dinas Kesehatan": "grup_dinas_kesehatan",
    # Default jika tidak ada yang cocok
    "Dinas Umum": "grup_dinas_umum",
    "Tidak Diketahui": "grup_dinas_umum"
}
