from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.dataset import Dataset
from app.models.source_sync import SourceSyncState

from app.agents.discovery_agent import discovery_agent
from app.agents.kaggle_discovery_agent import (
    kaggle_discovery_agent,
)
from app.agents.metadata_agent import metadata_agent
from app.agents.quality_agent import quality_agent

from app.ai.qdrant_service import index_dataset


HUGGING_FACE_SOURCE = "Hugging Face"
KAGGLE_SOURCE = "Kaggle"


class DatasetSourceSyncAgent:
    """
    Incremental dataset synchronization agent.

    Flow:

        Hugging Face
              ↓
        Recently modified datasets
              ↓
        PostgreSQL duplicate check
              ↓
        Metadata Agent
              ↓
        Quality Agent
              ↓
        PostgreSQL
              ↓
        Qdrant
              ↓
        Save sync timestamp
    """

    def __init__(
        self,
        source: str = HUGGING_FACE_SOURCE,
    ):
        if source not in {
            HUGGING_FACE_SOURCE,
            KAGGLE_SOURCE,
        }:
            raise ValueError(
                "Unsupported dataset source: "
                f"{source}"
            )

        self.source = source

    # ==========================================
    # DISCOVERY AGENT
    # ==========================================

    def get_discovery_agent(self):
        """
        Return the discovery agent for the
        configured source.
        """

        if self.source == KAGGLE_SOURCE:
            return kaggle_discovery_agent

        return discovery_agent

    # ==========================================
    # SYNC STATE
    # ==========================================

    def get_or_create_state(
        self,
        db: Session,
    ):

        state = (
            db.query(SourceSyncState)
            .filter(
                SourceSyncState.source
                == self.source
            )
            .first()
        )

        if state:
            return state

        state = SourceSyncState(
            source=self.source,
            last_dataset_id=None,
            last_sync_at=None,
            datasets_discovered=0,
            datasets_inserted=0,
            datasets_updated=0,
            datasets_failed=0,
        )

        db.add(state)
        db.commit()
        db.refresh(state)

        return state

    # ==========================================
    # FIND EXISTING DATASET
    # ==========================================

    def find_existing(
        self,
        db: Session,
        dataset: dict,
    ):

        slug = dataset.get("slug")

        download_url = dataset.get(
            "download_url"
        )

        existing = None

        # --------------------------------------
        # Check slug
        # --------------------------------------

        if slug:

            existing = (
                db.query(Dataset)
                .filter(
                    Dataset.slug == slug
                )
                .first()
            )

        # --------------------------------------
        # Check download URL
        # --------------------------------------

        if (
            not existing
            and download_url
        ):

            existing = (
                db.query(Dataset)
                .filter(
                    Dataset.download_url
                    == download_url
                )
                .first()
            )

        return existing

    # ==========================================
    # PARSE MODIFIED TIME
    # ==========================================

    @staticmethod
    def parse_datetime(
        value,
    ):
        """
        Convert Hugging Face lastModified
        value into timezone-aware datetime.
        """

        if value is None:
            return None

        if isinstance(
            value,
            datetime,
        ):

            if value.tzinfo is None:

                return value.replace(
                    tzinfo=timezone.utc
                )

            return value

        if isinstance(
            value,
            str,
        ):

            try:

                parsed = (
                    datetime.fromisoformat(
                        value.replace(
                            "Z",
                            "+00:00",
                        )
                    )
                )

                if parsed.tzinfo is None:

                    parsed = parsed.replace(
                        tzinfo=timezone.utc
                    )

                return parsed

            except ValueError:

                return None

        return None

    # ==========================================
    # DISCOVER NEW DATASETS
    # ==========================================

    def discover_new_datasets(
        self,
        last_sync_at,
        limit: int,
    ):
        """
        Discover recently modified datasets.

        If last_sync_at exists, only datasets
        modified after that time are considered.

        If no last_sync_at exists, this is the
        first sync and the newest datasets are
        returned.
        """

        new_datasets = []

        print()
        print(
            "Starting incremental discovery..."
        )

        print(
            f"Last sync time: "
            f"{last_sync_at}"
        )

        discovery = self.get_discovery_agent()

        if self.source == KAGGLE_SOURCE:

            discovered_datasets = (
                discovery.discover(
                    limit=limit,
                    search=None,
                )
            )

        else:

            discovered_datasets = (
                discovery.discover(
                    limit=limit,
                    search=None,
                    offset=0,
                    sort="lastModified",
                )
            )

        for dataset in discovered_datasets:

            modified_at = dataset.get(
                "_last_modified"
            )

            modified_at = (
                self.parse_datetime(
                    modified_at
                )
            )

            # ----------------------------------
            # Existing sync boundary
            # ----------------------------------

            if (
                last_sync_at
                and modified_at
            ):

                # Make both timezone aware.

                if (
                    last_sync_at.tzinfo
                    is None
                ):

                    last_sync_at = (
                        last_sync_at.replace(
                            tzinfo=timezone.utc
                        )
                    )

                # Because discovery is newest-first,
                # once we reach an older/equal dataset,
                # we can stop.

                if (
                    modified_at
                    <= last_sync_at
                ):

                    print(
                        "Reached previous "
                        "sync time boundary."
                    )

                    break

            # ----------------------------------
            # Add new candidate
            # ----------------------------------

            new_datasets.append(
                dataset
            )

            print(
                f"New candidate "
                f"{len(new_datasets)}: "
                f"{dataset.get('name')}"
            )

            if (
                len(new_datasets)
                >= limit
            ):

                break

        return new_datasets

    # ==========================================
    # RUN SYNC
    # ==========================================

    def run(
        self,
        db: Session,
        limit: int = 20,
        batch_size: int = 20,
    ):
        """
        Run one incremental source sync.
        """

        print()
        print(
            "================================"
        )

        print(
            "DATASET SOURCE SYNC"
        )

        print(
            "================================"
        )

        print(
            f"Source: {self.source}"
        )

        print(
            f"Limit: {limit}"
        )

        print(
            f"Batch size: {batch_size}"
        )

        # --------------------------------------
        # Get state
        # --------------------------------------

        state = (
            self.get_or_create_state(
                db
            )
        )

        print(
            f"Last sync: "
            f"{state.last_sync_at}"
        )

        # --------------------------------------
        # Discover new datasets
        # --------------------------------------

        discovered = (
            self.discover_new_datasets(
                last_sync_at=(
                    state.last_sync_at
                ),
                limit=limit,
            )
        )

        print()
        print(
            f"New datasets discovered: "
            f"{len(discovered)}"
        )

        # --------------------------------------
        # Nothing new
        # --------------------------------------

        if not discovered:

            state.last_sync_at = (
                datetime.now(
                    timezone.utc
                )
            )

            db.commit()

            print()
            print(
                "No new datasets found."
            )

            return {
                "discovered": 0,
                "inserted": 0,
                "updated": 0,
                "skipped": 0,
                "failed": 0,
            }

        # --------------------------------------
        # Statistics
        # --------------------------------------

        total_inserted = 0
        total_updated = 0
        total_skipped = 0
        total_failed = 0

        # --------------------------------------
        # Process batches
        # --------------------------------------

        for start in range(
            0,
            len(discovered),
            batch_size,
        ):

            batch = discovered[
                start:start + batch_size
            ]

            print()
            print(
                "--------------------------------"
            )

            print(
                f"SYNC BATCH "
                f"{start + 1}-"
                f"{start + len(batch)}"
            )

            print(
                "--------------------------------"
            )

            new_datasets = []

            # ==================================
            # DUPLICATE CHECK
            # ==================================

            for dataset in batch:

                try:

                    existing = (
                        self.find_existing(
                            db,
                            dataset,
                        )
                    )

                    if existing:

                        self.update_existing(
                            db,
                            existing,
                            dataset,
                        )

                        total_updated += 1

                    else:

                        new_datasets.append(
                            dataset
                        )

                except Exception as error:

                    db.rollback()

                    print(
                        f"Dataset check failed "
                        f"for "
                        f"{dataset.get('name')}: "
                        f"{error}"
                    )

                    total_failed += 1

            print(
                f"New: "
                f"{len(new_datasets)}"
            )

            print(
                f"Updated existing: "
                f"{total_updated}"
            )

            # ==================================
            # METADATA
            # ==================================

            if not new_datasets:

                try:
                    db.commit()
                except Exception:
                    db.rollback()

                continue

            try:

                metadata_processed = (
                    metadata_agent.process_batch(
                        new_datasets
                    )
                )

            except Exception as error:

                print(
                    f"Metadata processing failed: "
                    f"{error}"
                )

                total_failed += (
                    len(new_datasets)
                )

                continue

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
                    f"Quality processing failed: "
                    f"{error}"
                )

                total_failed += (
                    len(metadata_processed)
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

            print(
                f"Quality -> "
                f"READY: {len(ready)} | "
                f"REVIEW: {len(review)} | "
                f"REJECT: {len(rejected)}"
            )

            # ==================================
            # INSERT READY DATASETS
            # ==================================

            for dataset in ready:

                try:

                    normalized = (
                        self.normalize_dataset(
                            dataset
                        )
                    )

                    new_dataset = Dataset(
                        **normalized
                    )

                    db.add(
                        new_dataset
                    )

                    db.flush()

                    index_dataset(
                        new_dataset
                    )

                    total_inserted += 1

                except Exception as error:

                    db.rollback()

                    print(
                        f"Insert failed for "
                        f"{dataset.get('name')}: "
                        f"{error}"
                    )

                    total_failed += 1

            # ==================================
            # COMMIT
            # ==================================

            try:

                db.commit()

            except Exception as error:

                db.rollback()

                print(
                    f"Database commit failed: "
                    f"{error}"
                )

                total_failed += len(
                    batch
                )

        # ======================================
        # UPDATE SYNC STATE
        # ======================================

        state.last_sync_at = (
            datetime.now(
                timezone.utc
            )
        )

        state.datasets_discovered += (
            len(discovered)
        )

        state.datasets_inserted += (
            total_inserted
        )

        state.datasets_updated += (
            total_updated
        )

        state.datasets_failed += (
            total_failed
        )

        # Keep the field for compatibility
        # with the existing database model.
        #
        # We store the newest source ID seen.

        if discovered:

            state.last_dataset_id = (
                discovered[0].get(
                    "_source_id"
                )
            )

        db.commit()

        # ======================================
        # RESULT
        # ======================================

        result = {
            "discovered": len(
                discovered
            ),

            "inserted": (
                total_inserted
            ),

            "updated": (
                total_updated
            ),

            "skipped": (
                total_skipped
            ),

            "failed": (
                total_failed
            ),
        }

        print()
        print(
            "================================"
        )

        print(
            "SOURCE SYNC COMPLETE"
        )

        print(
            "================================"
        )

        print(
            result
        )

        return result

    # ==========================================
    # UPDATE EXISTING DATASET
    # ==========================================

    @staticmethod
    def update_existing(
        db: Session,
        existing: Dataset,
        dataset: dict,
    ):
        """
        Update metadata for an existing dataset
        and refresh its Qdrant vector.
        """

        fields = [
            "name",
            "description",
            "category",
            "ml_task",
            "data_type",
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

        for field in fields:

            value = dataset.get(
                field
            )

            if value is not None:

                setattr(
                    existing,
                    field,
                    value,
                )

        db.flush()

        # Refresh Qdrant vector

        index_dataset(
            existing
        )

    # ==========================================
    # NORMALIZE DATASET
    # ==========================================

    def normalize_dataset(
        self,
        dataset: dict,
    ) -> dict:
        """
        Convert discovery/metadata output
        into Dataset model fields.
        """

        self_source = self.source

        return {
            "name": (
                dataset.get("name")
                or "Unnamed Dataset"
            ),

            "slug": (
                dataset.get("slug")
                or "unknown-dataset"
            ),

            "description": (
                dataset.get("description")
                or "No description available."
            ),

            "category": (
                dataset.get("category")
                or "Other"
            ),

            "ml_task": (
                dataset.get("ml_task")
                or "Unknown"
            ),

            "data_type": (
                dataset.get("data_type")
                or "Unknown"
            ),

            "difficulty": (
                dataset.get("difficulty")
                or "Unknown"
            ),

            "source": (
                dataset.get("source")
                or self_source
            ),

            "download_url": (
                dataset.get(
                    "download_url"
                )
                or ""
            ),

            "license": (
                dataset.get("license")
                or "Unknown"
            ),

            "rows": (
                dataset.get("rows")
                or 0
            ),

            "columns": (
                dataset.get("columns")
                or 0
            ),

            "file_size": (
                dataset.get("file_size")
                or "Unknown"
            ),

            "target_column": (
                dataset.get(
                    "target_column"
                )
                or "Unknown"
            ),

            "language": (
                dataset.get("language")
                or "Unknown"
            ),

            "tags": (
                dataset.get("tags")
                or ""
            ),

            "thumbnail": (
                dataset.get("thumbnail")
                or ""
            ),

            "downloads": (
                dataset.get("downloads")
                or 0
            ),

            "rating": (
                dataset.get("rating")
                or 0.0
            ),
        }


# ==========================================
# SOURCE AGENT INSTANCES
# ==========================================

source_sync_agent = (
    DatasetSourceSyncAgent(
        source=HUGGING_FACE_SOURCE
    )
)

kaggle_sync_agent = (
    DatasetSourceSyncAgent(
        source=KAGGLE_SOURCE
    )
)


# ==========================================
# TERMINAL ENTRY POINT
# ==========================================

if __name__ == "__main__":

    db = SessionLocal()

    try:

        source_sync_agent.run(
            db=db,
            limit=20,
            batch_size=20,
        )

    finally:

        db.close()
