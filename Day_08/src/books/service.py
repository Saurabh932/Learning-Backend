"""
Service layer for Book-related business logic.
This keeps DB logic separated from route handlers (clean architecture).
"""

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from datetime import datetime
from .models import Book
from .schema import BookCreateModel, BookUpdate  # import your pydantic/sqlmodel schemas


class BookService:
    async def get_all_books(self, session: AsyncSession):
        """
        Return all books ordered by created_at desc
        """
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_book(self, book_uid: str, session: AsyncSession):
        """
        Return a single book by uid or None if not found.
        """
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book = result.first()
        return book if book is not None else None

    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        """
        Create a Book from BookCreateModel, convert published_date string to datetime,
        save and return the created Book (with uid, timestamps).
        """
        book_data_dict = book_data.model_dump()
        new_book = Book(**book_data_dict)

        # Convert published_date string ("YYYY-MM-DD") to datetime (optional)
        new_book.published_date = datetime.strptime(book_data_dict['published_date'], "%Y-%m-%d")

        session.add(new_book)
        await session.commit()
        # refresh so DB-generated fields (uid, created_at) are loaded into new_book
        await session.refresh(new_book)
        return new_book

    async def update_book(self, book_uid: str, update_data: BookUpdate, session: AsyncSession):
        """
        Update only the fields provided in update_data (exclude_unset) and return updated object.
        """
        book_update = await self.get_book(book_uid, session)
        if book_update is not None:
            # Only apply provided fields (partial update)
            update_data_dict = update_data.model_dump(exclude_unset=True)
            for k, v in update_data_dict.items():
                setattr(book_update, k, v)

            await session.commit()
            await session.refresh(book_update)
            return book_update
        else:
            return None

    async def delete_book(self, book_uid: str, session: AsyncSession):
        """
        Delete a book and commit. Return {} on success or None if not found.
        """
        book_to_delete = await self.get_book(book_uid, session)
        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()
            return {}
        else:
            return None
