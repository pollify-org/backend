from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID as UUID_PG
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Mapped, mapped_column

@as_declarative()
class BaseModel:
    """Base model for all tables with common fields, including soft delete and deleted_by."""
    
    __name__: str

    # ID UUID field
    id: Mapped[UUID] = mapped_column(UUID_PG(as_uuid=True), primary_key=True, default=uuid4)
    
    # Timestamps for creation and update
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
    
    # User ID for the creator of the record
    id_usuario_cad: Mapped[UUID] = mapped_column(UUID_PG(as_uuid=True), nullable=True)
    
    # Soft delete: timestamp of when the record was deleted
    deleted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
    
    # Track who deleted the record
    deleted_by: Mapped[UUID] = mapped_column(UUID_PG(as_uuid=True), nullable=True, default=None)

    @declared_attr
    def __tablename__(cls) -> str:
        """Automatically generates table name in lowercase from class name."""
        return cls.__name__.lower()
