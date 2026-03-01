
from typing import Optional

from fastapi import FastAPI,Query,Body,HTTPException
from pydantic import BaseModel,Field
from datetime import datetime
from decimal import Decimal
from starlette import status

app = FastAPI()

current_year = datetime.now().year
class Book:
    id: int
    title: str
    author: str
    genre: str
    year_published : int
    is_available: bool
    rating: float

    def __init__(self,id,title,author,genre,year_published, is_available,rating):
        self.id = id
        self.title = title
        self.author = author
        self.genre = genre
        self.year_published = year_published
        self.is_available = is_available
        self.rating = rating

class BookRequest(BaseModel):
    id : Optional[int] = Field(description = "ID is not needed to create", default=None)
    title : str = Field(min_length = 3)
    author : str = Field(min_length=3)
    genre : str = Field(min_length=3)
    year_published : int = Field (ge = 1800, le = current_year)
    is_available : bool
    rating : float = Field(ge=0, le=5)

    model_config = {
        "json_schema_extra": {
           "example":
               {
                   "title": "Atomic Habits",
                   "author": "James Clear",
                   "genre": "Self-Help",
                   "year_published": 2018,
                   "is_available": True,
                   "rating": 4.8
               }


        }
    }

BOOKS = [
    Book(1, "The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "Science Fiction", 1979, True, 4.2),
    Book(2, "Foundation", "Isaac Asimov", "Science Fiction", 1951, False, 4.5),
    Book(3, "The Silent Patient", "Alex Michaelides", "Psychological Thriller", 2019, True, 4.1),
    Book(4, "Atomic Habits", "James Clear", "Self-Help", 2018, True, 4.8),
    Book(5, "Habits", "Isaac Asimov", "Self-Help", 2019, True, 4.8)
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def Books_data():
    return BOOKS

@app.post("/create_book")
async def create_book(book_request : BookRequest):
    data = book_request.model_dump()
    new_id = max( book.id for book in BOOKS) + 1
    data["id"] = new_id

    new_book = Book(**data)
    BOOKS.append(new_book)
    return new_book

@app.get("/books/by_rating")
async def book_by_ratings(by_ratings : float):
    book_ratings = [book for book in BOOKS if book.rating > by_ratings]
    if book_ratings:
        return book_ratings

    return {"message" : "No books available with that ratings"}


@app.get("/books/{book_id}")
async def book_by_id(book_id: int):
    book_data = next((book for book in BOOKS if book.id == book_id), None)
    if book_data:
        return book_data


    return {"message": "Id not found in books"}


@app.put("/books/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            return {"Message": "Book data is updated successfully"}


    return{"message": "Book id is not found"}

@app.delete("/books/{book_id")
async def delete_book(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            return {"message": " Book data deleted"}
            break

    return {"message": "Id not found"}


