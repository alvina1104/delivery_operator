from datetime import datetime
from pydantic import BaseModel, ConfigDict
from mysite.database.models import OrderStatus

class OrderCreateSchema(BaseModel):
    product_id: int


class OrderStatusUpdateSchema(BaseModel):
    product_id: int
    status: OrderStatus


class OrderOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    user_id: int
    status: OrderStatus
    created_date: datetime


