from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ProductCreateSchema(BaseModel):
    category: str
    store: str
    product_name: str
    price: float


class ProductUpdateSchema(BaseModel):
    category: str | None = None
    store: str | None = None
    product_name: str | None = None
    price: float | None = None


class ProductOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category: str
    store: str
    product_name: str
    price: float
    created_date: datetime