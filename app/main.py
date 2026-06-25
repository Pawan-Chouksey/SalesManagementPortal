from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi import Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine

from app.routes.auth import router as auth_router
from app.routes.customers import router as customer_router
from app.routes.sales_activity import router as sales_activity_router
from app.routes.opportunities import router as opportunity_router
from app.routes.manager import router as manager_router
from app.routes.auth import get_current_user

import app.models
from app.models.user import User
from app.models.customer import Customer
from app.models.customer_contact import CustomerContact
from app.models.customer_interaction import CustomerInteraction
from app.models.account_plan import AccountPlan
from app.models.renewal import Renewal
from app.models.sales_activity import SalesActivity
from app.models.opportunity import Opportunity
from app.models.user import User


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(auth_router)
app.include_router(customer_router)
app.include_router(sales_activity_router)
app.include_router(opportunity_router)
app.include_router(manager_router)


@app.get("/")
def home(user: User = Depends(get_current_user)):

    if not user:

        return RedirectResponse(
            url="/login",
            status_code=302
        )

    return RedirectResponse(
        url=f"/{user.role}",
        status_code=302
    )