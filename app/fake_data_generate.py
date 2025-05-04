from faker import Faker
from sqlalchemy.orm import Session
from models.user import User
from models.leave_quota import LeaveQuota
from models.leave_request import LeaveRequest, LeaveStatus
from models.leave_type import LeaveType
from models.department import Department
from models.notification import Notification
from models.leave_request_attachment import LeaveRequestAttachment
from models.manager import Manager
from werkzeug.security import generate_password_hash

from database import SessionLocal

fake = Faker()

def generate_fake_departments(db: Session, num_departments: int = 5):
    for _ in range(num_departments):
        department = Department(
            name=fake.company(),
        )
        db.add(department)
    db.commit()

def generate_fake_users(db: Session, num_users: int = 20):
    departments = db.query(Department).all()
    users = []  # 儲存所有生成的使用者
    for _ in range(num_users):
        user = User(
            employee_id=f"EMP{fake.unique.random_number(digits=3)}",
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            department_id=fake.random_element(elements=departments).id,
            position=fake.job(),
            hire_date=fake.date_this_decade(),
            is_manager=fake.boolean(),
            password_hash=generate_password_hash('password123'),
        )
        db.add(user)
        users.append(user)
    
    db.commit()

    # 設置上司與下屬關係
    for user in users:
        if user.is_manager:  # 隨機選擇下屬
            subordinates = fake.random_elements(elements=users, length=fake.random_int(1, 5))
            for subordinate in subordinates:
                manager_entry = Manager(user_id=subordinate.id, manager_id=user.id)
                db.add(manager_entry)

    db.commit()

def generate_fake_leave_types(db: Session, num_leave_types: int = 5):
    for _ in range(num_leave_types):
        leave_type = LeaveType(
            name=fake.word(),
            color_code=fake.color(),
        )
        db.add(leave_type)
    db.commit()

def generate_fake_leave_quotas(db: Session, num_quotas: int = 30):
    users = db.query(User).all()
    leave_types = db.query(LeaveType).all()
    for _ in range(num_quotas):
        leave_quota = LeaveQuota(
            user_id=fake.random_element(elements=users).id,
            leave_type_id=fake.random_element(elements=leave_types).id,
            year=fake.year(),
            quota=fake.random_int(min=10, max=30),
        )
        db.add(leave_quota)
    db.commit()

def generate_fake_leave_requests(db: Session, num_requests: int = 20):
    users = db.query(User).all()
    leave_types = db.query(LeaveType).all()
    for _ in range(num_requests):
        leave_request = LeaveRequest(
            user_id=fake.random_element(elements=users).id,
            leave_type_id=fake.random_element(elements=leave_types).id,
            start_date=fake.date_this_year(),
            end_date=fake.date_this_year(),
            reason=fake.text(),
            status=fake.random_choice(elements=["Pending", "Approved", "Rejected"]),
        )
        db.add(leave_request)
    db.commit()

def generate_fake_notifications(db: Session, num_notifications: int = 20):
    users = db.query(User).all()
    for _ in range(num_notifications):
        notification = Notification(
            user_id=fake.random_element(elements=users).id,
            title=fake.sentence(),
            message=fake.text(),
            related_to=fake.word(),
            related_id=fake.random_int(),
            is_read=fake.boolean(),
        )
        db.add(notification)
    db.commit()

def init_db():
    """Initialize the database with fake data."""
    db = SessionLocal()
    try:
        generate_fake_departments(db)
        # generate_fake_users(db)
        # generate_fake_leave_types(db)
        # generate_fake_leave_quotas(db)
        # generate_fake_leave_requests(db)
        # generate_fake_notifications(db)
    except Exception as e:
        print(f"Error generating fake data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()