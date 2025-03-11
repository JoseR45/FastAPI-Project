from fastapi import FastAPI
from settings.settings import MIDDLEWARES, ROUTES


app = FastAPI()


for middleware, options in MIDDLEWARES:
        app.add_middleware(middleware, **options)

for router, prefix in ROUTES:
        app.include_router(router, prefix=prefix)


    