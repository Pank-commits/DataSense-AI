from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.dataset import (
    DatasetCreate,
    DatasetListResponse,
    DatasetUpdate,
)

from app.services.dataset_service import (
    create_dataset,
    get_all_datasets,
    get_dataset_by_slug,
    update_dataset,
    delete_dataset,
    search_datasets,
    filter_by_category,
    paginate_datasets,
    sort_datasets,
)

router = APIRouter(
    prefix="/datasets",
    tags=["Datasets"]
)

# ==========================
# CREATE
# ==========================
@router.post("/")
def add_dataset(
    dataset: DatasetCreate,
    db: Session = Depends(get_db)
):
    return create_dataset(db, dataset)


# ==========================
# GET ALL
# ==========================
@router.get("/", response_model=DatasetListResponse)
def get_datasets(
    search: str | None = Query(
        default=None,
        description="Search dataset name, description, category, or tags"
    ),
    category: str | None = Query(default=None),
    ml_task: str | None = Query(default=None),
    difficulty: str | None = Query(default=None),
    data_type: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=6, ge=1),
    sort: str | None = Query(
        default=None,
        description="Sort by: name, category, difficulty, downloads, rating, rows"
    ),
    order: str = Query(
        default="asc",
        description="asc or desc"
    ),
    db: Session = Depends(get_db)
):
    return get_all_datasets(
        db=db,
        search=search,
        category=category,
        ml_task=ml_task,
        difficulty=difficulty,
        data_type=data_type,
        sort_by=sort,
        order=order,
        page=page,
        limit=limit,
    )


# ==========================
# SEARCH
# ==========================
@router.get("/search")
def search(
    q: str,
    db: Session = Depends(get_db)
):
    return search_datasets(db, q)


# ==========================
# FILTER
# ==========================
@router.get("/filter")
def filter_category(
    category: str,
    db: Session = Depends(get_db)
):
    return filter_by_category(db, category)


# ==========================
# PAGINATION
# ==========================
@router.get("/page")
def pagination(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    return paginate_datasets(db, page, limit)


# ==========================
# GET BY SLUG
# ==========================
@router.get("/{slug}")
def get_dataset(
    slug: str,
    db: Session = Depends(get_db)
):
    return get_dataset_by_slug(db, slug)


# ==========================
# UPDATE BY SLUG
# ==========================
@router.put("/{slug}")
def update(
    slug: str,
    dataset: DatasetUpdate,
    db: Session = Depends(get_db)
):
    return update_dataset(
        db,
        slug,
        dataset
    )


# ==========================
# DELETE BY SLUG
# ==========================
@router.delete("/{slug}")
def delete(
    slug: str,
    db: Session = Depends(get_db)
):
    return delete_dataset(
        db,
        slug
    )