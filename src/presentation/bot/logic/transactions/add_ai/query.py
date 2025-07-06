from aiohttp import ClientSession

from src.utils.config import settings


class InvalidTransactionTextError(Exception):
    pass


async def parse_text_with_ai(text: str, categories: list[str]) -> dict:
    async with ClientSession() as session:
        async with session.post(
            f"{settings.api_client.base_url}/ai/parse-transaction",
            json={"text": text, "categories": categories},
        ) as resp:
            if resp.status != 200:
                try:
                    error_data = await resp.json()
                    detail = error_data.get("detail", "Неизвестная ошибка")
                except Exception:
                    detail = await resp.text()
                raise InvalidTransactionTextError(f"❌ {detail}")

            return await resp.json()