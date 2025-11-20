from datetime import datetime, date
from typing import Optional, List
import uuid
from pydantic import BaseModel, Field
from src.books.schema import Book

class UserCreation(BaseModel):
    first_name : str = Field(max_length=20)
    last_name : str = Field(max_length=20)
    username : str = Field(max_length=8)
    email : str = Field(max_length=40)
    password : str = Field(...)
    

class UserModel(BaseModel):
    uid: uuid.UUID
    username : str
    email : str
    first_name : str
    last_name : str
    is_verified : bool 
    password_hash : str = Field(exclude=True)
    created_at: datetime 
    updated_at: Optional[datetime] = None
    

class UserBooksModel(BaseModel):
    books: List[Book]
    

class UserLoginModel(BaseModel):
    email : str = Field(max_length=40)
    password : str = Field(...)