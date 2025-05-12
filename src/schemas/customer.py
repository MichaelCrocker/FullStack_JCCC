from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    address_code_id = Column(Integer, ForeignKey("address_codes.id"))

    address = relationship("AddressCode", back_populates="customer_address")
    dogs = relationship("Dogs", back_populates="customer")