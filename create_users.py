from app.database import SessionLocal

from app.models.user import User
from app.models.customer import Customer
from app.models.customer_contact import CustomerContact
from app.models.customer_interaction import CustomerInteraction
from app.models.account_plan import AccountPlan
from app.models.renewal import Renewal

from app.utils.auth import hash_password

db = SessionLocal()

users = [
    {
        "name": "Sales Representative",
        "email": "salesrep@test.com",
        "password": "1234",
        "role": "sales_rep"
    },
    {
        "name": "Sales Manager",
        "email": "salesmanager@test.com",
        "password": "1234",
        "role": "sales_manager"
    },
    {
        "name": "Account Manager",
        "email": "accountmanager@test.com",
        "password": "1234",
        "role": "account_manager"
    },
    {
        "name": "Marketing",
        "email": "marketing@test.com",
        "password": "1234",
        "role": "marketing"
    },
    {
        "name": "Product Manager",
        "email": "productmanager@test.com",
        "password": "1234",
        "role": "product_manager"
    },
    {
        "name": "Executive",
        "email": "executive@test.com",
        "password": "1234",
        "role": "executive"
    }
]

for user_data in users:

    existing_user = db.query(User).filter(
        User.email == user_data["email"]
    ).first()

    if not existing_user:

        user = User(
            name = user_data["name"],
            email = user_data["email"],
            password = hash_password(user_data["password"]),
            role = user_data["role"]
        )

        db.add(user)

db.commit()

print("Users created successfully")