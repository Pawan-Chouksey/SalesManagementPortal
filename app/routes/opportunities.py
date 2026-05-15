from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.opportunity import Opportunity
from app.models.customer import Customer
from app.models.user import User

from app.routes.auth import get_current_user


router = APIRouter(prefix="/opportunities",tags=["Opportunities"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def list_opportunities(request: Request,db: Session = Depends(get_db),user: User = Depends(get_current_user)):

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=302
        )

    opportunities = db.query(Opportunity).all()

    total_pipeline = sum(opp.deal_value for opp in opportunities)

    won_deals = [
        opp for opp in opportunities
        if opp.stage == "Won"
    ]

    lost_deals = [
        opp for opp in opportunities
        if opp.stage == "Lost"
    ]

    return templates.TemplateResponse(
        request=request,
        name="opportunities/list.html",
        context={
            "user": user,
            "opportunities": opportunities,
            "total_pipeline": total_pipeline,
            "won_count": len(won_deals),
            "lost_count": len(lost_deals)
        }
    )


@router.get("/create", response_class=HTMLResponse)
def create_opportunity_page(request: Request,db: Session = Depends(get_db),user: User = Depends(get_current_user)):

    customers = db.query(Customer).all()

    return templates.TemplateResponse(
        request=request,
        name="opportunities/create.html",
        context={
            "request": request,
            "customers": customers,
            "user": user
        }
    )


@router.post("/create")
def create_opportunity(
    customer_id: int = Form(...),
    title: str = Form(...),
    deal_value: float = Form(...),
    stage: str = Form(...),
    probability: int = Form(...),
    expected_close_date: str = Form(None),
    competitor_name: str = Form(None),

    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    opportunity = Opportunity(
        customer_id=customer_id,
        owner_id=user.id,
        title=title,
        deal_value=deal_value,
        stage=stage,
        probability=probability,
        competitor_name=competitor_name
    )

    if expected_close_date:
        opportunity.expected_close_date = (
            datetime.fromisoformat(
                expected_close_date
            ).date()
        )

    db.add(opportunity)

    db.commit()

    return RedirectResponse(
        url="/opportunities",
        status_code=302
    )


@router.post("/{opportunity_id}/stage")
def update_stage(opportunity_id: int,stage: str = Form(...),loss_reason: str = Form(None),db: Session = Depends(get_db),user: User = Depends(get_current_user)):

    opportunity = db.query(Opportunity).filter(
        Opportunity.id == opportunity_id
    ).first()

    if not opportunity:
        raise HTTPException(
            status_code=404,
            detail="Opportunity not found"
        )

    opportunity.stage = stage

    if stage == "Lost":
        opportunity.loss_reason = loss_reason

    db.commit()

    return RedirectResponse(
        url="/opportunities",
        status_code=302
    )


@router.post("/{opportunity_id}/delete")
def delete_opportunity(opportunity_id: int,db: Session = Depends(get_db),user: User = Depends(get_current_user)):

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=302
        )

    opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()

    if not opportunity:
        raise HTTPException(
            status_code=404,
            detail="Opportunity not found"
        )

    db.delete(opportunity)

    db.commit()

    return RedirectResponse(
        url="/opportunities",
        status_code=302
    )
