

from fastapi import FastAPI,Body
books = [
    {"id": 1,"title": "Title One", "author": "Edwin", "category": "science"},
    {"id": 2,"title": "Title Two", "author": "Irvin", "category": "science"},
    {"id": 3,"title": "Title Three", "author": "Jonathan", "category": "history"},
    {"id": 4,"title": "Title Four", "author": "Steve", "category": "math"},
    {"id": 5,"title": "Title Five", "author": "Harry", "category": "math"},
    {"id": 6,"title": "Title Six", "author": "Steve", "category": "math"}
  ]


app = FastAPI()

@app.get("/")
async def home():
    return "Welcome to all books shop"

@app.get("/books")
async def get_books():
    return books


@app.get("/books/author")
async def books_author(author: str):
    result = []
    for book in books:
        if book.get("author").casefold() == author.casefold():
            result.append(book)

    if result:
        return result
    return {"error": "No book found with that author"}

@app.get("/books/{id}")
async def books_id(id : int):
    for book in books:
        if book.get("id") == id:
            return book

    return {"No book found with that id"}



@app.post("/books/create")
async def create_book(new_book = Body()):
    books.append(new_book)
    return{"message":"Book added successfully", "book": new_book}


@app.put("/books/update")
async def books_update(update_book = Body()):

    for i in range(len(books)):
        if books[i]["id"] == update_book.get("id"):
            books[i] = update_book
            return {"message": "Book updated successfully", "book": update_book}

    return {"Book not found"}




@app.delete("/books/delete/{id}")
async def delete_book(id : int):

    for i in range(len(books)):
        if books[i]["id"] == id:
            deleted = books.pop(i)
            return {"message": "deleted successfully", "book": deleted}


    return {"Book not found"}






