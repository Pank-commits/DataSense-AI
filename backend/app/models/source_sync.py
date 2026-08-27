from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.db.database import Base


class SourceSyncState(Base):
    __tablename__ = "source_sync_state"

    id = Column(Integer, primary_key=True, index=True)

    source = Column(
        String(100),
        unique=True,
        nullable=False,
    )

    last_dataset_id = Column(
        String(500),
        nullable=True,
    )

    last_sync_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    datasets_discovered = Column(
        Integer,
        default=0,
    )

    datasets_inserted = Column(
        Integer,
        default=0,
    )

    datasets_updated = Column(
        Integer,
        default=0,
    )

    datasets_failed = Column(
        Integer,
        default=0,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )