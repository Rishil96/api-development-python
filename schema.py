from pydantic import BaseModel, EmailStr
from datetime import datetime


# Create a schema for receiving post data from request
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


# Post Response
class PostResponse(BaseModel):
    title: str
    content: str
    published: bool
    created_at: datetime

    # Create config class in Pydantic Model to ensure smooth conversion into dictionary between pydantic and sqlalchemy
    class Config:
        orm_mode = True


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
