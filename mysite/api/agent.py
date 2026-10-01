from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from sqlalchemy.orm import Session

from mysite.api.auth import get_current_user
from mysite.database.db import SessionLocal
from mysite.database.models import UserProfile, DailyUsage, Status
from mysite.database.schema import AgentRequest, AgentResponse


agent_router = APIRouter(prefix="/ai", tags=["AI"])

model = ChatGoogleGenerativeAI(model="gemini-3.1-pro-preview", temperature=0)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

system_message = SystemMessage(
    content=(
        "Ты очень опытный Python Senior разработчик. "
        "Отвечаешь на вопросы кратко и с примерами. "
        "Ответ должен быть максимум 5 предложений."
    )
)


def get_daily_usage(db: Session, user_id: int):
    usage = db.query(DailyUsage).filter(DailyUsage.user_id == user_id,
        DailyUsage.usage_date == date.today()).first()

    if not usage:
        usage = DailyUsage(
            user_id=user_id,
            usage_date=date.today(),
            messages_used=0,
            images_used=0
        )
        db.add(usage)
        db.commit()
        db.refresh(usage)

    return usage


def check_message_limit(db: Session, user: UserProfile):
    if user.status == Status.pro:
        return None

    usage = get_daily_usage(db, user.id)

    if usage.messages_used >= 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Дневной лимит исчерпан. На тарифе Basic доступно 50 сообщений в день."
                            )

    return usage


def check_image_limit(db: Session, user: UserProfile):
    if user.status == Status.pro:
        return None

    usage = get_daily_usage(db, user.id)

    if usage.images_used >= 3:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Дневной лимит исчерпан. На тарифе Basic доступно 3 изображения в день."
    )

    return usage


@agent_router.post("/", response_model=AgentResponse)
async def ask_ai(data: AgentRequest,db: Session = Depends(get_db),current_user: UserProfile = Depends(get_current_user)):
    usage = check_message_limit(db, current_user)

    messages = [system_message,HumanMessage(content=data.message)]

    response = await model.ainvoke(messages)

    if usage:
        usage.messages_used += 1
        db.commit()

    return {"answer": response.content}