from sqlalchemy.orm import Session
from app.models.series import Series
from app.schemas.series import SeriesCreate

def create_series(db: Session, series: SeriesCreate) -> Series:
    db_series = Series(**series.dict())
    db.add(db_series)
    db.commit()
    db.refresh(db_series)
    return db_series

def get_all_series(db: Session) -> list[Series]:
    return db.query(Series).all()

def get_series_by_id(db: Session, series_id: int) -> Series | None:
    return db.query(Series).filter(Series.id == series_id).first()