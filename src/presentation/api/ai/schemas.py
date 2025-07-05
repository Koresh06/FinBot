from pydantic import BaseModel, ConfigDict


class ParsedTransactionSchema(BaseModel):
    type: str
    category: str
    total_sum: float
    comment: str

    model_config = ConfigDict(from_attributes=True)


class ParseTransactionRequest(BaseModel):
    text: str
    categories: list[str]