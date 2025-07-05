from dataclasses import dataclass
import json
import os
from google import genai
from google.genai import types

from src.utils.config import settings
from src.presentation.api.ai.promt_template import TRANSACTION_PARSING_PROMPT


os.environ["HTTP_PROXY"] = settings.ai.proxy
os.environ["HTTPS_PROXY"] = settings.ai.proxy


class InvalidTransactionTextError(Exception):
    def __init__(self, message: str):
        self.message = message


@dataclass
class ParserTransactionAI:
    text: str  
    categories: list[str]
    client: genai.Client = genai.Client(api_key=settings.ai.gemeni_api_key)
    model: str = settings.ai.model  

    async def query_parser_transaction(self) -> dict:
        prompt = TRANSACTION_PARSING_PROMPT.format(text=self.text, categories=self.categories)

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        try:
            resp = response.text.strip()
            parsed = json.loads(resp)

            if "error" in parsed:
                raise InvalidTransactionTextError(parsed["error"])

            required_keys = {"type", "category", "total_sum", "comment"}
            if not required_keys.issubset(parsed.keys()):
                raise ValueError("Ответ не содержит все нужные ключи")

            return parsed

        except json.JSONDecodeError as e:
            raise ValueError(f"Ответ не является валидным JSON: {e}, текст: {resp}")

        except InvalidTransactionTextError:
            raise

        except Exception as e:
            raise ValueError(f"Неизвестная ошибка при обработке ответа Gemini: {e}, текст: {resp}")