from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Consulta Lattes"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "chave_fallback_insegura_apenas_dev")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    
    # Cache settings
    LATTES_CACHE_TTL_SECONDS: int = int(os.getenv("LATTES_CACHE_TTL_SECONDS", 3600)) # 1 hour
    LATTES_CACHE_MAX_SIZE: int = int(os.getenv("LATTES_CACHE_MAX_SIZE", 2000)) # 2000 records approx.
    
    # Rate Limit
    RATE_LIMIT_ENABLED: bool = str(os.getenv("RATE_LIMIT_ENABLED", "true")).lower() == "true"

    # Dev/Local Auth Bypass
    BYPASS_AUTH: bool = str(os.getenv("BYPASS_AUTH", "false")).lower() == "true"

    # CORS & Security
    # ALLOWED_ORIGINS: list =  str(os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:4173,http://consultalattes.fapemig.br,https://consultalattes.fapemig.br")).split(",")
    # FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://consultalattes.fapemig.br")

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
