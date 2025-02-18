import os
import random
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy.orm import Session
from PIL import Image, ImageDraw
from app.database import SessionLocal, engine, Base
from app.models import Post, Series
import uuid

IMAGE_DIR = os.path.join("app", "static", "images")


def ensure_image_dir_exists():
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
        print(f"Directory '{IMAGE_DIR}' created.")


def generate_random_image(save_name: str, width: int = 400, height: int = 300) -> str:
    random_color = (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )

    image = Image.new("RGB", (width, height), random_color)

    draw = ImageDraw.Draw(image)
    text = "copy-of-wanago.io"
    text_color = (255, 255, 255)
    draw.text((10, 10), text, fill=text_color)

    save_path = os.path.join(IMAGE_DIR, save_name)
    image.save(save_path, format="JPEG")
    print(f"Image saved: {save_path}")
    return os.path.join("static", "images", save_name)


def generate_unique_images(count: int) -> list[str]:
    ensure_image_dir_exists()
    images_paths = []
    for _ in range(count):
        filename = f"image_{uuid.uuid4().hex[:8]}.jpg"
        path = generate_random_image(filename)
        images_paths.append(path)
    return images_paths


def clear_database(db: Session):
    db.query(Post).delete()
    db.query(Series).delete()
    db.commit()
    print("Database cleared.")


def seed_data(num_posts: int = 20) -> None:
    fake = Faker()
    db: Session = SessionLocal()

    clear_database(db)

    total_images_needed = 3 + num_posts

    images = generate_unique_images(total_images_needed)

    series_images = images[:3]
    post_images = images[3:]

    series_list = []
    for i in range(3):
        new_series = Series(
            title=fake.sentence(nb_words=3),
            description=fake.paragraph(nb_sentences=5),
            image_url=series_images[i],
        )
        db.add(new_series)
        db.commit()
        db.refresh(new_series)
        series_list.append(new_series)
        print(f"Created series: {new_series.title}")

    for i in range(num_posts):
        selected_series = random.choice(series_list + [None])
        new_post = Post(
            title=fake.sentence(nb_words=6),
            content=fake.paragraph(nb_sentences=10)
            + "\n\n"
            + fake.paragraph(nb_sentences=5),
            image_url=post_images[i],
            published_at=datetime.now() - timedelta(days=random.randint(0, 365)),
            series_id=selected_series.id if selected_series else None,
            order_in_series=random.randint(1, 10) if selected_series else None,
        )
        db.add(new_post)
        print(f"Created post: {new_post.title}")

    db.commit()
    db.close()
    print("Seeding complete!")


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    seed_data()
