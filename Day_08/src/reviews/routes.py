from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from .schema import ReviewCreateModel
from .service import ReviewService

from src.db.model import User
from src.auth.dependencies import get_current_user
from src.db.main import get_session

review_service = ReviewService()

review_router = APIRouter()

@review_router.post("/book/{book_uid}")
async def review_to_books(book_uid: str, review_data: ReviewCreateModel,
                          session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    
    new_review = await review_service.add_reviews_to_book(user_email = current_user.email,
                                                    review_data = review_data,
                                                    book_uid = book_uid,
                                                    session=session)
    
    return new_review