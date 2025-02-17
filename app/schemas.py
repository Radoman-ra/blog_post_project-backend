from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class SeriesBase(BaseModel):
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None

class SeriesCreate(SeriesBase):
    pass

class Series(SeriesBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Post Schemas
class PostBase(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None

class PostCreate(PostBase):
    series_id: Optional[int] = None
    order_in_series: Optional[int] = None

class Post(PostBase):
    id: int
    published_at: datetime
    series_id: Optional[int] = None
    order_in_series: Optional[int] = None

    class Config:
        orm_mode = True

class SeriesDetail(Series):
    posts: List[Post] = []
