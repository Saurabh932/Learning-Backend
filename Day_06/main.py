from fastapi import FastAPI
from typing import Optional

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


