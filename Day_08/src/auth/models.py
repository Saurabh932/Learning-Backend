import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.dialects.postgresql import UUID


class User(SQLModel, table=True):
    __tablename__ = 'users'
    uid : uuid.UUID = Field(
                            default_factory=uuid.uuid4,
                            sa_column=Column(UUID(as_uuid=True),
                            primary_key=True,
                            default=uuid.uuid4))
    username : str
    first_name : str
    last_name : str
    is_verified : bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    
    
def __repr__(self):
    return f"<User {self.username}>"