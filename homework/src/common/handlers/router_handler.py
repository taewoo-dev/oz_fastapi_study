from users.router.routers import router as user_router
from products.routers import router as product_router
from users.router.routers_async import router as user_router_async


def attach_router_handlers(app):
    app.include_router(router=user_router)
    app.include_router(router=product_router)
    app.include_router(router=user_router_async)
