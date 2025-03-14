from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from settings.database import Base
from pydantic import BaseModel, EmailStr, field_validator
from post.schemas.post import PostResponse
import aiobcrypt
from typing import List
from commons.mixins.mixins import SoftDeleteMixin, TimestampMixin
from typing import Optional

class User(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True, index=True)
    email = Column(String(), unique=True, index=True, nullable=False)
    password = Column(String(), nullable=False)
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    is_staff = Column(Boolean, default=False, nullable=False)
    
    async def set_password(self, password: str) -> None:
        salt = await aiobcrypt.gensalt()
        self.password = (await aiobcrypt.hashpw(password.encode("utf-8"), salt)).decode("utf-8")

    async def verify_password(self, password: str) -> bool:
        return await aiobcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
    
    
class UserBase(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 4:
            raise ValueError("Password must be at least 4 characters long")
        return v

class UserCreate(UserBase):
    pass  

class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    password: Optional[str] = None 




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
    
class UserListResponse(BaseModel):
    page:Optional[int] = None
    size:Optional[int] = None
    
    users: List[UserResponse]