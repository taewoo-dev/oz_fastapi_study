from fastapi import FastAPI

# from common.post_construct import post_construct
from exceptions.exception_handler import attach_exception_handlers
from users.router import router as u_router
from products.router import router as p_router


app = FastAPI()
# post_construct(app)

app.include_router(router=u_router)
app.include_router(router=p_router)

# 예외 핸들러 등록
attach_exception_handlers(app)
