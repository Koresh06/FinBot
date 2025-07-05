from fastapi import APIRouter, Body, status

from src.presentation.api.ai.schemas import ParseTransactionRequest, ParsedTransactionSchema
from src.presentation.api.ai.query_ai import ParserTransactionAI


router = APIRouter(prefix="/ai", tags=["AI Parser"])


@router.post(
    "/parse-transaction",
    response_model=ParsedTransactionSchema,
    status_code=status.HTTP_200_OK,
)
async def parse_transaction(request: ParseTransactionRequest = Body(...)) -> ParsedTransactionSchema:
    parser = ParserTransactionAI(request.text, request.categories)
    result = await parser.query_parser_transaction()

    return ParsedTransactionSchema(
        type=result["type"],
        category=result["category"],
        total_sum=result["total_sum"],
        comment=result["comment"],
    )
