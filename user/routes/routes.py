from fastapi import APIRouter, Depends, HTTPException
from user.models.user_model import UserCreate, UserResponse, User
from sqlalchemy.orm import Session
from settings.database import get_db
router = APIRouter()



@router.post("/create/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(email=user.email)
    new_user.set_password(user.password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

