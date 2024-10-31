from restapi import authentication
from schemas import user_schema
from main import app

def test_create_employee_without_authentication(client):
    app.dependency_overrides[user_schema.get_user] = lambda: {}
    response = client.post("/api/employees", json={
        "name": "John Doe",
        "role": "Analyst",
        "department": "Engineering",
        "email": "john@example.com"
    }, headers={"Cache-Control": "no-cache"})
    assert response.status_code == 401
    assert '{"detail":"Not authenticated"}' == response.text

def test_create_employee_without_admin(client):
    app.dependency_overrides[authentication.get_current_user] = lambda: {"uname": "regular_user", "is_admin": False}
    response = client.post("/api/employees", json={
        "name": "John Doe",
        "role": "Analyst",
        "department": "Engineering",
        "email": "john@example.com"
    }, headers={"Cache-Control": "no-cache"})
    assert response.status_code == 403
    assert response.text == '{"detail":"Operation not permitted!, Need Admin permission for this."}'

def test_create_employee_with_admin(client):
    app.dependency_overrides[authentication.get_current_user] = lambda: {"uname": "admin_user", "is_admin": True}
    response = client.post(
        "/api/employees",
        json={
            "name": "John Doe",
            "role": "Analyst",
            "department": "Engineering",
            "email": "john@example.com"
            },
        headers={"Cache-Control": "no-cache"}
        )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"

def test_create_employee_email_duplication(client):
    app.dependency_overrides[authentication.get_current_user] = lambda: {"uname": "admin_user", "is_admin": True}
    response = client.post("/api/employees", json={
        "name": "John Doe",
        "role": "Analyst",
        "department": "Engineering",
        "email": "john@example.com"
    }, headers={"Cache-Control": "no-cache"})
    assert response.status_code == 400
    assert response.text == '{"detail":"Email already registered"}'

def test_create_employee_empty_name(client):
    app.dependency_overrides[authentication.get_current_user] = lambda: {"uname": "admin_user", "is_admin": True}
    response = client.post("/api/employees", json={
        "name": " ",
        "role": "Analyst",
        "department": "Engineering",
        "email": "john2@example.com"
    }, headers={"Cache-Control": "no-cache"})
    assert response.status_code == 400
    assert response.text == '{"detail":"Name should not be Empty!"}'
    