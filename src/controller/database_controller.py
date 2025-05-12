from sqlalchemy.orm import Session
from fastapi import FastAPI, Path, HTTPException, status
from typing import Optional
from datetime import datetime, timedelta

from models.customer import Customer as CustomerModel
from models.customer import CustomerCreate as CustomerCreateModel
from schemas.customer import Customer as CustomerSchema

from models.employee import Employee as EmployeeModel
from models.employee import EmployeeCreate as EmployeeCreateModel
from schemas.employee import Employee as EmployeeSchema

from models.dog import Dog as DogModel
from models.dog import DogCreate as DogCreateModel
from schemas.dog import Dogs as DogSchema

from models.employeeAvailability import EmployeeAvailability as EmployeeAvailabilityModel
from models.employeeAvailability import EmployeeAvailabilityCreate as EmployeeAvailabilityCreateModel
from schemas.employeeAvailability import EmployeeAvailability as EmployeeAvailabilitySchema

from models.addressCode import AddressCode as AddressCodeModel
from models.addressCode import AddressCodeCreate as AddressCodeCreateModel
from schemas.addressCode import AddressCode as AddressCodeSchema

from models.pricing import Pricing as PricingModel
from models.pricing import PricingCreate as PricingCreateModel
from schemas.pricing import Pricing as PricingSchema

from models.walk import Walk as WalkModel
from models.walk import WalkCreate as WalkCreateModel
from schemas.walk import Walk as WalkSchema

from models.walks_dogs import WalksDogsCreate as WalksDogsCreateModel
from schemas.walks_dogs import Walks_Dogs_Entry as WalksDogsSchema

from typing import Dict

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="Paws in Motion")

