from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    car_model = Column(String)
    status = Column(String, default="available")  # 'available', 'busy'
    balance = Column(Float, default=0.0)

class RideRequest(Base):
    __tablename__ = "ride_requests"

    id = Column(Integer, primary_key=True, index=True)
    rider_name = Column(String)
    source = Column(String)
    destination = Column(String)
    
    status = Column(String, default="pending")
    booking_type = Column(String, default="normal") # normal, flexible
    
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    scheduled_time = Column(DateTime, nullable=True)
    
    distance_km = Column(Float, default=0.0)
    
    is_delayed_mode = Column(Boolean, default=False)
    delay_minutes = Column(Integer, default=0)
    ad_watched = Column(Boolean, default=False) 
    
    base_fare = Column(Float, default=0.0)
    driver_incentive = Column(Float, default=0.0) 
    final_fare = Column(Float, default=0.0)
    
    # Stores IDs of drivers who rejected this ride (e.g., "1,4,7")
    rejected_by = Column(String, default="") 
    
    driver = relationship("Driver")