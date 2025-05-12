from pydantic import BaseModel

class CustomerCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    address_code_id: int
    street1: str
    street2: str
    city: str
    state: str
    zip: str

class Customer(CustomerCreate):
    id: int

    class Config:
        from_attributes = True