# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database import Base, engine
from app.api.v1.routes import router


# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Address Book API")

# Jinja templates setup
templates = Jinja2Templates(directory="app/templates")


# Include API routes
app.include_router(router)

# Home page (basic UI)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # You don't actually need to define a context dict if it only contains the request
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={}  # Add other variables here if needed
    )