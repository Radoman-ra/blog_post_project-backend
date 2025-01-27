from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import post as post_crud
from app.schemas.post import PostResponse, PostCreate

router = APIRouter()

@router.post("/", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    return post_crud.create_post(db, post)

@router.get("/", response_model=list[PostResponse])
def get_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return post_crud.get_posts(db, skip, limit)
