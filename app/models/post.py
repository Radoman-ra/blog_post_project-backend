from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    series_id = Column(Integer, ForeignKey("series.id", ondelete="CASCADE"))
    title = Column(String, nullable=False)
    image_url = Column(String)
    content = Column(Text, nullable=False)
    order_in_series = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    series = relationship("Series", back_populates="posts")
