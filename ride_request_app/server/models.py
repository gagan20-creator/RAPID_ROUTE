# File: ride_request_app/server/models.py

from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base

class Driver(Base):
    """
    Represents a driver in the database.
    """
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    # Status can be 'available', 'on_ride', 'offline'
    status = Column(String, default="available")


class RideRequest(Base):
    """
    Represents a ride request from a user.
    """
    __tablename__ = "ride_requests"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)
    destination = Column(String, index=True)
    # Status can be 'pending', 'accepted', 'completed', 'cancelled'
    status = Column(String, default="pending")

    # This links the ride to a driver. It's nullable because a ride
    # doesn't have a driver when it's first created.
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True)