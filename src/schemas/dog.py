from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class Dogs(Base):
    __tablename__ = "dogs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    breed = Column(String)
    age = Column(Integer)
    special_instructions = Column(String)
    customer_id = Column(Integer, ForeignKey("customers.id"))

    customer = relationship("Customer", back_populates="dogs")
    dog_toWalksDogs = relationship("Walks_Dogs_Entry", back_populates="walks_dogs_toDog")



