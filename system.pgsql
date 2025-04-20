    +-------------------------+
    |     Frontend (UI)       |
    |  (Next.js or React)     |
    +-------------------------+
              |
              | HTTP Requests (API Calls)
              v
   +---------------------------+
   |    API Layer (FastAPI)    | <---+--------------+
   |  (Authentication, Business|     |              |
   |   Logic, CRUD Operations) |     |              |
   +---------------------------+     v              v
              |                +------------------+    +------------------+
              | SQLAlchemy ORM |   Leave Service  |    | Attendance       |
              v                | (Leave Requests, |    | Service (Check-  |
      +--------------------+   | Leave Balance)   |    | in/out Tracking) |
      |  PostgreSQL DB      |   +------------------+    +------------------+
      | (Cloud SQL on GCP)  |
      +--------------------+
              |
              v
      +--------------------+
      | Google Cloud SQL   |
      |  (Managed DB)      |
      +--------------------+
              |
              v
      +--------------------+
      | Google Cloud Load  |
      | Balancer (GAE)     |
      +--------------------+
              |
              v
       +-------------------+
       | Google App Engine |
       | (FastAPI Deployed)|
       +-------------------+
