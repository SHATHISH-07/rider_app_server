from sqlalchemy.orm import Session
import models.user as model
import schemas.user as UserSchema
import uuid
from sqlalchemy import func

def create_user(db: Session, user: UserSchema.UserCreate):
    db_user = model.User(
        name=user.name,
        phone=user.phone
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_users(db: Session):
    return db.query(model.User).filter(model.User.deleted_at.is_(None)).all()

def get_user(db: Session, id: uuid.UUID):
    return db.query(model.User).filter(
            model.User.id == id,
            model.User.deleted_at.is_(None)
        ).first()

def update_user(db: Session, id: uuid.UUID, user: UserSchema.UserCreate):
    db_user = db.query(model.User).filter(
        model.User.id == id,
        model.User.deleted_at.is_(None)
    ).first()

    if not db_user:
        return None

    db_user.name = user.name
    db_user.phone = user.phone
    db_user.updated_at = func.now()
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, id: uuid.UUID):
    db_user = db.query(model.User).filter(
            model.User.id == id,
            model.User.deleted_at.is_(None)
        ).first()

    if not db_user:
        return None

    db_user.deleted_at = func.now()
    db.commit()
    return {"message": "User deleted successfully"}