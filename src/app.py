from fastapi import FastAPI, Path, HTTPException, status, Depends, Request, Form, responses
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from typing import Optional
from typing import Annotated
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.routing import Router

from models.customer import Customer as CustomerModel
from models.customer import CustomerCreate as CustomerCreateModel
from models.dog import Dog as dogModel
from models.dog import DogCreate as DogCreateModel
from models.employee import Employee as EmployeeModel
from models.employee import EmployeeCreate as EmployeeCreateModel
from models.pricing import Pricing as PricingModel
from models.pricing import PricingCreate as PricingCreateModel
from models.walk import Walk as WalkModel
from models.walk import WalkCreate as WalkCreateModel
from models.walks_dogs import WalksDogsCreate as WalksDogsCreate

from database import engine, SessionLocal, Base
from sqlalchemy.orm import Session
from controller.database_controller import DatabaseController
from typing import Dict

from datetime import datetime, timedelta

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="Paws in Motion")

app = FastAPI()
controller = DatabaseController()

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app.mount('/static', StaticFiles(directory='static', html=True), name='static')

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse) #Adding template response for basepage
def index(request: Request):
    context = {'request' : request}
    return templates.TemplateResponse("homepage.html", context) 

# FIND WALKER
@app.get("/find-a-walker", response_class=HTMLResponse)
async def get_active_employees( request: Request, 
                          db: Session = Depends(get_db),
                          start_time_search: Annotated[datetime, Form()] = datetime.now().replace(microsecond=0),
                          end_time_search: Annotated[datetime, Form()] = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(hours=24)
                          ):
    if (request.query_params.get("start_time") is not None and request.query_params.get("end_time") is not None):
        start_time_search = request._query_params.get("start_time")
        end_time_search = request.query_params.get("end_time")
    employee_availability = controller.get_active_employees(db, start_time_search, end_time_search)
    pricing = controller.get_pricing(db)
    context = {
        "request": request,
        "employee_availability": employee_availability,
        "start_time_search": start_time_search,
        "end_time_search": end_time_search,
        "query_params": request.query_params.get("start_time"),
        "pricing": pricing
    }
    return templates.TemplateResponse("findADogWalker.html", context)

# DOG #####
@app.get("/dogs", response_class=HTMLResponse)
def get_dogs(request: Request, db: Session = Depends(get_db)):
    dogs = controller.get_dogs(db)
    context = {
        "request": request,
        "dogs": dogs
        }
    return templates.TemplateResponse("dogs.html", context)

@app.get("/newDog", response_class=HTMLResponse) #Adding template response for registering dog
def index(request: Request):
    context = {'request' : request}
    return templates.TemplateResponse("newDog.html", context) 

@app.post("/newDog") # adding a new dog to system
def create_dog(dog: DogCreateModel, db: Session = Depends(get_db)):
    dog = controller.create_dog(dog, db)
    if (dog != False):
        return dog
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="DOG ALREADY EXSIST!")

@app.get("/updatedog/{id}")
def get_customer(request: Request, id: int = Path(description="Enternumber", gt=0), db: Session = Depends(get_db)):
    customer = controller.get_customer(id, db)

    if customer is None:
        return f"Customer id {id} does not exist."
    name = customer.first_name + " " + customer.last_name 
    customer_id = customer.id
    dogs = customer.dogs
    context = {
        "request": request,
        "customer": name,
        "dogs": dogs,
        "customer_id": customer_id
    }
    return templates.TemplateResponse("updatedog.html", context)
    
@app.put("/update_dog")  #updates a dog that exsist in the system
def update_dog(dog: DogCreateModel, db: Session = Depends(get_db)):
    dog = controller.update_dog(dog, db)

    if dog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DOG DOES NOT EXSIST")
    return dog

@app.get("/deletedog/{id}", response_class=HTMLResponse) #Adding template response for basepage
def get_customer(request: Request, id: int = Path(description="Enternumber", gt=0), db: Session = Depends(get_db)):
    customer = controller.get_customer(id, db)

    if customer is None:
        return f"Customer id {id} does not exist."
    name = customer.first_name + " " + customer.last_name 
    customer_id = customer.id
    dogs = customer.dogs
    context = {
        "request": request,
        "customer": name,
        "dogs": dogs,
        "customer_id": customer_id
    }
    return templates.TemplateResponse("deletedog.html", context)

