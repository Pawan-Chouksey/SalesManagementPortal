from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.customer import Customer
from app.models.user import User
from app.models.customer_contact import CustomerContact
from app.models.customer_interaction import CustomerInteraction
from app.models.renewal import Renewal
from app.models.account_plan import AccountPlan

from app.routes.auth import get_current_user

router = APIRouter(prefix="/customers", tags=["Customers"])

templates = Jinja2Templates(directory="app/templates")
@router.get("/", response_class=HTMLResponse)
def list_customers(request: Request, db: Session = Depends(get_db),user: User = Depends(get_current_user)):

    if not user:
        return RedirectResponse(url="/login", status_code=302)

    customers = db.query(Customer).all()

    return templates.TemplateResponse(
        request=request,
        name="customers/list.html",
        context={
            "user": user,
            "customers": customers
        }
    )
@router.get("/create", response_class=HTMLResponse)
def create_customer_page(request: Request,user: User = Depends(get_current_user)):

    if not user:
        return RedirectResponse(url="/login", status_code=302)

    return templates.TemplateResponse(
        request=request,
        name="customers/create.html",
        context={"user": user}
    )
@router.post("/create")
def create_customer(company_name: str = Form(...), address: str = Form(None), website: str = Form(None), db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    if not user:
        return RedirectResponse(url="/login", status_code=302)

    customer = Customer(company_name=company_name, address=address, website=website, assigned_rep_id=user.id)

    db.add(customer)

    db.commit()

    return RedirectResponse(
        url="/customers",
        status_code=302
    )
@router.get("/{customer_id}", response_class=HTMLResponse)
def customer_detail(customer_id: int, request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user) ):

    if not user:
        return RedirectResponse(url="/login", status_code=302)

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return templates.TemplateResponse(
        request=request,
        name="customers/detail.html",
        context={
            "user": user,
            "customer": customer
        }
    )
@router.get("/{customer_id}/edit", response_class=HTMLResponse)
def edit_customer_page(customer_id: int, request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    if not user:
        return RedirectResponse(url="/login", status_code=302)

    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return templates.TemplateResponse(
        request=request,
        name="customers/edit.html",
        context={
            "user": user,
            "customer": customer
        }
    )
@router.post("/{customer_id}/edit")
def update_customer(customer_id: int, company_name: str = Form(...), address: str = Form(None), website: str = Form(None), db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    if not user:
        return RedirectResponse(url="/login", status_code=302)

    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    customer.company_name = company_name
    customer.address = address
    customer.website = website

    db.commit()

    return RedirectResponse(
        url="/customers",
        status_code=302
    )
@router.post("/{customer_id}/delete")
def delete_customer(customer_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    if not user:
        return RedirectResponse(url="/login", status_code=302)

    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    db.delete(customer)

    db.commit()

    return RedirectResponse(
        url="/customers",
        status_code=302
    )
@router.post("/{customer_id}/contacts/add")
def add_contact(customer_id: int, name: str = Form(...), designation: str = Form(None), email: str = Form(None), phone: str = Form(None), db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=302
        )

    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    contact = CustomerContact(customer_id=customer.id, name=name, designation=designation, email=email, phone=phone )

    db.add(contact)

    db.commit()

    return RedirectResponse(
        url=f"/customers/{customer_id}",
        status_code=302
    )
@router.post("/{customer_id}/interactions/add")
def add_interaction(customer_id: int, interaction_type: str = Form(...), notes: str = Form(None), db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=302
        )

    customer = db.query(Customer).filter(Customer.id == customer_id ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    interaction = CustomerInteraction(customer_id=customer.id, user_id=user.id, interaction_type=interaction_type, notes=notes )

    db.add(interaction)

    db.commit()

    return RedirectResponse(
        url=f"/customers/{customer_id}",
        status_code=302
    )
@router.post("/{customer_id}/renewals/add")
def add_renewal(customer_id: int, contract_start: str = Form(None), contract_end: str = Form(None), renewal_status: str = Form(...), reminder_date: str = Form(None), db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=302
        )

    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    renewal = Renewal(
        customer_id=customer.id,
        contract_start=contract_start if contract_start else None,
        contract_end=contract_end if contract_end else None,
        renewal_status=renewal_status,
        reminder_date=reminder_date if reminder_date else None
    )

    db.add(renewal)

    db.commit()

    return RedirectResponse(
        url=f"/customers/{customer_id}",
        status_code=302
    )
@router.post("/{customer_id}/account-plans/add")
def add_account_plan(customer_id: int, goals: str = Form(None), renewal_value: int = Form(None), db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=302
        )

    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    account_plan = AccountPlan(customer_id=customer.id, goals=goals, renewal_value=renewal_value )

    db.add(account_plan)

    db.commit()

    return RedirectResponse(
        url=f"/customers/{customer_id}",
        status_code=302
    )