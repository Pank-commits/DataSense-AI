from typing import Iterator
import time

from huggingface_hub import HfApi


# ==========================================
# CONFIGURATION
# ==========================================

SOURCE_NAME = "Hugging Face"

api = HfApi()

# Large-scale discovery settings
DEFAULT_LIMIT = 100
PROGRESS_INTERVAL = 1000
MAX_RETRIES = 3
RETRY_DELAY = 5


# ==========================================
# DATASET DISCOVERY AGENT
# ==========================================

class DatasetDiscoveryAgent:
    """
    Large-scale Hugging Face dataset discovery.

    Discovery only:

        Hugging Face
              ↓
        Metadata Agent
              ↓
        Quality Agent
              ↓
        PostgreSQL
              ↓
        Qdrant

    Important:
        This agent DOES NOT download dataset files.

    Hugging Face's list_datasets() returns an iterator.
    The iterator handles API pagination internally.
    """

    def __init__(self):
        self.api = api

    # ======================================
    # DISCOVER DATASETS
    # ======================================

    def discover(
        self,
        limit: int = DEFAULT_LIMIT,
        search: str | None = None,
        offset: int = 0,
        sort: str = "lastModified",
    ) -> Iterator[dict]:
        """
        Discover datasets from Hugging Face.

        Args:
            limit:
                Maximum number of datasets to discover.

            search:
                Optional Hugging Face search query.

            offset:
                Number of datasets to skip.

            sort:
                Hugging Face sorting field.

            direction:
                Sort direction.

                -1 = descending / newest first
                 1 = ascending / oldest first

        Yields:
            Normalized DataSense dataset records.
        """

        if limit <= 0:
            return

        if offset < 0:
            offset = 0

        print(
            f"Starting Hugging Face discovery "
            f"(limit={limit:,}, "
            f"search={search!r}, "
            f"sort={sort})"
        )

        # ----------------------------------
        # Request datasets
        # ----------------------------------

        datasets = None

        for attempt in range(
            1,
            MAX_RETRIES + 1,
        ):

            try:

                # Hugging Face returns an iterator.
                # Pagination is handled internally.

                datasets = self.api.list_datasets(
                    search=search,
                    sort=sort,
                    limit=offset + limit,
                )

                break

            except Exception as error:

                print(
                    f"Hugging Face discovery failed "
                    f"(attempt {attempt}/{MAX_RETRIES}): "
                    f"{error}"
                )

                if attempt >= MAX_RETRIES:
                    raise

                time.sleep(RETRY_DELAY)

        if datasets is None:
            return

        # ----------------------------------
        # Duplicate protection
        # ----------------------------------

        seen_ids = set()

        count = 0
        skipped = 0

        # ----------------------------------
        # Process datasets
        # ----------------------------------

        for dataset in datasets:

            # ----------------------------------
            # Offset support
            # ----------------------------------

            if skipped < offset:

                skipped += 1

                continue

            if count >= limit:
                break

            # ----------------------------------
            # Dataset ID
            # ----------------------------------

            dataset_id = getattr(
                dataset,
                "id",
                None,
            )

            if not dataset_id:
                continue

            normalized_id = (
                str(dataset_id)
                .lower()
                .strip()
            )

            # ----------------------------------
            # Duplicate protection
            # ----------------------------------

            if normalized_id in seen_ids:
                continue

            seen_ids.add(
                normalized_id
            )

            # ----------------------------------
            # Normalize
            # ----------------------------------

            record = self._normalize_dataset(
                dataset
            )

            if not record:
                continue

            count += 1

            # ----------------------------------
            # Progress
            # ----------------------------------

            if (
                count == 1
                or count % PROGRESS_INTERVAL == 0
            ):

                print(
                    f"Discovered {count:,} "
                    f"/ {limit:,} datasets"
                )

            yield record

        # ----------------------------------
        # Completion
        # ----------------------------------

        print(
            f"Hugging Face discovery complete: "
            f"{count:,} datasets"
        )

    # ======================================
    # NORMALIZE DATASET
    # ======================================

    def _normalize_dataset(
        self,
        dataset,
    ):
        """
        Convert Hugging Face DatasetInfo
        into a DataSense-compatible record.
        """

        dataset_id = getattr(
            dataset,
            "id",
            None,
        )

        if not dataset_id:
            return None

        # ----------------------------------
        # Name
        # ----------------------------------

        name = str(
            dataset_id
        ).split("/")[-1]

        # ----------------------------------
        # Description
        # ----------------------------------

        description = (
            getattr(
                dataset,
                "description",
                None,
            )
            or ""
        )

        # ----------------------------------
        # Tags
        # ----------------------------------

        tags = getattr(
            dataset,
            "tags",
            None,
        ) or []

        if not isinstance(
            tags,
            (list, tuple, set),
        ):
            tags = [tags]

        # ----------------------------------
        # Dataset URL
        # ----------------------------------

        download_url = (
            "https://huggingface.co/datasets/"
            f"{dataset_id}"
        )

        # ----------------------------------
        # License
        # ----------------------------------

        license_name = None

        card_data = getattr(
            dataset,
            "card_data",
            None,
        )

        if card_data:

            license_name = getattr(
                card_data,
                "license",
                None,
            )

        # ----------------------------------
        # Downloads
        # ----------------------------------

        downloads = getattr(
            dataset,
            "downloads",
            0,
        ) or 0

        # ----------------------------------
        # Likes
        # ----------------------------------

        likes = getattr(
            dataset,
            "likes",
            0,
        ) or 0

        # ----------------------------------
        # Normalized record
        # ----------------------------------

        return {
            "name": name,

            "slug": self._create_slug(
                dataset_id
            ),

            "description": description,

            "category": self._infer_category(
                tags,
                description,
            ),

            "ml_task": self._infer_ml_task(
                tags
            ),

            "data_type": self._infer_data_type(
                tags
            ),

            "difficulty": None,

            "source": SOURCE_NAME,

            "download_url": download_url,

            "license": license_name,

            "rows": None,

            "columns": None,

            "file_size": None,

            "target_column": None,

            "language": self._extract_language(
                tags
            ),

            "tags": self._format_tags(
                tags
            ),

            "thumbnail": None,

            "downloads": downloads,

            "rating": None,

            # Internal source information
            "_source_id": dataset_id,

            "_source_likes": likes,
        }

    # ======================================
    # CREATE SLUG
    # ======================================

    @staticmethod
    def _create_slug(
        dataset_id: str,
    ):
        """
        Convert Hugging Face ID into
        a DataSense-friendly slug.
        """

        slug = str(
            dataset_id
        ).lower()

        slug = slug.replace(
            "/",
            "-",
        )

        slug = slug.replace(
            "_",
            "-",
        )

        return slug

    # ======================================
    # FORMAT TAGS
    # ======================================

    @staticmethod
    def _format_tags(tags):
        """
        Convert tags into comma-separated
        format used by DataSense.
        """

        if not tags:
            return ""

        cleaned = []

        for tag in tags:

            if not tag:
                continue

            tag = str(
                tag
            ).strip()

            if tag:
                cleaned.append(
                    tag
                )

        # Avoid extremely large metadata
        return ",".join(
            cleaned[:50]
        )

    # ======================================
    # LANGUAGE
    # ======================================

    @staticmethod
    def _extract_language(tags):
        """
        Extract language information from
        Hugging Face tags.
        """

        for tag in tags:

            if not tag:
                continue

            tag = str(
                tag
            ).strip()

            if tag.startswith(
                "language:"
            ):

                return tag.split(
                    ":",
                    1,
                )[1]

        return None

    # ======================================
    # DATA TYPE
    # ======================================

    @staticmethod
    def _infer_data_type(tags):
        """
        Infer a compatible data type
        from Hugging Face tags.
        """

        text = " ".join(
            str(tag)
            for tag in tags
            if tag
        ).lower()

        rules = (

            (
                "Multimodal",
                (
                    "multimodal",
                    "multi-modal",
                    "image-text",
                    "video-text",
                    "audio-text",
                    "vision-language",
                ),
            ),

            (
                "Image",
                (
                    "modality:image",
                    "imagefolder",
                    "computer-vision",
                    "image",
                    "vision",
                ),
            ),

            (
                "Audio",
                (
                    "modality:audio",
                    "audio",
                    "speech",
                    "voice",
                    "sound",
                    "asr",
                    "tts",
                ),
            ),

            (
                "Video",
                (
                    "modality:video",
                    "video",
                ),
            ),

            (
                "Tabular",
                (
                    "tabular",
                    "csv",
                    "parquet",
                    "dataframe",
                    "spreadsheet",
                    "database",
                ),
            ),

            (
                "Text",
                (
                    "modality:text",
                    "text",
                    "nlp",
                    "natural-language-processing",
                    "language",
                    "document",
                ),
            ),
        )

        for data_type, keywords in rules:

            if any(
                keyword in text
                for keyword in keywords
            ):

                return data_type

        return "Other"

    # ======================================
    # CATEGORY
    # ======================================

    @staticmethod
    def _infer_category(
        tags,
        description,
    ):
        """
        Conservative source-level category.

        The Metadata Agent remains responsible
        for final classification.
        """

        text = " ".join(
            str(tag)
            for tag in tags
        )

        text += " "

        text += str(
            description or ""
        )

        text = text.lower()

        # ----------------------------------
        # Healthcare
        # ----------------------------------

        if any(
            word in text
            for word in [
                "health",
                "healthcare",
                "medical",
                "medicine",
                "disease",
                "clinical",
                "patient",
                "diagnosis",
            ]
        ):

            return "Healthcare"

        # ----------------------------------
        # Finance
        # ----------------------------------

        if any(
            word in text
            for word in [
                "finance",
                "financial",
                "stock",
                "banking",
                "market",
                "investment",
            ]
        ):

            return "Finance"

        # ----------------------------------
        # Computer Vision
        # ----------------------------------

        if any(
            word in text
            for word in [
                "image",
                "images",
                "vision",
                "computer-vision",
                "object-detection",
                "image-classification",
                "segmentation",
            ]
        ):

            return "Computer Vision"

        # ----------------------------------
        # NLP
        # ----------------------------------

        if any(
            word in text
            for word in [
                "nlp",
                "natural-language-processing",
                "text",
                "language",
                "sentiment",
                "question-answering",
                "summarization",
                "translation",
            ]
        ):

            return "NLP"

        # ----------------------------------
        # Education
        # ----------------------------------

        if any(
            word in text
            for word in [
                "education",
                "school",
                "student",
                "learning",
                "academic",
            ]
        ):

            return "Education"

        # ----------------------------------
        # Time Series
        # ----------------------------------

        if any(
            word in text
            for word in [
                "time-series",
                "timeseries",
                "forecasting",
                "forecast",
            ]
        ):

            return "Time Series"

        return "Other"

    # ======================================
    # ML TASK
    # ======================================

    @staticmethod
    def _infer_ml_task(tags):

        text = " ".join(
            str(tag)
            for tag in tags
        ).lower()

        # ----------------------------------
        # Classification
        # ----------------------------------

        if any(
            word in text
            for word in [
                "classification",
                "text-classification",
                "image-classification",
                "multi-class-classification",
                "multiclass-classification",
            ]
        ):

            return "Classification"

        # ----------------------------------
        # Regression
        # ----------------------------------

        if any(
            word in text
            for word in [
                "regression",
                "tabular-regression",
            ]
        ):

            return "Regression"

        # ----------------------------------
        # Object Detection
        # ----------------------------------

        if any(
            word in text
            for word in [
                "object-detection",
                "object detection",
            ]
        ):

            return "Object Detection"

        # ----------------------------------
        # Segmentation
        # ----------------------------------

        if any(
            word in text
            for word in [
                "image-segmentation",
                "semantic-segmentation",
                "instance-segmentation",
                "segmentation",
            ]
        ):

            return "Segmentation"

        # ----------------------------------
        # Summarization
        # ----------------------------------

        if any(
            word in text
            for word in [
                "summarization",
                "text-summarization",
            ]
        ):

            return "Summarization"

        # ----------------------------------
        # Question Answering
        # ----------------------------------

        if any(
            word in text
            for word in [
                "question-answering",
                "question answering",
            ]
        ):

            return "Question Answering"

        # ----------------------------------
        # Translation
        # ----------------------------------

        if any(
            word in text
            for word in [
                "translation",
                "text-translation",
            ]
        ):

            return "Translation"

        return None


# ==========================================
# SINGLE AGENT INSTANCE
# ==========================================

discovery_agent = DatasetDiscoveryAgent()