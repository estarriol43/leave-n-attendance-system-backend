from fastapi import FastAPI
from app.routes import auth, leave, attendance
from app.database import engine, Base


app = FastAPI()

# Include routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(leave.router, prefix="/leave", tags=["leave"])
app.include_router(attendance.router, prefix="/attendance", tags=["attendance"])

# Create database tables
@app.on_event("startup")
def create_tables():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Leave and Attendance Management System"}
