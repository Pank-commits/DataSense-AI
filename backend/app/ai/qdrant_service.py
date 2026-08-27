import re

import os
import re

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)

from app.ai.embedding import create_embedding


COLLECTION_NAME = "datasets"

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))

client = QdrantClient(
    host=QDRANT_HOST,
    port=QDRANT_PORT,
    timeout=5,
)


# ==========================================
# COLLECTION
# ==========================================

def create_collection():
    """
    Create the Qdrant collection if it doesn't exist.
    """

    collections = client.get_collections().collections

    names = [
        collection.name
        for collection in collections
    ]

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


def verify_connection():
    """Verify local Qdrant and ensure the dataset collection exists."""
    client.get_collections()
    create_collection()
    collection = client.get_collection(COLLECTION_NAME)
    return {
        "connected": True,
        "host": QDRANT_HOST,
        "port": QDRANT_PORT,
        "collection": COLLECTION_NAME,
        "vectors_count": (collection.points_count
        if collection.points_count is not None
        else 0),
    }


# ==========================================
# INDEX DATASET
# ==========================================

def index_dataset(dataset):
    """
    Insert or update one dataset in Qdrant.
    """

    if not getattr(dataset, "id", None):
        raise ValueError("Cannot index a dataset without a database ID")

    # Upsert is idempotent: the database primary key is the Qdrant point ID.
    # Re-indexing an updated dataset replaces the existing vector and payload.
    create_collection()
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
                    "description": dataset.description,
                    "category": dataset.category,
                    "ml_task": dataset.ml_task,
                    "data_type": dataset.data_type,
                    "difficulty": dataset.difficulty,
                    "tags": dataset.tags,
                    "source": dataset.source,
                },
            )
        ],
    )


# ==========================================
# DELETE DATASET
# ==========================================

def delete_dataset_vector(dataset_id: int):
    """
    Delete dataset embedding from Qdrant.
    """

    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=[dataset_id],
    )


# ==========================================
# TEXT HELPERS
# ==========================================

def normalize_text(text):
    """
    Normalize text for matching.
    """

    if not text:
        return ""

    text = str(text).lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text,
    )

    return " ".join(
        text.split()
    )


def tokenize(text):
    """
    Convert text into useful tokens.
    """

    normalized = normalize_text(text)

    if not normalized:
        return set()

    stop_words = {
        "the",
        "a",
        "an",
        "for",
        "to",
        "of",
        "and",
        "or",
        "in",
        "on",
        "with",
        "dataset",
        "datasets",
        "data",
        "need",
        "find",
        "recommend",
        "recommendation",
        "looking",
        "want",
        "give",
        "show",
        "me",
        "i",
        "am",
        "is",
        "are",
        "can",
        "you",
        "machine",
        "learning",
        "task",
    }

    return {
        word
        for word in normalized.split()
        if (
            word not in stop_words
            and len(word) > 1
        )
    }


# ==========================================
# KEYWORD SCORE
# ==========================================

def calculate_keyword_score(
    query,
    payload,
):
    """
    Calculate lexical relevance.

    Dataset name receives the strongest weight.
    """

    query_tokens = tokenize(query)

    if not query_tokens:
        return 0.0

    name = normalize_text(
        payload.get("name")
    )

    category = normalize_text(
        payload.get("category")
    )

    ml_task = normalize_text(
        payload.get("ml_task")
    )

    description = normalize_text(
        payload.get("description")
    )

    tags = normalize_text(
        payload.get("tags")
    )

    score = 0.0

    normalized_query = normalize_text(
        query
    )

    # Exact query phrase in dataset name
    if (
        normalized_query
        and normalized_query in name
    ):
        score += 1.0

    for token in query_tokens:

        if token in name:
            score += 0.55

        if token in category:
            score += 0.25

        if token in ml_task:
            score += 0.25

        if token in tags:
            score += 0.20

        if token in description:
            score += 0.10

    return min(
        score / 2.0,
        1.0,
    )


