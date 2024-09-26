from fastapi import FastAPI

# from common.post_construct import post_construct
from exceptions.exception_handler import attach_exception_handlers
from users.router import router as user_router
from products.router import router as product_router
from users.router_async import router as user_router_async

app = FastAPI()
# post_construct(app)

app.include_router(router=user_router)
app.include_router(router=product_router)
app.include_router(router=user_router_async)

# 예외 핸들러 등록
attach_exception_handlers(app)
