from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
from settings.config import SECRET_KEY, ALGORITHM
from user.models.user_model import User
from settings.database import get_db
from sqlalchemy.future import select

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")  

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Payload decodificado:", payload)
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(status_code=401, detail="No autenticado")
        
        result = await db.execute(
            select(User).where(User.id == user_id, User.is_deleted == False)
        )
        user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")
        
        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError as e:
        print(f"Error: Token inválido - {e}")
        raise HTTPException(status_code=401, detail="Token inválido")
