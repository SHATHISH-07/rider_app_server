from sqlalchemy.orm import Session
import models.driver as model
import schemas.driver as DriverSchema
import uuid
from sqlalchemy import func

def get_available_driver(db: Session):
    return db.query(model.Driver).filter(
        model.Driver.is_available == True,
        model.Driver.deleted_at.is_(None)
    ).first()

def create_driver(db: Session, driver: DriverSchema.DriverCreate):
    db_driver = model.Driver(
        name=driver.name,
        phone=driver.phone,
        vehicle_no=driver.vehicle_no
    )

    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return db_driver

def get_drivers(db: Session):
    return db.query(model.Driver).filter(model.Driver.deleted_at.is_(None),model.Driver.is_available == True).all()

def get_driver(db: Session, id: uuid.UUID):
    return db.query(model.Driver).filter(
            model.Driver.id == id,
            model.Driver.deleted_at.is_(None)
        ).first()

from sqlalchemy.orm import Session
import models.driver as model
import schemas.driver as DriverSchema
import uuid
from sqlalchemy import func


def update_driver(db: Session, id: uuid.UUID, driver: DriverSchema.DriverCreate):
    db_driver = db.query(model.Driver).filter(
        model.Driver.id == id,
        model.Driver.deleted_at.is_(None)
    ).first()

    if not db_driver:
        return None

    db_driver.name = driver.name,
    db_driver.phone=driver.phone,
    db_driver.vehicle_no = driver.vehicle_no
    db_driver.updated_at = func.now()
    db.commit()
    db.refresh(db_driver)

    return db_driver

def delete_driver(db: Session, id: uuid.UUID):
    db_driver = db.query(model.Driver).filter(
            model.Driver.id == id,
            model.Driver.deleted_at.is_(None)
        ).first()

    if not db_driver:
        return None

    db_driver.deleted_at = func.now()
    db.commit()
    return {"message": "Driver deleted successfully"}