class DatabaseController:
    def get_pricing(self, db: Session):
        return db.query(PricingSchema).all()

    def get_customers(self, db: Session):
        return db.query(CustomerSchema).all()
    
    def get_customer(self, id: int, db: Session):
        return db.query(CustomerSchema).filter(CustomerSchema.id == id).first()

    def create_customer(self, customer: CustomerCreateModel, db: Session):
        addressCode = self.create_addressCode(customer.street1, customer.street2, customer.city, customer.state, customer.zip, db)
        db_customer = CustomerSchema(first_name = customer.first_name,
                           last_name = customer.last_name, 
                           email = customer.email,
                           phone = customer.phone,
                           address_code_id = addressCode.id)
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        response = self.get_customer(db_customer.id, db=db)
        return response
    
    def get_active_employees(self, db: Session, start_time_search, end_time_search):
        return db.query(*EmployeeSchema.__table__.columns, *EmployeeAvailabilitySchema.__table__.columns, *AddressCodeSchema.__table__.columns)\
                .join(EmployeeAvailabilitySchema, EmployeeAvailabilitySchema.employee_id==EmployeeSchema.id)\
                .join(AddressCodeSchema, AddressCodeSchema.id==EmployeeSchema.address_code_id)\
                .order_by(EmployeeAvailabilitySchema.employee_id)\
                .filter(EmployeeAvailabilitySchema.availability_start.between(start_time_search, end_time_search))
    
    def get_dogs(self, db: Session):
        return db.query(DogSchema).all()
    
    def get_dog(self, id: int, db: Session):
        return db.query(DogSchema).filter(DogSchema.id == id).first()
    
    def create_dog(self, dog: DogCreateModel, db: Session):
        response = None
        DogDB = db.query(DogSchema).filter(DogSchema.name == dog.name and DogSchema.customer_id == dog.Customer_id).first()

        if DogDB is None:
            db_dog = DogSchema(name = dog.name, 
                            age = dog.age, 
                            customer_id = dog.Customer_id, 
                            special_instructions = dog.special_instructions,
                            breed = dog.breed)
            db.add(db_dog)
            db.commit()
            db.refresh(db_dog)
            response = self.get_dog(db_dog.id, db=db)
        else:
            return False
        return response
    
    def update_dog(self, dog: DogCreateModel, db: Session):
        response = None 
        #find the dog to update
        DogDB = db.query(DogSchema).filter(DogSchema.name == dog.name and DogSchema.customer_id == dog.Customer_id).first()
        if DogDB is not None:
            DogDB.age = dog.age 
            DogDB.special_instructions = dog.special_instructions
            DogDB.breed = dog.breed
            db.commit()
            response = self.get_dog(DogDB.id, db=db)
        return response
    
    def delete_dog(self, dog: DogCreateModel, db: Session):
        DogDB = db.query(DogSchema).filter(DogSchema.name == dog.name and DogSchema.customer_id == dog.Customer_id).first()
        if DogDB is not None:
            db.delete(DogDB)
            db.commit()
        else:
            raise Exception( "DOG DOES NOT EXSIST")
        return {} 
    
    def get_employee(self, id: int, db: Session):
        return db.query(EmployeeSchema).filter(EmployeeSchema.id == id).first()
    
    def register_contractor(self, employee: EmployeeCreateModel, db: Session):
        addressCode = self.create_addressCode(employee.street1, employee.street2, employee.city, employee.state, employee.zip, db)
        db_employee = EmployeeSchema(first_name = employee.first_name, 
                           last_name = employee.last_name, 
                           email = employee.email, 
                           max_dogs = employee.max_dogs,
                           phone = employee.phone,
                           address_code_id = addressCode.id)
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        response = self.get_employee(db_employee.id, db=db)
        return response
    
    def get_allWalks(self, db:Session):
        return db.query(WalkSchema).all()

    def get_walk_by_id(self, id: int, db: Session):
        return db.query(WalkSchema).filter(WalkSchema.id == id).first()
    
    def get_walks_by_employee_id(self, employee_id: int, db: Session):
        return db.query(WalkSchema).filter(WalkSchema.employee_id == employee_id).all()

    def create_walk(self, walk: WalkCreateModel, db: Session):
        response = None
        addressCode = self.create_addressCode(walk.street1, walk.street2, walk.city, walk.state, walk.zip, db)
        walkToAdd = WalkSchema(
                        employee_id = walk.employee_id, 
                        start_time = walk.start_time, 
                        end_time = walk.end_time, 
                        address_code_id = addressCode.id,
                        notes = walk.notes
                    )
        db.add(walkToAdd)
        db.commit()
        db.refresh(walkToAdd)
        response = self.get_walk_by_id(walkToAdd.id, db=db)
        return response
    
    def update_walk(self, walk: WalkCreateModel, db: Session):
        response = None 
        #find the walk to update
        WalkDB = db.query(WalkSchema).filter(
            WalkSchema.employee_id == walk.employee_id and 
            WalkSchema.start_time == walk.start_time).first()
        if WalkDB is not None:
            WalkDB.start_time = walk.start_time
            WalkDB.end_time = walk.end_time
            WalkDB.address_code_id = walk.address_code_id
            WalkDB.notes = walk.notes
            db.commit()
            response = self.get_walk_by_id(WalkDB.id, db=db)
        return response
    
    def delete_walk(self, walk: WalkCreateModel, db: Session):
        WalkDB = db.query(WalkSchema).filter(
            WalkSchema.employee_id == walk.employee_id and 
            WalkSchema.start_time == walk.start_time).first()
        if WalkDB is not None:
            db.delete(WalkDB)
            db.commit()
        else:
            raise Exception( "WALK DOES NOT EXSIST")
        return {} 
    
    def get_walksDogs_by_walk_id(self, walk_id: int, db: Session):
        return db.query(WalksDogsSchema).filter(WalksDogsSchema.walk_id == walk_id).all()

    def get_walksDogs_by_dog_id(self, dog_id: int, db: Session):
        return db.query(WalksDogsSchema).filter(WalksDogsSchema.dog_id == dog_id).all()
    
    def get_walksDogs_by_walk_and_dog_ids(self, walk_id: int, dog_id: int, db:Session):
        return db.query(WalksDogsSchema).filter(
            WalksDogsSchema.walk_id == walk_id and 
            WalksDogsSchema.dog_id == dog_id
        ).first()

    def create_walksDogs(self, walksDogs: WalksDogsCreateModel, db: Session):
        response = None
        walksDogsEntry = db.query(WalksDogsSchema).filter(
            WalksDogsSchema.walk_id == walksDogs.walk_id and 
            WalksDogsSchema.dog_id == walksDogs.dog_id
        ).first()

        if walksDogsEntry is None:
            walksDogsEntryToAdd = WalksDogsSchema(
                            walk_id = walksDogs.walk_id, 
                            dog_id = walksDogs.dog_id, 
                            cost = walksDogs.cost, 
                            notes = walksDogs.notes
                        )
            db.add(walksDogsEntryToAdd)
            db.commit()
            db.refresh(walksDogsEntryToAdd)
            response = self.get_walksDogs_by_walk_and_dog_ids(
                walk_id=walksDogsEntryToAdd.walk_id,
                dog_id=walksDogsEntryToAdd.dog_id,
                db=db
            )
        else:
            return False
        return response
    
    def update_walksDogs(self, walksDogs: WalksDogsCreateModel, db: Session):
        response = None 
        #find the walksDogs to update
        WalksDogsDB = db.query(WalksDogsSchema).filter(
            WalksDogsSchema.walk_id == walksDogs.walk_id and 
            WalksDogsSchema.dog_id == walksDogs.dog_id).first()
        if WalksDogsDB is not None:
            WalksDogsDB.walk_id = walksDogs.walk_id
            WalksDogsDB.dog_id = walksDogs.dog_id
            WalksDogsDB.cost = walksDogs.cost
            WalksDogsDB.notes = walksDogs.notes
            db.commit()
            response = self.get_walksDogs_by_walk_and_dog_ids(
                walk_id=WalksDogsDB.walk_id,
                dog_id=WalksDogsDB.dog_id,
                db=db
            )
        return response

    def delete_walksDogs(self, walksDogs: WalksDogsCreateModel, db: Session):
        WalksDogsDB = db.query(WalksDogsSchema).filter(
            WalksDogsSchema.walk_id == walksDogs.walk_id and 
            WalksDogsSchema.dog_id == walksDogs.dog_id).first()
        if WalksDogsDB is not None:
            db.delete(WalksDogsDB)
            db.commit()
        else:
            raise Exception( "WALKS_DOGS ENTRY DOES NOT EXSIST")
        return {} 
    
    def get_addressCode_by_address(self, aC_street1, aC_street2, aC_city, aC_state, aC_zip, db: Session):
        return db.query(AddressCodeSchema).filter(
            AddressCodeSchema.street1 == aC_street1 and
            AddressCodeSchema.street2 == aC_street2 and
            AddressCodeSchema.city == aC_city and
            AddressCodeSchema.state == aC_state and
            AddressCodeSchema.zip_code == aC_zip
        ).first()
    
    def get_addressCode_by_LatLng(self, latitude: float, longitude: float, db: Session):
        return db.query(AddressCodeSchema).filter(
            AddressCodeSchema.latitude == latitude and
            AddressCodeSchema.longitude == longitude
        ).first()

    def create_addressCode(self, aC_street1, aC_street2, aC_city, aC_state, aC_zip, db: Session):
        response = None
        addressCodeEntry = self.get_addressCode_by_address(aC_street1, aC_street2, aC_city, aC_state, aC_zip, db)

        if addressCodeEntry is None:
            addressString = aC_street1 + "," + aC_street2 + "," + aC_city + "," + aC_state + " " + aC_zip
            addressCodeEntryToAdd = AddressCodeSchema(
                            street1 = aC_street1,
                            street2 = aC_street2,
                            zip_code = aC_zip, 
                            state = aC_state, 
                            city = aC_city, 
                            latitude = geolocator.geocode(addressString).latitude,
                            longitude = geolocator.geocode(addressString).longitude
                        )
            db.add(addressCodeEntryToAdd)
            db.commit()
            db.refresh(addressCodeEntryToAdd)
            response = self.get_addressCode_by_address(aC_street1, aC_street2, aC_city, aC_state, aC_zip, db)
        else:
            return addressCodeEntry
        return response

    #def update_addressCode

    #def delete_addressCode

    def LoginLogic(self, customer: CustomerCreateModel, db: Session):
        
        login = db.query(CustomerSchema).filter(CustomerSchema.email == customer.email and CustomerSchema.id == customer.id).first()
        if login is not None:
            return True
