from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, sessionmaker):
        self.sessionmaker = sessionmaker

    async def __call__(
        self,
        handler: Callable[[Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any]
    ) -> Any:
        async with self.sessionmaker() as session:
            data["session"] = session 
            return await handler(event, data)
