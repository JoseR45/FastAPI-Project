from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from settings.database import Base
from pydantic import BaseModel
from typing import List
from commons.mixins.mixins import SoftDeleteMixin, TimestampMixin

post_tags = Table(
    'post_tags',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)


class Post(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")


class Comment(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))

    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
        

class Tag(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    posts = relationship("Post", secondary=post_tags, back_populates="tags")
    
    
    
    
class PostResponse(BaseModel):
    id: int
    title: str
    content: str  
    
    class Config:
        from_attributes = True

class PostCreate(BaseModel):
    title: str
    content: str