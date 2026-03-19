from pydantic import BaseModel
from datetime import datetime
import uuid

class DriverCreate(BaseModel):
    name:str
    phone:str
    vehicle_no:str
    
class DriverResponse(BaseModel):
    id:uuid.UUID
    name:str
    phone:str
    vehicle_no:str
    created_at:datetime
    updated_at:datetime | None

    class Config:
        from_attribute=True