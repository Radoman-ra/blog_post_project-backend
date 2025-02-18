from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import engine, Base, get_db
from app.routers import posts, series

app = FastAPI(
    title="copy-of-wanago.io API",
    description="API for copy-of-wanago.io",
    version="1.0.0"
)

@app.post("/pingdb", summary="Check database connection")
def ping_db(db: Session = Depends(get_db)):

    try:
        result = db.execute(text("SELECT 1")).scalar()
        if result == 1:
            return {"status": "Database connection OK"}
        else:
            raise HTTPException(status_code=500, detail="Unexpected result from database")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")

@app.get("/", summary="Main page")
def read_root():
    return {"message": "welcome to copy-of-wanago.io API"}

Base.metadata.create_all(bind=engine)

app.include_router(posts.router)
app.include_router(series.router)
