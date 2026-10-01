from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr


class UserRegisterSchema(BaseModel):
    username: str
    email: EmailStr
    phone_number: str
    password: str


class UserLoginSchema(BaseModel):
    username: str
    password: str


class UserOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    phone_number: str
    registered_date: date


class CurrentUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenSchema(BaseModel):
    refresh_token: str