
import uvicorn

from app.settings import settings


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "app.application:get_app",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        factory=True,
    )


if __name__ == "__main__":
    main()
