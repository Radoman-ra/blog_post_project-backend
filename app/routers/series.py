from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/series", tags=["series"])


@router.get("/", response_model=List[schemas.Series])
def get_series(db: Session = Depends(get_db)):
    series_list = (
        db.query(models.Series).order_by(models.Series.created_at.desc()).all()
    )
    return series_list


@router.get("/{series_id}", response_model=schemas.SeriesDetail)
def get_series_detail(series_id: int, db: Session = Depends(get_db)):
    series_obj = db.query(models.Series).filter(models.Series.id == series_id).first()
    if not series_obj:
        raise HTTPException(status_code=404, detail="Series not found")

    posts = (
        db.query(models.Post)
        .filter(models.Post.series_id == series_id)
        .order_by(models.Post.order_in_series)
        .all()
    )
    series_detail = schemas.SeriesDetail.from_orm(series_obj)
    series_detail.posts = posts
    return series_detail


@router.post("/", response_model=schemas.Series, status_code=status.HTTP_201_CREATED)
def create_series(series: schemas.SeriesCreate, db: Session = Depends(get_db)):
    new_series = models.Series(**series.dict())
    db.add(new_series)
    db.commit()
    db.refresh(new_series)
    return new_series


@router.put("/{series_id}", response_model=schemas.Series)
def update_series(
    series_id: int, series_update: schemas.SeriesUpdate, db: Session = Depends(get_db)
):
    series_obj = db.query(models.Series).filter(models.Series.id == series_id).first()
    if not series_obj:
        raise HTTPException(status_code=404, detail="Series not found")
    for key, value in series_update.dict(exclude_unset=True).items():
        setattr(series_obj, key, value)
    db.commit()
    db.refresh(series_obj)
    return series_obj


@router.delete("/{series_id}", response_model=dict)
def delete_series(series_id: int, db: Session = Depends(get_db)):
    series_obj = db.query(models.Series).filter(models.Series.id == series_id).first()
    if not series_obj:
        raise HTTPException(status_code=404, detail="Series not found")
    db.delete(series_obj)
    db.commit()
    return {"detail": "Series deleted"}
