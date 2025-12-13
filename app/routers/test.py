from app.models.results import TestResult
from app.utils.config import config
from fastapi import APIRouter, Response, Depends, Request, staticfiles
import jwt
from sqlalchemy import Result
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse, RedirectResponse
from app.models.user import User
from app.upgrademidlleware import get_current_user
from app.models.tests import Keyrsi, Motivacionniy, Tomas
from app.schemas.test_schemas import Test
from app.utils.config import security
from app.db import get_db
from app.solvers.keyrsi import keyrsi
from app.solvers.Tomastest import tomas
from app.solvers.motivac import motiv

from fastapi.templating import Jinja2Templates


router = APIRouter(prefix="/test", tags=["Тестирование"])
router.mount("/static", staticfiles.StaticFiles(directory="app/static"))
templates = Jinja2Templates("app/templates")

def prepare_test_data_from_db(db_model, db_session):
    """
    Универсальная функция для подготовки данных теста из БД
    """
    test_data = []
    current_question = None
    
    for item in db_session.query(db_model).order_by(db_model.id).all():
        if item.questions:  # Если это вопрос
            if current_question:
                test_data.append(current_question)
            
            current_question = {
                "question_id": item.id,
                "question_text": item.questions,
                "answers": []
            }
            
            # Добавляем первый вариант ответа
            if item.answers:
                current_question["answers"].append({
                    "id": item.id,
                    "text": item.answers
                })
        else:  # Если это вариант ответа
            if item.answers and current_question:
                current_question["answers"].append({
                    "id": item.id,
                    "text": item.answers
                })
    
    # Добавляем последний вопрос
    if current_question:
        test_data.append(current_question)
    
    return test_data

@router.get("/keyrsi", dependencies=[Depends(get_current_user)])
def keyrsi_test(request: Request, db: Session = Depends(get_db)):
    test_data = prepare_test_data_from_db(Keyrsi, db)
    token = request.cookies.get("my_access_token")
    return templates.TemplateResponse("keyrsi.html", {
        "request": request,
        "test_data": test_data,
        "token": token
    })

@router.post("/keyrsi", dependencies=[Depends(get_current_user)])
def keyrsi_post(
    answers: Test,
    request: Request,
    db: Session = Depends(get_db)
):
    token = request.cookies.get("my_access_token")
    payload = jwt.decode(
        token,
        config.JWT_SECRET_KEY,
        config.JWT_ALGORITHM
    )
    username = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()
    result = keyrsi(answers.answers)
    result_records = TestResult(
        user_id = user.id,
        test = "keyrsi",
        result = result
    )
    db.add(result_records)
    db.commit()
    db.refresh(result_records)
    return result



@router.get("/tomas", dependencies=[Depends(get_current_user)])
def tomas_test(request: Request, db: Session = Depends(get_db)):
    test_data = prepare_test_data_from_db(Tomas, db)
    token = request.cookies.get("my_access_token")
    return templates.TemplateResponse("tomas.html", {
        "request": request,
        "test_data": test_data,
        "token": token
    })


@router.post("/tomas", dependencies=[Depends(get_current_user)])
def tomas_post(
    answers: Test,
    request: Request,
    db: Session = Depends(get_db)
):
    token = request.cookies.get("my_access_token")
    payload = jwt.decode(
        token,
        config.JWT_SECRET_KEY,
        config.JWT_ALGORITHM
    )
    username = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()
    result = tomas(answers.answers)
    result_records = TestResult(
        user_id = user.id,
        test = "tomas",
        result = result
    )
    db.add(result_records)
    db.commit()
    db.refresh(result_records)
    return result

    

@router.get("/motivacionniy", dependencies=[Depends(get_current_user)])
def motivacionniy_test(request: Request, db: Session = Depends(get_db)):
    test_data = prepare_test_data_from_db(Motivacionniy, db)
    token = request.cookies.get("my_access_token")
    return templates.TemplateResponse("motivacionniy.html", {
        "request": request,
        "test_data": test_data,
        "token": token
    })


@router.post("/motivacionniy", dependencies=[Depends(get_current_user)])
def motivacionniy_post(
    answers: Test,
    request: Request,
    db: Session = Depends(get_db)
):
    token = request.cookies.get("my_access_token")
    payload = jwt.decode(
        token,
        config.JWT_SECRET_KEY,
        config.JWT_ALGORITHM
    )
    username = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()
    result = motiv(answers.answers)
    result_records = TestResult(
        user_id = user.id,
        test = "motivacionniy",
        result = result
    )
    old_record = db.query(TestResult).filter(TestResult.user_id == user.id, TestResult.test == "motivacionniy").first()
    if old_record:
        old_record.result = result
        db.commit()
        db.refresh(old_record)
    else:
        db.add(result_records)
        db.commit()
        db.refresh(result_records)
    return result

@router.get("/result", dependencies=[Depends(get_current_user)])
def result(test: str, request: Request, db: Session = Depends(get_db)):

    token = request.cookies.get("my_access_token")
    payload = jwt.decode(
        token,
        config.JWT_SECRET_KEY,
        config.JWT_ALGORITHM
    )

    username = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()

    result = db.query(TestResult).filter(TestResult.test == test, TestResult.user_id == user.id).first()

    return templates.TemplateResponse("result.html", {
        "request": request,
        "result": result,
        "token": token
    })
