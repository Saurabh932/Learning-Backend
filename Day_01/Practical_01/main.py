from fastapi import FastAPI
import json

app = FastAPI()

def load_data():
    with open("Day_01/Practical_01/patient.json", 'r') as f:
        data = json.load(f)
        return data

@app.get("/")
def hello():
    return {"message":"Patient Management System API"}

@app.get("/about")
def about():
    return {'message': 'A fully functional API to manage your patient records'}

@app.get("/veiw")
def veiw():
    data = load_data()  # loading the json data from the function
    return data