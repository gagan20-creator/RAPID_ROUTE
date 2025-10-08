# File: ride_request_app/server/crud.py

from sqlalchemy.orm import Session
from . import models, schemas

# --- Read Operations ---

def get_ride(db: Session, ride_id: int):
    """Fetches a single ride by its ID."""
    return db.query(models.RideRequest).filter(models.RideRequest.id == ride_id).first()

def get_pending_rides(db: Session):
    """Fetches all rides with a 'pending' status."""
    return db.query(models.RideRequest).filter(models.RideRequest.status == 'pending').all()

def get_driver_rides(db: Session, driver_id: int):
    """Fetches all rides assigned to a specific driver."""
    return db.query(models.RideRequest).filter(models.RideRequest.driver_id == driver_id).all()

def get_driver(db: Session, driver_id: int):
    """Fetches a single driver by their ID."""
    return db.query(models.Driver).filter(models.Driver.id == driver_id).first()


# --- Create Operations ---

def create_ride_request(db: Session, ride: schemas.RideRequestCreate):
    """Creates a new ride request in the database."""
    # Create a new SQLAlchemy model instance from the schema data
    db_ride = models.RideRequest(
        source=ride.source,
        destination=ride.destination,
        status='pending' # Default status on creation
    )
    db.add(db_ride)  # Add the new ride to the session
    db.commit()     # Commit the transaction to the database
    db.refresh(db_ride) # Refresh the instance to get the new ID from the DB
    return db_ride


# --- Update Operations ---

def update_ride_status(db: Session, ride_id: int, status: str, driver_id: int = None):
    """Updates the status and optionally the driver of a ride."""
    db_ride = get_ride(db, ride_id)
    if db_ride:
        db_ride.status = status
        if driver_id:
            db_ride.driver_id = driver_id
        db.commit()
        db.refresh(db_ride)
    return db_ride