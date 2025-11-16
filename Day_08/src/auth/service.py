from .schemas import UserCreation
from .utils import generate_passwd_hash
from src.db.model import User
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select

class UserService:
    async def get_user_by_email(self, email : str, session:AsyncSession):
        statement = select(User).where(User.email == email)
        
        result = await session.execute(statement)
        user = result.scalar_one_or_none()
        return user
    
    async def user_exists(self, email, session:AsyncSession):
        user = await self.get_user_by_email(email, session)
        
        return True if user is not None else False
    
    
    async def create_user(self, user_data: UserCreation, session: AsyncSession):
        user_data_dict = user_data.model_dump()

        new_user = User(**user_data_dict)
        new_user.password_hash = generate_passwd_hash(user_data_dict['password'])
        new_user.role = "user"

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user
