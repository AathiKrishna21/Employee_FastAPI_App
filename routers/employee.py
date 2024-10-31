from fastapi import APIRouter, Query, HTTPException, status, Depends
from typing import List
from bson import ObjectId
from schemas import employee_schema
from restapi import db, authentication
from datetime import datetime

router = APIRouter(
    prefix="/api/employees",
    tags=["Employee"]
)


@router.get('/', response_model=List[employee_schema.Employee])
def get_employees(
    sort_by: str = None,
    sort_order: employee_schema.SortOrder = None,
    department: str = None,
    role: str = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1),
    db=Depends(db.MongoDB.get_db)
):
    skip = (page - 1) * per_page
    if sort_order == "asc":
        sort_order = 1
    elif sort_order == "desc":
        sort_order = -1

    query = {}
    if department:
        query['department'] = department
    if role:
        query['role'] = role

    if sort_by:
        employees = db.employees.find(query).sort(sort_by, sort_order).skip(skip).limit(per_page)
    else:
        employees = db.employees.find(query).skip(skip).limit(per_page)
    return [employee_schema.employee_serializer(employee) for employee in employees]


@router.get('/{employee_id}', response_model=employee_schema.Employee)
def get_employees(
    employee_id: str,
    current_user: dict = Depends(authentication.get_current_active_user),
    db=Depends(db.MongoDB.get_db)
):
    try:
        # Convert string ID to ObjectId
        object_id = ObjectId(employee_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")

    query = {'_id': object_id}
    employees = db.employees.find_one(query)
    if employees is None:
        raise HTTPException(status_code=404, detail="Employee with this ID not found")
    return employee_schema.employee_serializer(employees)


@router.post("/", response_model=employee_schema.Employee, status_code=status.HTTP_201_CREATED)
async def create_employee(
    employee: employee_schema.EmployeeRequest,
    current_user: dict = Depends(authentication.get_current_admin_user),
    db=Depends(db.MongoDB.get_db)
):
    # Check if the email already exists
    if not employee.name.strip():
        raise HTTPException(status_code=400, detail="Name should not be Empty!")
    if not db.employees.find_one({"email": employee.email}) is None:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create employee document
    employee_doc = employee.to_dict()  # Exclude fields handled by MongoDB
    employee_doc["_id"] = ObjectId()  # Generate a new ObjectId
    employee_doc["date_joined"] = datetime.now().isoformat()  # Generate current date

    # Insert into MongoDB
    db.employees.insert_one(employee_doc)
    employee_doc["id"] = str(employee_doc["_id"])
    del employee_doc["_id"]

    return employee_schema.Employee.from_dict(employee_doc)


@router.put("/{employee_id}", response_model=employee_schema.Employee)
def update_employee(
    employee_id: str,
    employee: employee_schema.EmployeeRequest,
    current_user: dict = Depends(authentication.get_current_admin_user),
    db=Depends(db.MongoDB.get_db)
    ):
    #Check whether Eemployee exists to update
    try:
        object_id = ObjectId(employee_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    existing_employee = db.employees.find_one({"_id": object_id})
    if not existing_employee:
        raise HTTPException(status_code=404, detail="Employee with this ID not found")
    
    #updating the employee
    updated_employee = employee.to_dict()
    if not employee.name.strip():
        raise HTTPException(status_code=400, detail="Name should not be Empty!")
    if not db.employees.find_one({"email": employee.email}) is None:
        raise HTTPException(status_code=400, detail="Email already registered")
    db.employees.update_one({"_id": object_id}, {"$set": updated_employee})
    updated_employee["id"] = employee_id
    updated_employee["date_joined"] = existing_employee["date_joined"]
    return employee_schema.Employee.from_dict(updated_employee)


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: str,
    current_user: dict = Depends(authentication.get_current_admin_user),
    db=Depends(db.MongoDB.get_db)
    ):
    # Check if the employee exists
    try:
        object_id = ObjectId(employee_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    existing_employee = db.employees.find_one({"_id": object_id})
    if not existing_employee:
        raise HTTPException(status_code=404, detail="Employee with this ID not found")

    # Delete the employee
    db.employees.delete_one({"_id": object_id})
    return {"detail": f"Employee with ID-{employee_id} deleted successfully."}
