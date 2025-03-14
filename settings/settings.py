from starlette.middleware.cors import CORSMiddleware
from commons.middlewares.request_middleware import RequestTimeMiddleware, AdminAccessMiddleware
from user.routes.routes import router as users_router
from post.routes.post import router as post_router
from admin.routes.tags import router as admin_tags_router
from post.routes.Comment import router as comment_router



MIDDLEWARES = [
    (CORSMiddleware, {  
        "allow_origins": ["*"],  
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    }),
    (RequestTimeMiddleware, {}),
    (AdminAccessMiddleware, {}),
]

ROUTES = [
     (admin_tags_router, "/admin"),
     (users_router, "/users"),
     (post_router, "/post"),
     (comment_router, "/coment"),
]


