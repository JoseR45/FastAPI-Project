from fastapi import APIRouter, Depends, HTTPException
from post.models.post_relations_model import Tag, Post, Comment 
from post.schemas.tags import TagCreateUpdate, TagResponse, TagListResponse 
from sqlalchemy.ext.asyncio import AsyncSession
from settings.database import get_db
from sqlalchemy.future import select
from settings.current_user_security import get_current_user
from user.models.user_model import User
from typing import List


router = APIRouter()



@router.post("/tags", response_model=TagResponse)
async def create_tag(
    tag_data: TagCreateUpdate, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):

    new_tag = Tag(
        name=tag_data.name,
    )
    db.add(new_tag)
    await db.commit()
    await db.refresh(new_tag)
    return new_tag


@router.get("/tags", response_model=TagListResponse)
async def tags_list(
    page: int = None, 
    size: int = None, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = select(Tag).filter(
        Tag.is_deleted == False
    )
    
    result = await db.execute(query)
    tags = result.scalars().all()  
    if page is not None and size is not None:
        tags = tags[page * size: page * size + size]
        
    return {
        "page": page,
        "size": size,
        "tags":tags,
        }


@router.delete("/tags/{tag_id}", status_code=204)
async def delete_tag(
    tag_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    
    query = select(Tag).filter(
        Tag.id == tag_id,
        Tag.is_deleted == False
    )

    result = await db.execute(query)
    tag = result.scalar_one_or_none()

    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found or unauthorized")

    await tag.delete(db)
    

@router.put("/tags/{tag_id}", response_model=TagResponse)
async def update_tag(
    tag_id: int,
    tag_data: TagCreateUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    query = select(Tag).filter(
        Tag.id == tag_id,
        Tag.is_deleted == False
    )

    result = await db.execute(query)
    tag = result.scalar_one_or_none()

    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found or unauthorized")

    if tag_data.name is not None:
        tag.name = tag_data.name

    await db.commit()
    await db.refresh(tag) 

    return tag


@router.delete("/post/{post_id}", status_code=204)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    query = select(Post).filter(
        Post.id == post_id,
        Post.is_deleted == False
    )

    result = await db.execute(query)
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    await post.delete(db)


@router.delete("/comment/{comment_id}", status_code=204)
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    query = select(Comment).filter(
        Comment.id == comment_id,
        Comment.is_deleted == False
    )

    result = await db.execute(query)
    comment = result.scalar_one_or_none()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    await comment.delete(db)

@router.delete("/user/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    query = select(User).filter(
        User.id == user_id,
        User.is_deleted == False
    )

    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await user.delete(db)
    
