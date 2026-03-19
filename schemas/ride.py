from pydantic import BaseModel
from datetime import datetime
import uuid

class RideCreate(BaseModel):
    user_id:uuid.UUID
    source:str
    destination:str

class RideResponse(BaseModel):
    id:uuid.UUID
    user_id:uuid.UUID
    driver_id:uuid.UUID | None
    source:str
    destination:str
    status:str
    created_at:datetime
    updated_at:datetime | None

    class Config:
        from_attribute=True