# ==========================================
# METADATA MATCH SCORE
# ==========================================

def calculate_metadata_score(
    payload,
    intent=None,
):
    """
    Calculate intent-aware metadata relevance.

    Category and ML task receive the strongest
    weight because they are explicit user intent.

    This does NOT filter datasets.
    It ranks them.
    """

    if not intent:
        return 0.0

    category = normalize_text(
        payload.get("category")
    )

    ml_task = normalize_text(
        payload.get("ml_task")
    )

    difficulty = normalize_text(
        payload.get("difficulty")
    )

    data_type = normalize_text(
        payload.get("data_type")
    )

    requested_category = normalize_text(
        intent.get("category")
    )

    requested_task = normalize_text(
        intent.get("ml_task")
    )

    requested_difficulty = normalize_text(
        intent.get("difficulty")
    )

    requested_data_type = normalize_text(
        intent.get("data_type")
    )

    score = 0.0
    total_weight = 0.0

    # --------------------------------------
    # Category
    # --------------------------------------

    if requested_category:

        total_weight += 4.0

        if (
            category
            and requested_category == category
        ):
            score += 4.0

        elif (
            requested_category in category
            or category in requested_category
        ):
            score += 3.0

    # --------------------------------------
    # ML Task
    # --------------------------------------

    if requested_task:

        total_weight += 4.0

        if (
            ml_task
            and requested_task == ml_task
        ):
            score += 4.0

        elif (
            requested_task in ml_task
            or ml_task in requested_task
        ):
            score += 3.0

    # --------------------------------------
    # Difficulty
    # --------------------------------------

    if requested_difficulty:

        total_weight += 2.0

        if (
            difficulty
            and requested_difficulty == difficulty
        ):
            score += 2.0

    # --------------------------------------
    # Data type
    # --------------------------------------

    if requested_data_type:

        total_weight += 2.0

        if (
            data_type
            and requested_data_type == data_type
        ):
            score += 2.0

        elif (
            requested_data_type in data_type
            or data_type in requested_data_type
        ):
            score += 1.0

    if total_weight == 0:
        return 0.0

    return score / total_weight


# ==========================================
# INTENT KEYWORD SCORE
# ==========================================

def calculate_intent_keyword_score(
    query,
    payload,
    intent=None,
):
    """
    Additional domain/entity relevance.

    This helps queries such as:

        predicting heart disease

    prefer datasets containing:

        heart
        disease
        diabetes
        patient
        medical
        cardiac

    instead of unrelated datasets.
    """

    if not intent:
        return 0.0

    query_text = normalize_text(
        query
    )

    dataset_text = normalize_text(
        " ".join(
            [
                str(payload.get("name") or ""),
                str(payload.get("description") or ""),
                str(payload.get("tags") or ""),
            ]
        )
    )

    if not query_text or not dataset_text:
        return 0.0

    # --------------------------------------
    # Important domain terms
    # --------------------------------------

    domain_groups = {
        "healthcare": [
            "heart",
            "disease",
            "diabetes",
            "cancer",
            "patient",
            "medical",
            "health",
            "clinical",
            "hospital",
            "cardiac",
        ],

        "finance": [
            "finance",
            "financial",
            "bank",
            "credit",
            "loan",
            "stock",
            "fraud",
            "investment",
        ],

        "retail": [
            "customer",
            "product",
            "shopping",
            "retail",
            "sales",
            "ecommerce",
        ],

        "agriculture": [
            "crop",
            "agriculture",
            "farming",
            "plant",
            "soil",
            "yield",
        ],

        "education": [
            "student",
            "education",
            "school",
            "exam",
            "academic",
        ],

        "nlp": [
            "text",
            "language",
            "sentiment",
            "translation",
            "document",
            "chatbot",
        ],

        "computer vision": [
            "image",
            "images",
            "vision",
            "object",
            "face",
            "pixel",
        ],
    }

    category = normalize_text(
        intent.get("category")
    )

    keywords = domain_groups.get(
        category,
        [],
    )

    if not keywords:
        return 0.0

    query_matches = [
        keyword
        for keyword in keywords
        if keyword in query_text
    ]

    if not query_matches:
        return 0.0

    dataset_matches = [
        keyword
        for keyword in query_matches
        if keyword in dataset_text
    ]

    if not dataset_matches:
        return 0.0

    return min(
        len(dataset_matches)
        / len(query_matches),
        1.0,
    )


