from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base


class Walk(Base):
    __tablename__ = "walks"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    address_code_id = Column(Integer, ForeignKey("address_codes.id"))
    notes = Column(String)
    
    address = relationship("AddressCode", back_populates="walk_address")
    walk_employee = relationship("Employee", back_populates="employee_walk")
    walk_toWalksDogs = relationship("Walks_Dogs_Entry", back_populates="walks_dogs_toWalk")