from typing import Optional

from fastapi import FastAPI,Path,Query, HTTPException
from pydantic import BaseModel,Field
from starlette import status

app = FastAPI()

class Book:
    def __init__(self, id, title, author, description, rating, published_year):
        self.id = id
        self.author = author
        self.title = title
        self.description = description
        self.rating = rating
        self.published_year = published_year

class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published_year: int = Field(gt=1999, lt=2030)


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
    Book(4, 'Nathaniel Hawthorne', 'The Scarlet Letter', 'Very good book', 5,2012),
    Book(5, 'Jonathan Swift', 'Gullivers Travels', 'Very good book', 5,2018),
    Book(6, 'Charles Dickens', 'Little Women', 'good book', 3,2020),

]



@app.get("/books/published_year", status_code=status.HTTP_200_OK)
def get_books_by_year(published_year: int= Query(gt=1999, lt=2030)):
    return [b for b in BOOKS if b.published_year == published_year]




@app.get("/books/ratings/by_rating", status_code=status.HTTP_200_OK)
def get_books_by_rating(rating: int= Query(gt=-1, lt=6)):
    return [b for b in BOOKS if b.rating == rating]

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
def get_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book

    raise HTTPException(status_code=404, detail="Item not found")


@app.get('/books', status_code=status.HTTP_200_OK)
async def real_all_books():
    return BOOKS

@app.post("/create_body",status_code=status.HTTP_201_CREATED)
async def create_body(book_request : BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(id_creation(new_book))

def id_creation(book: Book):
    book.id =1 if len(BOOKS) ==0 else BOOKS[-1].id + 1
    return book

@app.put("/books/update_data",status_code=status.HTTP_204_NO_CONTENT)
async def updating_data(book: BookRequest):
    book_change=False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_change=True

    if not book_change:
        raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/books/{id}",status_code=status.HTTP_204_NO_CONTENT)
def deleting_data(id : int= Path(gt=0)):
    book_change = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == id:
            BOOKS.pop(i)
            book_change=True
            break


    if not book_change:
        raise HTTPException(status_code=404, detail="Item not found")