from fastapi import FastAPI

books = [
    {"id": 1,"title": "Title One", "author": "Author One", "category": "science"},
    {"id": 2,"title": "Title Two", "author": "Author Two", "category": "science"},
    {"id": 3,"title": "Title Three", "author": "Author Three", "category": "history"},
    {"id": 4,"title": "Title Four", "author": "Author Four", "category": "math"},
    {"id": 5,"title": "Title Five", "author": "Author Five", "category": "math"},
    {"id": 6,"title": "Title Six", "author": "Author Two", "category": "math"}
  ]


app = FastAPI()

@app.get("/books")
def all_books():
    return books