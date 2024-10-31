from restapi import authentication
from schemas import user_schema
from main import app

def test_update_employee_without_authentication(client):
    app.dependency_overrides[user_schema.get_user] = lambda: {}
    response = client.put("/api/employees/6722785c3e5999f4fcc0aefc", json={
        "name": "John Doe",
        "role": "Analyst",
        "department": "Engineering",
        "email": "john@example.com"
    }, headers={
        "accept": "application/json",
        "Content-Type": "application/json",
        "Cache-Control": "no-cache"
        })
    assert response.status_code == 401
    assert '{"detail":"Not authenticated"}' == response.text

def test_update_employee_without_admin(client):
    app.dependency_overrides[authentication.get_current_user] = lambda: {"uname": "regular_user", "is_admin": False}
    response = client.put("/api/employees/6722785c3e5999f4fcc0aefc", json={
        "name": "John Doe",
        "role": "Analyst",
        "department": "Engineering",
        "email": "john@example.com"
    }, headers={
        "accept": "application/json",
        "Content-Type": "application/json",
        "Cache-Control": "no-cache"
        })
    assert response.status_code == 403
    assert response.text == '{"detail":"Operation not permitted!, Need Admin permission for this."}'

def test_update_employee_with_admin(client):
    app.dependency_overrides[authentication.get_current_user] = lambda: {"uname": "admin_user", "is_admin": True}
    response = client.put(
        "/api/employees/6722785c3e5999f4fcc0aefc",
        json={
            "name": "John Doe",
            "role": "Analyst",
            "department": "Engineering",
            "email": "john@example.com"
            },
        headers={
        "accept": "application/json",
        "Content-Type": "application/json",
        "Cache-Control": "no-cache"
        })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"

def test_update_employee_email_duplication(client):
    app.dependency_overrides[authentication.get_current_user] = lambda: {"uname": "admin_user", "is_admin": True}
    response = client.put("/api/employees/6722785c3e5999f4fcc0aefc", json={
        "name": "John Doe",
        "role": "Analyst",
        "department": "Engineering",
        "email": "john@example.com"
    }, headers={
        "accept": "application/json",
        "Content-Type": "application/json",
        "Cache-Control": "no-cache"
        })
    assert response.status_code == 400
    assert response.text == '{"detail":"Email already registered"}'

def test_update_employee_empty_name(client):
    app.dependency_overrides[authentication.get_current_user] = lambda: {"uname": "admin_user", "is_admin": True}
    response = client.put("/api/employees/6722785c3e5999f4fcc0aefc", json={
        "name": " ",
        "role": "Analyst",
        "department": "Engineering",
        "email": "john2@example.com"
    }, headers={
        "accept": "application/json",
        "Content-Type": "application/json",
        "Cache-Control": "no-cache"
        })
    assert response.status_code == 400
    assert response.text == '{"detail":"Name should not be Empty!"}'

def test_update_employee_with_admin_no_body(client):
    app.dependency_overrides[authentication.get_current_user] = lambda: {"uname": "admin_user", "is_admin": True}
    response = client.put(
        "/api/employees/6722785c3e5999f4fcc0aefd",
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
            "Cache-Control": "no-cache"
        })
    assert response.status_code == 400
    assert response.text == '{"detail":[{"type":"missing","loc":["body"],"msg":"Field required","input":null}]}'

def test_update_employee_with_admin_no_emp(client):
    app.dependency_overrides[authentication.get_current_user] = lambda: {"uname": "admin_user", "is_admin": True}
    response = client.put(
        "/api/employees/6722785c3e5999f4fcc0aefd",
        json={
            "name": " ",
            "role": "Analyst",
            "department": "Engineering",
            "email": "john2@example.com"
        },
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
            "Cache-Control": "no-cache"
        })
    assert response.status_code == 404
    assert response.text == '{"detail":"Employee with this ID not found"}'
    
    