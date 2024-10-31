# Employee_FastAPI_App
This repo is about: Sample Demo project to learn FastAPI

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints.
To know more about Usage:  [FastAPI - Tutorial](https://fastapi.tiangolo.com/tutorial/)

This is a Simple application with CRUD operation on the Employee db with authentication support. It is build with FastAPI and and users Mongo Db as Database.

## How to Run this Application:
Steps to run this Application:
1. Clone this repo in local
2. It is good to use a python environement. To create a virtual env: `python -m venv <environment name>` and activate this environment.
3. Install the requirements.txt. Using `pip install -r requirements.txt`
4. Now, run the main file which will start the application.
5. Application will be running at http://127.0.0.1:8000 and swagger will be exposed in "/docs" route also check the documentation from the "/redoc" route.

## Details:
We can able to Get(entire list with filter and sorting or can be fetched with Id), create, Update, Delete operations on the employee table.Employee contains name, role, department, email and id. This Application also have user and login routes. Creation of a new User can be done with "/register" endpoint. Password will be stored as encrypted text in the DB. and User login can be done with "/token" route, on post login token will be generated.

To Access employee route, we need the login token to authorize the user. On user creation there is a parameter "is_admin" which is a boolean parameter that will be ture for admin user and false for normal user. Certain routes like create, update and delete needs admin previlages while fetching employee with ID needs authentication(with any user) and fetching all employee doesn't need any authentication.
