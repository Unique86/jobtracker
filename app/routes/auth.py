from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from app.models.user import User
from app.database import SessionLocal
from fastapi.responses import RedirectResponse
from fastapi.responses import PlainTextResponse
from app.security import hash_password, verify_password
from fastapi import APIRouter, Form, Request, Query

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/register")
def register_page(
    request: Request,
    error: str = Query(None)
):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "error": error
        }
    )

@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        request,
        "login.html",
        {}
    )

@router.post("/login")
def login_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)

):
    username = username.strip()
   
    db = SessionLocal()

    user = db.query(User).filter(
        User.username == username
    ).first()

    db.close()

    if not user:
        return PlainTextResponse(
            "Invalid username or password",
            status_code=401
        )

    if not verify_password(password, user.hashed_password):
       return PlainTextResponse(
        "Invalid username or password",
        status_code=401
    )

    request.session["user_id"] = user.id
    request.session["username"] = user.username

    return RedirectResponse(
    url="/dashboard",
    status_code=303
    )



@router.post("/register")
def register_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    db = SessionLocal()

    existing_username = db.query(User).filter(
        User.username == username
    ).first()

    if existing_username:
        db.close()
        return RedirectResponse(
            url="/register?error=username",
            status_code=303
        )

    existing_email = db.query(User).filter(
        User.email == email
    ).first()

    if existing_email:
        db.close()
        return RedirectResponse(
            url="/register?error=email",
            status_code=303
        )

    hashed_pw = hash_password(password)

    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed_pw
    )

    db.add(new_user)
    db.commit()
    db.close()

    return RedirectResponse(
        url="/",
        status_code=303
    )

@router.get("/logout")
def logout(request: Request):

    request.session.clear()

    return RedirectResponse(
        url="/",
        status_code=303
    )