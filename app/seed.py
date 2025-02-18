import random
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine, Base
from app.models import Post, Series

def seed_data() -> None:
    fake = Faker()
    db: Session = SessionLocal()

    series_list = []
    for i in range(3):
        new_series = Series(
            title=fake.sentence(nb_words=3),
            description=fake.paragraph(nb_sentences=5),
            image_url=fake.image_url(),
        )
        db.add(new_series)
        db.commit()
        db.refresh(new_series)
        series_list.append(new_series)

    num_posts = 20
    for i in range(num_posts):
        selected_series = random.choice(series_list + [None])
        new_post = Post(
            title=fake.sentence(nb_words=6),
            content=fake.paragraph(nb_sentences=10) + "\n\n" + fake.paragraph(nb_sentences=5),
            image_url=fake.image_url(),
            published_at=datetime.now() - timedelta(days=random.randint(0, 365)),
            series_id=selected_series.id if selected_series else None,
            order_in_series=random.randint(1, 10) if selected_series else None,
        )
        db.add(new_post)
    db.commit()
    db.close()
