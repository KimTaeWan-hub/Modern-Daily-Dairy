from pydantic import BaseModel
from app.schemas.entry import EntryCreate, EntryResponse
from app.schemas.transaction import TransactionCreate, TransactionResponse


class EntryWithTransactionsCreate(BaseModel):
    """일상 기록과 경제 기록 통합 생성 스키마"""
    entry: EntryCreate
    transactions: list[TransactionCreate] = []


class EntryWithTransactionsResponse(BaseModel):
    """일상 기록과 경제 기록 통합 응답 스키마"""
    entry: EntryResponse
    transactions: list[TransactionResponse]

