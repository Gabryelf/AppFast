from pydantic import BaseModel
from typing import Optional, List


class UserForm(BaseModel):
    email: str
    password: str


class UserCreateForm(BaseModel):
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    nick_name: Optional[str] = None


class ItemCreateForm(BaseModel):
    title: str
    description: Optional[str] = None
    cover_image: Optional[str] = None
    images: Optional[List[str]] = None


class ItemUpdateForm(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    cover_image: Optional[str] = None
    images: Optional[List[str]] = None