from fastapi import FastAPI, Request
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
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})