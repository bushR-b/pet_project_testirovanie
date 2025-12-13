from datetime import datetime, timedelta
import secrets
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
import jwt
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.schemas.user_schemas import UserLogin, UserRegister
from app.utils.auth import get_password_hash, verify_password
from app.utils.config import security, config

router = APIRouter(prefix="/auth", tags=["Аунтефикация и авторизация"])


@router.post('/register')
def register(creds: UserRegister, response: Response, db: Session = Depends(get_db)):
    if db.query(User).filter(creds.username==User.username).first():
        raise HTTPException(
            status_code=401,
            detail=["User already exists"]
        )
    
    if creds.password != creds.confirm_password:
        raise HTTPException(
            status_code=401,
            detail=["Password and confirm password doesn't match"]
        )
    
    db_user = User(
        name=creds.name,
        surname=creds.surname,
        last_name=creds.last_name,
        username=creds.username,
        hashed_password=get_password_hash(creds.password),
    )    

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    jti = secrets.token_urlsafe(32)
    token = security.create_access_token(uid=creds.username, jti=jti)
    refresh_token = security.create_refresh_token(uid=creds.username, jti=jti)

    db_refresh_token = RefreshToken(
        id=jti,
        user_id=db_user.id,
        token=refresh_token,
        expires_at=datetime.now() + timedelta(days=30),
        is_revoked=False,
        created_at=datetime.now()
    )

    db.add(db_refresh_token)
    db.commit()

    response.set_cookie(
        key="my_access_token",
        value=token,
        max_age=900
    )
    
    response.set_cookie(
        key="my_refresh_token",
        value=refresh_token,
        max_age=30*24*60*60
    )

    return "success"



@router.post('/login')
def login(creds: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username==creds.username).first()

    if not user:
        raise HTTPException(401, detail="User wasn't found")
    
    if not verify_password(creds.password, user.hashed_password):
        raise HTTPException(401, detail={"message": "Bad credentials"})

    jti = secrets.token_urlsafe(32)
    
    # Создаем токены с одним jti
    access_token = security.create_access_token(uid=user.username, jti=jti)
    refresh_token = security.create_refresh_token(uid=user.username, jti=jti)
    
    # Сохраняем refresh token в БД
    db_refresh_token = RefreshToken(
        id=jti,
        user_id=user.id,
        token=refresh_token,
        expires_at=datetime.now() + timedelta(days=30),
        is_revoked=False,
        created_at=datetime.now()
    )
    
    db.add(db_refresh_token)
    db.commit()
    
    # Устанавливаем cookies БЕЗ httponly и secure
    response.set_cookie(
        key="my_access_token",
        value=access_token,
        max_age=900  # 15 минут
    )
    response.set_cookie(
        key="my_refresh_token",
        value=refresh_token,
        max_age=30*24*60*60  # 30 дней
    )
    
    return {"message": "Login successful", "user_id": user.id}


@router.post("/refresh")
def refresh(request: Request, response: Response, db: Session = Depends(get_db)):
    # Получаем refresh token из cookies
    refresh_token_value = request.cookies.get("my_refresh_token")

    if not refresh_token_value:
        raise HTTPException(status_code=401, detail="No refresh token")
    
    try:
        payload = jwt.decode(
            refresh_token_value,
            config.JWT_SECRET_KEY,
            config.JWT_ALGORITHM
        )

        username = payload.get("sub")
        jti = payload.get("jti")
        
        if not username or not jti:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        db_token = db.query(RefreshToken).filter(
            RefreshToken.token == refresh_token_value,
        ).first()
        
        if not db_token:
            raise HTTPException(status_code=401, detail="Token revoked or expired")
        
        # Проверяем срок действия
        if datetime.now() > db_token.expires_at:
            # Помечаем как отозванный
            db_token.is_revoked = True
            db.commit()
            raise HTTPException(status_code=401, detail="Token expired")
        

        user = db.query(User).filter(User.username == username).first()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        new_jti = secrets.token_urlsafe(32)
        
        new_access_token = security.create_access_token(uid=user.username, jti=new_jti)
        new_refresh_token = security.create_refresh_token(uid=user.username, jti=new_jti)
    
        db_token.is_revoked = True
        db_token.revoked_at = datetime.now()

        db.add(RefreshToken(
            id=new_jti,
            user_id=user.id,
            token=new_refresh_token,
            expires_at=datetime.now() + timedelta(days=30),
            is_revoked=False,
            created_at=datetime.now()
        ))

        db.commit()

        response.set_cookie(
            key="my_access_token",
            value=new_access_token,
            max_age=900,  # 15 минут
        )

        response.set_cookie(
            key="my_refresh_token",
            value=new_refresh_token,
            max_age=30*24*60*60,  # 30 дней
        )
        return {"message": "Tokens refreshed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Refresh error: {e}")
        raise HTTPException(status_code=401, detail="Token refresh failed")
