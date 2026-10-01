from pydantic import BaseModel, Field

class TicketInputSchema(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


class TicketOutputSchema(BaseModel):
    answer: str = Field(min_length=1, max_length=300)
    order_id: int | None = Field(ge=1, default=None)
    priority: int = Field(ge=1, le=3)


class AnswerInputSchema(BaseModel):
    text: str = Field(min_length=1, max_length=2000)
    facts: str | None = Field(default=None, max_length=1000)

class AnswerOutputSchema(BaseModel):
    text_draft: str
    review: bool = True


class OrderItemSchema(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    category: str = Field(min_length=1, max_length=100)
    description: str = Field(max_length=300)
    quantity: int = Field(ge=1)
    price: float | None = Field(default=None, ge=0)
    total_price: float | None = Field(default=None, ge=0)

class OrderCreateInputSchema(BaseModel):
    text: str = Field(min_length=1, max_length=2000)

class OrderCreateOutputSchema(BaseModel):
    items: list[OrderItemSchema]