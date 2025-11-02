from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

book = [
        {
            "id": 1,
            "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
            "author": "Robert C. Martin",
            "publisher": "Prentice Hall",
            "published_date": "2008-08-01",
            "page_count": 464,
            "language": "English"
        },
        {
            "id": 2,
            "title": "Design Patterns: Elements of Reusable Object-Oriented Software",
            "author": "Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides",
            "publisher": "Addison-Wesley",
            "published_date": "1994-10-31",
            "page_count": 395,
            "language": "English"
        },
        {
            "id": 3,
            "title": "Python Crash Course",
            "author": "Eric Matthes",
            "publisher": "No Starch Press",
            "published_date": "2019-05-03",
            "page_count": 544,
            "language": "English"
        },
        {
            "id": 4,
            "title": "Fluent Python",
            "author": "Luciano Ramalho",
            "publisher": "O'Reilly Media",
            "published_date": "2022-03-01",
            "page_count": 1014,
            "language": "English"
        },
        {
            "id": 5,
            "title": "Algorithms and Data Structures In Python",
            "author": "Kent Lee",
            "publisher": "Springer, Inc",
            "published_date": "2021-01-01",
            "page_count": 928,
            "language": "English"
        },
        {
            "id": 6,
            "title": "Introduction to Machine Learning with Python",
            "author": "Andreas C. Müller, Sarah Guido",
            "publisher": "O'Reilly Media",
            "published_date": "2016-09-26",
            "page_count": 394,
            "language": "English"
        }
        ]

class Book(BaseModel):
    id : int
    title : str
    author : str
    publisher : str
    published_date : str
    page_count : int
    language : str

class BookUpdate(BaseModel):
    title : str
    publisher : str
    page_count : int
    language : str
    

@app.get("/", response_model=List[Book])
async def get_all_book():
    return book

@app.post("/book", status_code=status.HTTP_201_CREATED)
async def create_book(book_data:Book) -> dict:
    new_book = book_data.model_dump()
    book.append(new_book)
    return new_book

@app.get("/book/{book_id}")
async def get_book(book_id:int) -> dict:
    for b in book:
        if b['id'] == book_id:
            return b
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail="Book not found")

@app.patch("/book/{book_id}")
async def update_book(book_id:int, book_update_data : BookUpdate) -> dict:
    for b in book:
        if b['id'] == book_id:
            b['title'] = book_update_data.title
            b['publisher'] = book_update_data.publisher
            b['page_count'] = book_update_data.page_count
            b['language'] = book_update_data.language
            
            return book
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found.")
            

@app.delete("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:int):
    for b in book:
        if b['id'] == book_id:
            book.remove(b)
            
            return {}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found.")