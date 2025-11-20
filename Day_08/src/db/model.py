import uuid
from typing import List, Optional
from datetime import datetime, date

from src.db import model
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import SQLModel, Field, Column, Relationship
from sqlalchemy.dialects.postgresql import UUID



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
    
    user: Optional["User"] = Relationship(back_populates="books")
    reviews: List["Review"] = Relationship(back_populates="book", sa_relationship_kwargs={"lazy": "selectin"})
    
    
    # Nice __repr__ for debugging/logging
    def __repr__(self):
        return f"<Book {self.title}>"



class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    username: str
    email: str
    first_name: str
    last_name: str
    role: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, server_default="user"))
    is_verified: bool = Field(default=False)
    password_hash: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False), exclude=True
    )
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    update_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    
    books: List["Book"] = Relationship(back_populates="user",
                                             sa_relationship_kwargs={"lazy":"selectin"})

    reviews: List["Review"] = Relationship(back_populates="user",
                                             sa_relationship_kwargs={"lazy":"selectin"})
    
    
    def __repr__(self):
        return f"<User {self.username}>"
    
    
class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    rating: int = Field(lt=5)
    review_text: str

    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    book_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="books.uid")

    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))  # ← FIXED

    user: Optional["User"] = Relationship(back_populates="reviews")
    book: Optional["Book"] = Relationship(back_populates="reviews")

    def __repr__(self):
        return f"<Review for {self.book_uid} by {self.user_uid}>"
