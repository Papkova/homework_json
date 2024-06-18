from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError, field_validator
from typing import Any
from datetime import datetime
from fastapi.responses import JSONResponse


app = FastAPI()

class Book(BaseModel):
    title: str
    author: str
    year: int
    isbn: str = None

    @field_validator('year')
    @classmethod
    def year_big(cls, value: Any):
        years = datetime.now().year
        if not (1500 > value <= years):
            raise ValueError("Рік видання книги повинний бути від 1500 до поточного року")
        return value


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