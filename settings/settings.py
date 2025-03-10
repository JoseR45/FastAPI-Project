from starlette.middleware.cors import CORSMiddleware
from commons.middlewares.request_time_middleware import RequestTimeMiddleware
from user.routes.routes import router as users_router



MIDDLEWARES = [
    (RequestTimeMiddleware, {}),
    (CORSMiddleware, {  
        "allow_origins": ["*"],  
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    }),
]

ROUTES = [
     (users_router, "/users")
]


