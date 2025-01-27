from fastapi import FastAPI
from app.routers import post

app = FastAPI(title="Blog API", version="1.0.0")

app.include_router(post.router, prefix="/posts", tags=["posts"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Blog API"}
