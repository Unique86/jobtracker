from fastapi import Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.application import Application


pwd_context = CryptContext(
    schemes=["bcrypt"],

    deprecated="auto"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,

    hashed_password: str
) -> bool:
    return pwd_context.verify(
        plain_password,
        
        hashed_password
    )

def require_login(request: Request) -> RedirectResponse | None:

    if "user_id" not in request.session:
        return RedirectResponse(
            url="/login",
            status_code=303
            
        )

    return None



def get_owned_application(
    db: Session,
    request: Request,
    application_id: int,
) -> RedirectResponse | None:

    application = db.get(Application, application_id)

    if application is None:
        return RedirectResponse(
            url="/dashboard",
            status_code=303
        )

    if application.user_id != request.session["user_id"]:
        return RedirectResponse(
            url="/dashboard",
            status_code=303
        )

    return application