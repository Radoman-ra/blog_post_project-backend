from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import series as series_crud
from app.schemas.series import SeriesCreate, SeriesResponse

router = APIRouter()

@router.post("/", response_model=SeriesResponse)
def create_series_endpoint(series_data: SeriesCreate, db: Session = Depends(get_db)):
    return series_crud.create_series(db, series_data)

@router.get("/", response_model=list[SeriesResponse])
def get_all_series_endpoint(db: Session = Depends(get_db)):
    return series_crud.get_all_series(db)

@router.get("/{series_id}", response_model=SeriesResponse)
def get_series_by_id_endpoint(series_id: int, db: Session = Depends(get_db)):
    db_series = series_crud.get_series_by_id(db, series_id)
    if not db_series:
        raise HTTPException(status_code=404, detail="Series not found")
    return db_series
