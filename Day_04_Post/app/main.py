'''
    Path Parameter - it is used to provide meta data, validation rules, and documentation
                     hints for path parameters in your API endpoints.
'''

from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

app = FastAPI()

class  Patient(BaseModel):
    id:Annotated[str, Field(..., description='ID of the patient', examples=["P001"])]
    name:Annotated[str, Field(..., description="Enter Patient Name", examples=["Nikhil"])]
    city:Annotated[str, Field(..., description="Enter the city", examples=["Delhi"])]
    age:Annotated[int, Field(gt=0, description="Enter age greater than 0")]
    gender:Annotated[Literal["M", "F", "O"], Field(..., description="Gender of Patient", examples=["M or F or O"])]
    height:Annotated[float, Field(..., gt=0, description="Height Of Patient in meters")]
    weight:Annotated[float, Field(..., gt=0, description="Weight Of Patient in kg")]
    # bmi:Annotated[float, Field(..., gt=0, description="BMI Of Patient")]
    # verdict:str


    @computed_field
    @property
    def bmi_calculator(self) -> float:
        if self.height < 0 or self.weight < 0:
            raise ValueError("Invalid value. Enter value greater than 0")
        
        bmi = round(self.weight / (self.height)**2, 3)
        return bmi


    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi_calculator < 18.5:
            return "Underweight"
        elif self.bmi_calculator < 30:
            return "Nortmal"
        else:
            return "Overweight"

def load_data():
    with open(r"C:\Saurabh\Dev\Full Stack\Backend\Day_04_Post\patient.json", "r") as f:
        data = json.load(f)
        return data

    
# Saving the data
def save_data(data):
    with open(r"C:\Saurabh\Dev\Full Stack\Backend\Day_04_Post\patient.json", "w") as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return "Welcome to the Patient API"

@app.get("/about")
def about():
    return ""

''' Path Parameter '''
@app.get("/patient/{patient_id}")
def patient(patient_id: str = Path(..., description="ID of the Patient", example="P001")):
    data = load_data() # loading data
    
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")


'''  Query Parameter  '''
@app.get("/sort")
def sort_by(sort:str = Query(..., description="Sort by category"), 
            order:str = Query('asc', description="Sort in order")):
    
    valid_field = ['height', 'weight', 'bmi']
    
    if sort not in valid_field:
        raise HTTPException(status_code=404, detail=f"Invalid feild selected from {valid_field}")
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=404, detail="Invaild order selected between asc and desc.")
    
    data = load_data()
    
    sort_order = True if order=='desc' else False
    
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort, 0), reverse=False)
    
    return sorted_data


@app.post("/create")
def create_patient(patient: Patient):
    
    # Loading the data
    data = load_data()
    
    # Checking if patient already exit
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exit")
    
    # New patient added to data
    data[patient.id] = patient.model_dump(exclude=['id'])  # converting the pydantic model to dictionary
    
    # Saving into the json file
    save_data(data)
    
    return JSONResponse(status_code=201, content={'message': 'Patient created successfully'})