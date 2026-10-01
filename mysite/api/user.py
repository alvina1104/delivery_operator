from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mysite.database.db import SessionLocal
from mysite.database.models import UserProfile
from mysite.database.schema import UserInputSchema, UserOutSchema, UserUpdateSchema
from mysite.api.auth import get_password_hash


user_router = APIRouter(prefix="/user", tags=["User"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user_router.post("/", response_model=UserOutSchema)
async def create_user(user: UserInputSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    email_db = db.query(UserProfile).filter(UserProfile.email == user.email).first()

    if user_db or email_db:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    user_data = UserProfile(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password)
    )

    db.add(user_data)
    db.commit()
    db.refresh(user_data)

    return user_data


@user_router.get("/", response_model=List[UserOutSchema])
async def list_user(db: Session = Depends(get_db)):
    return db.query(UserProfile).all()


@user_router.get("/{user_id}/", response_model=UserOutSchema)
async def detail_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()

    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    return user_db


@user_router.put("/{user_id}/", response_model=UserOutSchema)
async def update_user(user_id: int, user_in: UserUpdateSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()

    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_in.model_dump(exclude_unset=True)

    if "username" in update_data:
        username_db = db.query(UserProfile).filter(
            UserProfile.username == update_data["username"],
            UserProfile.id != user_id
        ).first()

        if username_db:
            raise HTTPException(status_code=400, detail="Username already exists")

    if "email" in update_data:
        email_db = db.query(UserProfile).filter(
            UserProfile.email == update_data["email"],
            UserProfile.id != user_id
        ).first()

        if email_db:
            raise HTTPException(status_code=400, detail="Email already exists")

    if "password" in update_data:
        update_data["password"] = get_password_hash(update_data["password"])

    for key, value in update_data.items():
        setattr(user_db, key, value)

    db.commit()
    db.refresh(user_db)

    return user_db


@user_router.delete("/{user_id}/", response_model=dict)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()

    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user_db)
    db.commit()

    return {"message": "User successful deleted"}