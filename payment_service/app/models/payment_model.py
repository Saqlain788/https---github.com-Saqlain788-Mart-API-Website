from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Payment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    order_id: int
    amount: float
    status: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

class PaymentCreate(SQLModel):
    user_id: int
    order_id: int
    amount: float
    status: str

class PaymentUpdate(SQLModel):
    user_id: Optional[int] = None
    order_id: Optional[int] = None
    amount: Optional[float] = None
    status: Optional[str] = None
