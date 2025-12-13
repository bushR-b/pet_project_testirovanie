from datetime import datetime, timedelta
from typing import Optional
import authx
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from passlib.context import CryptContext
import os 
from app.db import get_db
from app.models.user import User
from app.utils.config import config

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

# функции для работы с паролями
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет пароль - работает с паролями любой длины"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Хеширует пароль - работает с паролями любой длины"""
    return pwd_context.hash(password)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None
