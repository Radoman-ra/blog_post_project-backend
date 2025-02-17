from fastapi import FastAPI
from app.database import engine, Base
from routers import posts, series

Base.metadata.create_all(bind=engine)

app = FastAPI(title="copy-of-wanago.io API")

app.include_router(posts.router)
app.include_router(series.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to copy-of-wanago.io API"}
