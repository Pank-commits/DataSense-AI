from apscheduler.schedulers.background import BackgroundScheduler

from app.db.database import SessionLocal

from app.agents.source_sync_agent import (
    source_sync_agent,
    kaggle_sync_agent,
)


# ==========================================
# SCHEDULER
# ==========================================

scheduler = BackgroundScheduler()


# ==========================================
# HUGGING FACE SYNC
# ==========================================

def run_huggingface_sync():

    print()
    print("================================")
    print("AUTOMATIC HUGGING FACE SYNC")
    print("================================")

    db = SessionLocal()

    try:

        result = source_sync_agent.run(
            db=db,
            limit=100,
            batch_size=100,
        )

        print()
        print("Hugging Face sync result:")
        print(result)

    except Exception as error:

        print()
        print(
            f"Hugging Face sync failed: {error}"
        )

    finally:

        db.close()


# ==========================================
# KAGGLE SYNC
# ==========================================

def run_kaggle_sync():

    print()
    print("================================")
    print("AUTOMATIC KAGGLE SYNC")
    print("================================")

    db = SessionLocal()

    try:

        result = kaggle_sync_agent.run(
            db=db,
            limit=100,
            batch_size=100,
        )

        print()
        print("Kaggle sync result:")
        print(result)

    except Exception as error:

        print()
        print(
            f"Kaggle sync failed: {error}"
        )

    finally:

        db.close()


# ==========================================
# COMPLETE DATASET SYNC
# ==========================================

def run_dataset_sync():

    print()
    print("================================")
    print("AUTOMATIC DATASET SYNC")
    print("================================")

    # --------------------------------------
    # HUGGING FACE
    # --------------------------------------

    run_huggingface_sync()

    # --------------------------------------
    # KAGGLE
    # --------------------------------------

    run_kaggle_sync()

    # --------------------------------------
    # COMPLETE
    # --------------------------------------

    print()
    print("================================")
    print("AUTOMATIC DATASET SYNC COMPLETE")
    print("================================")


# ==========================================
# START SCHEDULER
# ==========================================

def start_scheduler():

    if scheduler.running:
        return

    # --------------------------------------
    # Run once immediately on startup
    # --------------------------------------

    scheduler.add_job(
        run_dataset_sync,
        id="dataset_initial_sync",
        replace_existing=True,
    )

    # --------------------------------------
    # Run every 6 hours
    # --------------------------------------

    scheduler.add_job(
        run_dataset_sync,
        "interval",
        hours=6,
        id="dataset_source_sync",
        replace_existing=True,
        max_instances=1,
    )

    # --------------------------------------
    # Start scheduler
    # --------------------------------------

    scheduler.start()

    print()
    print("================================")
    print("DATASET SCHEDULER")
    print("================================")

    print(
        "Dataset sync scheduler started."
    )

    print(
        "Initial sync: Hugging Face + Kaggle."
    )

    print(
        "Recurring sync: every 6 hours."
    )


# ==========================================
# STOP SCHEDULER
# ==========================================

def stop_scheduler():

    if scheduler.running:

        scheduler.shutdown(
            wait=False
        )

        print(
            "Dataset sync scheduler stopped."
        )