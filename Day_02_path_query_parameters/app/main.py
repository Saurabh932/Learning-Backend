'''
    Path Parameter - it is used to provide meta data, validation rules, and documentation
                     hints for path parameters in your API endpoints.
'''

from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def load_data():
    with open("C:\Saurabh\Dev\Full Stack\Backend\Day_02_path_query_parameters\patient.json", "r") as f:
        data = json.load(f)
        return data

@app.get("/")
def hello():
    return ""

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