@app.delete("/delete_dog") # deletes dog in the system
def delete_dog(dog: DogCreateModel, db: Session = Depends(get_db)):
    try:
        controller.delete_dog(dog, db)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DOG DNE")

    return {}

# CUSTOMER #####
@app.get("/customers", response_class=HTMLResponse)
def get_customers(request: Request, db: Session = Depends(get_db)):
    customers = controller.get_customers(db)
    context = {
        "request": request,
        "customers": customers
    }
    return templates.TemplateResponse("customers.html", context)

@app.get("/customers/{id}")
def get_customer(request: Request, id: int = Path(description="Enternumber", gt=0), db: Session = Depends(get_db)):
    customer = controller.get_customer(id, db)

    if customer is None:
        return f"Customer id {id} does not exist."
    name = customer.first_name + " " + customer.last_name
    dogs = customer.dogs
    context = {
        "request": request,
        "customer": name,
        "dogs": dogs
    }
    return templates.TemplateResponse("customerdogs.html", context)

@app.get("/newCustomerAccount", response_class=HTMLResponse) #Adding template response for basepage
def index(request: Request):
    context = {'request' : request}
    return templates.TemplateResponse("newCustomerAccount.html", context)

@app.post("/newCustomerAccount")
def create_customerAccount(customer: CustomerCreateModel, db: Session = Depends(get_db)):
    customer = controller.create_customer(customer, db)
    return customer

# EMPLOYEE / CONTRACTOR #####
@app.get("/registerContractor", response_class=HTMLResponse) #Adding template response for basepage
def index(request: Request):
    context = {'request' : request}
    return templates.TemplateResponse("registerContractor.html", context) 

@app.post("/registerContractor")
def register_contractor(employee: EmployeeCreateModel, db: Session = Depends(get_db)):
    employee = controller.register_contractor(employee, db)
    return employee

@app.get("/contractorLogin", response_class=HTMLResponse) #Adding template response for basepage
def index(request: Request):
    context = {'request' : request}
    return templates.TemplateResponse("contractorLogin.html", context) 

# GEOCODER #####
@app.get("/geocodeTester-byAddress/{address}")
def get_addressCode_byAddress(request: Request, address: str = Path(description="Enter-address"), db: Session = Depends(get_db)):
    return controller.get_addressCode_by_address(address, db)

@app.get("/geocodeTester-byLatLng/{latitude} {longitude}")
def get_addressCode_byLatLng(request: Request, latitude: float = Path(description="Enter-latitude"), longitude: float = Path(description="Enter-longitude"), db: Session = Depends(get_db)):
    return controller.get_addressCode_by_LatLng(latitude, longitude, db)

@app.get("/geocodeTester-address/{latitude} {longitude}")
def get_address(request: Request, latitude: float = Path(description="Enter-latitude"), longitude: float = Path(description="Enter-longitude")):
    LatLngString = f"{latitude}, {longitude}"
    print(LatLngString)
    return str(geolocator.reverse(LatLngString))

# WALKS #####
@app.get("/get-all-walks")
def get_all_walks(request: Request, db: Session = Depends(get_db)):
    return controller.get_allWalks(db)

@app.get("/get-walks-by-employee-id/{employee_id}")
def get_walks_by_employee_id(request: Request, employee_id: int = Path(description="Enter-employee_id", gt=0), db: Session = Depends(get_db)):
    return controller.get_walks_by_employee_id(employee_id, db)

@app.get("/book-a-walk/{employee_id}")
def book_a_walk(request: Request, employee_id: int = Path(description="Enter-employee_id", gt=0), db: Session = Depends(get_db)):
    employee = controller.get_employee(employee_id, db)
    context = {
        'request': request,
        'employee': employee
        }
    return templates.TemplateResponse("book_a_walk.html", context)

@app.post("/book-a-walk")
def create_walk(walk: WalkCreateModel, db: Session = Depends(get_db)):
    walkCreate = controller.create_walk(walk, db)
    walksDogs = WalksDogsCreate(walk_id=walkCreate.id, dog_id=walk.dog_id, cost=10, notes="")
    controller.create_walksDogs(walksDogs, db)
    return walkCreate

# LOGIN #####
@app.post("/login")
def login(customer: CustomerCreateModel, db: Session = Depends(get_db)):
    if controller.LoginLogic(customer, db):
        pass
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ACCOUNT NOT FOUND!")

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", reload=True)
