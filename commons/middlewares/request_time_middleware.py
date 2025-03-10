from fastapi import Request
import time
from starlette.middleware.base import BaseHTTPMiddleware

class RequestTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        request_time = time.perf_counter() - start_time
        print(f"Method: {request.method}\nURL: {request.url}\nTotal time: {request_time} ")
        return response
