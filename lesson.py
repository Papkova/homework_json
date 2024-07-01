from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, ValidationError, field_validator, EmailStr, conint
from sqlalchemy import create_engine, Boolean, Integer, String, Column, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from typing import Optional

DATABASE_URL = "sqlite:///to_do.db"
engine = create_engine(DATABASE_URL)
session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
base = declarative_base


class ToDoItem(base):
    __teblename__ = "to_do"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(100))
    status = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


base.metadata.create_all(bind=engine)

app = FastAPI()


class ToDoBase(BaseModel):
    title: str
    description: str
    status: bool = False


class ToDoCreate(ToDoBase):
    pass


class ToDoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


@app.get("/to_do")
def get_all_todos(db: Session = Depends(get_db)):
    to_dos = db.query(ToDoItem).all()
    return to_dos


@app.get("/to_do/{todo_id}")
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    to_do = db.query(ToDoItem).filter(todo_id == ToDoItem.id)
    if not to_do:
        raise HTTPException(status_code=404, detail="There are no todos")
    return to_do


@app.post("/to_do")
def create_todo(todo: ToDoCreate, db: Session = Depends(get_db)):
    to_do = ToDoItem(**todo.dict())
    db.add(to_do)
    db.commit()
    db.refresh(to_do)
    return to_do


@app.put("/to_do/{todo_id}", response_model=ToDoItem)
def update_todo(todo_id: int, todo: ToDoUpdate, db: Session = Depends(get_db)):
    to_do = db.query(ToDoItem).filter(todo_id == ToDoItem.id).first()
    if not to_do:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo.title is not None:
        to_do.title = todo.title
    if todo.description is not None:
        to_do.description = todo.description
    if todo.status is not None:
        to_do.status = todo.status
    db.commit()
    db.refresh(to_do)
    return to_do


@app.delete("/to_do/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    to_do = db.query(ToDoItem).filter(todo_id == ToDoItem.id).first()
    if not to_do:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(to_do)
    db.commit()
    return {"message": "Todo successfully deleted"}
