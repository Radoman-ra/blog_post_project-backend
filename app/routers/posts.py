from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/", response_model=List[schemas.Post])
def get_posts(
    offset: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    posts = db.query(models.Post).order_by(models.Post.published_at.desc()).offset(offset).limit(limit).all()
    return posts

@router.get("/{post_id}", response_model=schemas.Post)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
