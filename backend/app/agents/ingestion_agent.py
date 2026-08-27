from sqlalchemy.orm import Session
from itertools import islice
from sqlalchemy import or_
from app.agents.discovery_agent import discovery_agent
from app.agents.metadata_agent import metadata_agent
from app.agents.quality_agent import quality_agent

from app.models.dataset import Dataset

from app.ai.qdrant_service import (
    create_collection,
    index_dataset,
)


# ==========================================
# INGESTION AGENT
# ==========================================

class DatasetIngestionAgent:
    """
    Bulk-ready dataset ingestion pipeline.

    Discovery
        ↓
    Metadata
        ↓
    Quality
        ↓
    Normalize
        ↓
    PostgreSQL
        ↓
    Qdrant
    """

    def __init__(self):
        create_collection()

    # ======================================
    # SAFE VALUE
    # ======================================

    @staticmethod
    def _safe_value(value, default):

        if value is None:
            return default

        if isinstance(value, str):
            value = value.strip()

            if not value:
                return default

        return value

    # ======================================
    # NORMALIZE DATABASE FIELDS
    # ======================================

    @classmethod
    def _normalize_for_database(
        cls,
        data: dict,
    ) -> dict:

        return {
            "name": cls._safe_value(
                data.get("name"),
                "Unnamed Dataset",
            ),

            "slug": cls._safe_value(
                data.get("slug"),
                "unknown-dataset",
            ),

            "description": cls._safe_value(
                data.get("description"),
                "No description available.",
            ),

            "category": cls._safe_value(
                data.get("category"),
                "Other",
            ),

            "ml_task": cls._safe_value(
                data.get("ml_task"),
                "Unknown",
            ),

            "data_type": cls._safe_value(
                data.get("data_type"),
                "Unknown",
            ),

            "difficulty": cls._safe_value(
                data.get("difficulty"),
                "Unknown",
            ),

            "source": cls._safe_value(
                data.get("source"),
                "Unknown",
            ),

            "download_url": cls._safe_value(
                data.get("download_url"),
                "",
            ),

            "license": cls._safe_value(
                data.get("license"),
                "Unknown",
            ),

            "rows": data.get("rows"),

            "columns": data.get("columns"),

            "file_size": data.get("file_size"),

            "target_column": data.get(
                "target_column"
            ),

            "language": data.get(
                "language"
            ),

            "tags": cls._safe_value(
                data.get("tags"),
                "",
            ),

            "thumbnail": data.get(
                "thumbnail"
            ),

            "downloads": data.get(
                "downloads"
            ) or 0,

            "rating": data.get(
                "rating"
            ) or 0,
        }

    # ======================================
    # INGEST
    # ======================================

    def ingest(
        self,
        db: Session,
        limit: int = 100,
        search: str | None = None,
        batch_size: int = 1000,
        offset: int = 0,
    ):
        """
        Streaming bulk ingestion.

        Example:

            ingest(
                db,
                limit=959900,
                batch_size=1000,
                offset=40100,
            )

        This processes:

            1000 datasets
                ↓
            Metadata
                ↓
            Quality
                ↓
            PostgreSQL
                ↓
            Qdrant
                ↓
            next 1000 datasets

        Unlike the previous implementation, this does NOT
        load all discovered datasets into memory at once.
        """

        if limit <= 0:
            return {
                "discovered": 0,
                "metadata_processed": 0,
                "ready": 0,
                "review": 0,
                "rejected": 0,
                "inserted": 0,
                "updated": 0,
                "qdrant_indexed": 0,
                "failed": 0,
                "batches": 0,
            }

        if batch_size <= 0:
            batch_size = 1000

        if offset < 0:
            offset = 0

        print(
            f"\nStarting ingestion "
            f"(limit={limit}, "
            f"batch_size={batch_size}, "
            f"offset={offset})"
        )

        # ==================================
        # STREAMING DISCOVERY
        # ==================================

        print(
            f"Streaming discovery "
            f"(offset={offset:,}, "
            f"remaining={limit:,})"
        )

        discovered_iter = discovery_agent.discover(
            limit=limit,
            search=search,
            offset=offset,
        )

        # ==================================
        # GLOBAL STATISTICS
        # ==================================

        total_discovered = 0

        total_metadata = 0
        total_ready = 0
        total_review = 0
        total_rejected = 0

        total_inserted = 0
        total_updated = 0
        total_qdrant = 0
        total_failed = 0

        total_batches = 0

        # ==================================
        # PROCESS STREAMING BATCHES
        # ==================================

        while total_discovered < limit:

            # ----------------------------------
            # GET ONLY ONE BATCH FROM DISCOVERY
            # ----------------------------------

            batch = list(
                islice(
                    discovered_iter,
                    batch_size,
                )
            )

            if not batch:
                break

            total_batches += 1

            batch_start = (
                offset
                + total_discovered
                + 1
            )

            batch_end = (
                batch_start
                + len(batch)
                - 1
            )

            total_discovered += len(batch)

            print()
            print(
                "================================"
            )

            print(
                f"BATCH {total_batches} "
                f"({batch_start:,}-"
                f"{batch_end:,}/"
                f"{offset + limit:,})"
            )

            print(
                "================================"
            )

            # ==================================
            # METADATA
            # ==================================

            try:

                metadata_processed = (
                    metadata_agent.process_batch(
                        batch
                    )
                )

            except Exception as error:

                print(
                    f"Metadata batch failed: "
                    f"{error}"
                )

                total_failed += len(
                    batch
                )

                continue

            total_metadata += len(
                metadata_processed
            )

            # ==================================
            # QUALITY
            # ==================================

            try:

                evaluated = (
                    quality_agent.evaluate_batch(
                        metadata_processed
                    )
                )

            except Exception as error:

                print(
                    f"Quality batch failed: "
                    f"{error}"
                )

                total_failed += len(
                    metadata_processed
                )

                continue

            ready = [
                dataset
                for dataset in evaluated
                if dataset.get(
                    "_quality",
                    {},
                ).get(
                    "status"
                ) == "READY"
            ]

            review = [
                dataset
                for dataset in evaluated
                if dataset.get(
                    "_quality",
                    {},
                ).get(
                    "status"
                ) == "REVIEW"
            ]

            rejected = [
                dataset
                for dataset in evaluated
                if dataset.get(
                    "_quality",
                    {},
                ).get(
                    "status"
                ) == "REJECT"
            ]

            total_ready += len(
                ready
            )

            total_review += len(
                review
            )

            total_rejected += len(
                rejected
            )

            print(
                f"Quality -> "
                f"READY: {len(ready)} | "
                f"REVIEW: {len(review)} | "
                f"REJECT: {len(rejected)}"
            )

            # ==================================
            # DATABASE BATCH
            # ==================================

            qdrant_objects = []

            batch_inserted = 0
            batch_updated = 0
            batch_failed = 0

            for dataset in ready:

                try:

                    normalized = (
                        self._normalize_for_database(
                            dataset
                        )
                    )

                    download_url = (
                        normalized.get(
                            "download_url"
                        )
                    )

                    existing = None

                    # --------------------------
                    # DUPLICATE CHECK
                    # --------------------------

                    slug = normalized.get("slug")
                    condition = []

                    if download_url:
                        condition.append(
                            Dataset.download_url == download_url
                        )

                    if slug:
                        condition.append(
                            Dataset.slug == slug
                        )

                    if condition:

                        existing = (
                            db.query(Dataset)
                            .filter(
                                or_(*condition)
                            )
                            .first()
                        )
                    # --------------------------
                    # UPDATE
                    # --------------------------

                    if existing:

                        self._update_dataset(
                            existing,
                            normalized,
                        )

                        db.flush()

                        qdrant_objects.append(
                            existing
                        )

                        batch_updated += 1

                    # --------------------------
                    # INSERT
                    # --------------------------

                    else:

                        new_dataset = (
                            self._create_dataset(
                                normalized
                            )
                        )

                        db.add(
                            new_dataset
                        )

                        db.flush()

                        qdrant_objects.append(
                            new_dataset
                        )

                        batch_inserted += 1

                except Exception as error:

                    # Important:
                    # rollback the failed transaction
                    # and continue safely.

                    db.rollback()

                    batch_failed += 1

                    dataset_name = (
                        dataset.get(
                            "name",
                            "Unknown",
                        )
                    )

                    print(
                        f"Dataset failed: "
                        f"{dataset_name} -> "
                        f"{error}"
                    )

            # ==================================
            # DATABASE COMMIT
            # ==================================

            try:

                db.commit()

                total_inserted += (
                    batch_inserted
                )

                total_updated += (
                    batch_updated
                )

                print(
                    f"PostgreSQL -> "
                    f"Inserted: {batch_inserted} | "
                    f"Updated: {batch_updated}"
                )

            except Exception as error:

                db.rollback()

                print(
                    f"PostgreSQL commit failed: "
                    f"{error}"
                )

                total_failed += (
                    batch_inserted
                    + batch_updated
                )

                qdrant_objects = []

            total_failed += (
                batch_failed
            )

            # ==================================
            # QDRANT
            # ==================================

            qdrant_batch_count = 0

            for dataset in qdrant_objects:

                try:

                    index_dataset(
                        dataset
                    )

                    total_qdrant += 1
                    qdrant_batch_count += 1

                except Exception as error:

                    print(
                        f"Qdrant indexing failed "
                        f"for {dataset.name}: "
                        f"{error}"
                    )

                    total_failed += 1

            print(
                f"Qdrant indexed: "
                f"{qdrant_batch_count}"
            )

            # ==================================
            # GLOBAL PROGRESS
            # ==================================

            global_progress = (
                offset
                + total_discovered
            )

            print(
                f"Progress: "
                f"{global_progress:,}/1,000,000"
            )

        # ==================================
        # FINAL RESULT
        # ==================================

        result = {
            "discovered": total_discovered,

            "metadata_processed":
                total_metadata,

            "ready":
                total_ready,

            "review":
                total_review,

            "rejected":
                total_rejected,

            "inserted":
                total_inserted,

            "updated":
                total_updated,

            "qdrant_indexed":
                total_qdrant,

            "failed":
                total_failed,

            "batches":
                total_batches,
        }

        print()
        print(
            "================================"
        )

        print(
            "INGESTION COMPLETE"
        )

        print(
            "================================"
        )

        print(
            result
        )

        return result

    # ======================================
    # CREATE DATABASE OBJECT
    # ======================================

    @staticmethod
    def _create_dataset(
        data: dict,
    ) -> Dataset:

        return Dataset(

            name=data.get(
                "name"
            ),

            slug=data.get(
                "slug"
            ),

            description=data.get(
                "description"
            ),

            category=data.get(
                "category"
            ),

            ml_task=data.get(
                "ml_task"
            ),

            data_type=data.get(
                "data_type"
            ),

            difficulty=data.get(
                "difficulty"
            ),

            source=data.get(
                "source"
            ),

            download_url=data.get(
                "download_url"
            ),

            license=data.get(
                "license"
            ),

            rows=data.get(
                "rows"
            ),

            columns=data.get(
                "columns"
            ),

            file_size=data.get(
                "file_size"
            ),

            target_column=data.get(
                "target_column"
            ),

            language=data.get(
                "language"
            ),

            tags=data.get(
                "tags"
            ),

            thumbnail=data.get(
                "thumbnail"
            ),

            downloads=data.get(
                "downloads"
            ),

            rating=data.get(
                "rating"
            ),
        )

    # ======================================
    # UPDATE DATABASE OBJECT
    # ======================================

    @staticmethod
    def _update_dataset(
        existing: Dataset,
        data: dict,
    ):

        fields = [
            "name",
            "slug",
            "description",
            "category",
            "ml_task",
            "data_type",
            "difficulty",
            "source",
            "download_url",
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

        required_fields = {
            "name",
            "slug",
            "description",
            "category",
            "ml_task",
            "data_type",
            "difficulty",
            "source",
            "download_url",
            "license",
            "tags",
        }

        for field in fields:

            value = data.get(
                field
            )

            if field in required_fields:

                setattr(
                    existing,
                    field,
                    value,
                )

            elif value is not None:

                setattr(
                    existing,
                    field,
                    value,
                )


# ==========================================
# SINGLE AGENT INSTANCE
# ==========================================

ingestion_agent = DatasetIngestionAgent()