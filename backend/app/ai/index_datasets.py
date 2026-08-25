from app.db.database import SessionLocal
from app.models.dataset import Dataset

from app.ai.qdrant_service import (
    create_collection,
    index_dataset,
)


def main():

    print("=" * 60)
    print("Starting Dataset Indexing...")
    print("=" * 60)

    db = SessionLocal()

    try:

        create_collection()

        datasets = db.query(Dataset).all()

        print(f"Found {len(datasets)} datasets.")

        for dataset in datasets:

            index_dataset(dataset)

            print(f"Indexed: {dataset.name}")

        print("=" * 60)
        print("All datasets indexed successfully!")
        print("=" * 60)

    finally:

        db.close()


if __name__ == "__main__":
    main()