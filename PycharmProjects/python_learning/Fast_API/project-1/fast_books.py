from typing import Optional

from fastapi import Body,FastAPI
from fastapi.responses import PlainTextResponse
import json


app = FastAPI()

with open("./books_data.json","r") as file:
    books = json.load(file)
    print(books)


@app.get('/')
async def first_api():
     return "welcome to first api"
@app.get('/books')
async def all_books():
    return books

@app.get('/books/{dynamic_param}')
async def parameter(dynamic_param: str):

    return {'dynamic_param': dynamic_param}

@app.get("/books/id/{id}", response_class=PlainTextResponse)
async def read_book(id: int):
    for book in books:
        if book["id"] == id:
            return (
                f"title = {book['title']}\n"
                f"author = {book['author']}\n"
                f"category = {book['category']}"
            )

    return "Book Not found"


@app.get("/books/filter")
def filter_data(
        id: Optional[int] = None,
        title: Optional[str] = None,
        author: Optional[str] = None,
        category: Optional[str] = None
):
    results = books

    if id is not None:
        results = [book for book in results if book["id"] == id]
    if title:
        results = [book for book in results if title.casefold() in book["title"].casefold()]
    if author:
        results = [book for book in results if author.casefold() in book["author"].casefold()]
    if category:
        results = [book for book in results if category.casefold() in book["category"].casefold()]

    return results

@app.post("/books/create_book")
def create_body(new_book=Body()):
    books.append(new_book)

@app.put("/books/apdating_book")
def updating_body(update_book = Body()):
    for i in range(len(books)):
        if update_book.get("title").casefold() == books[i].get("title").casefold():
            books[i]=update_book
            return "Book updated successfully"


    return "Data not found"

@app.delete("/books/delete_data/{book_title}")
def delete_data(book_title : str):
    for i in range(len(books)):
        if books[i].get("title").casefold() == book_title.casefold():
            books.pop(i)
            return "Data deleted"

    return "Data not found"





