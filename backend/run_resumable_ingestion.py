import json
import os
import time

from app.db.database import SessionLocal
from app.agents.ingestion_agent import ingestion_agent


# ============================================================
# CONFIG
# ============================================================

TARGET = 1_000_000
BATCH_SIZE = 100

CHECKPOINT_FILE = "ingestion_checkpoint.json"

# You stopped after batch 401
# This is used only if no checkpoint file exists.
DEFAULT_START = 40_100


# ============================================================
# CHECKPOINT
# ============================================================

def load_checkpoint():
    """
    Load the last successfully completed dataset position.
    """

    if not os.path.exists(CHECKPOINT_FILE):
        return DEFAULT_START

    try:
        with open(
            CHECKPOINT_FILE,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        processed = int(
            data.get(
                "processed",
                DEFAULT_START,
            )
        )

        print(
            f"Checkpoint found: "
            f"{processed:,} datasets already processed."
        )

        return processed

    except Exception as error:

        print(
            f"Checkpoint could not be read: {error}"
        )

        print(
            f"Starting from {DEFAULT_START:,}"
        )

        return DEFAULT_START


def save_checkpoint(processed):
    """
    Save progress after a completed batch.
    """

    temp_file = (
        CHECKPOINT_FILE
        + ".tmp"
    )

    data = {
        "processed": processed,
        "target": TARGET,
        "batch_size": BATCH_SIZE,
    }

    with open(
        temp_file,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
        )

    # Atomic replacement
    os.replace(
        temp_file,
        CHECKPOINT_FILE,
    )


# ============================================================
# MAIN
# ============================================================

def main():

    processed = load_checkpoint()

    if processed >= TARGET:

        print(
            "Target already reached."
        )

        return

    remaining = (
        TARGET
        - processed
    )

    print()
    print("=" * 60)
    print("RESUMABLE DATASET INGESTION")
    print("=" * 60)

    print(
        f"Target       : {TARGET:,}"
    )

    print(
        f"Already done : {processed:,}"
    )

    print(
        f"Remaining    : {remaining:,}"
    )

    print(
        f"Batch size   : {BATCH_SIZE}"
    )

    print("=" * 60)
    print()

    batch_number = (
        processed // BATCH_SIZE
    ) + 1

    db = SessionLocal()

    try:

        while processed < TARGET:

            current_batch_size = min(
                BATCH_SIZE,
                TARGET - processed,
            )

            start_position = (
                processed + 1
            )

            end_position = (
                processed
                + current_batch_size
            )

            print()
            print("=" * 40)

            print(
                f"BATCH {batch_number} "
                f"({start_position:,}-"
                f"{end_position:,}/"
                f"{TARGET:,})"
            )

            print("=" * 40)

            try:

                # IMPORTANT:
                # The discovery agent currently starts
                # from the beginning. We will update it
                # in Step 2 below to support resume_offset.

                result = ingestion_agent.ingest(
                    db=db,
                    limit=current_batch_size,
                    offset=processed,
                )

                print(
                    f"Quality -> "
                    f"READY: {result.get('ready', 0)} | "
                    f"REVIEW: {result.get('review', 0)} | "
                    f"REJECT: {result.get('rejected', 0)}"
                )

                print(
                    f"PostgreSQL -> "
                    f"Inserted: {result.get('inserted', 0)} | "
                    f"Updated: {result.get('updated', 0)}"
                )

                print(
                    f"Qdrant indexed: "
                    f"{result.get('qdrant_indexed', 0)}"
                )

                failed = result.get(
                    "failed",
                    0,
                )

                print(
                    f"Failed: {failed}"
                )

                # --------------------------------------------
                # SAVE CHECKPOINT
                # --------------------------------------------

                processed = end_position

                save_checkpoint(
                    processed
                )

                print(
                    f"Checkpoint saved: "
                    f"{processed:,}/{TARGET:,}"
                )

                print(
                    f"Progress: "
                    f"{processed:,}/{TARGET:,}"
                )

                batch_number += 1

            except KeyboardInterrupt:

                print()
                print(
                    "Ingestion stopped by user."
                )

                print(
                    f"Last saved checkpoint: "
                    f"{processed:,}"
                )

                break

            except Exception as error:

                print()
                print(
                    "BATCH FAILED:"
                )

                print(error)

                print()
                print(
                    "Checkpoint was NOT advanced."
                )

                print(
                    f"Will retry from: "
                    f"{processed + 1:,}"
                )

                time.sleep(5)

    finally:

        db.close()

    print()
    print("=" * 60)
    print("INGESTION SESSION FINISHED")
    print("=" * 60)

    print(
        f"Processed checkpoint: "
        f"{processed:,}/{TARGET:,}"
    )


if __name__ == "__main__":
    main()