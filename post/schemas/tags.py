from pydantic import BaseModel, field_validator
from typing import List, Optional




class TagResponse(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True
    
class TagCreateUpdate(BaseModel):
    name: str
    
    @field_validator('name')
    def name_length(cls, v):
        if len(v) < 5 or len(v) > 30:
            raise ValueError('Name must be between 5 and 30 characters')
        return v

class TagListResponse(BaseModel):
    page:Optional[int] = None
    size:Optional[int] = None
    
    tags: List[TagResponse]
    