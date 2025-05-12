from pydantic import BaseModel

class AddressCreate(BaseModel):
    zip_code: int
    state: str
    city: str
    latitude: float
    longitude: float
    street1: str
    street2: str
    

class Address(AddressCreate):
    id: int

    class Config:
        from_attributes = True