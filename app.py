from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError, field_validator, EmailStr, conint
from typing import Any
from datetime import datetime
from fastapi.responses import JSONResponse


app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: conint(gt=0)


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: conint(gt=0)


class UserUpdate(BaseModel):
    name: str = None
    email: EmailStr = None
    age: conint(gt=0)

users = []


@app.get('/users')
def get_all():
    return users


@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return users
    raise HTTPException(status_code=404, detail="User not found ")


@app.post("/users")
def user_create(user: UserCreate):
    user_id = len(users)+1
    new_user = User(id=user_id, **user.dict())
    users.append(new_user)
    return new_user


@app.put("/users/{user_id}")
def update_user(user_id: int, user_update: UserUpdate):
    for user in users:
        if user.id == user_id:
            if user_update.name is not None:
                user.name = user_update.name
            if user_update.email is not None:
                user.email = user_update.email
            if user_update.age is not None:
                user.age = user_update.age
            return user
    raise HTTPException(status_code=404, detail="User not found ")


@app.delete("/user/{user_id")
def del_user(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User not found ")