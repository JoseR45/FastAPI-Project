from fastapi import Request, HTTPException
import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.security import OAuth2PasswordBearer
from user.models.user_model import User
from settings.database import get_db
from settings.current_user_security import get_current_user
from starlette.responses import JSONResponse

class RequestTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        request_time = time.perf_counter() - start_time
        print(f"Method: {request.method}\nURL: {request.url}\nTotal time: {request_time} ")
        return response


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

class AdminAccessMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            if request.url.path.startswith("/admin/"):
                db = await anext(get_db())
                token = request.headers.get("Authorization")
                if token:
                    token = token.replace("Bearer ", "")
                    current_user = await get_current_user(token, db) 
                    
                
                    if not current_user.is_staff:
                        raise HTTPException(status_code=403, detail="Permiso denegado")
                else:
                    raise HTTPException(status_code=403, detail="Permiso denegado")

            response = await call_next(request)
            return response
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

        except Exception as e:
            return JSONResponse(status_code=500, content={"detail": "Internal server error"})