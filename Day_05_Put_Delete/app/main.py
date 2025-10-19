'''
    Path Parameter - it is used to provide meta data, validation rules, and documentation
                     hints for path parameters in your API endpoints.
'''

from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()

class  Patient(BaseModel):
    id:Annotated[str, Field(..., description='ID of the patient', examples=["P001"])]
    name:Annotated[str, Field(..., description="Enter Patient Name", examples=["Nikhil"])]
    city:Annotated[str, Field(..., description="Enter the city", examples=["Delhi"])]
    age:Annotated[int, Field(gt=0, description="Enter age greater than 0")]
    gender:Annotated[Literal['male', 'female', 'others'], Field(..., description="Gender of Patient", examples=["M or F or O"])]
    height:Annotated[float, Field(..., gt=0, description="Height Of Patient in meters")]
    weight:Annotated[float, Field(..., gt=0, description="Weight Of Patient in kg")]


    @computed_field
    @property
    def bmi_calculator(self) -> float:
        # if self.height < 0 or self.weight < 0:
        #     raise ValueError("Invalid value. Enter value greater than 0")
        
        bmi = round(self.weight/(self.height**2),2)
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

''' To Update Patient '''
class Update_Patient(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]



def load_data():
    with open("C:/Saurabh/Dev/Full Stack/Backend/Day_05_Put_Delete/patient.json", "r") as f:
        data = json.load(f)
        return data

    
# Saving the data
def save_data(data):
    with open("C:/Saurabh/Dev/Full Stack/Backend/Day_05_Put_Delete/patient.json", "w") as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return "Welcome to the Patient API"

@app.get("/about")
def about():
    return ""

''' Path Parameter '''
@app.get("/patient/{patient_id}")
def patient(patient_id: str = Path(..., description="ID of the Patient", examples="P001")):
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


@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: Update_Patient):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    #existing_patient_info -> pydantic object -> updated bmi + verdict
    existing_patient_info['id'] = patient_id
    patient_pydandic_obj = Patient(**existing_patient_info)
    #-> pydantic object -> dict
    existing_patient_info = patient_pydandic_obj.model_dump(exclude='id')

    # add this dict to data
    data[patient_id] = existing_patient_info

    # save data
    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient updated'})



@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')

    del data[patient_id]
    
    save_data(data)
    
    return JSONResponse(status_code=200, content={'message':'patient deleted'})
