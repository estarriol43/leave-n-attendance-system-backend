from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    email: str 
    password: str

class DepartmentOut(BaseModel):
    id: int
    name: str
class UserOut(BaseModel):
    id: int
    employee_id: str
    first_name: str
    last_name: str
    email: str
    department: DepartmentOut
    position: str
    is_manager: bool

class TokenResponse(BaseModel):
    token: str
    user: UserOut

class UserRegister(BaseModel):
    employee_id: str
    first_name: str
    last_name: str
    email: str 
    password: str
    department_id: int
    postiion: str
    manager_id: int
    is_manager: bool
    annual_leave_quota: int
    sick_leave_quota: int
    personal_leav_quota: int
    public_holiday_quota: int
