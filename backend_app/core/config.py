from os import environ


class Settings:
    APP_NAME: str = "Backend Practice API"
    VERSION: str = "1.0.0"

    SECRET_KEY: str = environ.get("SECRET_KEY", "change-me-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 2

    DATABASE_URL: str = environ.get("DATABASE_URL", "sqlite:///./items.db")


settings = Settings()
