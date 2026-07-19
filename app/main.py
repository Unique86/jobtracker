from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.models.application import Application
from app.models.user import User
from app.database import Base, engine
from app.routes.applications import router as application_router
from app.routes.auth import router as auth_router
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Job Tracker")

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY")
)



Base.metadata.create_all(bind=engine)



app.include_router(application_router)

app.include_router(auth_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )