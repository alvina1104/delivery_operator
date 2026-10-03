from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from mysite.database.models import Status


class UserRegisterSchema(BaseModel):
    username: str
    email: EmailStr
    phone_number: str
    password: str


class UserOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    phone_number: str
    status: Status
    registered_date: date


class UserLoginSchema(BaseModel):
    username: str
    password: str


class UserUpdateSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None


class CurrentUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    status: Status


class AgentRequest(BaseModel):
    message: str


class AgentResponse(BaseModel):
    answer: str


class FileObjectCreateSchema(BaseModel):
    dataset_file: str
    task_file: Optional[str] = None
    img_file: Optional[str] = None


class FileObjectOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    dataset_file: str
    task_file: Optional[str] = None
    img_file: Optional[str] = None
    user_id: int