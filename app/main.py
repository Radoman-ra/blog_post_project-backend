from fastapi import FastAPI
from app.routers import post, series

app = FastAPI(title="Blog API", version="1.0.0")

app.include_router(post.router, prefix="/posts", tags=["posts"])
app.include_router(series.router, prefix="/series", tags=["series"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Blog API"}
