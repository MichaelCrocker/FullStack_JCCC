from pydantic import BaseModel
from datetime import datetime

class WalkCreate(BaseModel):
    employee_id: int
    start_time: datetime
    end_time: datetime
    street1: str
    street2: str
    city: str
    state: str
    zip: str
    address_code_id: int
    notes: str
    dog_id: int

class Walk(WalkCreate):
    id: int

    class Config:
        from_attributes = True