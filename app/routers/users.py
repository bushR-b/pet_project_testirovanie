from fastapi import APIRouter, Body, Depends, HTTPException, Request, Response, staticfiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.results import TestResult
from app.models.user import User
from app.schemas.user_schemas import UserRefresh, UserLogin, UserPublic
from app.upgrademidlleware import get_current_user
from app.utils.auth import decode_token
from app.utils.config import security

router = APIRouter(prefix="/user", tags=["user"])
router.mount("/static", staticfiles.StaticFiles(directory="app/static"))
templates = Jinja2Templates("app/templates")

@router.get("/me")
def get_current_user_info(
    request: Request, 
    db: Session = Depends(get_db),
    dependencies = Depends(get_current_user)    
):
    result = []
    username = decode_token(request.cookies.get("my_refresh_token"))["sub"]

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    motiv_result = db.query(TestResult).filter(TestResult.test == "motivacionniy", TestResult.user_id == user.id).first()
    tomas_result = db.query(TestResult).filter(TestResult.test == "tomas" and TestResult.user_id == user.id).first()
    keyrsi_result = db.query(TestResult).filter(TestResult.test == "keyrsi", TestResult.user_id == user.id).first()

    result.append(f"Мотивационный тест: {motiv_result.result}")
    result.append(f"Стратегия поведения в конфилктах по тесту Томаса : {tomas_result.result}")
    result.append(f"Тест Кейрси: {keyrsi_result.result}")
    return templates.TemplateResponse("user.html", context={"request": request, "user": user, "result": result})

@router.get("/logout")
def logout(
    response: Response
):
    response.delete_cookie("my_access_token", path="/")
    response.delete_cookie("my_refresh_token", path="/")
    response.headers["Location"] = "/"
    response.status_code = 303
    return response
    


    
