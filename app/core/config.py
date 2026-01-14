try:
    # Prefer pydantic-settings if available (pydantic v2+)
    from pydantic_settings import BaseSettings
except Exception:
    # Fallback to pydantic v1 BaseSettings
    try:
        from pydantic import BaseSettings
    except Exception as exc:  # pragma: no cover - provide helpful error
        raise RuntimeError(
            "Missing pydantic or pydantic-settings package. Install requirements: pip install -r requirements.txt"
        ) from exc


class Settings(BaseSettings):
    MONGO_URI: str
    RESEND_API_KEY: str
    FROM_EMAIL: str
    PROJECT_NAME: str

    class Config:
        env_file = ".env"



try:
    settings = Settings()
except Exception as exc:  # pragma: no cover - surface clear configuration errors at startup
    raise RuntimeError(
        "Failed to load configuration from .env or environment variables.\n"
        "Ensure .env exists in the backend folder and contains MONGO_URI, SMTP_* and PROJECT_NAME.\n"
        f"Original error: {exc}"
    ) from exc