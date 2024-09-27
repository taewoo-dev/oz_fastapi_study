from core.middlewares.middlewares.jwt_auth_middleware import JWTAuthMiddleware


def attach_middleware_handlers(app):
    app.add_middleware(JWTAuthMiddleware)
