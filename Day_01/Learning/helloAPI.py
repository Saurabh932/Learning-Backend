from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {'message' : 'hello world!! this is my first fastapi'}