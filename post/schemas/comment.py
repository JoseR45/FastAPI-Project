from pydantic import BaseModel, field_validator
from typing import List, Optional



class CommentResponse(BaseModel):
    id: int
    content: str
    user_id: int
    post_id: int
    class Config:
        from_attributes = True
        
        
class CommentListResponse(BaseModel):
    page:Optional[int] = None
    size:Optional[int] = None
    
    comments: List[CommentResponse]


class CommentCreate(BaseModel):
    post_id: int
    content: str

    @field_validator('content')
    def content_length(cls, v):
        if len(v) > 300:
            raise ValueError('Content must be a maximum of 300 characters')
        return v

class CommentUpdate(BaseModel):
    content: str

    @field_validator('content')
    def content_length(cls, v):
        if len(v) > 300:
            raise ValueError('Content must be a maximum of 300 characters')
        return v