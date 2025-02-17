import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import random
from datetime import datetime, timedelta

from faker import Faker
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import Post, Series


def seed_data():
    fake = Faker()
    db: Session = SessionLocal()

    series_list = []
    for i in range(3):
        series_obj = Series(
            title=fake.sentence(nb_words=3),
            description=fake.paragraph(nb_sentences=5),
            image_url=fake.image_url(),
        )
        db.add(series_obj)
        db.commit()
        db.refresh(series_obj)
        series_list.append(series_obj)
        print(f"Created series: {series_obj.title}")

    num_posts = 20 
    for i in range(num_posts):
        selected_series = random.choice(series_list + [None])
        post = Post(
            title=fake.sentence(nb_words=6),
            content=fake.paragraph(nb_sentences=10) + "\n\n" + fake.paragraph(nb_sentences=5),
            image_url=fake.image_url(),
            published_at=datetime.now() - timedelta(days=random.randint(0, 365)),
            series_id=selected_series.id if selected_series else None,
            order_in_series=random.randint(1, 10) if selected_series else None,
        )
        db.add(post)
        print(f"Created post: {post.title}")
    db.commit()
    db.close()
    print("Seeding complete!")

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    seed_data()
