from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Double
from sqlalchemy.orm import relationship
from database import Base


class AddressCode(Base):
    __tablename__ = "address_codes"

    id = Column(Integer, primary_key=True, index=True)
    zip_code = Column(String)
    state = Column(String)
    city = Column(String)
    latitude = Column(Double)
    longitude = Column(Double)
    street1 = Column(String)
    street2 = Column(String)

    employee_address = relationship("Employee", back_populates="address")
    customer_address = relationship("Customer", back_populates="address")
    walk_address = relationship("Walk", back_populates="address")