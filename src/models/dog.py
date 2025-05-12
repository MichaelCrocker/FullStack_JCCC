from pydantic import BaseModel

class DogCreate(BaseModel):
    Customer_id: int
    name: str
    breed: str
    age: int
    special_instructions: str

class Dog(DogCreate):
    id: int

    class Config:
        from_attributes = True


