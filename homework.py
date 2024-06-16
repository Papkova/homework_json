from fastapi import FastAPI
from pydantic import BaseModel, field_validator, EmailStr
from typing import Any, Union
from fastapi.responses import JSONResponse


app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    age: int
    email: EmailStr


class Address(BaseModel):
    id: int
    address: str
    type: Union[str, None] = None

    @field_validator('email')
    @classmethod
    def email_(cls, value: Any):
        if "@" not in value:
            raise ValueError("В емейлі повинний бути символ @")
        return value


users = []


@app.post("/users")
def post_user(users: User):
    users.append(users.dict())
    return JSONResponse(status_code=201, content=users.dict())


@app.get('/users')
def get_all():
    return users


addresses = []


@app.post("/addresses")
def post_address(address: Address):
    addresses.append(address.dict())
    return JSONResponse(status_code=201, content=address.dict())


@app.get('/addresses')
def get_all():
    return addresses