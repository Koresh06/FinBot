from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.presentation.api.ai.query_ai import InvalidTransactionTextError



def register_error_handlers(app: FastAPI) -> None:

    @app.exception_handler(InvalidTransactionTextError)
    async def invalid_transaction_exception_handler(request: Request, exc: InvalidTransactionTextError):
        return JSONResponse(
            status_code=400,
            content={"detail": exc.message},
        )