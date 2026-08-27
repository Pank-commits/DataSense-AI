from app.ai.qdrant_service import search
from app.ai.rag_service import build_context
from app.ai.llm_service import ask_gemini


# ==========================================
# AGENT TOOLS
# ==========================================

def semantic_search_tool(
    query: str,
    limit: int = 5,
    intent: dict | None = None,
):
    """
    Search Qdrant using both the query
    and detected user intent.
    """

    return search(
        query=query,
        limit=limit,
        intent=intent,
    )


# ==========================================
# RE-RANKING
# ==========================================

def rerank_datasets(
    datasets: list,
    question: str,
    intent: dict,
):
    """
    Re-rank Qdrant results using:

        1. Topic / keyword match
        2. Category match
        3. ML task match
        4. Data type match
        5. Semantic similarity

    Qdrant provides the initial semantic candidates.
    This function improves the final ordering.
    """

    if not datasets:
        return []

    question_text = (
        question or ""
    ).lower().strip()

    # --------------------------------------
    # Extract useful words from question
    # --------------------------------------

    stop_words = {
        "a",
        "an",
        "the",
        "for",
        "of",
        "to",
        "and",
        "or",
        "is",
        "are",
        "me",
        "my",
        "i",
        "in",
        "on",
        "with",
        "dataset",
        "datasets",
        "recommend",
        "recommendation",
        "machine",
        "learning",
    }

    question_words = {
        word.strip(
            ".,!?;:()[]{}"
        )
        for word in question_text.split()
        if word.strip(
            ".,!?;:()[]{}"
        ) not in stop_words
        and len(
            word.strip(
                ".,!?;:()[]{}"
            )
        ) > 2
    }

    # --------------------------------------
    # Intent values
    # --------------------------------------

    category = (
        intent.get("category")
        if intent
        else None
    )

    ml_task = (
        intent.get("ml_task")
        if intent
        else None
    )

    data_type = (
        intent.get("data_type")
        if intent
        else None
    )

    difficulty = (
        intent.get("difficulty")
        if intent
        else None
    )

    category = (
        str(category).lower()
        if category
        else None
    )

    ml_task = (
        str(ml_task).lower()
        if ml_task
        else None
    )

    data_type = (
        str(data_type).lower()
        if data_type
        else None
    )

    difficulty = (
        str(difficulty).lower()
        if difficulty
        else None
    )

    # ======================================
    # SCORE EACH DATASET
    # ======================================

    scored = []

    for dataset in datasets:

        # ----------------------------------
        # Dataset fields
        # ----------------------------------

        name = str(
            dataset.get("name")
            or ""
        ).lower()

        description = str(
            dataset.get("description")
            or ""
        ).lower()

        dataset_category = str(
            dataset.get("category")
            or ""
        ).lower()

        dataset_ml_task = str(
            dataset.get("ml_task")
            or ""
        ).lower()

        dataset_data_type = str(
            dataset.get("data_type")
            or ""
        ).lower()

        dataset_difficulty = str(
            dataset.get("difficulty")
            or ""
        ).lower()

        tags = str(
            dataset.get("tags")
            or ""
        ).lower()

        # Qdrant may contain records indexed before metadata was corrected.
        # Use explicit tags as a safety net during final ranking as well.
        effective_ml_task = dataset_ml_task
        if (
            "classification" in tags
            and effective_ml_task in {"", "unknown", "other", "reinforcement learning"}
        ):
            effective_ml_task = "classification"

        effective_data_type = dataset_data_type
        if (
            "tabular" in tags
            or "tabular-classification" in tags
            or "tabular classification" in tags
        ):
            effective_data_type = "tabular"

        effective_category = dataset_category
        if (
            any(term in searchable_text for term in
                ["diabetes", "patient", "medical", "healthcare"])
            and not effective_category
            or effective_category in {"unknown", "other"}
            and any(term in searchable_text for term in
                    ["diabetes", "patient", "medical", "healthcare"])
        ):
            effective_category = "healthcare"

        # ----------------------------------
        # Combined searchable text
        # ----------------------------------

        searchable_text = " ".join(
            [
                name,
                description,
                tags,
            ]
        )

        # ----------------------------------
        # Start score
        # ----------------------------------

        score = 0.0

        # ==================================
        # 1. TOPIC / KEYWORD MATCH
        # ==================================

        matched_keywords = 0

        for word in question_words:

            if word in name:

                # Strongest keyword match
                score += 8.0
                matched_keywords += 1

            elif word in tags:

                score += 5.0
                matched_keywords += 1

            elif word in description:

                score += 3.0
                matched_keywords += 1

            elif word in searchable_text:

                score += 1.0

        # ==================================
        # 2. EXACT PHRASE MATCH
        # ==================================

        # Important domain phrases
        # get extra weight.

        important_phrases = [
            phrase
            for phrase in [
                "heart disease",
                "diabetes",
                "cancer",
                "breast cancer",
                "mental health",
                "sentiment analysis",
                "image classification",
                "object detection",
                "fraud detection",
                "house prices",
                "customer churn",
                "sales forecasting",
                "time series",
            ]
            if phrase in question_text
        ]

        for phrase in important_phrases:

            if phrase in name:

                score += 20.0

            elif phrase in tags:

                score += 12.0

            elif phrase in description:

                score += 8.0

        # ==================================
        # 3. CATEGORY MATCH
        # ==================================

        topic_match = int(any(
            phrase in question_text and phrase in searchable_text
            for phrase in ["diabetes", "heart disease", "cancer", "patient"]
        ))
        task_match = int(bool(ml_task) and (
            ml_task == effective_ml_task
            or ml_task in effective_ml_task
        ))
        category_match = int(bool(category) and (
            category == dataset_category
            or category in dataset_category
        ))
        type_match = int(bool(data_type) and (
            data_type == effective_data_type
            or data_type in effective_data_type
        ))

        if (
            category
            and dataset_category
        ):

            if (
                category
                == dataset_category
            ):

                score += 15.0

            elif (
                category in
                dataset_category
                or
                dataset_category in
                category
            ):

                score += 8.0

        # ==================================
        # 4. ML TASK MATCH
        # ==================================

        if (
            ml_task
            and dataset_ml_task
        ):

            if ml_task == effective_ml_task:

                score += 12.0

            elif (
                ml_task in
                effective_ml_task
                or
                effective_ml_task in
                ml_task
            ):

                score += 6.0

        # ==================================
        # 5. DATA TYPE MATCH
        # ==================================

        if (
            data_type
            and dataset_data_type
        ):

            if data_type == effective_data_type:

                score += 7.0

            elif (
                data_type in
                effective_data_type
                or
                effective_data_type in
                data_type
            ):

                score += 3.0

        # ==================================
        # 6. DIFFICULTY MATCH
        # ==================================

        if (
            difficulty
            and dataset_difficulty
        ):

            if (
                difficulty
                == dataset_difficulty
            ):

                score += 5.0

        # ==================================
        # 7. SEMANTIC SCORE
        # ==================================

        semantic_score = dataset.get(
            "score"
        )

        if semantic_score is not None:

            try:

                semantic_score = float(
                    semantic_score
                )

                # Keep semantic similarity
                # useful but don't allow it
                # to overpower exact topic
                # matches.

                score += (
                    semantic_score * 10.0
                )

            except (
                TypeError,
                ValueError,
            ):

                pass

        # ----------------------------------
        # Store score
        # ----------------------------------

        dataset_copy = dict(
            dataset
        )

        # Return the same normalized metadata that was used for scoring.
        # Otherwise the LLM can receive stale Qdrant values (for example an
        # old Reinforcement Learning label) despite correct ranking logic.
        if effective_ml_task:
            dataset_copy["ml_task"] = effective_ml_task.title()
        if effective_data_type:
            dataset_copy["data_type"] = effective_data_type.title()
        if effective_category:
            dataset_copy["category"] = effective_category.title()

        dataset_copy[
            "_rerank_score"
        ] = round(
            score,
            4,
        )

        dataset_copy[
            "_matched_keywords"
        ] = matched_keywords

        dataset_copy["_intent_priority"] = (
            topic_match,
            task_match,
            category_match,
            type_match,
        )

        scored.append(
            dataset_copy
        )

    # ======================================
    # SORT
    # ======================================

    scored.sort(
        key=lambda item: (
            item.get("_intent_priority", (0, 0, 0, 0)),
            item.get("_rerank_score", 0),
        ),
        reverse=True,
    )

    # ======================================
    # RETURN
    # ======================================

    return scored


