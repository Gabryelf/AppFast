from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List


class BaseResponse(BaseModel):
    message: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class UserCreate(UserLogin):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    nick_name: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    nick_name: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    created_at: str

    class Config:
        from_attributes = True


class TokenResponse(BaseResponse):
    token: str


class ItemBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    cover_image: Optional[str] = None
    images: Optional[List[str]] = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    title: Optional[str] = Field(None, min_length=1, max_length=255)


class ItemResponse(ItemBase):
    id: int
    user_id: int
    created_at: str
    author: Optional[UserResponse] = None

    class Config:
        from_attributes = True


class ItemsListResponse(BaseResponse):
    items: List[ItemResponse]
    count: int
