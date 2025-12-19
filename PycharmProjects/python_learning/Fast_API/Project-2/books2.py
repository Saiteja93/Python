from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel,Field

app = FastAPI()

class Book:
    id : Optional[int]=None
    title : str = Field(min_length=3)
    author : str = Field(min_length=3)
    description : str = Field(min_length=3, max_length=100)
    rating : int = Field(gt=-1, lt=6)
    published_year : int

    def __init__(self, id, author,title, description, rating, published_year):
        self.id = id
        self.author = author
        self.title = title
        self.description = description
        self.rating = rating
        self.published_year = published_year

class BookRequest(BaseModel):
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_year : int

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A New Journey",
                "author": "Author Name",
                "description": "A fascinating description",
                "rating": 5,
                "published_year" : 2012
            }
        }
    }


BOOKS=[
    Book(1,'rodrigue','A man walking on street', 'Very good book', 4, 2012),
    Book(2, 'Miguel de Cervantes', 'Don Quixote', 'good book', 3,2015),
    Book(3, 'Robert Louis Stevenson', 'Treasure Island', 'good book', 4,2019),
    Book(4, 'Nathaniel Hawthorne', 'The Scarlet Letter', 'Very good book', 5,2011),
    Book(5, 'Jonathan Swift', 'Gullivers Travels', 'Very good book', 5,2018),
    Book(6, 'Charles Dickens', 'Little Women', 'good book', 3,2020),

]

@app.get('/books')
async def real_all_books():
    return BOOKS


@app.get('/books/{book_id}')
async def request_book_id(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book
    return "Book not found"

@app.get('/books/by_rating')
async def request_by_rating(by_rating : int):
    rating_data= []
    for book in BOOKS:
        if book.rating == by_rating:
            rating_data.append(book)

    return rating_data

@app.get('/books/{published_year}')
async def data_published_year(published_year : int):
    year_data =[]
    for book in BOOKS:
        if book.published_year == published_year:
            year_data.append(book)
    return year_data


@app.post("/create_body")
async def create_body(book_request : BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(id_creation(new_book))

def id_creation(book: Book):
    book.id =1 if len(BOOKS) ==0 else BOOKS[-1].id + 1
    return book

@app.put("/books/update_data")
async def updating_data(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book

@app.delete("/boobks/{id}")
def deleting_data(id : int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == id:
            BOOKS.pop(i)
            break