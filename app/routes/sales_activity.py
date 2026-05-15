from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import Request
from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse

from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.sales_activity import SalesActivity
from app.models.customer import Customer
from app.models.user import User

from app.routes.auth import get_current_user


router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/activities", response_class=HTMLResponse)
def activities_page(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=302
        )

    activities = db.query(SalesActivity).filter(
        SalesActivity.user_id == user.id
    ).order_by(
        SalesActivity.follow_up_date.asc()
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="activities/activities.html",
        context={
            "user": user,
            "activities": activities
        }
    )


@router.get("/activities/new", response_class=HTMLResponse)
def create_activity_page(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    customers = db.query(Customer).all()

    return templates.TemplateResponse(
        request=request,
        name="activities/create_activity.html",
        context={
            "request": request,
            "customers": customers,
            "user": user
        }
    )


@router.post("/activities/new")
def create_activity(
    customer_id: int = Form(...),
    activity_type: str = Form(...),
    title: str = Form(...),
    notes: str = Form(...),
    follow_up_date: str = Form(None),

    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    activity = SalesActivity(
        user_id=user.id,
        customer_id=customer_id,
        activity_type=activity_type,
        title=title,
        notes=notes,
        status="pending"
    )

    if follow_up_date:
        activity.follow_up_date = datetime.fromisoformat(
            follow_up_date
        )

    db.add(activity)

    db.commit()

    return RedirectResponse(
        url="/activities",
        status_code=302
    )

@router.get("/activities/{activity_id}", response_class=HTMLResponse)
def activity_detail(
    activity_id: int,
    request: Request,

    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=302
        )

    activity = db.query(SalesActivity).filter(
        SalesActivity.id == activity_id
    ).first()

    if not activity:
        raise HTTPException(
            status_code=404,
            detail="Activity not found"
        )

    return templates.TemplateResponse(
        request=request,
        name="activities/activity_detail.html",
        context={
            "request": request,
            "user": user,
            "activity": activity
        }
    )

@router.post("/activities/{activity_id}/status")
def update_activity_status(
    activity_id: int,
    status: str = Form(...),

    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    activity = db.query(SalesActivity).filter(
        SalesActivity.id == activity_id
    ).first()

    if not activity:
        raise HTTPException(
            status_code=404,
            detail="Activity not found"
        )

    activity.status = status

    db.commit()

    return RedirectResponse(
        url=f"/activities/{activity_id}",
        status_code=302
    )