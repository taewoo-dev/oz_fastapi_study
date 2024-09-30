from core.config import settings

JWT_SECRET_KEY = settings.jwt_secret_key
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_SECONDS = 24 * 60 * 60  # 하루: 24시간 * 60분 * 60초
