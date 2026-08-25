from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)

from app.ai.embedding import create_embedding

COLLECTION_NAME = "datasets"

client = QdrantClient(
    host="localhost",
    port=6333,
)


def create_collection():
    """
    Create the collection if it doesn't exist.
    """

    collections = client.get_collections().collections

    names = [collection.name for collection in collections]

    if COLLECTION_NAME in names:
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE,
        ),
    )

    print("Qdrant collection created.")


def index_dataset(dataset):
    """
    Insert one dataset into Qdrant.
    """

    vector = create_embedding(dataset)

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=dataset.id,
                vector=vector,
                payload={
                    "id": dataset.id,
                    "name": dataset.name,
                    "slug": dataset.slug,
                    "category": dataset.category,
                    "ml_task": dataset.ml_task,
                },
            )
        ],
    )


def delete_dataset_vector(dataset_id: int):
    """
    Delete dataset embedding.
    """

    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=[dataset_id],
    )


def search(query: str, limit: int = 5):
    """
    Semantic Search
    """

    vector = create_embedding(
        type(
            "Query",
            (),
            {
                "name": query,
                "description": query,
                "category": "",
                "ml_task": "",
                "data_type": "",
                "difficulty": "",
                "tags": "",
                "source": "",
            },
        )
    )

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
        limit=limit,
    )

    return [
        point.payload
        for point in results.points
    ]