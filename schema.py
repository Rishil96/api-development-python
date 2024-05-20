from pydantic import BaseModel
from typing import Optional


# Create a schema for receiving post data from request
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
