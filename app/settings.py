from pathlib import Path
from tempfile import gettempdir

import pydantic
from yarl import URL

TEMP_DIR = Path(gettempdir())


class Settings(pydantic.BaseSettings):
    """Application settings."""

    service_name: str = "backend-api"
    api_version: str
    host: str
    port: int

    # quantity of workers for uvicorn
    workers_count: int

    # Enable uvicorn reloading
    reload: bool

    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    db_base: str

    db_pool_size: int = 5
    db_pool_recycle: int = 30
    db_max_overflow: int = 10

    debug: bool

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.
        :return: database URL.
        """
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )

    @property
    def db_url_alembic(self) -> URL:
        """
        Assemble database URL from settings.
        :return: database URL.
        """
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
