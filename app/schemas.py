from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class SeriesBase(BaseModel):
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None


class SeriesCreate(SeriesBase):
    pass


class SeriesUpdate(SeriesBase):
    pass


class Series(SeriesBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None


class PostCreate(PostBase):
    series_id: Optional[int] = None
    order_in_series: Optional[int] = None


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None
    series_id: Optional[int] = None
    order_in_series: Optional[int] = None


class Post(PostBase):
    id: int
    published_at: datetime
    series_id: Optional[int] = None
    order_in_series: Optional[int] = None

    class Config:
        from_attributes = True


class SeriesDetail(Series):
    posts: List[Post] = []
