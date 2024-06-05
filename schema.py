from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# Create a schema for receiving post data from request
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


# Create a user
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# User Response Model
class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True


# User login Model
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Post Response
class PostResponse(BaseModel):
    title: str
    content: str
    published: bool
    created_at: datetime
    owner_id: int
    owner: UserResponse         # Retrieve the user that created the post

    # Create config class in Pydantic Model to ensure smooth conversion into dictionary between pydantic and sqlalchemy
    class Config:
        orm_mode = True


# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str


# Token Data
class TokenData(BaseModel):
    id: Optional[int] = None