def calculate_exact_intent_score(query, payload, intent=None):
    """Reward the requested domain/task/entity appearing in the dataset."""
    if not intent:
        return 0.0
    query_text = normalize_text(query)
    dataset_text = normalize_text(" ".join([
        str(payload.get("name") or ""),
        str(payload.get("description") or ""),
        str(payload.get("tags") or ""),
    ]))
    requested = [normalize_text(intent.get(key)) for key in
                 ("category", "ml_task", "data_type")]
    requested = [value for value in requested if value]
    entity_terms = [term for term in
                    ("diabetes", "heart disease", "cancer", "patient")
                    if term in query_text]
    signals = requested + entity_terms
    if not signals:
        return 0.0
    matches = sum(1 for signal in signals if signal in dataset_text)
    score = matches / len(signals)
    # A title-level entity match is especially valuable for recommendations.
    name = normalize_text(payload.get("name"))
    if any(signal in name for signal in entity_terms):
        score = min(1.0, score + 0.25)
    return score


def calculate_intent_priority(query, payload, intent=None):
    """Return a deterministic specificity tier for recommendation ranking."""
    if not intent:
        return (0, 0, 0, 0)

    query_text = normalize_text(query)
    dataset_text = normalize_text(" ".join([
        str(payload.get("name") or ""),
        str(payload.get("description") or ""),
        str(payload.get("tags") or ""),
    ]))
    category = normalize_text(payload.get("category"))
    task = normalize_text(payload.get("ml_task"))
    data_type = normalize_text(payload.get("data_type"))
    requested_category = normalize_text(intent.get("category"))
    requested_task = normalize_text(intent.get("ml_task"))
    requested_type = normalize_text(intent.get("data_type"))

    # Topic is intentionally derived from the query because the intent
    # extractor does not yet expose a stable topic field.
    topic_terms = [term for term in
                   ("diabetes", "heart disease", "cancer", "patient")
                   if term in query_text]
    topic_match = int(bool(topic_terms) and any(
        term in dataset_text for term in topic_terms
    ))
    task_match = int(bool(requested_task) and (
        task == requested_task or requested_task in task
    ))
    category_match = int(bool(requested_category) and (
        category == requested_category or requested_category in category
    ))
    # For diabetes prediction, tabular is the preferred concrete modality
    # even when the extractor leaves data_type unset.
    type_requested = requested_type or (
        "tabular" if "diabetes" in query_text else ""
    )
    type_match = int(bool(type_requested) and (
        data_type == type_requested or type_requested in data_type
    ))
    return (topic_match, task_match, category_match, type_match)


# ==========================================
# HYBRID SEARCH
# ==========================================

