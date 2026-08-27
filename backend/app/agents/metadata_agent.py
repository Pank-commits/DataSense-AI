import re
from typing import Any


# ============================================================
# METADATA AGENT
# ============================================================

class DatasetMetadataAgent:
    """
    Dataset Metadata Agent

    Responsibilities:
        1. Normalize dataset metadata
        2. Infer category
        3. Infer ML task
        4. Infer data type
        5. Infer difficulty
        6. Detect license
        7. Attach confidence scores

    Designed for large-scale dataset ingestion.
    """

    # ========================================================
    # CONSTANTS
    # ========================================================

    UNKNOWN = "Unknown"
    OTHER = "Other"

    # ========================================================
    # CATEGORY RULES
    # ========================================================

    CATEGORY_OVERRIDES = {
        "heart disease prediction": "Healthcare",
        "pima diabetes": "Healthcare",
        "diabetes": "Healthcare",
        "breast cancer wisconsin": "Healthcare",
        "breast cancer": "Healthcare",
        "heart disease": "Healthcare",

        "house prices": "Finance",
        "housing prices": "Finance",
        "california housing": "Finance",
        "adult income": "Finance",
        "credit card fraud": "Finance",
        "loan prediction": "Finance",

        "customer churn": "Retail",

        "amazon reviews": "NLP",
        "imdb reviews": "NLP",
        "imdb": "NLP",
        "fake news": "NLP",
        "sms spam": "NLP",
        "wikipedia": "NLP",

        "mnist": "Computer Vision",
        "fashion mnist": "Computer Vision",
        "cifar": "Computer Vision",

        "crop recommendation": "Agriculture",

        "air quality": "Time Series",
        "bike sharing": "Time Series",
        "energy consumption": "Time Series",

        "iris": "Other",
        "titanic survival": "Other",
    }

    CATEGORY_RULES = {

        "Healthcare": [
            "healthcare",
            "health care",
            "medical",
            "medicine",
            "patient",
            "hospital",
            "clinical",
            "disease",
            "diagnosis",
            "diagnostic",
            "diabetes",
            "pima",
            "heart disease",
            "breast cancer",
            "cancer",
            "tumor",
            "mri",
            "xray",
            "x-ray",
            "radiology",
            "pathology",
            "epidemiology",
            "mental health",
            "health",
        ],

        "Finance": [
            "finance",
            "financial",
            "banking",
            "bank",
            "credit",
            "credit card",
            "credit risk",
            "loan",
            "mortgage",
            "stock",
            "stocks",
            "trading",
            "investment",
            "investing",
            "portfolio",
            "fraud",
            "transaction",
            "income",
            "adult income",
            "financial risk",
        ],

        "Agriculture": [
            "agriculture",
            "agricultural",
            "crop",
            "crops",
            "farming",
            "farm",
            "soil",
            "plant",
            "plants",
            "leaf",
            "leaves",
            "yield",
            "irrigation",
            "pesticide",
            "fertilizer",
            "rice",
            "wheat",
            "maize",
            "corn",
        ],

        "Retail": [
            "retail",
            "customer",
            "customers",
            "shopping",
            "ecommerce",
            "e-commerce",
            "product recommendation",
            "recommendation",
            "sales",
            "store",
            "market basket",
            "transaction",
            "purchase",
            "consumer",
        ],

        "Computer Vision": [
            "computer vision",
            "image",
            "images",
            "imagefolder",
            "visual",
            "vision",
            "object detection",
            "segmentation",
            "image classification",
            "face recognition",
            "facial",
            "ocr",
            "handwritten",
            "mnist",
            "fashion mnist",
            "cifar",
            "coco",
        ],

        "NLP": [
            "nlp",
            "natural language",
            "text",
            "textual",
            "language",
            "linguistic",
            "sentiment",
            "sentiment analysis",
            "translation",
            "question answering",
            "question-answering",
            "summarization",
            "text generation",
            "fill-mask",
            "masked language",
            "language modeling",
            "language-modeling",
            "tokenization",
            "ner",
            "named entity",
            "chat",
            "conversation",
            "dialogue",
            "document",
            "documents",
            "wikipedia",
            "reviews",
            "imdb",
            "spam",
            "fake news",
        ],

        "Audio & Speech": [
            "audio",
            "speech",
            "voice",
            "sound",
            "asr",
            "speech recognition",
            "text to speech",
            "text-to-speech",
            "tts",
            "whisper",
            "speaker",
            "music",
            "sound classification",
        ],

        "Robotics": [
            "robot",
            "robotics",
            "robotic",
            "lerobot",
            "xarm",
            "manipulation",
            "reinforcement learning",
            "embodied ai",
            "embodied",
            "trajectory",
            "robot arm",
        ],

        "Time Series": [
            "time series",
            "timeseries",
            "forecast",
            "forecasting",
            "temporal",
            "timestamp",
            "stock price",
            "weather forecast",
            "energy consumption",
            "sensor data",
        ],

        "Education": [
            "education",
            "educational",
            "student",
            "students",
            "school",
            "university",
            "learning",
            "exam",
            "course",
            "teacher",
            "teaching",
            "academic",
        ],

        "Entertainment": [
            "netflix",
            "movie",
            "movies",
            "film",
            "films",
            "tv show",
            "tv shows",
            "television",
            "entertainment",
        ],

        "Real Estate": [
            "house price",
            "house prices",
            "housing price",
            "housing prices",
            "real estate",
            "property price",
            "property prices",
            "home price",
            "home prices",
        ],
    }

    # ========================================================
    # ML TASK RULES
    # ========================================================

    ML_TASK_RULES = {

        "Classification": [
            "task_categories:text-classification",
            "task_categories:image-classification",
            "task_categories:audio-classification",
            "task_categories:tabular-classification",
            "task_categories:multi-class-classification",
            "task_categories:classification",
            "task_ids:classification",
            "classification",
            "classify",
            "classifying",
            "categorization",
            "categorisation",
            "binary classification",
            "multiclass classification",
            "multi-class classification",
        ],

        "Regression": [
            "task_categories:tabular-regression",
            "task_categories:regression",
            "task_ids:regression",
            "regression",
            "regress",
            "continuous prediction",
            "predict a value",
            "price prediction",
            "house prices",
            "housing prices",
        ],

        "Clustering": [
            "task_categories:clustering",
            "task_ids:clustering",
            "clustering",
            "cluster",
            "clusters",
            "group similar",
        ],

        "Object Detection": [
            "task_categories:object-detection",
            "task_ids:object-detection",
            "object detection",
            "object-detection",
            "bounding box",
            "bounding boxes",
        ],

        "Image Segmentation": [
            "task_categories:image-segmentation",
            "task_ids:image-segmentation",
            "image segmentation",
            "image-segmentation",
            "semantic segmentation",
            "instance segmentation",
        ],

        "Text Generation": [
            "task_categories:text-generation",
            "task_ids:text-generation",
            "text generation",
            "text-generation",
            "language modeling",
            "language-modeling",
            "language model",
        ],

        "Question Answering": [
            "task_categories:question-answering",
            "task_ids:question-answering",
            "question answering",
            "question-answering",
            "qa",
        ],

        "Text Summarization": [
            "task_categories:text-summarization",
            "task_ids:text-summarization",
            "text summarization",
            "text-summarization",
            "summarization",
        ],

        "Translation": [
            "task_categories:translation",
            "task_ids:translation",
            "translation",
        ],

        "Speech Recognition": [
            "task_categories:automatic-speech-recognition",
            "task_ids:automatic-speech-recognition",
            "automatic speech recognition",
            "speech recognition",
            "speech-to-text",
            "speech to text",
            "asr",
            "whisper",
        ],

        "Text to Speech": [
            "task_categories:text-to-speech",
            "task_ids:text-to-speech",
            "text to speech",
            "text-to-speech",
            "tts",
        ],

        "Named Entity Recognition": [
            "task_categories:token-classification",
            "task_ids:token-classification",
            "named entity recognition",
            "named-entity-recognition",
            "ner",
            "token classification",
        ],

        "Fill Mask": [
            "task_categories:fill-mask",
            "task_ids:fill-mask",
            "fill mask",
            "fill-mask",
            "masked language modeling",
            "masked-language-modeling",
        ],

        "Ranking": [
            "task_categories:ranking",
            "task_ids:ranking",
            "ranking",
            "rank prediction",
        ],

        "Reinforcement Learning": [
            "task_categories:reinforcement-learning",
            "task_ids:reinforcement-learning",
            "reinforcement learning",
            "reinforcement-learning",
        ],
    }

    # ========================================================
    # DATA TYPE RULES
    # ========================================================

    DATA_TYPE_RULES = {

        "Image": [
            "modality:image",
            "format:imagefolder",
            "image",
            "images",
            "imagefolder",
            "jpg",
            "jpeg",
            "png",
            "bmp",
            "vision",
            "computer vision",
            "mnist",
            "cifar",
        ],

        "Audio": [
            "modality:audio",
            "audio",
            "speech",
            "voice",
            "sound",
            "wav",
            "mp3",
            "flac",
            "asr",
            "tts",
            "whisper",
        ],

        "Video": [
            "modality:video",
            "video",
            "videos",
            "mp4",
            "avi",
            "mov",
            "mkv",
            "webm",
        ],

        "Text": [
            "modality:text",
            "text",
            "textual",
            "nlp",
            "natural language",
            "language",
            "document",
            "documents",
            "sentiment",
            "reviews",
            "wikipedia",
        ],

        "Tabular": [
            "task_categories:tabular-classification",
            "task_categories:tabular-regression",
            "tabular",
            "table",
            "tables",
            "csv",
            "spreadsheet",
            "dataframe",
            "parquet",
            "database",
            "structured data",
        ],

        "Multimodal": [
            "multimodal",
            "multi-modal",
            "image-text",
            "image text",
            "video-text",
            "audio-text",
            "vision-language",
            "language-vision",
        ],
    }

    # ========================================================
    # DIFFICULTY RULES
    # ========================================================

    DIFFICULTY_RULES = {

        "Beginner": [
            "beginner",
            "beginners",
            "easy",
            "simple",
            "starter",
            "starting",
            "introductory",
            "intro",
            "basic",
            "toy dataset",
            "iris",
            "titanic",
        ],

        "Intermediate": [
            "intermediate",
            "medium",
            "moderate",
        ],

        "Advanced": [
            "advanced",
            "expert",
            "hard",
            "complex",
            "large scale",
            "large-scale",
            "massive",
            "production",
            "benchmark",
            "reinforcement learning",
            "multimodal",
        ],
    }

    # ========================================================
    # PUBLIC API
    # ========================================================

    def process(
        self,
        dataset: dict,
    ) -> dict:

        if not dataset:
            return {}

        data = dict(dataset)

        name = self._clean_text(
            data.get("name")
        )

        description = self._clean_text(
            data.get("description")
        )

        tags = self._clean_text(
            data.get("tags")
        )

        source_text = self._clean_text(
            data.get("source")
        )

        combined_text = self._normalize(
            " ".join(
                [
                    name,
                    description,
                    tags,
                    source_text,
                ]
            )
        )

        # ----------------------------------------
        # Agent inference
        # ----------------------------------------

        detected_category, category_confidence = (
            self._detect_category(
                name=name,
                description=description,
                tags=tags,
                combined_text=combined_text,
            )
        )

        detected_ml_task, ml_task_confidence = (
            self._detect_ml_task(
                name=name,
                description=description,
                tags=tags,
                combined_text=combined_text,
            )
        )

        detected_data_type, data_type_confidence = (
            self._detect_data_type(
                name=name,
                description=description,
                tags=tags,
                combined_text=combined_text,
                ml_task=detected_ml_task,
            )
        )

        detected_difficulty, difficulty_confidence = (
            self._detect_difficulty(
                name=name,
                description=description,
                tags=tags,
                combined_text=combined_text,
            )
        )

        detected_license, license_detected = (
            self._detect_license(
                data.get("license"),
                tags,
                description,
            )
        )

        # ==================================================
        # PRESERVE RELIABLE SOURCE METADATA
        # ==================================================

        existing_category = self._clean_text(
            data.get("category")
        )

        existing_ml_task = self._clean_text(
            data.get("ml_task")
        )

        existing_data_type = self._clean_text(
            data.get("data_type")
        )

        existing_difficulty = self._clean_text(
            data.get("difficulty")
        )

        existing_license = self._clean_text(
            data.get("license")
        )

        # ----------------------------------------
        # Category
        # ----------------------------------------

        if self._is_reliable(
            existing_category,
            [
                self.UNKNOWN,
                self.OTHER,
            ],
        ):
            final_category = existing_category
            final_category_confidence = 0.99
        else:
            final_category = detected_category
            final_category_confidence = category_confidence

        # ----------------------------------------
        # ML task
        # ----------------------------------------

        if self._is_reliable(
            existing_ml_task,
            [
                self.UNKNOWN,
                self.OTHER,
            ],
        ):
            final_ml_task = existing_ml_task
            final_ml_task_confidence = 0.99
        else:
            final_ml_task = detected_ml_task
            final_ml_task_confidence = ml_task_confidence

        # Do not preserve a contradictory source value when explicit tags
        # and prediction language identify supervised classification.
        normalized_tags = self._normalize(tags)
        classification_tag = (
            "classification" in normalized_tags.split()
            or "tabular classification" in normalized_tags
        )
        if (
            classification_tag
            and final_ml_task == "Reinforcement Learning"
        ):
            final_ml_task = "Classification"
            final_ml_task_confidence = 0.99

        # ----------------------------------------
        # Data type
        # ----------------------------------------

        if self._is_reliable(
            existing_data_type,
            [
                self.UNKNOWN,
                self.OTHER,
            ],
        ):
            final_data_type = existing_data_type
            final_data_type_confidence = 0.99
        else:
            final_data_type = detected_data_type
            final_data_type_confidence = data_type_confidence

        # Explicit tabular tags are authoritative for both Kaggle and
        # Hugging Face records, even when an older stored type says Text.
        if any(
            phrase in normalized_tags
            for phrase in ["tabular", "tabular classification", "tabular regression"]
        ):
            final_data_type = "Tabular"
            final_data_type_confidence = 0.99

        # ----------------------------------------
        # Difficulty
        # ----------------------------------------

        if self._is_reliable(
            existing_difficulty,
            [
                self.UNKNOWN,
            ],
        ):
            final_difficulty = existing_difficulty
            final_difficulty_confidence = 0.99
        else:
            final_difficulty = detected_difficulty
            final_difficulty_confidence = difficulty_confidence

        # ----------------------------------------
        # License
        # ----------------------------------------

        if self._is_reliable(
            existing_license,
            [
                self.UNKNOWN,
                "None",
                "null",
            ],
        ):
            final_license = existing_license
            final_license_detected = True
        else:
            final_license = detected_license
            final_license_detected = license_detected

        # ==================================================
        # APPLY
        # ==================================================

        data["name"] = (
            name
            or "Unknown Dataset"
        )

        data["description"] = (
            description
            or "Dataset description not available."
        )

        data["category"] = final_category

        data["ml_task"] = final_ml_task

        data["data_type"] = final_data_type

        data["difficulty"] = final_difficulty

        data["license"] = final_license

        # ==================================================
        # METADATA INFORMATION
        # ==================================================

        data["_metadata_agent"] = {
            "processed": True,

            "category_confidence": round(
                final_category_confidence,
                2,
            ),

            "ml_task_confidence": round(
                final_ml_task_confidence,
                2,
            ),

            "data_type_confidence": round(
                final_data_type_confidence,
                2,
            ),

            "difficulty_confidence": round(
                final_difficulty_confidence,
                2,
            ),

            "license_detected":
                final_license_detected,
        }

        return data

    # ========================================================
    # BATCH PROCESSING
    # ========================================================

    def process_batch(
        self,
        datasets: list[dict],
    ) -> list[dict]:

        if not datasets:
            return []

        processed = []

        for dataset in datasets:

            try:

                result = self.process(
                    dataset
                )

                if result:
                    processed.append(
                        result
                    )

            except Exception as error:

                print(
                    "Metadata processing failed "
                    f"for {dataset.get('name')}: "
                    f"{error}"
                )

        return processed

    # ========================================================
    # CATEGORY DETECTION
    # ========================================================

    def _detect_category(
        self,
        name: str,
        description: str,
        tags: str,
        combined_text: str,
    ):

        name_text = self._normalize(
            name
        )

        tags_text = self._normalize(
            tags
        )

        description_text = self._normalize(
            description
        )

        combined_text = self._normalize(
            combined_text
        )

        # ----------------------------------------
        # Dataset-specific overrides
        # ----------------------------------------

        for dataset_name, category in (
            self.CATEGORY_OVERRIDES.items()
        ):

            override_key = self._normalize(
                dataset_name
            )

            if name_text == override_key:
                return (
                    category,
                    0.99,
                )

            if (
                override_key
                and override_key in name_text
                and len(
                    override_key.split()
                ) >= 2
            ):
                return (
                    category,
                    0.98,
                )

        # ----------------------------------------
        # Category scoring
        # ----------------------------------------

        best_category = self.OTHER
        best_score = 0.0
        second_score = 0.0

        weak_keywords = {
            "health",
            "income",
            "customer",
            "customers",
            "transaction",
            "consumer",
            "learning",
            "data",
            "dataset",
            "document",
            "documents",
            "text",
            "language",
            "plant",
            "product",
            "recommendation",
        }

        for category, keywords in (
            self.CATEGORY_RULES.items()
        ):

            score = 0.0

            for keyword in keywords:

                key = self._normalize(
                    keyword
                )

                if not key:
                    continue

                is_weak = (
                    key in weak_keywords
                )

                # Name = strongest
                if key in name_text:

                    score += (
                        1.50
                        if not is_weak
                        else 0.25
                    )

                # Tags
                if key in tags_text:

                    score += (
                        1.10
                        if not is_weak
                        else 0.20
                    )

                # Description
                if key in description_text:

                    score += (
                        0.35
                        if not is_weak
                        else 0.05
                    )

            if score > best_score:

                second_score = best_score
                best_score = score
                best_category = category

            elif score > second_score:

                second_score = score

        # ----------------------------------------
        # Confidence
        # ----------------------------------------

        if best_score >= 2.50:
            confidence = 0.98

        elif best_score >= 1.50:
            confidence = 0.95

        elif best_score >= 1.00:
            confidence = 0.85

        elif best_score >= 0.60:
            confidence = 0.70

        else:

            confidence = 0.25
            best_category = self.OTHER

        if (
            best_category != self.OTHER
            and second_score > 0
            and (
                best_score
                - second_score
            ) < 0.20
        ):

            confidence = min(
                confidence,
                0.60,
            )

        return (
            best_category,
            confidence,
        )

    # ========================================================
    # ML TASK DETECTION
    # ========================================================

    def _detect_ml_task(
        self,
        name: str,
        description: str,
        tags: str,
        combined_text: str,
    ):

        name_text = self._normalize(
            name
        )

        tags_text = self._normalize(
            tags
        )

        combined_text = self._normalize(
            combined_text
        )

        # Explicit source tags take priority over incidental task keywords.
        explicit_classification = (
            "classification" in tags_text.split()
            or "classify" in tags_text.split()
            or "tabular classification" in tags_text
            or "classification dataset" in tags_text
        )

        best_task = self.OTHER
        best_score = 0.0

        for task, keywords in (
            self.ML_TASK_RULES.items()
        ):

            score = 0.0

            for keyword in keywords:

                key = self._normalize(
                    keyword
                )

                if not key:
                    continue

                if key in tags_text:
                    score += 1.00

                if key in name_text:
                    score += 0.70

                if key in combined_text:
                    score += 0.25

            if score > best_score:

                best_score = score
                best_task = task

        # A dataset can carry a generic/incorrect RL tag while its name and
        # description clearly describe supervised prediction.  Prediction
        # language is stronger evidence than an incidental RL tag.
        prediction_signals = [
            "predict diabetes",
            "diabetes prediction",
            "disease prediction",
            "predict disease",
            "classification dataset",
            "binary classification",
            "classify",
            "classification",
        ]
        has_prediction_signal = any(
            phrase in name_text or phrase in combined_text
            for phrase in prediction_signals
        )
        if best_task == "Reinforcement Learning" and has_prediction_signal:
            best_task = "Classification"
            best_score = max(best_score, 1.0)

        if explicit_classification and best_task != "Classification":
            best_task = "Classification"
            best_score = max(best_score, 1.0)

        # ----------------------------------------
        # Semantic fallbacks
        # ----------------------------------------

        if best_score == 0:

            if any(
                phrase in combined_text
                for phrase in [
                    "predict survival",
                    "predict whether",
                    "predict disease",
                    "predict diabetes",
                    "diagnostic dataset",
                    "classification dataset",
                    "house price prediction",
                    "house prices",
                    "housing price",
                ]
            ):

                if any(
                    phrase in combined_text
                    for phrase in [
                        "house price",
                        "house prices",
                        "housing price",
                        "housing prices",
                    ]
                ):

                    best_task = "Regression"

                else:

                    best_task = "Classification"

                best_score = 0.80

            elif any(
                phrase in combined_text
                for phrase in [
                    "price prediction",
                    "predict price",
                    "continuous value",
                ]
            ):

                best_task = "Regression"
                best_score = 0.80

        # ----------------------------------------
        # Confidence
        # ----------------------------------------

        if best_score >= 2.0:
            confidence = 0.99

        elif best_score >= 1.0:
            confidence = 0.98

        elif best_score >= 0.7:
            confidence = 0.90

        elif best_score >= 0.4:
            confidence = 0.70

        else:

            confidence = 0.20
            best_task = self.OTHER

        return (
            best_task,
            confidence,
        )

    # ========================================================
    # DATA TYPE DETECTION
    # ========================================================

    def _detect_data_type(
        self,
        name: str,
        description: str,
        tags: str,
        combined_text: str,
        ml_task: str,
    ):

        name_text = self._normalize(
            name
        )

        tags_text = self._normalize(
            tags
        )

        combined_text = self._normalize(
            combined_text
        )

        explicit_tabular = any(
            phrase in tags_text
            for phrase in [
                "tabular",
                "tabular classification",
                "tabular regression",
                "structured data",
            ]
        )

        if explicit_tabular:
            return "Tabular", 0.99

        best_type = self.OTHER
        best_score = 0.0

        for data_type, keywords in (
            self.DATA_TYPE_RULES.items()
        ):

            score = 0.0

            for keyword in keywords:

                key = self._normalize(
                    keyword
                )

                if not key:
                    continue

                if key in tags_text:
                    score += 1.00

                if key in name_text:
                    score += 0.75

                if key in combined_text:
                    score += 0.25

            if score > best_score:

                best_score = score
                best_type = data_type

        # ----------------------------------------
        # ML task fallback
        # ----------------------------------------

        if best_score == 0:

            if ml_task in [
                "Text Generation",
                "Question Answering",
                "Text Summarization",
                "Translation",
                "Named Entity Recognition",
                "Fill Mask",
            ]:

                best_type = "Text"
                best_score = 0.75

            elif ml_task in [
                "Speech Recognition",
                "Text to Speech",
            ]:

                best_type = "Audio"
                best_score = 0.75

            elif ml_task in [
                "Object Detection",
                "Image Segmentation",
            ]:

                best_type = "Image"
                best_score = 0.75

            elif ml_task == "Classification":

                if "tabular" in combined_text:

                    best_type = "Tabular"
                    best_score = 0.70

        # Healthcare prediction datasets are commonly described as patient
        # records/features and may omit an explicit "tabular" tag.
        if (
            ml_task == "Classification"
            and any(term in combined_text for term in [
                "csv", "patient records", "patient data", "health indicators",
                "structured data", "pima", "diabetes prediction",
            ])
        ):
            best_type = "Tabular"
            best_score = max(best_score, 0.90)

        # ----------------------------------------
        # Confidence
        # ----------------------------------------

        if best_score >= 2.0:
            confidence = 0.99

        elif best_score >= 1.0:
            confidence = 0.98

        elif best_score >= 0.7:
            confidence = 0.90

        elif best_score >= 0.4:
            confidence = 0.70

        else:

            confidence = 0.20
            best_type = self.OTHER

        return (
            best_type,
            confidence,
        )

    # ========================================================
    # DIFFICULTY DETECTION
    # ========================================================

    def _detect_difficulty(
        self,
        name: str,
        description: str,
        tags: str,
        combined_text: str,
    ):

        name_text = self._normalize(
            name
        )

        combined_text = self._normalize(
            combined_text
        )

        best_difficulty = self.UNKNOWN
        best_score = 0.0

        for difficulty, keywords in (
            self.DIFFICULTY_RULES.items()
        ):

            score = 0.0

            for keyword in keywords:

                key = self._normalize(
                    keyword
                )

                if not key:
                    continue

                if key in name_text:
                    score += 0.90

                if key in combined_text:
                    score += 0.30

            if score > best_score:

                best_score = score
                best_difficulty = difficulty

        # ----------------------------------------
        # Dataset characteristics
        # ----------------------------------------

        if best_score == 0:

            if any(
                word in name_text
                for word in [
                    "iris",
                    "titanic",
                    "mnist",
                    "fashion mnist",
                ]
            ):

                best_difficulty = "Beginner"
                best_score = 0.80

            elif any(
                word in combined_text
                for word in [
                    "massive",
                    "large scale",
                    "large-scale",
                    "billions",
                    "multimodal",
                    "reinforcement learning",
                ]
            ):

                best_difficulty = "Advanced"
                best_score = 0.75

        # ----------------------------------------
        # Confidence
        # ----------------------------------------

        if best_score >= 1.0:
            confidence = 0.90

        elif best_score >= 0.7:
            confidence = 0.80

        elif best_score >= 0.4:
            confidence = 0.65

        else:

            confidence = 0.30
            best_difficulty = self.UNKNOWN

        return (
            best_difficulty,
            confidence,
        )

    # ========================================================
    # LICENSE DETECTION
    # ========================================================

    def _detect_license(
        self,
        license_value: Any,
        tags: str,
        description: str,
    ):

        existing = self._clean_text(
            license_value
        )

        if existing and (
            existing.lower()
            not in [
                "unknown",
                "none",
                "null",
            ]
        ):

            return (
                existing,
                True,
            )

        combined = self._normalize(
            f"{tags} {description}"
        )

        license_patterns = [
            "apache-2.0",
            "apache 2.0",
            "mit",
            "cc-by-4.0",
            "cc by 4.0",
            "cc-by-3.0",
            "cc by 3.0",
            "cc-by-sa-4.0",
            "cc by sa 4.0",
            "cc-by-nc-sa-4.0",
            "gpl-3.0",
            "gpl 3.0",
            "bsd-3-clause",
            "bsd 3 clause",
            "bsd-2-clause",
            "bsd 2 clause",
            "mpl-2.0",
            "odc-by-1.0",
            "openrail",
        ]

        for pattern in license_patterns:

            if self._normalize(
                pattern
            ) in combined:

                return (
                    pattern,
                    True,
                )

        return (
            self.UNKNOWN,
            False,
        )

    # ========================================================
    # TEXT HELPERS
    # ========================================================

    @staticmethod
    def _clean_text(
        value: Any,
    ) -> str:

        if value is None:
            return ""

        if isinstance(
            value,
            list,
        ):

            value = ", ".join(
                str(item)
                for item in value
            )

        return str(
            value
        ).strip()

    @staticmethod
    def _normalize(
        value: Any,
    ) -> str:

        if value is None:
            return ""

        text = str(
            value
        ).lower()

        text = text.replace(
            "_",
            " ",
        )

        text = text.replace(
            "-",
            " ",
        )

        text = re.sub(
            r"[^a-z0-9\s]",
            " ",
            text,
        )

        return " ".join(
            text.split()
        )

    @staticmethod
    def _is_reliable(
        value: str,
        invalid_values: list[str],
    ) -> bool:
        """
        Determine whether a source-provided
        metadata value should be preserved.
        """

        if not value:
            return False

        normalized = (
            str(value)
            .strip()
            .lower()
        )

        invalid = {
            str(item)
            .strip()
            .lower()
            for item in invalid_values
        }

        return (
            normalized not in invalid
        )


# ============================================================
# SINGLE AGENT INSTANCE
# ============================================================

metadata_agent = DatasetMetadataAgent()
