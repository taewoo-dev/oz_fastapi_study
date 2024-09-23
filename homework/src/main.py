from fastapi import FastAPI
from users.router import router as u_router
from products.router import router as p_router


app = FastAPI()

app.include_router(router=u_router)
app.include_router(router=p_router)
