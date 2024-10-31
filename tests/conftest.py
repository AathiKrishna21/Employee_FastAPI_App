from fastapi.testclient import TestClient
from bson import ObjectId
import pytest
from restapi import db
import mongomock
from main import app

mock_client = mongomock.MongoClient()

@pytest.fixture
def client():
    # Create a new instance of TestClient for each test
    with TestClient(app) as client:
        yield client

# Override the MongoClient in your app
@pytest.fixture(scope="module")
def mock_db():
    app.dependency_overrides[db.MongoDB.get_db] = lambda: mock_client['employees']
    yield
    del app.dependency_overrides[db.MongoDB.get_db]

sample_employee_data = [
    {
        "_id": ObjectId("6722785c3e5999f4fcc0aefa"),
        "name": f"Akash",
        "role": "Analyst",
        "department": "Sales",
        "email": f"akash@example.com",
        "date_joined": "2024-10-29T07:02:10.331122"
    },
    {
        "_id": ObjectId("6722785c3e5999f4fcc0aefb"),
        "name": f"Abisek",
        "role": "Developer",
        "department": "Engineering",
        "email": f"abisek@example.com",
        "date_joined": "2024-10-29T07:02:10.331122"
    },
    {
        "_id": ObjectId("6722785c3e5999f4fcc0aefc"),
        "name": f"Arun",
        "role": "Manager",
        "department": "HR",
        "email": f"arun@example.com",
        "date_joined": "2024-10-29T07:02:10.331122"
    }
]

@pytest.fixture(scope="module", autouse=True)
def setup_database(mock_db):
    db = mock_client["employees"]
    db.employees.insert_many(sample_employee_data)
    users = [
        {"uname": "admin_user", "is_admin": True, "email": "admin@example.com"},
        {"uname": "regular_user", "is_admin": False, "email": "user@example.com"}
    ]
    db.users.insert_many(users)

    yield  # This will run the test
    # Clear again after the test
    db.employees.delete_many({})
    db.users.delete_many({})