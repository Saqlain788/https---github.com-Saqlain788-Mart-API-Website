from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    inventory_id: int
    quantity: int
    total_price: float
    status: str
    # created_at: datetime = Field(default_factory=datetime.utcnow)
    # updated_at: Optional[datetime] = None
class OrderCreate(SQLModel):
    inventory_id: int
    payment_id: int
    quantity: int
    total_price: float
class UpdatedOrder(SQLModel):
    status: Optional[str] = None
    # updated_at: datetime = Field(default_factory=datetime.utcnow)
