from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db

from app.models.user import User
from app.models.customer import Customer
from app.models.opportunity import Opportunity
from app.models.sales_activity import SalesActivity

from app.routes.auth import role_required


router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/manager/dashboard", response_class=HTMLResponse)
def manager_dashboard(request: Request, db: Session = Depends(get_db), user: User = Depends(role_required(["sales_manager", "executive"]))):

    total_customers = db.query(Customer).count()

    total_opportunities = db.query(Opportunity).count()

    total_pipeline = db.query(func.sum(Opportunity.deal_value)).scalar() or 0

    won_deals = db.query(Opportunity).filter(Opportunity.stage == "Won").count()

    lost_deals = db.query(Opportunity).filter(Opportunity.stage == "Lost").count()

    completed_activities = db.query(SalesActivity).filter(SalesActivity.status == "completed").count()

    pending_activities = db.query(SalesActivity).filter(SalesActivity.status == "pending").count()

    sales_reps = db.query(User).filter(User.role == "sales_rep").all()

    rep_stats = []

    for rep in sales_reps:

        rep_pipeline = db.query(func.sum(Opportunity.deal_value)).filter(Opportunity.owner_id == rep.id).scalar() or 0

        rep_customers = db.query(Customer).filter(Customer.assigned_rep_id == rep.id).count()

        rep_stats.append({
            "name": rep.name,
            "pipeline": rep_pipeline,
            "customers": rep_customers
        })

    return templates.TemplateResponse(
        request=request,
        name="manager/manager_dashboard.html",
        context={
            "user": user,
            "total_customers": total_customers,
            "total_opportunities": total_opportunities,
            "total_pipeline": total_pipeline,
            "won_deals": won_deals,
            "lost_deals": lost_deals,
            "completed_activities": completed_activities,
            "pending_activities": pending_activities,
            "rep_stats": rep_stats
        }
    )