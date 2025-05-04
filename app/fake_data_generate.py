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
from werkzeug.security import generate_password_hash # hash後密碼字數會爆炸，先暫時不用
import random
from datetime import datetime, timedelta

from database import SessionLocal

fake = Faker()

def generate_fake_departments(db: Session, num_departments: int = 5):
    print("Generating fake departments...")
    for _ in range(num_departments):
        department = Department(
            name=fake.company(),
        )
        db.add(department)
    db.commit()

def generate_fake_users(db: Session, num_users: int = 20):
    print("Generating fake users...")
    departments = db.query(Department).all()
    if not departments:
        raise ValueError("Departments must be generated before users.")
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
            password_hash='test',
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
    print("Generating fake leave types...")
    for _ in range(num_leave_types):
        leave_type = LeaveType(
            name=fake.word(),
            color_code=fake.color(),
        )
        db.add(leave_type)
    db.commit()

def generate_fake_leave_quotas(db: Session, num_quotas: int = 30):
    print("Generating fake leave quotas...")
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
    print("Generating fake leave requests...")
    users = db.query(User).all()
    leave_types = db.query(LeaveType).all()

    if not users or not leave_types:
        raise ValueError("請先建立使用者與假期類型資料")

    for _ in range(num_requests):
        status = random.choice(list(LeaveStatus))
        user = fake.random_element(elements=users)
        leave_type = fake.random_element(elements=leave_types)

        # start_date < end_date
        start_date = fake.date_between(start_date='-30d', end_date='today')
        end_date = start_date + timedelta(days=random.randint(1, 5))

        leave_request = LeaveRequest(
            request_id=f"REQ{datetime.now().strftime('%Y%m%d')}{fake.unique.random_int(min=1000, max=9999)}",
            user_id=user.id,
            leave_type_id=leave_type.id,
            start_date=start_date,
            end_date=end_date,
            reason=fake.text(),
            status=status,
            days_count=(end_date - start_date).days + 1,
            approved_at=datetime.now() if status == LeaveStatus.approved else None,
            rejection_reason=fake.sentence() if status == LeaveStatus.rejected else None,
        )
        db.add(leave_request)

    db.commit()

def generate_fake_notifications(db: Session, num_notifications: int = 20):
    print("Generating fake notifications...")
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

def generate_fake_leave_request_attachments(db: Session, num_attachments: int = 20):
    print("Generating fake leave request attachments...")
    leave_requests = db.query(LeaveRequest).all()

    if not leave_requests:
        raise ValueError("cannot generate attachments without leave requests")

    file_extensions = ['pdf', 'jpg', 'png', 'docx']

    for _ in range(num_attachments):
        lr = fake.random_element(elements=leave_requests)
        ext = fake.random_element(elements=file_extensions)
        attachment = LeaveRequestAttachment(
            leave_request_id=lr.id,
            file_name=f"{fake.word()}.{ext}",
            file_type=ext,
            file_size=fake.random_int(min=100, max=2048),  # 單位：KB
        )
        db.add(attachment)

    db.commit()


def init_db():
    """Initialize the database with fake data."""
    db = SessionLocal()
    try:
        generate_fake_departments(db)
        generate_fake_users(db)
        generate_fake_leave_types(db)
        generate_fake_leave_quotas(db)
        generate_fake_leave_requests(db)
        generate_fake_notifications(db)
        generate_fake_leave_request_attachments(db)
        print("Fake data generation completed successfully.")
        
    except Exception as e:
        print(f"Error generating fake data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()