from pydantic import BaseModel
from datetime import datetime

class SeriesBase(BaseModel):
    title: str
    description: str | None = None
    image_url: str | None = None

class SeriesCreate(SeriesBase):
    pass

class SeriesResponse(SeriesBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
