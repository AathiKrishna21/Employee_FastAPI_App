from fastapi import APIRouter, HTTPException
from schemas import user_schema
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from restapi import authentication

router = APIRouter(
    prefix="/api/users",
    tags=["User"]
)


@router.get("/me")
async def read_users_me(
    current_user: dict = Depends(authentication.get_current_active_user)
    ):
    if "password" in current_user:
        del current_user["password"]
    if "hashed_password" in current_user:
        del current_user["hashed_password"]
    return current_user


@router.post("/register/")
async def register(
    user: user_schema.User,
    current_user: dict = Depends(authentication.get_current_admin_user)
    ):
    if user_schema.get_user(user.uname):
        raise HTTPException(status_code=400, detail="Username already Taken! try different name.")
    user_schema.create_user(user)
    return {"msg": "User created successfully"}

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_schema.get_user(form_data.username)
    if not user or not user_schema.pwd_context.verify(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=authentication.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authentication.create_access_token(data={"sub": user["uname"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
