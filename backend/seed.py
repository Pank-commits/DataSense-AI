import csv
import os
import re
from app.db.database import SessionLocal
from app.models.dataset import Dataset

def generate_slug(name: str):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

def seed_datasets():
    db = SessionLocal()

    csv_path = os.path.join(
        os.path.dirname(__file__),
        "data",
        "datasets.csv"
    )

    if not os.path.exists(csv_path):
        print(f"CSV file not found: {csv_path}")
        return

    imported = 0
    updated = 0

    with open(csv_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            slug = generate_slug(row["name"])

            existing = (
                db.query(Dataset)
                .filter(Dataset.slug == slug)
                .first()
            )

            field_values = {
                "name": row["name"],
                "slug": slug,
                "description": row["description"],
                "category": row["category"],
                "ml_task": row["ml_task"],
                "data_type": row["data_type"],
                "difficulty": row["difficulty"],
                "source": row["source"],
                "download_url": row["download_url"],
                "license": row["license"],
                "rows": int(row["rows"]),
                "columns": int(row["columns"]),
                "file_size": row["file_size"],
                "target_column": row["target_column"],
                "language": row["language"],
                "tags": row["tags"],
                "thumbnail": row["thumbnail"],
            }

            if existing:
                for field, value in field_values.items():
                    setattr(existing, field, value)

                updated += 1
                continue

            dataset = Dataset(**field_values)
            db.add(dataset)
            imported += 1

    db.commit()
    db.close()

    print("=" * 50)
    print(f"Imported : {imported}")
    print(f"Updated  : {updated}")
    print("=" * 50)


if __name__ == "__main__":
    seed_datasets()
