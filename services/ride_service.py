from sqlalchemy.orm import Session
from crud import ride as ride_crud
from crud import driver as driver_crud
import uuid

def request_ride(db: Session, ride_data):
    try:
        return ride_crud.create_ride(db, ride_data)
    except ValueError as e:
        return {"message": str(e)}

def assign_driver(db: Session, ride_id: uuid.UUID):
    ride = ride_crud.get_ride(db, ride_id)

    if not ride or ride.status != "requested":
        return None 

    driver = driver_crud.get_available_driver(db)
    if not driver:
        return None

    ride.driver_id = driver.id
    ride.status = "assigned"
    driver.is_available = False   

    db.commit()
    db.refresh(ride)
    return ride

def complete_ride(db: Session, ride_id: uuid.UUID):
    ride = ride_crud.get_ride(db, ride_id)
    
    if not ride or ride.status != "assigned":
        return None

    ride.status = "completed"
    
    if ride.driver_id:
        driver = driver_crud.get_driver(db, ride.driver_id)
        if driver:
            driver.is_available = True 

    db.commit()
    db.refresh(ride)
    return ride

def cancel_ride(db: Session, ride_id: uuid.UUID):
    ride = ride_crud.get_ride(db, ride_id)

    if not ride:
        return None

    if ride.driver_id:
        driver = driver_crud.get_driver(db, ride.driver_id)
        if driver:
            driver.is_available = True

    ride.status = "cancelled"
    db.commit()
    db.refresh(ride)
    return ride