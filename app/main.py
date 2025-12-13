from fastapi import FastAPI, Depends, HTTPException, Request, Response, staticfiles
from fastapi.templating import Jinja2Templates
from authx import AuthX, AuthXConfig
from pydantic import BaseModel
from app.routers.auth import router as aurouter
from app.routers.test import router as terouter
from app.routers.users import router as usrouter
from app.upgrademidlleware import get_current_user

app = FastAPI(title="My Base App")

app.mount("/static", staticfiles.StaticFiles(directory="app/static"))
templates = Jinja2Templates("app/templates")

@app.get("/")
def get_root(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})

app.include_router(aurouter)
app.include_router(terouter)
app.include_router(usrouter)
