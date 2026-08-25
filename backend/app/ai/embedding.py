from sentence_transformers import SentenceTransformer


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


def create_embedding(dataset):
    """
    Create one searchable text from dataset.
    """

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

    return embedding_model.encode(searchable_text)