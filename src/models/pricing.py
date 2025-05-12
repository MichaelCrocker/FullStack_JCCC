from pydantic import BaseModel

class PricingCreate(BaseModel):
    size: int
    cost_per_hour: float

class Pricing(PricingCreate):
    id: int

    class Config:
        from_attributes = True