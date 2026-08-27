from fastapi import APIRouter, Depends
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.database import get_db
from app.models.dataset import Dataset

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    # ==========================
    # Dashboard Summary
    # ==========================
    total_datasets = db.query(Dataset).count()

    total_categories = (
        db.query(Dataset.category)
        .distinct()
        .count()
    )

    total_downloads = (
        db.query(
            func.coalesce(func.sum(Dataset.downloads), 0)
        ).scalar()
    )

    average_rating = (
        db.query(
            func.coalesce(func.avg(Dataset.rating), 0)
        ).scalar()
    )

    # ==========================
    # Recent Datasets
    # ==========================
    recent_datasets = (
        db.query(Dataset)
        .order_by(Dataset.created_at.desc())
        .limit(5)
        .all()
    )

    # ==========================
    # Category Statistics
    # ==========================
    category_stats = (
        db.query(
            Dataset.category,
            func.count(Dataset.id).label("count")
        )
        .group_by(Dataset.category)
        .order_by(func.count(Dataset.id).desc())
        .all()
    )

    # ==========================
    # ML Task Statistics
    # ==========================
    ml_task_stats = (
        db.query(
            Dataset.ml_task,
            func.count(Dataset.id).label("count")
        )
        .group_by(Dataset.ml_task)
        .order_by(func.count(Dataset.id).desc())
        .all()
    )

    # ==========================
    # Top Rated Datasets
    # ==========================
    top_rated = (
        db.query(Dataset)
        .order_by(Dataset.rating.desc())
        .limit(5)
        .all()
    )

    return {
        "total_datasets": total_datasets,
        "total_categories": total_categories,
        "total_downloads": total_downloads,
        "average_rating": round(float(average_rating), 2),

        "recent_datasets": [
            {
                "id": dataset.id,
                "name": dataset.name,
                "slug": dataset.slug,
                "category": dataset.category,
                "ml_task": dataset.ml_task,
                "downloads": dataset.downloads,
                "rating": dataset.rating,
                "created_at": dataset.created_at,
            }
            for dataset in recent_datasets
        ],

        "category_stats": [
            {
                "category": item.category,
                "count": item.count,
            }
            for item in category_stats
        ],

        "ml_task_stats": [
            {
                "task": item.ml_task,
                "count": item.count,
            }
            for item in ml_task_stats
        ],

        "top_rated_datasets": [
            {
                "id": dataset.id,
                "name": dataset.name,
                "slug": dataset.slug,
                "category": dataset.category,
                "rating": dataset.rating,
                "downloads": dataset.downloads,
            }
            for dataset in top_rated
        ]
    }
