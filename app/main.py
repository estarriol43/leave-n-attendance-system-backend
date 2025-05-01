from fastapi import FastAPI
from app.database import engine, Base
from .routes import auth


app = FastAPI()

app.include_router(auth.router)

# Create database tables
@app.on_event("startup")
def create_tables():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Leave and Attendance Management System"}
