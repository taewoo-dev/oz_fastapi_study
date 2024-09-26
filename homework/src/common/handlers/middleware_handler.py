from core.middlewares.middleware.JWTAuthMiddleware import JWTAuthMiddleware


def attach_middleware_handlers(app):
    app.add_middleware(JWTAuthMiddleware)
