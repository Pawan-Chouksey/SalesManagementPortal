from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.database import Base, engine
from app.routes.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)


@app.get("/", response_class=HTMLResponse)
def home():

    return """
    <h1>Sales Management Portal</h1>

    <a href="/login">
        Go To Login
    </a>
    """