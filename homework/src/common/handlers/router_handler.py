from users.routers.router import router as user_router
from products.routers import router as product_router
from users.routers.router_async import router as user_router_async


def attach_router_handlers(app):
    app.include_router(router=user_router)
    app.include_router(router=product_router)
    app.include_router(router=user_router_async)
