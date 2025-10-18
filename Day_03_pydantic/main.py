# ----------------------------------------------
# 🧾 Example: Pydantic Data Validation Model (Patient Record)
# Demonstrates:
# - Field validation and constraints
# - Field and Model validators
# - Computed properties
# - Nested models
# - JSON serialization
# ----------------------------------------------

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated


# ----------------------------------------------
# 🏠 Nested Model: Address
# Used inside Patient model to show nested data structure
# ----------------------------------------------
class Address(BaseModel):
    city: str
    state: str
    pincode: int


# ----------------------------------------------
# 👨‍⚕️ Main Model: Patient
# Demonstrates type validation, constraints, validators, and computed fields
# ----------------------------------------------
class Patient(BaseModel):
    # --------------------------
    # Field Validation
    # --------------------------
    # max_length, title, description -> Field-level validation
    name: Annotated[str, Field(max_length=50, title="Name of Patient",
                               description="Maximum length 50 characters")]

    # Type Validation (Python type hints enforce type checking)
    age: int
    weight: float = Field(gt=0, description="Weight must be greater than 0 (in kg)")  # Field validation with gt constraint
    height: int = Field(gt=0, description="Height in centimeters")  # Field validation with gt constraint

    # Optional field (type validation ensures it is bool if provided)
    married: Optional[bool] = None

    # Type Validation: ensures each element in the list is a string
    allergies: List[str]  # List type validation

    # Email field with built-in validation (checks for correct email format)
    email: EmailStr  # Data validation

    # Type Validation: ensures contact is a dictionary with string keys and values
    contact: Dict[str, str]  # Data and type validation

    # Nested Model Validation: validates that 'address' is an instance of Address class
    address: Address  # Field & type validation


    # ----------------------------------------------
    # ✉️ Field-level Validator (email)
    # Validates email domain — allows only specified company domains
    # ----------------------------------------------
    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domain = ['hdfc.com', 'icici.com']
        
        # Split domain part from email (after '@')
        domain_name = value.split('@')[-1]
        
        if domain_name not in valid_domain:
            raise ValueError("❌ Invalid email domain. Only hdfc.com or icici.com are allowed.")
        
        return value  # Return validated value (must return same type)

    # ----------------------------------------------
    # ⚙️ Model-level Validator
    # Checks multiple fields together
    # Logic: If age > 60, then contact must contain an 'emergency' key
    # ----------------------------------------------
    @model_validator(mode='after')
    @classmethod
    def emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact:
            raise ValueError("⚠️ Patient older than 60 years must have an emergency contact.")
        return model

    # ----------------------------------------------
    # 📏 Computed Field (BMI)
    # Automatically calculates BMI based on weight and height
    # Formula: weight / (height in meters)^2
    # ----------------------------------------------
    @computed_field
    @property
    def bmi_calculate(self) -> float:
        if self.weight <= 0 or self.height <= 0:
            raise ValueError("❌ Weight and Height must be positive values.")
        
        # Convert height from cm → m for BMI formula
        bmi = round(self.weight / (self.height / 100) ** 2, 2)
        return bmi


# ----------------------------------------------
# 🗂️ Function: Insert patient details
# Simulates saving or displaying patient data
# ----------------------------------------------
def insert_patient_details(patient: Patient):
    print(f"👤 Name: {patient.name}")
    print(f"🎂 Age: {patient.age}")
    print(f"⚖️ Weight: {patient.weight} kg")
    print(f"📏 Height: {patient.height} cm")
    print(f"💍 Married: {patient.married}")
    print(f"🤧 Allergies: {patient.allergies}")
    print(f"✉️ Email: {patient.email}")
    print(f"📞 Contact: {patient.contact}")
    print(f"📈 BMI: {patient.bmi_calculate}")
    print(f"🏠 Address: {patient.address}")
    print("✅ Details inserted successfully.\n")


# ----------------------------------------------
# 🧩 Example Usage
# Creating nested Address instance and main Patient object
# ----------------------------------------------
address_info = {
    'city': 'Nagpur',
    'state': 'Maharashtra',
    'pincode': 440017
}

address1 = Address(**address_info)  # Unpacking dict into Address model

# Main patient info with nested address
patient_info = {
    "name": "Saurabh",
    "age": 30,
    "weight": 65.5,
    "height": 170,
    "married": False,
    "allergies": ['pollen', 'dust'],
    "email": "xyz@hdfc.com",
    "contact": {"number": "6546546546"},
    "address": address1
}

# Instantiate Patient model using unpacking (**)
patient1 = Patient(**patient_info)

# Display all details
insert_patient_details(patient1)

# Access nested field
print(f"🏙️ City: {patient1.address.city}\n")

# Serialize to JSON (e.g., for API or DB)
json_output = patient1.model_dump_json()
print("🧾 Serialized JSON Output:")
print(json_output)
print(f"Type: {type(json_output)}")
