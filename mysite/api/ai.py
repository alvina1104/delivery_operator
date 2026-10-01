from fastapi import APIRouter, HTTPException
from mysite.chain.ticket_chain import ticket_chain
from mysite.chain.answer_chain import ai_chain
from mysite.chain.order_chain import order_create_chain
from mysite.schemas.ai_schema import (TicketOutputSchema, TicketInputSchema, AnswerOutputSchema, AnswerInputSchema,
                                      OrderCreateOutputSchema, OrderCreateInputSchema)
from langchain_core.exceptions import OutputParserException
import asyncio


ai_router = APIRouter(prefix='/ai', tags=['AI Delivery Assistant'])


@ai_router.post('/analyze/', response_model=TicketOutputSchema)
async def analyze_ticket(ticket: TicketInputSchema):
    text = ticket.text.strip()

    if not text:
        raise HTTPException(status_code=422, detail='Маалымат туура эмес форматта берилди')

    try:
        result = await asyncio.wait_for(
            ticket_chain.ainvoke({"text": text}), timeout=120
        )

    except TimeoutError:
        raise HTTPException(status_code=500, detail='Модел не успел отвечать на вопросу')

    except OutputParserException:
        raise HTTPException(status_code=500, detail='Ответ модела не совпадает со схемой')

    return result


@ai_router.post('/answer/', response_model=AnswerOutputSchema)
async def answer_list(answer: AnswerInputSchema):
    text = answer.text.strip()
    facts = answer.facts.strip() if answer.facts else ""

    if not text:
        raise HTTPException(status_code=422, detail='Маалымат туура эмес форматта берилди')

    try:
        result = await asyncio.wait_for(ai_chain.ainvoke({"text": text, "facts": facts}), timeout=120)

    except TimeoutError:
        raise HTTPException(status_code=504, detail='Модель белгиленген убакытта жооп бере алган жок')

    except ValueError as error:
        raise HTTPException(status_code=500, detail=str(error))

    return AnswerOutputSchema(text_draft=result.strip())



@ai_router.post('/order_create/', response_model=OrderCreateOutputSchema)
async def order_create(order: OrderCreateInputSchema):
    text = order.text.strip()

    if not text:
        raise HTTPException(status_code=422, detail='Маалымат туура эмес форматта берилди')

    try:
        result = await asyncio.wait_for(order_create_chain.ainvoke({"text": text}), timeout=120)

    except TimeoutError:
        raise HTTPException(status_code=504, detail='Модель белгиленген убакытта жооп бере алган жок')

    except OutputParserException:
        raise HTTPException(status_code=500, detail='Ответ модели не совпадает со схемой')

    return result