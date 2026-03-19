from fastapi import FastAPI
from db.session import engine
from db.base import Base

import models.user
import models.driver
import models.ride

from api.v1 import user, driver, ride

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ride App Backend API")

@app.get("/")
def root():
    return {"message": "API is running "}

app.include_router(user.router, prefix="/api/v1")
app.include_router(driver.router, prefix="/api/v1")
app.include_router(ride.router, prefix="/api/v1")