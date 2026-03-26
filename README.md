# Address Book FastAPI

## Setup

### 1. Clone the repository

bash command

git clone https://github.com/your-username/address-book-fastapi.git
cd address-book-fastapi

### 2. Create Virtual Env
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Run App
uvicorn app.main:app --reload

### 5. Open Browser
http://127.0.0.1:8000/docs

---

## Docker Run

docker build -t address-api .
docker run -p 8000:8000 address-api

---

## Features

1. Initial project structure
2. Database setup & accessing through ORM
3. Models added
4. SQLite database for saving addresses
5. Schemas with validation
6. CRUD operations
7. Distance logic
8. API routes v1
9. Logging implementation
10. Jinja frontend
11. Tests added
12. Docker support
13. README completed