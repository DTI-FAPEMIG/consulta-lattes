from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Consulta Lattes"
    SECRET_KEY: str = "chave_fallback_insegura_apenas_dev"
    ALGORITHM: str = "HS256"

    # Cache settings
    LATTES_CACHE_TTL_SECONDS: int = 3600
    LATTES_CACHE_MAX_SIZE: int = 2000

    # Rate Limit
    RATE_LIMIT_ENABLED: bool = True

    # Dev/Local Auth Bypass
    BYPASS_AUTH: bool = False

    # CORS & Security
    ALLOWED_ORIGINS: str = (
        "http://localhost:5173,"
        "http://localhost:4173,"
        "https://consultalattes.fapemig.br"
    )
    FRONTEND_URL: str = "https://consultalattes.fapemig.br"

    @property
    def allowed_origins_list(self) -> list[str]:
        return [
            origin.strip().strip('"').strip("'")
            for origin in self.ALLOWED_ORIGINS.split(",")
            if origin.strip()
        ]

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


settings = Settings()
