from pydantic import BaseModel
from datetime import datetime

class SeriesBase(BaseModel):
    title: str
    description: str
    image_url: str

class SeriesCreate(SeriesBase):
    pass

class SeriesResponse(SeriesBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
