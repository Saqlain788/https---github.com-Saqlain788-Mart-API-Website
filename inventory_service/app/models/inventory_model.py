from sqlmodel import SQLModel, Field
from typing import Optional

class InventoryItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int
    variant_id: int | None = None
    quantity: int
    status: str 

class UpdatedInventoryItem(SQLModel):
    product_id: int
    variant_id: int | None = None
    quantity: int
    status: str
