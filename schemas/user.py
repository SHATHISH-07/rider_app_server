from pydantic import BaseModel
from datetime import datetime
import uuid

class UserCreate(BaseModel):
    name:str
    phone:str

class UserResponse(BaseModel):
    id:uuid.UUID
    name:str
    phone:str
    created_at:datetime
    updated_at:datetime | None
        
    class Config:
        from_attribute=True