from fastapi import APIRouter, Depends, HTTPException
from user.models.user_model import UserCreate, UserResponse, UserLoginResponse, User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from settings.database import get_db
from typing import Dict
from fastapi.security import OAuth2PasswordRequestForm
from settings.jwt_security import create_access_token, create_refresh_token, verify_token, RefreshTokenData

router = APIRouter()

@router.post("/create", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user.email, User.is_deleted == False))
    db_user = result.scalars().first()

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(email=user.email)
    await new_user.set_password(user.password)

    db.add(new_user)
    await db.commit() 
    await db.refresh(new_user)  

    return new_user


@router.post("/login", response_model=UserLoginResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_db)
):
    query = select(User).where(User.email == form_data.username, User.is_deleted == False)
    result = await db.execute(query)
    user = result.scalars().first()

    if not user or not await user.verify_password(form_data.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})

    return UserLoginResponse(user=user, access_token=access_token, refresh_token=refresh_token)

@router.post("/refresh")
def refresh_token(token_data: RefreshTokenData):
    payload = verify_token(token_data.refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    new_access_token = create_access_token({"sub": payload["sub"]})
    return {"access_token": new_access_token, "token_type": "bearer"}