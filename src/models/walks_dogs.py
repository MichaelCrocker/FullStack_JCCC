from pydantic import BaseModel
from datetime import datetime

class WalksDogsCreate(BaseModel):
    walk_id: int
    dog_id: int
    cost: float
    notes: str