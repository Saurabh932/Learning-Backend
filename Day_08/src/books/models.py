
"""
This file defines the Book table structure using SQLModel.
Each class here represents a table in the database.
"""

from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, date
import uuid
from typing import Optional
from src.db import model

# Define the Book table model
class Book(SQLModel, table=True):
    # Explicitly specify table name in the DB
    __tablename__ = "books"

    # Unique ID column (Primary Key) using PostgreSQL UUID type
    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    # Basic columns — SQLModel will map these to appropriate SQL types
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str

    # For establishing relationship between ueers and books
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    
    # Timestamps: using PostgreSQL TIMESTAMP column with defaults
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    
    user: Optional["model.User"] = Relationship(back_populates="books")

    # Nice __repr__ for debugging/logging
    def __repr__(self):
        return f"<Book {self.title}>"

