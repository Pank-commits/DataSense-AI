import re
from urllib.parse import urlparse


# ============================================================
# QUALITY AGENT
# ============================================================

class DatasetQualityAgent:
    """
    Dataset Quality Agent

    Evaluates normalized dataset metadata before it is
    stored in PostgreSQL and indexed into Qdrant.

    STATUS:

        READY
            Dataset has sufficient core metadata.

        REVIEW
            Dataset is usable but has uncertainty or
            missing non-critical metadata.

        REJECT
            Dataset is fundamentally unusable.

    Important:
        difficulty and license are OPTIONAL.
        Missing optional metadata should NOT automatically
        send a dataset to REVIEW.
    """

    # ========================================================
    # REQUIRED CORE FIELDS
    # ========================================================

    REQUIRED_FIELDS = [
        "name",
        "description",
        "source",
        "download_url",
        "category",
        "ml_task",
        "data_type",
    ]

    # ========================================================
    # OPTIONAL FIELDS
    # ========================================================

    OPTIONAL_FIELDS = [
        "difficulty",
        "license",
        "rows",
        "columns",
        "file_size",
        "target_column",
        "language",
        "tags",
        "thumbnail",
        "downloads",
        "rating",
    ]

    # ========================================================
    # PLACEHOLDER VALUES
    # ========================================================

    UNKNOWN_VALUES = {
        "",
        "unknown",
        "none",
        "null",
        "n/a",
        "na",
        "not available",
        "not specified",
    }

    # ========================================================
    # THRESHOLDS
    # ========================================================

    READY_SCORE = 70

    REVIEW_SCORE = 45

    # ========================================================
    # PUBLIC API
    # ========================================================

    def evaluate(self, dataset: dict) -> dict:
        """
        Evaluate a single dataset.
        """

        if not dataset:
            return {
                "_quality": {
                    "status": "REJECT",
                    "score": 0,
                    "checks": {},
                    "reasons": [
                        "Dataset metadata is empty."
                    ],
                }
            }

        checks = {}

        reasons = []

        score = 100

        # ====================================================
        # 1. NAME
        # ====================================================

        name = self._clean(
            dataset.get("name")
        )

        name_valid = (
            len(name) >= 2
        )

        checks["name"] = name_valid

        if not name_valid:

            score -= 35

            reasons.append(
                "Dataset name is missing or invalid."
            )

        # ====================================================
        # 2. DESCRIPTION
        # ====================================================

        description = self._clean(
            dataset.get("description")
        )

        description_valid = (
            len(description) >= 20
        )

        checks["description"] = description_valid

        if not description_valid:

            score -= 20

            reasons.append(
                "Description is missing or too short."
            )

        # ====================================================
        # 3. SOURCE
        # ====================================================

        source = self._clean(
            dataset.get("source")
        )

        source_valid = (
            len(source) >= 2
        )

        checks["source"] = source_valid

        if not source_valid:

            score -= 15

            reasons.append(
                "Dataset source is missing."
            )

        # ====================================================
        # 4. URL
        # ====================================================

        url = self._clean(
            dataset.get("download_url")
        )

        url_valid = self._is_valid_url(
            url
        )

        checks["url"] = url_valid

        if not url_valid:

            score -= 35

            reasons.append(
                "Dataset URL is missing or invalid."
            )

        # ====================================================
        # 5. CATEGORY
        # ====================================================

        category = self._clean(
            dataset.get("category")
        )

        category_valid = (
            category.lower()
            not in self.UNKNOWN_VALUES
            and len(category) >= 2
        )

        checks["category"] = category_valid

        if not category_valid:

            score -= 8

            reasons.append(
                "Category is missing or uncertain."
            )

        # ====================================================
        # 6. ML TASK
        # ====================================================

        ml_task = self._clean(
            dataset.get("ml_task")
        )

        ml_task_valid = (
            ml_task.lower()
            not in self.UNKNOWN_VALUES
            and len(ml_task) >= 2
        )

        checks["ml_task"] = ml_task_valid

        if not ml_task_valid:

            score -= 10

            reasons.append(
                "Machine learning task is missing or uncertain."
            )

        # ====================================================
        # 7. DATA TYPE
        # ====================================================

        data_type = self._clean(
            dataset.get("data_type")
        )

        data_type_valid = (
            data_type.lower()
            not in self.UNKNOWN_VALUES
            and len(data_type) >= 2
        )

        checks["data_type"] = data_type_valid

        if not data_type_valid:

            score -= 10

            reasons.append(
                "Data type is missing or uncertain."
            )

        # ====================================================
        # 8. METADATA AGENT CONFIDENCE
        # ====================================================

        metadata = (
            dataset.get(
                "_metadata_agent",
                {},
            )
            or {}
        )

        metadata_quality = (
            self._evaluate_metadata_confidence(
                metadata
            )
        )

        checks["metadata"] = (
            metadata_quality["valid"]
        )

        # Confidence should influence quality,
        # but should NOT destroy otherwise valid datasets.

        if metadata_quality["penalty"] > 0:

            score -= metadata_quality[
                "penalty"
            ]

            reasons.extend(
                metadata_quality[
                    "reasons"
                ]
            )

        # ====================================================
        # 9. DUPLICATE CHECK
        # ====================================================

        duplicate = dataset.get(
            "_duplicate",
            False,
        )

        duplicate_valid = (
            duplicate is not True
        )

        checks["duplicate"] = duplicate_valid

        if duplicate:

            score -= 60

            reasons.append(
                "Dataset appears to be a duplicate."
            )

        # ====================================================
        # 10. OPTIONAL METADATA
        # ====================================================

        optional_missing = []

        for field in self.OPTIONAL_FIELDS:

            value = dataset.get(field)

            if self._is_missing(
                value
            ):
                optional_missing.append(
                    field
                )

        # IMPORTANT:
        # Missing difficulty/license/etc.
        # does NOT automatically cause REVIEW.

        if optional_missing:

            reasons.append(
                "Optional metadata missing: "
                + ", ".join(
                    optional_missing
                )
            )

        # ====================================================
        # 11. SCORE NORMALIZATION
        # ====================================================

        score = max(
            0,
            min(
                int(round(score)),
                100,
            ),
        )

        # ====================================================
        # 12. STATUS DECISION
        # ====================================================

        status = self._determine_status(
            score=score,
            checks=checks,
            dataset=dataset,
        )

        # ====================================================
        # 13. DEFAULT SUCCESS MESSAGE
        # ====================================================

        if not reasons:

            reasons.append(
                "Dataset passed all basic quality checks."
            )

        elif status == "READY":

            reasons.insert(
                0,
                "Dataset has sufficient core metadata."
            )

        # ====================================================
        # RESULT
        # ====================================================

        dataset["_quality"] = {
            "status": status,

            "score": score,

            "checks": checks,

            "reasons": reasons,
        }

        return dataset

    # ========================================================
    # BATCH EVALUATION
    # ========================================================

    def evaluate_batch(
        self,
        datasets: list[dict],
    ) -> list[dict]:
        """
        Evaluate multiple datasets.
        """

        if not datasets:
            return []

        results = []

        for dataset in datasets:

            try:

                result = self.evaluate(
                    dataset
                )

                results.append(
                    result
                )

            except Exception as error:

                print(
                    "Quality evaluation failed "
                    f"for {dataset.get('name')}: "
                    f"{error}"
                )

                failed = dict(
                    dataset
                )

                failed["_quality"] = {
                    "status": "REVIEW",
                    "score": 40,
                    "checks": {},
                    "reasons": [
                        "Quality evaluation failed.",
                        str(error),
                    ],
                }

                results.append(
                    failed
                )

        return results

    # ========================================================
    # METADATA CONFIDENCE
    # ========================================================

    def _evaluate_metadata_confidence(
        self,
        metadata: dict,
    ):

        if not metadata:

            return {
                "valid": True,
                "penalty": 0,
                "reasons": [],
            }

        fields = [
            (
                "category_confidence",
                "Category",
            ),
            (
                "ml_task_confidence",
                "ML task",
            ),
            (
                "data_type_confidence",
                "Data type",
            ),
            (
                "difficulty_confidence",
                "Difficulty",
            ),
        ]

        penalty = 0

        reasons = []

        core_confidence = []

        # --------------------------------------------
        # Core fields
        # --------------------------------------------

        for key, label in fields[:3]:

            value = self._safe_float(
                metadata.get(key)
            )

            if value is None:
                continue

            core_confidence.append(
                value
            )

            if value < 0.30:

                penalty += 6

                reasons.append(
                    f"{label} confidence is very low."
                )

            elif value < 0.50:

                penalty += 2

                reasons.append(
                    f"{label} confidence is moderate."
                )

        # --------------------------------------------
        # Difficulty is optional
        # --------------------------------------------

        difficulty_confidence = (
            self._safe_float(
                metadata.get(
                    "difficulty_confidence"
                )
            )
        )

        if (
            difficulty_confidence is not None
            and difficulty_confidence < 0.30
        ):

            # Difficulty is optional metadata.
            # Do not reduce the quality score because
            # difficulty could not be confidently inferred.
            pass

        # --------------------------------------------
        # Core confidence validity
        # --------------------------------------------

        if core_confidence:

            valid = (
                sum(core_confidence)
                / len(core_confidence)
                >= 0.55
            )

        else:

            valid = True

        return {
            "valid": valid,
            "penalty": min(
                penalty,
                20,
            ),
            "reasons": reasons,
        }

    # ========================================================
    # STATUS DECISION
    # ========================================================

    def _determine_status(
        self,
        score: int,
        checks: dict,
        dataset: dict,
    ) -> str:
        """
        Determine READY / REVIEW / REJECT.

        Critical fields:
            name
            description
            source
            url

        Important fields:
            category
            ml_task
            data_type

        Optional:
            difficulty
            license
            rows
            columns
            etc.
        """

        # ====================================================
        # HARD REJECT CONDITIONS
        # ====================================================

        critical_failures = [
            "name",
            "description",
            "source",
            "url",
        ]

        critical_missing = [
            field
            for field in critical_failures
            if not checks.get(field, False)
        ]

        if len(
            critical_missing
        ) >= 2:

            return "REJECT"

        # Duplicate is a strong rejection signal.

        if (
            checks.get(
                "duplicate"
            )
            is False
        ):

            return "REJECT"

        # ====================================================
        # IMPORTANT METADATA
        # ====================================================

        important_failures = [
            field
            for field in [
                "category",
                "ml_task",
                "data_type",
            ]
            if not checks.get(
                field,
                False,
            )
        ]

        # ====================================================
        # READY
        # ====================================================

        if (
            score >= self.READY_SCORE
            and len(
                critical_missing
            ) == 0
            and len(
                important_failures
            ) == 0
        ):

            return "READY"

        # ====================================================
        # REVIEW
        # ====================================================

        return "REVIEW"

    # ========================================================
    # URL VALIDATION
    # ========================================================

    @staticmethod
    def _is_valid_url(
        value: str,
    ) -> bool:

        if not value:
            return False

        try:

            parsed = urlparse(
                value
            )

            if parsed.scheme not in [
                "http",
                "https",
            ]:
                return False

            if not parsed.netloc:
                return False

            return True

        except Exception:

            return False

    # ========================================================
    # VALUE HELPERS
    # ========================================================

    @staticmethod
    def _clean(
        value,
    ) -> str:

        if value is None:
            return ""

        return str(
            value
        ).strip()

    def _is_missing(
        self,
        value,
    ) -> bool:

        if value is None:
            return True

        if isinstance(
            value,
            str,
        ):

            return (
                value.strip().lower()
                in self.UNKNOWN_VALUES
            )

        return False

    @staticmethod
    def _safe_float(
        value,
    ):

        try:

            if value is None:
                return None

            return float(
                value
            )

        except (
            TypeError,
            ValueError,
        ):

            return None


# ============================================================
# SINGLE AGENT INSTANCE
# ============================================================

quality_agent = DatasetQualityAgent()