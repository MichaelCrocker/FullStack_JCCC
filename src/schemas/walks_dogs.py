from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from database import Base


class Walks_Dogs_Entry(Base):
    __tablename__ = "walks_dogs"

    walk_id = Column(Integer, ForeignKey("walks.id"), primary_key=True)
    dog_id = Column(Integer, ForeignKey("dogs.id"), primary_key=True)
    cost = Column(DECIMAL)
    notes = Column(String)
    
    walks_dogs_toWalk = relationship("Walk", back_populates="walk_toWalksDogs")
    walks_dogs_toDog = relationship("Dogs", back_populates="dog_toWalksDogs")