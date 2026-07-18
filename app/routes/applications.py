
from datetime import date
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.application import Application
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.security import require_login, get_owned_application
templates = Jinja2Templates(directory="app/templates")

router = APIRouter()


@router.get("/add")
def add_application(request: Request):

    response = require_login(request)
    if response:
       return response

    return templates.TemplateResponse(
        request=request,
        name="add_application.html",
        context={},
        
    )

@router.post("/add")
def save_application(

     request: Request,

    company: str = Form(...),

    position: str = Form(...),

    location: str = Form(...),

    status: str = Form(...),

    notes: str = Form(...)

):
    

    response = require_login(request)
    if response:
        return response
   
    db: Session = SessionLocal()
    application = Application(

        company=company,

        position=position,

        location=location,

        status=status,

        date_applied=date.today(),

        feedback="",

        notes=notes,

        user_id=request.session["user_id"]

    )

    db.add(application)

    db.commit()

    db.close()

    return RedirectResponse(
    url="/dashboard",
    status_code=303
    )

@router.get("/dashboard")
def dashboard(request: Request):
    

    response = require_login(request)
    if response:
       return response
    

    db: Session = SessionLocal()

    applications = db.query(Application).filter(
    Application.user_id == request.session["user_id"]
    ).all()

    db.close()

    return templates.TemplateResponse(
    request=request,
    name="dashboard.html",
    context={
        "applications": applications
    }
)
    

@router.get("/edit/{application_id}")
def edit_application(
    application_id: int,
    request: Request,

    
):
    response = require_login(request)
    if response:
        return response


    db: Session = SessionLocal()

    application = get_owned_application(
    db,
    request,
    application_id,
    )

    if isinstance(application, RedirectResponse):
        db.close()
        return application
    
    db.close()
    return templates.TemplateResponse(
    request=request,
    name="edit_application.html",
    context={
        "application": application
    }
)

@router.post("/edit/{application_id}")
def update_application(
    application_id: int,

    request: Request,

    company: str = Form(...),

    position: str = Form(...),

    location: str = Form(...),

    status: str = Form(...),

    notes: str = Form(...),
):
    
    response = require_login(request)
    if response:
        return response
    
    db: Session = SessionLocal()

    application = get_owned_application(
        db,
        request,
        application_id,
    )

    if isinstance(application, RedirectResponse):
        db.close()
        return application

    application.company = company
    application.position = position
    application.location = location
    application.status = status
    application.notes = notes
    db.commit()
    db.close()

    return RedirectResponse(
    url="/dashboard",
    status_code=303
    )


@router.post("/delete/{application_id}")
def delete_application(application_id: int, 
                       request: Request,
                       ):

    response = require_login(request)
    if response:
       return response

    db: Session = SessionLocal()

    application = get_owned_application(
        db,
        request,
        application_id,
    )

    if isinstance(application, RedirectResponse):
        db.close()
        return application



    db.delete(application)

    db.commit()
    db.close()

    return RedirectResponse(
    url="/dashboard",
    status_code=303
   )


