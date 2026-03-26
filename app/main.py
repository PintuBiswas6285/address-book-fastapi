# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
import os
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from app.database import Base, engine
from app.api.v1.routes import router


# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Address Book API")

# Jinja templates setup
#templates = Jinja2Templates(directory="app/templates")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "templates"))

# Include API routes
app.include_router(router)

