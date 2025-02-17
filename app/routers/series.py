from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/series", tags=["series"])

@router.get("/", response_model=List[schemas.Series])
def get_series(db: Session = Depends(get_db)):
    series_list = db.query(models.Series).order_by(models.Series.created_at.desc()).all()
    return series_list

@router.get("/{series_id}", response_model=schemas.SeriesDetail)
def get_series_detail(series_id: int, db: Session = Depends(get_db)):
    series_obj = db.query(models.Series).filter(models.Series.id == series_id).first()
    if not series_obj:
        raise HTTPException(status_code=404, detail="Series not found")
    
    posts = db.query(models.Post).filter(models.Post.series_id == series_id).order_by(models.Post.order_in_series).all()
    series_detail = schemas.SeriesDetail.from_orm(series_obj)
    series_detail.posts = posts
    return series_detail
