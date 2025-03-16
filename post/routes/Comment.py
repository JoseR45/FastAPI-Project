from fastapi import APIRouter, Depends, HTTPException
from post.models.post_relations_model import Comment , Post
from post.schemas.comment import CommentCreate, CommentResponse, CommentListResponse, CommentUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from settings.database import get_db
from typing import Dict
from sqlalchemy.future import select
from settings.current_user_security import get_current_user
from user.models.user_model import User
from typing import List


router = APIRouter()


@router.post("/", response_model=CommentResponse)
async def create_comment(
    comment_data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    query = select(Post).filter(Post.id == comment_data.post_id, Post.is_deleted == False)
    result = await db.execute(query)
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = Comment(
        content=comment_data.content,
        user_id=current_user.id,
        post_id=comment_data.post_id
    )

    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    
    return new_comment


@router.get("/", response_model=CommentListResponse)
async def get_comments(
    page: int = None, 
    size: int = None, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    
    if current_user.is_staff:
        query = select(Comment).filter(
            Comment.is_deleted == False,
        )
    else:
        query = select(Comment).filter(
            Comment.user_id == current_user.id,
            Comment.is_deleted == False,
        )
  
    result = await db.execute(query)
    comments = result.scalars().all() 
    if page is not None and size is not None:
        comments = comments[page * size: page * size + size]
        
    return {
        "page": page,
        "size": size,
        "comments": comments
        }



@router.get("/post/{post_id}", response_model=CommentListResponse)
async def get_comments(
    post_id: int,
    page: int = None, 
    size: int = None, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    
    query = select(Comment).filter(
        Comment.post_id == post_id,
        Comment.is_deleted == False,
    )
  
    result = await db.execute(query)
    comments = result.scalars().all() 
    if page is not None and size is not None:
        comments = comments[page * size: page * size + size]
        
    return {
        "page": page,
        "size": size,
        "comments": comments
        }



@router.delete("/{comment_id}", status_code=204)
async def delete_Comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    
    query = select(Comment).filter(
        Comment.id == comment_id,
        Comment.user_id == current_user.id,
        Comment.is_deleted == False
    )

    result = await db.execute(query)
    comment = result.scalar_one_or_none()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found or unauthorized")

    await comment.delete(db)
    

@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    query = select(Comment).filter(
        Comment.id == comment_id,
        Comment.user_id == current_user.id,
        Comment.is_deleted == False
    )

    result = await db.execute(query)
    comment = result.scalar_one_or_none()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found or unauthorized")

    if comment_data.content is not None:
        comment.content = comment_data.content
        
    await db.commit()
    await db.refresh(comment)
    return comment