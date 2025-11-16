"""
API routes for Book resource.
Uses dependency injection to get the AsyncSession from src.db.main:get_session.
"""

from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession

# Import the request/response schemas (Pydantic/SQLModel models)
from src.books.schema import Book, BookUpdate, BookCreateModel

from src.books.service import BookService
from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer, RoleChecker


router = APIRouter()
book_service = BookService()
access_token_bearier = AccessTokenBearer()
role_checker = Depends(RoleChecker(['admin', 'user']))


@router.get("/", response_model=List[Book], dependencies=[role_checker])
async def get_all_books(session: AsyncSession = Depends(get_session),
                        user_details = Depends(access_token_bearier)):
    """
    GET /api/v1/book/
    Return list of books
    """
    print(user_details)
    books = await book_service.get_all_books(session)
    return books


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book,  dependencies=[role_checker])
async def create_book(book_data: BookCreateModel, 
                      session: AsyncSession = Depends(get_session),
                      user_details = Depends(access_token_bearier)) -> dict:
    """
    POST /api/v1/book/
    Create and return the created book
    """
    new_book = await book_service.create_book(book_data, session)
    return new_book


@router.get("/{book_uid}", response_model=Book,  dependencies=[role_checker])
async def get_book(book_uid: str, 
                   session: AsyncSession = Depends(get_session),
                   user_details = Depends(access_token_bearier)):
    """
    GET /api/v1/book/{book_uid}
    Return single book or 404
    """
    book = await book_service.get_book(book_uid, session)
    if book:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@router.patch("/{book_uid}", response_model=Book, dependencies=[role_checker])
async def update_book(book_uid: str, 
                      book_update_data: BookUpdate, 
                      session: AsyncSession = Depends(get_session),
                      user_details = Depends(access_token_bearier)):
    """
    PATCH /api/v1/book/{book_uid}
    Partial update — only fields provided in the body are updated
    """
    updated_book = await book_service.update_book(book_uid, book_update_data, session)
    if updated_book:
        return updated_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_book(book_uid: str, 
                      session: AsyncSession = Depends(get_session),
                      user_details = Depends(access_token_bearier)):
    """
    DELETE /api/v1/book/{book_uid}
    Delete the book. Return 204 if success, otherwise 404.
    """
    book_delete = await book_service.delete_book(book_uid, session)
    if book_delete is not None:
        return None
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
