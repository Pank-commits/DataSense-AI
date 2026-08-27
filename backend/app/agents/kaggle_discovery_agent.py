from kaggle.api.kaggle_api_extended import KaggleApi


class KaggleDiscoveryAgent:
    """
    Kaggle Dataset Discovery Agent

    Responsibilities:
        1. Discover datasets from Kaggle
        2. Normalize Kaggle metadata
        3. Infer obvious category / ML task / data type
        4. Return the common DataSense dataset format

    The existing Metadata Agent can further enrich these records.
    """

    def __init__(self):
        self.api = KaggleApi()
        self.api.authenticate()

    # ==========================================================
    # TEXT HELPERS
    # ==========================================================

    @staticmethod
    def _text(value):
        if value is None:
            return ""

        if isinstance(value, list):
            return " ".join(
                str(item)
                for item in value
            )

        return str(value).strip()

    @staticmethod
    def _normalize(value):
        text = (
            KaggleDiscoveryAgent._text(value)
            .lower()
        )

        text = text.replace(
            "_",
            " ",
        )

        text = text.replace(
            "-",
            " ",
        )

        return " ".join(
            text.split()
        )

    # ==========================================================
    # CATEGORY INFERENCE
    # ==========================================================

    def _infer_category(
        self,
        name,
        description,
        tags,
    ):
        text = self._normalize(
            f"{name} {description} {tags}"
        )

        # ------------------------------------------
        # Healthcare
        # ------------------------------------------

        healthcare = [
            "healthcare",
            "health care",
            "medical",
            "medicine",
            "patient",
            "hospital",
            "clinical",
            "disease",
            "diagnosis",
            "diabetes",
            "heart disease",
            "cancer",
            "tumor",
            "mri",
            "xray",
            "x ray",
            "radiology",
            "knee",
            "health",
        ]

        if any(
            keyword in text
            for keyword in healthcare
        ):
            return "Healthcare"

        # ------------------------------------------
        # Finance
        # ------------------------------------------

        finance = [
            "finance",
            "financial",
            "banking",
            "credit",
            "loan",
            "mortgage",
            "stock",
            "stocks",
            "trading",
            "investment",
            "portfolio",
            "fraud detection",
            "financial risk",
        ]

        if any(
            keyword in text
            for keyword in finance
        ):
            return "Finance"

        # ------------------------------------------
        # Education
        # ------------------------------------------

        education = [
            "education",
            "educational",
            "student",
            "students",
            "school",
            "university",
            "college",
            "exam",
            "academic",
            "study habits",
            "student performance",
        ]

        if any(
            keyword in text
            for keyword in education
        ):
            return "Education"

        # ------------------------------------------
        # Retail / E-Commerce
        # ------------------------------------------

        retail = [
            "retail",
            "ecommerce",
            "e commerce",
            "shopping",
            "customer",
            "customers",
            "sales",
            "product",
            "products",
            "store",
            "purchase",
            "consumer",
            "food delivery",
            "delivery orders",
        ]

        if any(
            keyword in text
            for keyword in retail
        ):
            return "Retail"

        # ------------------------------------------
        # Agriculture
        # ------------------------------------------

        agriculture = [
            "agriculture",
            "agricultural",
            "crop",
            "crops",
            "farming",
            "farm",
            "soil",
            "plant disease",
            "plant",
            "yield",
            "irrigation",
            "pesticide",
            "fertilizer",
            "rice",
            "wheat",
            "maize",
            "corn",
        ]

        if any(
            keyword in text
            for keyword in agriculture
        ):
            return "Agriculture"

        # ------------------------------------------
        # Computer Vision
        # ------------------------------------------

        computer_vision = [
            "computer vision",
            "image",
            "images",
            "image classification",
            "object detection",
            "segmentation",
            "face recognition",
            "facial",
            "ocr",
            "mnist",
            "cifar",
            "coco",
            "mri",
            "xray",
        ]

        if any(
            keyword in text
            for keyword in computer_vision
        ):
            return "Computer Vision"

        # ------------------------------------------
        # NLP
        # ------------------------------------------

        nlp = [
            "nlp",
            "natural language",
            "text classification",
            "sentiment",
            "sentiment analysis",
            "translation",
            "question answering",
            "language model",
            "text generation",
            "document classification",
        ]

        if any(
            keyword in text
            for keyword in nlp
        ):
            return "NLP"

        # ------------------------------------------
        # Audio / Speech
        # ------------------------------------------

        audio = [
            "audio",
            "speech",
            "voice",
            "music",
            "song",
            "sound",
            "speaker",
            "spotify",
        ]

        if any(
            keyword in text
            for keyword in audio
        ):
            return "Audio & Speech"

        # ------------------------------------------
        # Entertainment
        # ------------------------------------------

        entertainment = [
            "netflix",
            "movies",
            "movie",
            "tv shows",
            "television",
            "films",
            "film",
            "spotify",
            "music streaming",
        ]

        if any(
            keyword in text
            for keyword in entertainment
        ):
            return "Entertainment"

        # ------------------------------------------
        # Real Estate
        # ------------------------------------------

        real_estate = [
            "house price",
            "house prices",
            "housing price",
            "housing prices",
            "real estate",
            "property price",
            "property prices",
            "home price",
            "home prices",
        ]

        if any(
            keyword in text
            for keyword in real_estate
        ):
            return "Real Estate"

        return "Other"

    # ==========================================================
    # ML TASK INFERENCE
    # ==========================================================

    def _infer_ml_task(
        self,
        name,
        description,
        tags,
    ):
        text = self._normalize(
            f"{name} {description} {tags}"
        )

        # ------------------------------------------
        # Classification
        # ------------------------------------------

        classification = [
            "classification",
            "classifier",
            "classify",
            "classification dataset",
            "disease prediction",
            "diagnosis",
            "fraud detection",
            "spam detection",
            "sentiment analysis",
            "image classification",
        ]

        if any(
            keyword in text
            for keyword in classification
        ):
            return "Classification"

        # ------------------------------------------
        # Regression
        # ------------------------------------------

        regression = [
            "regression",
            "price prediction",
            "house price prediction",
            "house prices",
            "housing price prediction",
            "salary prediction",
            "sales prediction",
            "eta prediction",
            "demand prediction",
        ]

        if any(
            keyword in text
            for keyword in regression
        ):
            return "Regression"

        # ------------------------------------------
        # Forecasting
        # ------------------------------------------

        forecasting = [
            "forecast",
            "forecasting",
            "time series",
            "time-series",
            "future sales",
            "future demand",
            "sales forecasting",
        ]

        if any(
            keyword in text
            for keyword in forecasting
        ):
            return "Forecasting"

        # ------------------------------------------
        # Clustering
        # ------------------------------------------

        clustering = [
            "clustering",
            "cluster analysis",
            "customer segmentation",
            "segmentation",
        ]

        if any(
            keyword in text
            for keyword in clustering
        ):
            return "Clustering"

        return "Other"

    # ==========================================================
    # DATA TYPE INFERENCE
    # ==========================================================

    def _infer_data_type(
        self,
        name,
        description,
        tags,
    ):
        text = self._normalize(
            f"{name} {description} {tags}"
        )

        # ------------------------------------------
        # Image
        # ------------------------------------------

        image_keywords = [
            "image",
            "images",
            "mri",
            "xray",
            "x ray",
            "computer vision",
            "image classification",
            "object detection",
            "image segmentation",
            "jpeg",
            "jpg",
            "png",
        ]

        if any(
            keyword in text
            for keyword in image_keywords
        ):
            return "Image"

        # ------------------------------------------
        # Video
        # ------------------------------------------

        video_keywords = [
            "video",
            "videos",
            "video classification",
            "video dataset",
        ]

        if any(
            keyword in text
            for keyword in video_keywords
        ):
            return "Video"

        # ------------------------------------------
        # Audio
        # ------------------------------------------

        audio_keywords = [
            "audio",
            "speech",
            "voice",
            "music",
            "sound",
            "wav",
            "mp3",
        ]

        if any(
            keyword in text
            for keyword in audio_keywords
        ):
            return "Audio"

        # ------------------------------------------
        # Text
        # ------------------------------------------

        text_keywords = [
            "text",
            "nlp",
            "natural language",
            "sentiment",
            "document",
            "documents",
            "language",
            "text classification",
        ]

        if any(
            keyword in text
            for keyword in text_keywords
        ):
            return "Text"

        # ------------------------------------------
        # Tabular
        # ------------------------------------------

        tabular_keywords = [
            "csv",
            "excel",
            "spreadsheet",
            "tabular",
            "table",
            "structured data",
            "sales",
            "students",
            "house price",
            "house prices",
            "customer",
            "ecommerce",
            "e commerce",
        ]

        if any(
            keyword in text
            for keyword in tabular_keywords
        ):
            return "Tabular"

        return "Unknown"

    # ==========================================================
    # DISCOVERY
    # ==========================================================

    def discover(
        self,
        limit: int = 100,
        search: str | None = None,
    ):
        """
        Discover datasets from Kaggle.
        """

        print(
            f"Starting Kaggle discovery "
            f"(limit={limit}, search={search})"
        )

        datasets = []

        try:

            results = self.api.dataset_list(
                search=search,
                page=1,
                max_size=None,
            )

            for item in results:

                if len(datasets) >= limit:
                    break

                dataset_ref = getattr(
                    item,
                    "ref",
                    None,
                )

                if not dataset_ref:
                    continue

                name = getattr(
                    item,
                    "title",
                    None,
                )

                description = getattr(
                    item,
                    "subtitle",
                    None,
                )

                name = (
                    self._text(name)
                    or dataset_ref.split(
                        "/"
                    )[-1]
                )

                description = (
                    self._text(
                        description
                    )
                )

                # --------------------------------------
                # Tags
                # --------------------------------------

                tags = getattr(
                    item,
                    "tags",
                    None,
                )

                tags = self._text(
                    tags
                )

                # --------------------------------------
                # Stable slug
                # --------------------------------------

                slug = (
                    dataset_ref
                    .replace(
                        "/",
                        "-",
                    )
                    .replace(
                        "_",
                        "-",
                    )
                    .lower()
                )

                # --------------------------------------
                # Kaggle URL
                # --------------------------------------

                download_url = (
                    "https://www.kaggle.com/datasets/"
                    f"{dataset_ref}"
                )

                # --------------------------------------
                # Downloads
                # --------------------------------------

                downloads = getattr(
                    item,
                    "downloadCount",
                    0,
                )

                try:
                    downloads = int(
                        downloads or 0
                    )
                except (
                    TypeError,
                    ValueError,
                ):
                    downloads = 0

                # --------------------------------------
                # Dataset object
                # --------------------------------------

                dataset = {

                    "_source_id":
                        dataset_ref,

                    "_source":
                        "Kaggle",

                    "_last_modified":
                        None,

                    "name":
                        name,

                    "slug":
                        slug,

                    "description":
                        (
                            description
                            or
                            "Dataset description "
                            "not available."
                        ),

                    "category":
                        "Unknown",

                    "ml_task":
                        "Unknown",

                    "data_type":
                        "Unknown",

                    "difficulty":
                        "Unknown",

                    "source":
                        "Kaggle",

                    "download_url":
                        download_url,

                    "license":
                        "Unknown",

                    "rows":
                        0,

                    "columns":
                        0,

                    "file_size":
                        "Unknown",

                    "target_column":
                        "Unknown",

                    "language":
                        "Unknown",

                    "tags":
                        tags,

                    "thumbnail":
                        None,

                    "downloads":
                        downloads,

                    "rating":
                        0.0,
                }

                datasets.append(
                    dataset
                )

                print(
                    f"Discovered "
                    f"{len(datasets)} / "
                    f"{limit}: "
                    f"{name}"
                )

        except Exception as error:

            print(
                "Kaggle discovery failed: "
                f"{error}"
            )

            raise

        print(
            f"Kaggle discovery complete: "
            f"{len(datasets)} datasets"
        )

        return datasets


# ==========================================================
# SINGLE INSTANCE
# ==========================================================

kaggle_discovery_agent = (
    KaggleDiscoveryAgent()
)