# ==========================================
# AGENT PLANNER
# ==========================================

def understand_request(
    question: str,
):
    """
    Understand the user's dataset requirement.

    Detects:
        - category
        - ML task
        - difficulty
        - data type

    Examples:

        predict heart disease
            -> Classification

        predict diabetes
            -> Classification

        predict house prices
            -> Regression

        forecast sales
            -> Forecasting
    """

    text = (
        question or ""
    ).lower().strip()

    intent = {
        "category": None,
        "ml_task": None,
        "difficulty": None,
        "data_type": None,
    }

    # ======================================
    # CATEGORY DETECTION
    # ======================================

    categories = {

        "healthcare": [
            "health",
            "healthcare",
            "medical",
            "medicine",
            "disease",
            "diabetes",
            "heart",
            "heart disease",
            "cancer",
            "patient",
            "clinical",
            "hospital",
        ],

        "computer vision": [
            "image",
            "images",
            "computer vision",
            "vision",
            "object detection",
            "image classification",
            "face recognition",
            "image segmentation",
        ],

        "nlp": [
            "nlp",
            "text",
            "sentiment",
            "language",
            "natural language",
            "text classification",
            "text generation",
            "question answering",
            "translation",
            "chatbot",
        ],

        "finance": [
            "finance",
            "financial",
            "stock",
            "stocks",
            "banking",
            "bank",
            "credit",
            "loan",
            "fraud",
            "investment",
            "trading",
            "income",
        ],

        "education": [
            "education",
            "educational",
            "student",
            "students",
            "school",
            "learning",
            "exam",
            "academic",
        ],

        "retail": [
            "retail",
            "customer",
            "customers",
            "product",
            "products",
            "shopping",
            "ecommerce",
            "e-commerce",
            "sales",
        ],

        "agriculture": [
            "agriculture",
            "agricultural",
            "crop",
            "crops",
            "farming",
            "plant",
            "plants",
            "soil",
            "yield",
        ],

        "time series": [
            "time series",
            "time-series",
            "temporal",
        ],
    }

    for category, keywords in (
        categories.items()
    ):

        if any(
            keyword in text
            for keyword in keywords
        ):

            intent[
                "category"
            ] = category

            break

    # ======================================
    # ML TASK DETECTION
    # ======================================

    task_text = text.replace(
        "predicting",
        "predict",
    )

    # --------------------------------------
    # Classification
    # --------------------------------------

    classification_keywords = [

        "classification",
        "classify",
        "classifying",

        "predict heart disease",
        "predict diabetes",
        "predict cancer",
        "predict disease",

        "predict survival",
        "predict churn",
        "predict fraud",
        "predict spam",
        "predict whether",

        "detect disease",
        "detect cancer",
        "detect fraud",
        "detect spam",

        "diagnose",
        "diagnosis",
        "medical diagnosis",

        "disease prediction",
    ]

    # --------------------------------------
    # Regression
    # --------------------------------------

    regression_keywords = [

        "regression",

        "predict a value",

        "predict price",
        "predict prices",

        "predict house price",
        "predict house prices",

        "predict housing price",
        "predict housing prices",

        "predict salary",
        "predict income",

        "predict temperature",

        "estimate price",
        "estimate cost",
        "estimate value",

        "continuous value",
    ]

    # --------------------------------------
    # Forecasting
    # --------------------------------------

    forecasting_keywords = [

        "forecast",
        "forecasting",

        "future sales",
        "future demand",
        "future price",

        "sales over time",

        "predict future",

        "time series",
        "time-series",

        "temporal forecasting",
    ]

    # --------------------------------------
    # Clustering
    # --------------------------------------

    clustering_keywords = [

        "clustering",
        "cluster",

        "group similar",
        "grouping similar",

        "customer segmentation",
        "segment customers",
    ]

    # --------------------------------------
    # Determine ML task
    # --------------------------------------

    if any(
        keyword in task_text
        for keyword in classification_keywords
    ):

        intent[
            "ml_task"
        ] = "Classification"

    elif any(
        keyword in task_text
        for keyword in forecasting_keywords
    ):

        intent[
            "ml_task"
        ] = "Forecasting"

    elif any(
        keyword in task_text
        for keyword in regression_keywords
    ):

        intent[
            "ml_task"
        ] = "Regression"

    elif any(
        keyword in task_text
        for keyword in clustering_keywords
    ):

        intent[
            "ml_task"
        ] = "Clustering"

    elif (
        "predict" in task_text
        and intent[
            "category"
        ] == "healthcare"
    ):

        intent[
            "ml_task"
        ] = "Classification"

    # ======================================
    # DIFFICULTY DETECTION
    # ======================================

    if any(
        word in text
        for word in [
            "beginner",
            "easy",
            "simple",
            "starting",
            "starter",
            "basic",
            "new to machine learning",
            "new to ml",
        ]
    ):

        intent[
            "difficulty"
        ] = "Beginner"

    elif any(
        word in text
        for word in [
            "advanced",
            "expert",
            "hard",
            "complex",
            "challenging",
        ]
    ):

        intent[
            "difficulty"
        ] = "Advanced"

    elif any(
        word in text
        for word in [
            "intermediate",
            "medium",
        ]
    ):

        intent[
            "difficulty"
        ] = "Intermediate"

    # ======================================
    # DATA TYPE DETECTION
    # ======================================

    if any(
        word in text
        for word in [
            "image",
            "images",
            "computer vision",
            "visual",
        ]
    ):

        intent[
            "data_type"
        ] = "Image"

    elif any(
        word in text
        for word in [
            "audio",
            "speech",
            "voice",
            "sound",
            "asr",
            "text to speech",
            "tts",
        ]
    ):

        intent[
            "data_type"
        ] = "Audio"

    elif any(
        word in text
        for word in [
            "video",
            "videos",
        ]
    ):

        intent[
            "data_type"
        ] = "Video"

    elif any(
        word in text
        for word in [
            "text",
            "nlp",
            "sentiment",
            "language",
            "document",
            "documents",
        ]
    ):

        intent[
            "data_type"
        ] = "Text"

    elif any(
        word in text
        for word in [
            "tabular",
            "csv",
            "table",
            "spreadsheet",
            "structured data",
        ]
    ):

        intent[
            "data_type"
        ] = "Tabular"

    return intent


