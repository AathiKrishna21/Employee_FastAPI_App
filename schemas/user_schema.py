from pydantic import BaseModel, EmailStr
from restapi.db import MongoDB
from passlib.context import CryptContext


db = MongoDB.get_db()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    
class User(BaseModel):
    uname: str
    email: EmailStr
    password: str
    is_admin: bool = False

    @classmethod
    def from_dict(cls, data: dict):
        """Creates an Employee instance from a dictionary."""
        return cls(
            uname=data.get('uname'),
            email=data.get('email'),
            password=data.get('password'),
            is_admin=data.get('is_admin')
        )

    def to_dict(self):
        return {
            "uname": self.uname,
            "email": self.email,
            "password": self.password,
            "is_admin": self.is_admin
        }


class UserInDB(User):
    hashed_password: str


def get_user(uname: str):
    user = db.users.find_one({"uname": uname})
    if user:
        del user["_id"]
    return user


def create_user(user: User):
    hashed_password = pwd_context.hash(user.password)
    user_dict = user.to_dict()
    del user_dict["password"]
    user_dict["hashed_password"] = hashed_password
    db.users.insert_one(user_dict)
