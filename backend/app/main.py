from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.scheduler import scheduler
from app.db.session import SessionLocal
from app.services.bootstrap_service import init_db


def create_app() -> FastAPI:
    app = FastAPI(title="L-Tester Pro API", version="0.2.0")

    @app.get("/health", tags=["system"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(api_router, prefix="/api/v1")

    @app.on_event("startup")
    def _startup() -> None:
        db = SessionLocal()
        try:
            init_db(db)
        finally:
            db.close()
        scheduler.start()

    @app.on_event("shutdown")
    def _shutdown() -> None:
        if scheduler.running:
            scheduler.shutdown(wait=False)

    return app


app = create_app()
