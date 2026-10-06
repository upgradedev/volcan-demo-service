"""Application factory."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import router
from app.settings import Settings, load_settings
from app.store import Store, seeded_store


def create_app(settings: Settings | None = None, store: Store | None = None) -> FastAPI:
    settings = settings or load_settings()
    app = FastAPI(title="Workspace service")
    app.state.store = store or seeded_store()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_origins),
        allow_methods=list(settings.cors_methods),
        allow_headers=["Content-Type", "X-User-Id"],
        allow_credentials=settings.cors_allow_credentials,
    )
    app.include_router(router)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
