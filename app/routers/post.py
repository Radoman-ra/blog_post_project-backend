from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import post as post_crud
from app.schemas.post import PostResponse, PostCreate

router = APIRouter()

@router.post("/", response_model=PostResponse)
def create_post_endpoint(post_data: PostCreate, db: Session = Depends(get_db)):
    return post_crud.create_post(db, post_data)

@router.get("/", response_model=list[PostResponse])
def get_posts_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return post_crud.get_posts(db, skip=skip, limit=limit)

@router.get("/{post_id}", response_model=PostResponse)
def get_post_by_id_endpoint(post_id: int, db: Session = Depends(get_db)):
    db_post = post_crud.get_post_by_id(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post
