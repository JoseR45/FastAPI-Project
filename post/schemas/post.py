from pydantic import BaseModel, field_validator
from .comment import CommentResponse
from .tags import TagResponse
from typing import List, Optional


class PostResponse(BaseModel):
    id: int
    title: str
    content: str  
    
    class Config:
        from_attributes = True



class PostCreate(BaseModel):
    title: str
    content: str
    tag_ids: List[int] = [] 
    
    @field_validator('title')
    def title_length(cls, v):
        if len(v) < 5 or len(v) > 50:
            raise ValueError('Title must be between 5 and 50 characters')
        return v

    @field_validator('content')
    def content_length(cls, v):
        if len(v) > 255:
            raise ValueError('Content must be a maximum of 255 characters')
        return v

class PostUpdate(PostCreate):
    title: Optional[str] = None
    content: Optional[str] = None
    tag_ids: Optional[List[int]] = None
    
    
class PostInfoResponse(BaseModel):
    id: int
    title: str
    content: str  
    tags: List[TagResponse] = [] 
    comments: List[CommentResponse] = []
    
    class Config:
        from_attributes = True


class PostListResponse(BaseModel):
    page:Optional[int] = None
    size:Optional[int] = None
    
    posts: List[PostResponse]