from sqlmodel import SQLModel, Field
from typing import Optional

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float
    quantity: int       
    brand: str | None = None
    weight: float | None = None
    category: str

class updatedproduct(SQLModel):
    name: str
    description: str
    price: float
    quantity: int
    brand: str | None = None
    weight: float | None = None
    category: str