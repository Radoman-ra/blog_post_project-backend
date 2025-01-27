from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    title: str
    image_url: str
    content: str
    order_in_series: int

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
