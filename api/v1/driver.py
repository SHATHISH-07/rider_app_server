from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.deps import get_db
from schemas.driver import DriverCreate, DriverResponse
from crud import driver as driver_crud
import uuid

router = APIRouter(prefix="/drivers", tags=["Drivers"])

@router.post("/", response_model=DriverResponse)
def create_driver(driver: DriverCreate, db: Session = Depends(get_db)):
    return driver_crud.create_driver(db, driver)

@router.get("/", response_model=list[DriverResponse])
def get_drivers(db: Session = Depends(get_db)):
    return driver_crud.get_drivers(db)

@router.get("/{driver_id}", response_model=DriverResponse)
def get_driver(driver_id: uuid.UUID, db: Session = Depends(get_db)):
    driver = driver_crud.get_driver(db, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver

@router.put("/{driver_id}", response_model=DriverResponse)
def update_driver(driver_id: uuid.UUID, driver: DriverCreate, db: Session = Depends(get_db)):
    updated_driver = driver_crud.update_driver(db, driver_id, driver)
    if not updated_driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return updated_driver

@router.delete("/{driver_id}")
def delete_driver(driver_id: uuid.UUID, db: Session = Depends(get_db)):
    result = driver_crud.delete_driver(db, driver_id)
    if not result:
        raise HTTPException(status_code=404, detail="Driver not found")
    return result