from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field, field_validator
from typing import Optional
from datetime import datetime
from starlette import status



app= FastAPI()
class Book:
    def __init__(self,id: int,author: str,title: str,remarks: str,rating: int,year: int):
        self.id = id
        self.author = author
        self.title = title
        self.remarks = remarks
        self.rating = rating
        self.year = year


class BookRequest(BaseModel):
    id : Optional[int] = Field(description="it is optional", default=None)
    author : str = Field(min_length=3, max_length=15)
    title : str = Field(min_length=2, max_length=10)
    remarks: str = Field(min_length=2, max_length=120)
    rating: int = Field(gt=0, le=5)
    year : int

    @field_validator("year")
    def year_validator(cls, value):
        current_year = datetime.now().year
        if value > current_year:
            raise ValueError (f"Year cannot be more than {current_year}")
        if value < 1947:
            raise ValueError (f"year should be greater than 1947")

        return value


'''
class Book:
    id : int
    author : str
    title : str
    remarks : str
    rating : int
    year : int
    def __init__(self,id,author,title,remarks,rating,year):
        self.id = id
        self.author = author
        self.title = title
        self.remarks = remarks
        self.rating = rating
        self.year = year

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="no need of id", default=None)
    author: str = Field(min_length =2)
    title: str = Field(min_length=2, max_length=15)
    remarks: str = Field(min_length=5, max_length=25 )
    rating: int = Field(gt =0, lt=6)
    year: int = Field(gt=1970, lt = 9999)

'''
BOOKS=[

    Book(1,'rodrigue','A man walking on street', 'Very good book', 4, 2012),
    Book(2, 'Miguel de Cervantes', 'Don Quixote', 'good book', 3,2015),
    Book(3, 'Robert Louis Stevenson', 'Treasure Island', 'good book', 4,2019),
    Book(4, 'Nathaniel Hawthorne', 'The Scarlet Letter', 'Very good book', 5,2012),
    Book(5, 'Jonathan Swift', 'Gullivers Travels', 'Very good book', 5,2018),
    Book(6, 'Charles Dickens', 'Little Women', 'good book', 3,2020),

]

@app.get("/")
async def home():
    return "Welcome to books stack"
@app.get("/books")
async def all_books():
    return BOOKS

@app.get("/books/{id}", status_code=status.HTTP_200_OK)
async def books_id(id: int):
    for book in BOOKS:
        if book.id == id:
            return book

    raise HTTPException( status_code=404,detail="No book found with that id")

@app.post("/books/create_book", status_code=status.HTTP_201_CREATED)
async def creating_new_book(new_book: BookRequest):
    new_data = Book(**new_book.model_dump())

    BOOKS.append(id_creation(new_data))

    return {"description": "New book data created", "Book": new_data}


def id_creation(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1

    return book


@app.put("/books/update", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):

    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            updated_book = Book(**book.model_dump())
            BOOKS[i] = updated_book

            return {"description": "Book updated with new data", "Book": updated_book}


    raise HTTPException(status_code=404, detail="No book found with that ID")

@app.delete("/book/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == id:

            deleted = BOOKS.pop(i)
            return {"description": "Deleted selected book from stack", "book":deleted }

    raise HTTPException(status_code=404, detail="No book found with that ID")
'''
@app.get("/books")
async def books():
    return BOOKS


@app.get("/books/{id}")
async def book_id(id: int):
    for book in BOOKS:
        if book.id == id:
            return book

    return{"books id not found"}

@app.post("/books/create_book")
async def create_book_request(book_request : BookRequest):
    new_book = Book(**book_request.model_dump(),)

    BOOKS.append(generate_next_id(new_book))

    return{"description":"New book record created", "book": new_book}

def generate_next_id(book: Book):
    if len(BOOKS)>0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1

    return book


@app.put("/books/update")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
        return {"description": "Update book in BOOKS model", "book": book}


    return {"no book found"}



@app.delete("/books/delete/{book_id}")
async def delete_books(book_id: int):

    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            return{"description":"Book deleted from stack"}

'''