from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict

from mysite.database.models import Status


class UserInputSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str


class UserOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    status: Status
    registered_date: datetime


class UserLoginSchema(BaseModel):
    username: str
    password: str


class UserUpdateSchema(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]


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
    task_file: Optional[str]
    img_file: Optional[str]


class FileObjectOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    dataset_file: str
    task_file: Optional[str]
    img_file: Optional[str]
    user_id: int
