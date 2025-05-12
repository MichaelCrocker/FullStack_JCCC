from pydantic import BaseModel

class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    max_dogs: int
    address_code_id: int
    street1: str
    street2: str
    city: str
    state: str
    zip: str

class Employee(EmployeeCreate):
    id: int

    class Config:
        from_attributes = True