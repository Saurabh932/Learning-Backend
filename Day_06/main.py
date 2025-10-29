from fastapi import FastAPI, Header
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message":"Hello World"}


''' Path parameter '''
# @app.get("/greet/{name}")
# async def greet(name:str) -> dict:
#     return{"message":f"Hello {name}"}

''' Query parameter '''
# @app.get("/greet")
# async def greet(name:str) -> dict:
#     return{"message":f"Hello {name}"}


''' Path + Query parameter '''
# @app.get("/greet/{name}")
# async def greet(name:str, age:int) -> dict:
#     return{"message":f"Hello {name}", "age":age}


''' Have optional parameter '''
# @app.get("/greet")
# async def greet(name: Optional[str] = "User",
#                 age: int = 0) -> dict:
#     return{"message":f"Hello {name}" , "age":age}




''' POST method '''

# class CreateBook(BaseModel):
#     title : str
#     authur : str

# @app.post("/create_book")
# async def create_book(book_data : CreateBook):
#     return {
#         "title": book_data.title,
#         "authur": book_data.authur
#     }


''' Request Header '''

@app.get("/get_headers")
async def get_headers(accept:str = Header(None),
                      content_type:str = Header(None),
                      user_agen:str = Header(None),
                      host:str = Header(None)
                      ):
    request_header = {}
    
    request_header["Accept"] = accept
    request_header["Content-Type"] = content_type
    request_header["User-Agent"] = user_agen
    request_header['Host'] = host
    
    return request_header