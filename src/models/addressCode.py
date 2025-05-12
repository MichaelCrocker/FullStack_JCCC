from pydantic import BaseModel

class AddressCodeCreate(BaseModel):
    zip_code: str
    state: str
    city: str
    latitude: float
    longitude: float

class AddressCode(AddressCodeCreate):
    id: int

    class Config:
        from_attributes = True