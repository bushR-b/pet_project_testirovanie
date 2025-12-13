import secrets
from datetime import datetime, timedelta
from fastapi import Request, HTTPException, Depends, Response
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.db import get_db
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.utils.config import security  # Импортируем security из конфига


def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Зависимость для GET запросов, которая автоматически обновляет токены
    """
    access_token = request.cookies.get("my_access_token")
    refresh_token = request.cookies.get("my_refresh_token")
    
    if not access_token:
        if not refresh_token:
            raise HTTPException(status_code=401, detail="Not authenticated")
        return RedirectResponse("/auth/refresh")
    
    try:
        secret_key = security._config.JWT_SECRET_KEY
        algorithm = security._config.JWT_ALGORITHM
        
        payload = jwt.decode(access_token, secret_key, algorithms=[algorithm])
        username = payload.get("sub")
        
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = db.query(User).filter(User.username == username).first()
        
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
        
    except jwt.ExpiredSignatureError:
        # На фронте должен быть перехват 401 и вызов /auth/refresh
        raise HTTPException(
            status_code=401, 
            detail="Token expired. Please refresh your session."
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")