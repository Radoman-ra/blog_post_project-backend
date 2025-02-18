import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import engine, Base, get_db
from app.routers import posts, series
from app.seed import seed_data

load_dotenv()

app = FastAPI(
    title="copy-of-wanago.io API",
    description="API для работы с постами и сериями блога",
    version="1.0.0",
)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/pingdb", summary="Проверка подключения к базе данных")
def ping_db(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).scalar()
        if result == 1:
            return {"status": "Database connection OK"}
        else:
            raise HTTPException(
                status_code=500, detail="Unexpected result from database"
            )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500, detail=f"Database connection error: {str(e)}"
        )


@app.post("/seed", summary="Заполнить базу данных тестовыми данными")
def seed_database():
    try:
        seed_data()
        return {"status": "Database seeded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Seeding error: {str(e)}")


@app.get("/", summary="Главная страница")
def read_root():
    return {"message": "Добро пожаловать в API copy-of-wanago.io"}


Base.metadata.create_all(bind=engine)

app.include_router(posts.router)
app.include_router(series.router)
