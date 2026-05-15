from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from jose import jwt
from jose import JWTError
from fastapi import Cookie
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.utils.auth import verify_password


router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)

SECRET_KEY = "mysecretkey"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


def get_current_user(
    access_token: str = Cookie(None),
    db: Session = Depends(get_db)
):

    if not access_token:
        return None

    try:

        payload = jwt.decode(
            access_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:
            return None

    except JWTError:
        return None

    user = db.query(User).filter(
        User.email == email
    ).first()

    return user

def role_required(allowed_roles: list):

    def wrapper(user: User = Depends(get_current_user)):

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Authentication required"
            )

        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

        return user

    return wrapper

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )

@router.post("/login")
def login( email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email"
        )

    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    token = create_access_token(
        data={
            "sub": user.email,
            "role": user.role
        }
    )

    response = RedirectResponse(url=f"/{user.role}", status_code=302)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True
    )

    return response

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    user: User = Depends(get_current_user)
):

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=302
        )

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"user": user}
    )


@router.get("/sales_rep", response_class=HTMLResponse)
def sales_rep_dashboard(
    request: Request,
    user: User = Depends(
        role_required(["sales_rep"])
    )
):

    return templates.TemplateResponse(
        request=request,
        name="manager/sales_rep.html",
        context={"user": user}
    )


@router.get("/sales_manager", response_class=HTMLResponse)
def sales_manager_dashboard(
    request: Request,
    user: User = Depends(
        role_required(["sales_manager"])
    )
):

    return templates.TemplateResponse(
        request=request,
        name="manager/sales_manager.html",
        context={"user": user}
    )


@router.get("/account_manager", response_class=HTMLResponse)
def account_manager_dashboard(
    request: Request,
    user: User = Depends(
        role_required(["account_manager"])
    )
):

    return templates.TemplateResponse(
        request=request,
        name="manager/account_manager.html",
        context={"user": user}
    )


@router.get("/marketing", response_class=HTMLResponse)
def marketing_dashboard(
    request: Request,
    user: User = Depends(
        role_required(["marketing"])
    )
):

    return templates.TemplateResponse(
        request=request,
        name="manager/marketing.html",
        context={"user": user}
    )


@router.get("/product_manager", response_class=HTMLResponse)
def product_manager_dashboard(
    request: Request,
    user: User = Depends(
        role_required(["product_manager"])
    )
):

    return templates.TemplateResponse(
        request=request,
        name="manager/product_manager.html",
        context={"user": user}
    )


@router.get("/executive", response_class=HTMLResponse)
def executive_dashboard(
    request: Request,
    user: User = Depends(
        role_required(["executive"])
    )
):

    return templates.TemplateResponse(
        request=request,
        name="manager/executive.html",
        context={"user": user}
    )

@router.get("/logout")
def logout():

    response = RedirectResponse(
        url="/login",
        status_code=302
    )

    response.delete_cookie("access_token")

    return response

