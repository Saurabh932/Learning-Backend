import logging
from fastapi import status
from fastapi.exceptions import HTTPException
from src.db.model import Review
from src.auth.service import UserService
from src.books.service import BookService
from .schema import ReviewCreateModel, ReviweModel
from sqlmodel.ext.asyncio.session import AsyncSession

book_service = BookService()
user_service = UserService()

class ReviewService:
    async def add_reviews_to_book(self, user_email: str, book_uid: str, 
                                  review_data: ReviewCreateModel, session: AsyncSession):
        try:
            book = await book_service.get_book(book_uid=book_uid, session=session)
            
            user = await user_service.get_user_by_email(email=user_email, session=session)
            
            review_data_dict = review_data.model_dump()
            new_review = Review(**review_data_dict)
            
            if not book:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")
            
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
            
            new_review.user = user
            new_review.book = book
            
            session.add(new_review)
            
            await session.commit()
            
            return new_review
            
        except Exception as e:
            logging.exception(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Ooops... Something went wrong!")