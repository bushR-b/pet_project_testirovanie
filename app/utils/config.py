
from datetime import timedelta
import os
from authx import AuthX, AuthXConfig


config = AuthXConfig()
config.JWT_ALGORITHM = "HS256"
config.JWT_SECRET_KEY = "b8bfed98be9b0e73e5c6efd611272458a5b1d5900e00e6fdfb7aab86bc9ecefd"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=15)
config.JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=30) 
config.JWT_TOKEN_LOCATION=['headers', 'cookies']

security = AuthX(config=config)