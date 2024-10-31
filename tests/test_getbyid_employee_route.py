from fastapi import HTTPException
from restapi import authentication
from schemas import user_schema
# from fixture import common_fixture
from main import app

def test_getbyid_employee_without_authentication(client):
    app.dependency_overrides[user_schema.get_user] = lambda: {}
    response = client.get("/api/employees/6722785c3e5999f4fcc0aefc", headers={"Cache-Control": "no-cache"})
    assert response.status_code == 401
    assert '{"detail":"Not authenticated"}' == response.text

def test_getbyid_employee_without_admin(client):
    app.dependency_overrides[authentication.get_current_user] = lambda: {"uname": "regular_user", "is_admin": False}
    response = client.get("/api/employees/6722785c3e5999f4fcc0aefc", headers={"Cache-Control": "no-cache"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Arun"

def test_getbyid_employee_with_admin(client):
    app.dependency_overrides[authentication.get_current_user] = lambda: {"uname": "admin_user", "is_admin": True}
    response = client.get(
        "/api/employees/6722785c3e5999f4fcc0aefc",
        headers={"Cache-Control": "no-cache"}
        )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Arun"

def test_getbyid_employee_with_admin_no_emp(client):
    app.dependency_overrides[authentication.get_current_user] = lambda: {"uname": "admin_user", "is_admin": True}
    response = client.get(
        "/api/employees/6722785c3e5999f4fcc0aefd",
        headers={"Cache-Control": "no-cache"}
        )
    assert response.status_code == 404
    assert response.text == '{"detail":"Employee with this ID not found"}'
    