from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base


class EmployeeAvailability(Base):
    __tablename__ = "employee_availability"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    availability_start = Column(DateTime)
    availability_end = Column(DateTime)

    employee = relationship("Employee", back_populates="employee_availability")