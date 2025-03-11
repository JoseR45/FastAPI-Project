from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from settings.database import Base
from pydantic import BaseModel, EmailStr
from post.models.post_relations_model import PostResponse
import aiobcrypt
from typing import List
from commons.mixins.mixins import SoftDeleteMixin, TimestampMixin

class User(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True, index=True)
    email = Column(String(), unique=True, index=True, nullable=False)
    password = Column(String(), nullable=False)
    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")
    
    async def set_password(self, password: str) -> None:
        salt = await aiobcrypt.gensalt()
        self.password = (await aiobcrypt.hashpw(password.encode("utf-8"), salt)).decode("utf-8")

    async def verify_password(self, password: str) -> bool:
        return await aiobcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
    
    
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class UserLoginResponse(BaseModel):
    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserWithPostsResponse(BaseModel):
    id: int
    email: EmailStr
    posts: List[PostResponse]

    class Config:
        from_attributes = True