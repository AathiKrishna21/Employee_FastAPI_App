from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum


class Role(str, Enum):
    analyst = "Analyst"
    manager = "Manager"
    develop = "Developer"


class Department(str, Enum):
    engineering = "Engineering"
    sales = "Sales"
    hr = "HR"


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


class EmployeeRequest(BaseModel):
    name: str
    role: Optional[Role]
    department: Optional[Department]
    email: EmailStr

    @classmethod
    def from_dict(cls, data: dict):
        """Creates an Employee instance from a dictionary."""
        return cls(
            name=data.get('name'),
            role=data.get('role'),
            department=data.get('department'),
            email=data.get('email')
        )

    def to_dict(self):
        return {
            "name": self.name,
            "role": self.role,
            "department": self.department,
            "email": self.email
        }


class Employee(EmployeeRequest):
    id: str = Field(default_factory=str)
    date_joined: str = Field(default_factory=lambda: datetime.now().isoformat())

    @classmethod
    def from_dict(cls, data: dict):
        """Creates an Employee instance from a dictionary."""
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            role=data.get('role'),
            department=data.get('department'),
            email=data.get('email'),
            date_joined=data.get('date_joined')
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "department": self.department,
            "email": self.email,
            "date_joined": self.date_joined,
        }
    

def employee_serializer(employee) -> Employee:
    employee['id'] = str(employee['_id'])  # Convert ObjectId to string
    del employee['_id']  # Remove the original ObjectId
    return Employee.from_dict(employee)
