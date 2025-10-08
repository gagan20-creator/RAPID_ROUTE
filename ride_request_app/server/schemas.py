# File: ride_request_app/server/schemas.py

from pydantic import BaseModel
from typing import Optional

# --- Driver Schemas ---

class DriverBase(BaseModel):
    name: str

class Driver(DriverBase):
    id: int
    status: str

    class Config:
        orm_mode = True

# --- RideRequest Schemas ---

class RideRequestBase(BaseModel):
    source: str
    destination: str

class RideRequestCreate(RideRequestBase):
    # No extra fields are needed when creating,
    # as status and driver_id have defaults or are set later.
    pass

class RideRequest(RideRequestBase):
    id: int
    status: str
    driver_id: Optional[int] = None

    class Config:
        orm_mode = True