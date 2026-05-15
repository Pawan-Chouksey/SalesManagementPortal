from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.database import Base, engine

from app.routes.auth import router as auth_router
from app.routes.customers import router as customer_router
from app.routes.sales_activity import router as sales_activity_router


from app.models.user import User
from app.models.customer import Customer
from app.models.customer_contact import CustomerContact
from app.models.customer_interaction import CustomerInteraction
from app.models.account_plan import AccountPlan
from app.models.renewal import Renewal
from app.models.sales_activity import SalesActivity


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(customer_router)
app.include_router(sales_activity_router)



@app.get("/", response_class=HTMLResponse)
def home():

    return """
    <h1>Sales Management Portal</h1>

    <a href="/login">
        Go To Login
    </a>
    """