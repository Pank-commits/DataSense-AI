from datetime import datetime

from pydantic import BaseModel, HttpUrl, ConfigDict


class DatasetBase(BaseModel):
    # Basic
    name: str
    slug: str
    description: str

    # Classification
    category: str
    ml_task: str
    data_type: str
    difficulty: str

    # Source
    source: str
    download_url: HttpUrl
    license: str

    # Statistics
    rows: int
    columns: int
    file_size: str
    target_column: str

    # Extra
    language: str
    tags: str
    thumbnail: str


class DatasetCreate(DatasetBase):
    pass


class DatasetUpdate(DatasetBase):
    pass


class DatasetResponse(DatasetBase):
    id: int
    downloads: int
    rating: float
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DatasetListResponse(BaseModel):
    items: list[DatasetResponse]
    total: int
    page: int
    limit: int
    total_pages: int
