from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DriverBase(BaseModel):
    name: str
    car_model: str

class DriverCreate(DriverBase):
    pass

class DriverResponse(DriverBase):
    id: int
    status: str
    balance: float
    class Config:
        from_attributes = True

class RideRequestCreate(BaseModel):
    rider_name: str
    source: str
    destination: str
    booking_type: str = "normal" 
    initial_delay: int = 0        
    ad_watched: bool = False      

class DelayProposal(BaseModel):
    ride_id: int
    delay_minutes: int
    ad_watched: bool = False

class DelayResponse(BaseModel):
    ride_id: int
    accepted: bool

class RideAction(BaseModel):
    ride_id: int
    driver_id: Optional[int] = None

class RideResponse(BaseModel):
    id: int
    rider_name: str
    source: str
    destination: str
    status: str
    driver_id: Optional[int]
    distance_km: float
    is_delayed_mode: bool
    delay_minutes: int
    ad_watched: bool
    booking_type: str
    base_fare: float
    driver_incentive: float
    final_fare: float
    
    # This allows the frontend to access ride.driver.name
    driver: Optional[DriverResponse] = None

    class Config:
        from_attributes = True