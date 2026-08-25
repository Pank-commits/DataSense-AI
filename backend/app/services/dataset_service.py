from math import ceil

from fastapi import HTTPException
from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session
# ADD THESE IMPORTS AT THE TOP

from app.ai.qdrant_service import (
    create_collection,
    index_dataset,
    delete_dataset_vector,
)
from app.models.dataset import Dataset
from app.schemas.dataset import DatasetCreate, DatasetUpdate


# ==========================
# CREATE
# ==========================
def create_dataset(db: Session, dataset: DatasetCreate):

    new_dataset = Dataset(
        name=dataset.name,
        slug=dataset.slug,
        description=dataset.description,
        category=dataset.category,
        ml_task=dataset.ml_task,
        data_type=dataset.data_type,
        difficulty=dataset.difficulty,
        source=dataset.source,
        download_url=str(dataset.download_url),
        license=dataset.license,
        rows=dataset.rows,
        columns=dataset.columns,
        file_size=dataset.file_size,
        target_column=dataset.target_column,
        language=dataset.language,
        tags=dataset.tags,
        thumbnail=dataset.thumbnail,
    )

    db.add(new_dataset)
    db.commit()
    db.refresh(new_dataset)
    create_collection()
    index_dataset(new_dataset)  

    return new_dataset


# ==========================
# GET ALL
# ==========================
def get_all_datasets(
    db: Session,
    search: str | None = None,
    category: str | None = None,
    ml_task: str | None = None,
    difficulty: str | None = None,
    data_type: str | None = None,
    sort_by: str | None = None,
    order: str = "asc",
    page: int = 1,
    limit: int = 6,
):

    query = db.query(Dataset)

    if search:
        term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Dataset.name.ilike(term),
                Dataset.description.ilike(term),
                Dataset.category.ilike(term),
                Dataset.tags.ilike(term),
            )
        )

    if category:
        query = query.filter(Dataset.category.ilike(category))

    if ml_task:
        query = query.filter(Dataset.ml_task.ilike(ml_task))

    if difficulty:
        query = query.filter(Dataset.difficulty.ilike(difficulty))

    if data_type:
        query = query.filter(Dataset.data_type.ilike(data_type))

    columns = {
        "name": Dataset.name,
        "category": Dataset.category,
        "difficulty": Dataset.difficulty,
        "downloads": Dataset.downloads,
        "rating": Dataset.rating,
        "rows": Dataset.rows,
    }

    if sort_by in columns:
        column = columns[sort_by]

        query = query.order_by(
            desc(column)
            if order.lower() == "desc"
            else asc(column)
        )

    else:
        query = query.order_by(desc(Dataset.created_at))

    total = query.count()

    total_pages = max(1, ceil(total / limit))

    current_page = min(page, total_pages)

    offset = (current_page - 1) * limit

    items = (
        query.offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "items": items,
        "total": total,
        "page": current_page,
        "limit": limit,
        "total_pages": total_pages,
    }


# ==========================
# GET BY ID
# ==========================
def get_dataset_by_id(
    db: Session,
    dataset_id: int
):

    return (
        db.query(Dataset)
        .filter(Dataset.id == dataset_id)
        .first()
    )


# ==========================
# GET BY SLUG
# ==========================
def get_dataset_by_slug(
    db: Session,
    slug: str
):

    dataset = (
        db.query(Dataset)
        .filter(Dataset.slug == slug)
        .first()
    )

    if not dataset:

        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    return dataset


# ==========================
# UPDATE (BY SLUG)
# ==========================
def update_dataset(
    db: Session,
    slug: str,
    dataset: DatasetUpdate
):

    existing = (
        db.query(Dataset)
        .filter(Dataset.slug == slug)
        .first()
    )

    if not existing:

        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    existing.name = dataset.name
    existing.slug = dataset.slug
    existing.description = dataset.description
    existing.category = dataset.category
    existing.ml_task = dataset.ml_task
    existing.data_type = dataset.data_type
    existing.difficulty = dataset.difficulty
    existing.source = dataset.source
    existing.download_url = str(dataset.download_url)
    existing.license = dataset.license
    existing.rows = dataset.rows
    existing.columns = dataset.columns
    existing.file_size = dataset.file_size
    existing.target_column = dataset.target_column
    existing.language = dataset.language
    existing.tags = dataset.tags
    existing.thumbnail = dataset.thumbnail

    db.commit()
    db.refresh(existing)
    create_collection()
    index_dataset(existing)

    return existing


# ==========================
# DELETE (BY SLUG)
# ==========================
def delete_dataset(
    db: Session,
    slug: str
):

    dataset = (
        db.query(Dataset)
        .filter(Dataset.slug == slug)
        .first()
    )

    if not dataset:

        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )
    delete_dataset_vector(dataset.id)
    
    db.delete(dataset)
    db.commit()

    return {
        "message": "Dataset deleted successfully"
    }


# ==========================
# SEARCH
# ==========================
def search_datasets(
    db: Session,
    query: str
):

    return get_all_datasets(
        db,
        search=query
    )["items"]


# ==========================
# FILTER
# ==========================
def filter_by_category(
    db: Session,
    category: str
):

    return get_all_datasets(
        db,
        category=category
    )["items"]


# ==========================
# PAGINATION
# ==========================
def paginate_datasets(
    db: Session,
    page: int,
    limit: int
):

    return get_all_datasets(
        db,
        page=page,
        limit=limit,
    )


# ==========================
# SORT
# ==========================
def sort_datasets(
    db: Session,
    sort_by: str,
    order: str = "asc"
):

    return get_all_datasets(
        db,
        sort_by=sort_by,
        order=order,
    )["items"]