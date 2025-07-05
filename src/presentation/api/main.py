from fastapi import FastAPI

from src.utils.logging import setup_logging
from src.presentation.api.ai.routes import router as router_ai
from src.presentation.api.ai.error_handler import register_error_handlers


def create_app() -> FastAPI:
    
    app = FastAPI(
        title="AI"
    )

    setup_logging()
    register_error_handlers(app)

    app.include_router(router_ai)

    return app