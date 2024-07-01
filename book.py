from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator, EmailStr, Field, ValidationError
from typing import Any, Union
from fastapi.responses import JSONResponse
from datetime import datetime

app = FastAPI()


class Book(BaseModel):
    id: int
    title: str
    year: int = Field(..., gt=1600, le=datetime.now().year)
    author: str
    genre: str
    page_count: int = Field(..., gt=0)


class CreateBook(BaseModel):
    title: str
    year: int = Field(..., gt=1600, le=datetime.now().year)
    author: str
    genre: str
    page_count: int = Field(..., gt=0)


class UpdateBook(BaseModel):
    title: str = None
    year: int = Field(..., gt=1600, le=datetime.now().year)
    author: str = None
    genre: str = None
    page_count: int = Field(..., gt=0)


    @field_validator('title', "author")
    @classmethod
    def check_must_not_be_empty(cls, value: Any):
        if not value.strip():
            raise ValueError("Value must not be empty")


books = []


@app.get('books')
def get_all_books():
    return books


@app.get("/book/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/books")
def create_book(book: CreateBook):
    book_id = len(books) + 1
    new_book = Book(id=book_id, **book.dict())
    books.append(new_book)
    return new_book


@app.put('/books/{book_id}')
def update_book(book_id: int, book_update: UpdateBook):
    for book in books:
        if book.id == book_id:
            if book_update.title is not None:
                book.title = book_update.title
            if book_update.year is not None:
                book.year = book_update.year
            if book_update.author is not None:
                book.author = book_update.author
            if book_update.genre is not None:
                book.genre = book_update.genre
            if book_update.page_count is not None:
                book.page_count = book_update.page_count
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for book in books:
        if book.id == book_id:
            books.remove(book)
            return book
    raise HTTPException(status_code=404, detail="Book not found")