# ==========================================
# AGENT QUERY BUILDER
# ==========================================

def build_search_query(
    question: str,
    intent: dict,
):
    """
    Convert the user request and detected
    intent into a stronger search query.
    """

    parts = [
        question.strip()
    ]

    if intent.get(
        "category"
    ):

        parts.append(
            f"category "
            f"{intent['category']}"
        )

    if intent.get(
        "ml_task"
    ):

        parts.append(
            f"machine learning task "
            f"{intent['ml_task']}"
        )

    if intent.get(
        "difficulty"
    ):

        parts.append(
            f"difficulty "
            f"{intent['difficulty']}"
        )

    if intent.get(
        "data_type"
    ):

        parts.append(
            f"data type "
            f"{intent['data_type']}"
        )

    return " ".join(
        parts
    )


# ==========================================
# DATASET AGENT
# ==========================================

def run_dataset_agent(
    question: str,
):
    """
    DataSense Dataset Recommendation Agent.

    Workflow:

        User question
              ↓
        Understand request
              ↓
        Build search query
              ↓
        Qdrant candidate retrieval
              ↓
        Re-ranking
              ↓
        Build context
              ↓
        Gemini explanation
              ↓
        Return recommendation
    """

    # --------------------------------------
    # Validate input
    # --------------------------------------

    if (
        not question
        or not question.strip()
    ):

        return {
            "question": question,

            "agent": {
                "name":
                    "Dataset Recommendation Agent",

                "intent": {
                    "category": None,
                    "ml_task": None,
                    "difficulty": None,
                    "data_type": None,
                },

                "search_query": "",
            },

            "answer":
                "Please provide a dataset requirement.",

            "datasets": [],
        }

    question = question.strip()

    # --------------------------------------
    # 1. Understand request
    # --------------------------------------

    intent = understand_request(
        question
    )

    # --------------------------------------
    # 2. Build search query
    # --------------------------------------

    search_query = build_search_query(
        question,
        intent,
    )

    # --------------------------------------
    # 3. Retrieve more candidates
    #
    # IMPORTANT:
    # We retrieve more than 5 so the
    # re-ranker has enough candidates.
    # --------------------------------------

    candidates = semantic_search_tool(
        query=search_query,
        limit=20,
        intent=intent,
    )

    # --------------------------------------
    # 4. Re-rank candidates
    # --------------------------------------

    datasets = rerank_datasets(
        datasets=candidates,
        question=question,
        intent=intent,
    )

    # --------------------------------------
    # 5. Return only top 5
    # --------------------------------------

    datasets = datasets[:5]

    # --------------------------------------
    # 6. Build RAG context
    # --------------------------------------

    context = build_context(
        datasets
    )

    # --------------------------------------
    # 7. Ask Gemini
    # --------------------------------------

    answer = ask_gemini(
        question=question,
        context=context,
    )

    # --------------------------------------
    # 8. Return result
    # --------------------------------------

    return {

        "question": question,

        "agent": {
            "name":
                "Dataset Recommendation Agent",

            "intent": intent,

            "search_query":
                search_query,
        },

        "answer": answer,

        "datasets": datasets,
    }


# ==========================================
# INTENT TEST HELPER
# ==========================================

def test_intent(
    question: str,
):
    """
    Test intent detection without
    calling Qdrant or Gemini.
    """

    intent = understand_request(
        question
    )

    return {
        "question": question,

        "intent": intent,

        "search_query":
            build_search_query(
                question,
                intent,
            ),
    }


# ==========================================
# COMPLETE AGENT TEST HELPER
# ==========================================

def test_agent(
    question: str,
):
    """
    Test the complete recommendation agent.
    """

    return run_dataset_agent(
        question
    )
