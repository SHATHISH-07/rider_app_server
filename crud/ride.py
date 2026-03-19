from sqlalchemy.orm import Session
import models.ride as model
import schemas.ride as RideSchema
import uuid
from sqlalchemy import func
from crud import user as user_crud

def create_ride(db: Session, ride: RideSchema.RideCreate):
    user = user_crud.get_user(db, ride.user_id)
    if not user:
        raise ValueError("User does not exist")

    db_ride = model.Ride(
        user_id=ride.user_id,
        source=ride.source,
        destination=ride.destination
    )

    db.add(db_ride)
    db.commit()
    db.refresh(db_ride)
    return db_ride

def get_rides(db: Session):
    return db.query(model.Ride).filter(model.Ride.deleted_at.is_(None)).all()

def get_ride(db: Session, id: uuid.UUID):
    return db.query(model.Ride).filter(
            model.Ride.id == id,
            model.Ride.deleted_at.is_(None)
        ).first()

def delete_ride(db: Session, id: uuid.UUID):
    db_ride = db.query(model.Ride).filter(
            model.Ride.id == id,
            model.Ride.deleted_at.is_(None)
        ).first()

    if not db_ride:
        return None

    db_ride.deleted_at = func.now()
    db.commit()
    return {"message": "Ride deleted successfully"}