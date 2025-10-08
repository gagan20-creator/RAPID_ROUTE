# File: ride_request_app/create_tables.py (Corrected)

from server.database import engine
# --- IMPORTANT CHANGE: Import the models themselves ---
from server.models import Base, Driver, RideRequest

def main():
    """Creates all database tables."""
    print("Creating database tables...")
    # By importing Driver and RideRequest, we ensure they are registered
    # with Base.metadata before we call create_all()
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    main()