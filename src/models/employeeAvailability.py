from pydantic import BaseModel
from datetime import datetime

class EmployeeAvailabilityCreate(BaseModel):
    employee_id: int 
    availability_start: datetime
    availability_end: datetime

class EmployeeAvailability(EmployeeAvailabilityCreate):
    id: int

    class Config:
        from_attributes = True