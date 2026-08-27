from huggingface_hub.utils import logging as huggingface_logging
from sentence_transformers import SentenceTransformer
from huggingface_hub.utils import logging as huggingface_logging
from transformers.utils import logging as transformers_logging


# Keep routine model download/load messages out of the API server logs.
huggingface_logging.set_verbosity_error()
transformers_logging.set_verbosity_error()


class EmbeddingModel:
    """
    Singleton embedding model.
    Loads only once when FastAPI starts.
    """

    def __init__(self):
        print("Loading Sentence Transformer model...")
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )
        print("Embedding model loaded successfully.")

    def encode(self, text: str):
        """
        Generate embedding vector for text.
        """

        return self.model.encode(
            text,
            normalize_embeddings=True
        ).tolist()


embedding_model = EmbeddingModel()


def build_searchable_text(dataset):
    """Build the canonical text representation indexed in Qdrant."""

    searchable_text = f"""
    Name: {dataset.name}

    Description: {dataset.description}

    Category: {dataset.category}

    ML Task: {dataset.ml_task}

    Data Type: {dataset.data_type}

    Difficulty: {dataset.difficulty}

    Tags: {dataset.tags}

    Source: {dataset.source}
    """

    return searchable_text


def create_embedding(dataset):
    """Create an embedding from canonical dataset metadata text."""
    return embedding_model.encode(build_searchable_text(dataset))
