# Leave and attendance backend system
## Overview
This project provides the backend for the **Leave and Attendance Management System**. The system is built using **FastAPI** and is designed to manage employee attendance, leave requests, and provide an API interface for frontend applications to interact with.

The backend is modular, scalable, and follows clean architecture principles to separate concerns effectively. It is containerized using **Docker** and deployed on **Google Cloud Platform (GCP)** using **Google App Engine (GAE)**.

## Tech Stack
- **FastAPI**: Python web framework for building APIs.
- **SQLAlchemy**: ORM for database operations.
- **PostgreSQL**: Relational database to store leave, attendance, and user data.
- **Uvicorn**: ASGI server to run the FastAPI application.
- **Pydantic**: Data validation for API requests.
- **Docker**: Containerization for easier deployment.
- **Google Cloud Platform (GCP)**: For deployment (App Engine).
- **Alembic**: For database migrations.

## Prerequisites
Before you begin, ensure you have the following installed on your system:
- **Python 3.7+**
- **Docker** (optional, for containerization)
- **PostgreSQL** (or Cloud SQL for GCP database management)
- **Google Cloud SDK** (for deployment to GCP)
- **Git** (to clone the repository)

## Setting Up the Development Environment

- Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/leave-attendance-backend.git
cd leave-attendance-backend
```

- Set up the Virtual Environment
```
python -m venv venv
source venv/bin/activate # mac/linux
venv\Scripts\activate # windows
```

- Install Dependencies
```
pip install -r requirements.txt
```

- Create Environment Variables
Create a `.env` file in the root directory of the project to store environment-specific variables like the database URL and secret keys.
```
DATABASE_URL=postgresql://username:password@localhost:5432/leave_attendance
JWT_SECRET=your-secret-key
```

- Run the Application Locally
```
uvicorn app.main:app --reload
```


## Folder Structure

``` 
leave-attendance-backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py                     # Entry point of FastAPI app
│   ├── models/                      # Database models
│   │   ├── user.py
│   │   ├── leave.py
│   │   └── attendance.py
│   ├── schemas/                     # Pydantic models (data validation)
│   │   ├── user.py
│   │   ├── leave.py
│   │   └── attendance.py
│   ├── crud/                        # CRUD operations for interacting with DB
│   │   ├── user.py
│   │   ├── leave.py
│   │   └── attendance.py
│   ├── dependencies/                # Dependency injection (for DB session)
│   │   └── db.py
│   ├── routes/                      # API route definitions
│   │   ├── auth.py
│   │   ├── leave.py
│   │   └── attendance.py
│   ├── services/                    # Business logic
│   │   ├── auth.py
│   │   ├── leave.py
│   │   └── attendance.py
│   ├── config.py                    # Configuration (DB, JWT, etc.)
│   └── .env                         # Environment variables
├── alembic.ini                      # Alembic configuration
├── migrations/                      # Database migrations
├── requirements.txt                 # Project dependencies
└── Dockerfile                       # Docker configuration for deployment

```