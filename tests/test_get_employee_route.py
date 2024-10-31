from fastapi.testclient import TestClient
from restapi import db
import mongomock
from bson import ObjectId
import pytest
import random
from main import app

client = TestClient(app)

mock_client = mongomock.MongoClient()

@pytest.fixture(scope="module")
def mock_db():
    app.dependency_overrides[db.MongoDB.get_db] = lambda: mock_client['employees']
    yield
    del app.dependency_overrides[db.MongoDB.get_db]

sample_employee_data = [
    {
        "name": f"Employee {i}",
        "role": random.choice(["Analyst", "Manager", "Developer"]),
        "department": random.choice(["Engineering", "Sales", "HR"]),
        "email": f"employee{i}@example.com"
    }
    for i in range(1, 16)
]

@pytest.fixture(scope="module", autouse=True)
def setup_database(mock_db):
    db = mock_client["employees"]
    for employee in sample_employee_data:
        employee_doc = {
            "_id": ObjectId(),
            **employee,
            "date_joined": "2023-01-01T00:00:00"
        }
        db.employees.insert_one(employee_doc)


def test_get_employee_no_params():
    response = client.get("/api/employees")
    assert response.status_code == 200

def test_get_employees_sort_by_alphabetical():
    response = client.get("/api/employees?sort_by=name")
    assert response.status_code == 200
    employees = response.json()
    assert len(employees) > 0
    assert sorted(employees, key=lambda x: x['name']) == employees

def test_get_employees_per_page():
    response = client.get("api/employees/?per_page=1")
    assert response.status_code == 200
    employees = response.json()
    assert len(employees) == 1

def test_get_employees_page():
    response = client.get("/api/employees?page=3&per_page=1")
    assert response.status_code == 200
    employees = response.json()
    assert len(employees) == 1


def test_get_employees_sort_by_email_desc():
    response = client.get("/api/employees?sort_by=email&sort_order=desc")
    assert response.status_code == 200
    employees = response.json()
    assert len(employees) > 0
    assert sorted(employees, key=lambda x: x['email'], reverse=True) == employees

def test_get_employees_sort_by_name():
    response = client.get("/api/employees?sort_by=name")
    assert response.status_code == 200
    employees = response.json()
    assert len(employees) > 0
    assert sorted(employees, key=lambda x: x['name']) == employees

def test_get_employees_filter_by_department():
    response = client.get("/api/employees?department=HR")
    assert response.status_code == 200
    employees = response.json()
    assert len(employees) > 0
    assert all([c['department'] == 'HR' for c in employees])

def test_get_employees_filter_by_role():
    response = client.get("/api/employees?role=Manager")
    assert response.status_code == 200
    employees = response.json()
    assert len(employees) > 0
    assert all([c['role'] == 'Manager' for c in employees])

def test_get_employees_filter_by_domain_and_sort_by_alphabetical():
    response = client.get("/api/employees?department=Sales&sort_by=email")
    assert response.status_code == 200
    employees = response.json()
    assert len(employees) > 0
    assert all([c['department'] == 'Sales' for c in employees])
    assert sorted(employees, key=lambda x: x['email']) == employees

def test_get_employees_filter_by_domain_and_sort_by_date():
    response = client.get("/api/employees?role=Developer&sort_by=name&sort_order=desc")
    assert response.status_code == 200
    employees = response.json()
    assert len(employees) > 0
    assert all([c['role'] == 'Developer' for c in employees])
    assert sorted(employees, key=lambda x: x['name'], reverse=True) == employees