def search(
    query: str,
    limit: int = 5,
    intent: dict | None = None,
):
    """
    Intent-aware hybrid dataset retrieval.

    Ranking:

        Semantic similarity
              +
        Keyword relevance
              +
        Metadata match
              +
        Domain/entity relevance

    Metadata is used for ranking,
    not hard filtering.
    """

    if not query or not query.strip():
        return []

    query = query.strip()

    # --------------------------------------
    # Create embedding
    # --------------------------------------

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

    # --------------------------------------
    # Candidate pool
    # --------------------------------------

    candidate_limit = max(
        limit * 10,
        50,
    )

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
        limit=candidate_limit,
        with_payload=True,
    )

    candidates = []

    for point in results.points:

        payload = point.payload or {}

        semantic_score = float(
            point.score or 0.0
        )

        keyword_score = (
            calculate_keyword_score(
                query,
                payload,
            )
        )

        metadata_score = (
            calculate_metadata_score(
                payload,
                intent,
            )
        )

        intent_keyword_score = (
            calculate_intent_keyword_score(
                query,
                payload,
                intent,
            )
        )
        exact_intent_score = calculate_exact_intent_score(
            query, payload, intent
        )
        intent_priority = calculate_intent_priority(
            query, payload, intent
        )

        # ----------------------------------
        # Metadata mismatch penalty
        # ----------------------------------
        #
        # Metadata matching is important for recommendation
        # queries. A dataset from the wrong category/task should
        # not rank highly just because its embedding is similar.
        #
        # This is a penalty, not a hard filter, so useful datasets
        # are still allowed through when metadata is incomplete.
        #

        metadata_penalty = 0.0

        if intent:

            requested_category = normalize_text(
                intent.get("category")
            )

            requested_task = normalize_text(
                intent.get("ml_task")
            )

            dataset_category = normalize_text(
                payload.get("category")
            )

            dataset_task = normalize_text(
                payload.get("ml_task")
            )

            # Wrong category
            if (
                requested_category
                and dataset_category
                and requested_category != dataset_category
                and requested_category not in dataset_category
                and dataset_category not in requested_category
            ):
                metadata_penalty += 0.20

            # Wrong ML task
            if (
                requested_task
                and dataset_task
                and requested_task != dataset_task
                and requested_task not in dataset_task
                and dataset_task not in requested_task
            ):
                metadata_penalty += 0.15

        # ----------------------------------
        # Query-specific relevance
        # ----------------------------------
        #
        # Give strong importance to words from the user's actual
        # request. For example:
        #
        #   "predicting heart disease"
        #
        # should strongly prefer a dataset whose name/description
        # contains "heart" and "disease".
        #

        query_tokens = tokenize(query)

        dataset_name = normalize_text(
            payload.get("name")
        )

        dataset_description = normalize_text(
            payload.get("description")
        )

        dataset_tags = normalize_text(
            payload.get("tags")
        )

        query_relevance = 0.0

        for token in query_tokens:

            if token in dataset_name:
                query_relevance += 0.50

            elif token in dataset_description:
                query_relevance += 0.25

            elif token in dataset_tags:
                query_relevance += 0.15

        query_relevance = min(
            query_relevance,
            1.0,
        )

        # ----------------------------------
        # Final ranking
        # ----------------------------------
        #
        # With intent:
        #
        # semantic          30%
        # keyword           20%
        # metadata          25%
        # intent relevance  25%
        # mismatch penalty  applied afterwards
        #
        # Without intent:
        #
        # semantic          65%
        # keyword           35%
        #

        if intent:

            hybrid_score = (
                semantic_score * 0.30
                + keyword_score * 0.20
                + metadata_score * 0.25
                + intent_keyword_score * 0.15
                + query_relevance * 0.10
                + exact_intent_score * 0.20
                - metadata_penalty
            )

        else:

            hybrid_score = (
                semantic_score * 0.65
                + keyword_score * 0.35
            )

        candidates.append(
            {
                "payload": payload,
                "semantic_score": semantic_score,
                "keyword_score": keyword_score,
                "metadata_score": metadata_score,
                "intent_keyword_score":
                    intent_keyword_score,
                "query_relevance": query_relevance,
                "exact_intent_score": exact_intent_score,
                "intent_priority": intent_priority,
                "metadata_penalty": metadata_penalty,
                "hybrid_score": hybrid_score,
            }
        )

    # --------------------------------------
    # Rank
    # --------------------------------------

    candidates.sort(
        key=lambda item: (
            item["intent_priority"],
            item["hybrid_score"],
        ),
        reverse=True,
    )

    # --------------------------------------
    # Return datasets
    # --------------------------------------

    return [
        item["payload"]
        for item in candidates[:limit]
    ]
