from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError, field_validator, Field
from typing import Any
from datetime import datetime
from fastapi.responses import JSONResponse


app = FastAPI()

class Book(BaseModel):
    id: int
    title: str
    year: int = Field(..., gt=1500, le=datetime.now().year)
    author: str
    genre: str
    page_count: int = Field(..., gt=0)

@app.post("/book/")
def create_item(book: Book):
    try:
        return JSONResponse(status_code=201, content=book.dict())
    except ValidationError as exc:
        errors = exc.errors()
        for error in errors:
            if error['type'] == 'value_error':
                error['msg'] = "Check your datas on validation"
        raise HTTPException(status_code=422, detail=errors)


books = []


@app.get('books')
def get_all_books():
    return books