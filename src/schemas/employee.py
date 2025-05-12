from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from schemas import addressCode

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    max_dogs = Column(Integer)
    address_code_id = Column(Integer, ForeignKey("address_codes.id"))

    address = relationship("AddressCode", back_populates="employee_address")
    employee_availability = relationship("EmployeeAvailability", back_populates="employee")
    employee_walk = relationship("Walk", back_populates="walk_employee")