from fastapi import FastAPI
from app.routes import auth, leave, attendance

app = FastAPI()

# Include routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(leave.router, prefix="/leave", tags=["leave"])
app.include_router(attendance.router, prefix="/attendance", tags=["attendance"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Leave and Attendance Management System"}
