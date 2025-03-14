from fastapi import APIRouter, Depends, HTTPException
from post.models.post_relations_model import Post, Tag 
from post.schemas.post import PostListResponse, PostCreate, PostInfoResponse, PostUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from settings.database import get_db
from typing import Dict
from sqlalchemy.future import select
from settings.current_user_security import get_current_user
from user.models.user_model import User
from sqlalchemy.orm import selectinload
from typing import List


router = APIRouter()



@router.post("/", response_model=PostInfoResponse)
async def create_post(
    post_data: PostCreate, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    new_post = Post(
            title=post_data.title,
            content=post_data.content, 
            user_id=current_user.id  
        )
    
    if post_data.tag_ids:
        query = select(Tag).where(Tag.id.in_(post_data.tag_ids))
        result = await db.execute(query)

        tags = result.scalars().all()
        
        if not tags:
            raise HTTPException(status_code=400, detail="Invalid tag IDs")
        
        
        new_post.tags = tags
        
        

    db.add(new_post) 
    await db.commit()
    await db.refresh(new_post)
    query = select(Post).options(selectinload(Post.tags), selectinload(Post.comments)).filter(
        Post.id == new_post.id,
        Post.user_id == current_user.id,
        Post.is_deleted == False
    )
    result = await db.execute(query)
    post = result.scalar_one_or_none()
    
    return PostInfoResponse.model_validate(post)

@router.get("/{post_id}", response_model=PostInfoResponse )
async def get_post_info(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    query = select(Post).options(selectinload(Post.tags), selectinload(Post.comments)).filter(
        Post.id == post_id,
        Post.is_deleted == False
    )
    
    result = await db.execute(query)
    post = result.scalar_one_or_none()

    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")


    return post
   


@router.get("/", response_model=PostListResponse)
async def get_post_list(
    page: int = None, 
    size: int = None, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = select(Post).filter(
        Post.is_deleted == False
    )
    
    result = await db.execute(query)
    posts = result.scalars().all()  
    if page is not None and size is not None:
        posts = posts[page * size: page * size + size]
    return {
        "page": page,
        "size": size,
        "posts": posts
    }


@router.delete("/{post_id}", status_code=204)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    query = select(Post).filter(
        Post.id == post_id,
        Post.user_id == current_user.id,
        Post.is_deleted == False
    )

    result = await db.execute(query)
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found or unauthorized")


    await post.delete(db)

    

@router.put("/{post_id}", response_model=PostInfoResponse)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = select(Post).options(selectinload(Post.tags), selectinload(Post.comments)).filter(
        Post.id == post_id,
        Post.user_id == current_user.id,
        Post.is_deleted == False
    )

    result = await db.execute(query)
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found or unauthorized")

    if post_data.title is not None:
        post.title = post_data.title
    if post_data.content is not None:
        post.content = post_data.content
    if post_data.tag_ids:
        query = select(Tag).where(Tag.id.in_(post_data.tag_ids))
        result = await db.execute(query)

        tags = result.scalars().all()
        
        if not tags:
            raise HTTPException(status_code=400, detail="Invalid tag IDs")
        
        
        post.tags = tags
    
    await db.commit()
    await db.refresh(post,["tags"])

    return post