class ExpiredTokenException(Exception):
    def __init__(self):
        super().__init__("Token Expired")


class InvalidRefreshTokenException(Exception):
    def __init__(self):
        super().__init__("Refresh Token not found")
