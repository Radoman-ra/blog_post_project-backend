from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostCreate

def create_post(db: Session, post: PostCreate) -> Post:
    db_post = Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts(db: Session, skip: int = 0, limit: int = 10) -> list[Post]:
    return db.query(Post).offset(skip).limit(limit).all()

def get_post_by_id(db: Session, post_id: int) -> Post | None:
    return db.query(Post).filter(Post.id == post_id).first()