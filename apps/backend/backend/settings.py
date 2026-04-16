import enum
from pathlib import Path
from tempfile import gettempdir

from ksef_client import KsefEnvironment

from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi.security import OAuth2PasswordBearer

TEMP_DIR = Path(gettempdir())


class LogLevel(enum.StrEnum):
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = "127.0.0.1"
    port: int = 8000
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    environment: str = "dev"

    # auth
    jwt_secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    token_type: str = "bearer"  # noqa: S105
    oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(
        tokenUrl="/api/auth/login", scheme_name="JWT"
    )

    # KSeF environment
    @classmethod
    def ksef_environment(cls) -> str:
        """Returns the KSeF environment to be used based on the current environment."""
        if cls().environment == "prod":
            return KsefEnvironment.PROD.value

        return KsefEnvironment.DEMO.value

    log_level: LogLevel = LogLevel.INFO
    # Variables for the database
    db_file: Path = TEMP_DIR / "db.sqlite3"
    db_echo: bool = False

    @property
    def db_url(self) -> str:
        """
        Assemble database URL from settings.

        Returns:
            Database URL.
        """
        return f"sqlite+aiosqlite:///{self.db_file.as_posix()}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="BACKEND_",
        env_file_encoding="utf-8",
    )


settings = Settings()
