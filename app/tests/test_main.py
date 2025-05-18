from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def login_as(username: str, password: str):
    response = client.post("/api/auth/login", json={"username": username, "password": password})
    assert response.status_code == 200
    # 取得 cookie
    cookies = response.cookies
    return cookies

def test_get_my_profile():
    # login as user id: 19
    cookie = login_as("jessicavalentine@example.org", "test")
    response = client.get("/api/users/me", cookies=cookie)
    assert response.status_code == 200
    assert response.json() == {
        "id": 19,
        "employee_id": "EMP166",
        "first_name": "Scott",
        "last_name": "Burton",
        "email": "jessicavalentine@example.org",
        "department": {
            "id": 6,
            "name": "Scott, Castillo and Mccann"
        },
        "position": "Hydrogeologist",
        "is_manager": True,
        "manager": None,
        "hire_date": "2023-02-04"
    }
