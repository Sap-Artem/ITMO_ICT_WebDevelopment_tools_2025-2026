from typing import Optional

from sqlmodel import SQLModel


class TransactionTagLinkCreate(SQLModel):
    transaction_id: int
    tag_id: int
    note: Optional[str] = None
    priority: Optional[int] = None


class TransactionTagLinkRead(SQLModel):
    transaction_id: int
    tag_id: int
    note: Optional[str] = None
    priority: Optional[int] = None