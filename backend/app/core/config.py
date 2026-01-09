from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    MONGODB_URI: str
    DATABASE_NAME: str = "internship_db"

    # Auth / JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    # Admin
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str

    # CORS
    CORS_ORIGINS: str = "*"

    # Pydantic v2 settings config
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
