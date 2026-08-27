from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from app.db.database import Base


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)

    # Basic Information
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    description = Column(String, nullable=False)

    # Classification
    category = Column(String(100), nullable=False)
    ml_task = Column(String(100), nullable=False)
    data_type = Column(String(100), nullable=False)
    difficulty = Column(String(50), nullable=True)

    # Source
    source = Column(String(100), nullable=False)
    download_url = Column(String(500), nullable=False)
    license = Column(String(100), nullable=False)

    # Statistics
    rows = Column(Integer, nullable=False)
    columns = Column(Integer, nullable=False)
    file_size = Column(String(50), nullable=False)
    target_column = Column(String(100), nullable=False)

    # Extra
    language = Column(String(50), nullable=False)
    tags = Column(String(500), nullable=False)
    thumbnail = Column(String(500), nullable=False)

    # Analytics
    downloads = Column(Integer, default=0)
    rating = Column(Float, default=0.0)

    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )