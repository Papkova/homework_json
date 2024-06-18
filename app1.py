from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError, field_validator, EmailStr, conint
from typing import Any
from datetime import datetime
from fastapi.responses import JSONResponse


app = FastAPI()


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: bool
    priority: conint(ge=1, le=5)


class TaskCreate(BaseModel):
    title: str
    description: str
    priority: conint(ge=1, le=5)


class TaskUpdate(BaseModel):
    title: str = None
    description: str = None
    status: bool = None
    priority: conint(ge=1, le=5) = None

tasks= []


@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found ")


@app.post("/tasks")
def create_task(task: TaskCreate):
    task_id = len(tasks) + 1
    new_task = Task(id=task_id, status=False, **task.dict())
    tasks.append(new_task)
    return new_task


@app.put('/tasks/{task_id}')
def update_task(task_id: int, task_update: TaskUpdate):
    for task in tasks:
        if task.id == task_id:
            if task_update.title is not None:
                task.title = task_update.title
            if task_update.description is not None:
                task.description = task_update.description
            if  task_update.status is not None:
                task.status = task_update.status

