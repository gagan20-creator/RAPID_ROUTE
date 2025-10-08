# File: ride_request_app/add_drivers.py

from server.database import SessionLocal
from server.models import Driver

def add_initial_drivers():
    """
    Connects to the database and adds a predefined list of drivers
    if they don't already exist.
    """
    db = SessionLocal()
    
    drivers_to_add = ["John", "Tom", "Jerry"]
    
    print("Checking for and adding initial drivers...")
    
    try:
        for name in drivers_to_add:
            # Check if the driver already exists to avoid duplicates
            exists = db.query(Driver).filter(Driver.name == name).first()
            if not exists:
                new_driver = Driver(name=name, status="available")
                db.add(new_driver)
                print(f"  - Added driver: {name}")
            else:
                print(f"  - Driver '{name}' already exists. Skipping.")
        
        db.commit()
        print("\nSuccessfully added drivers to the database.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback() # Roll back changes in case of an error
    finally:
        db.close()

if __name__ == "__main__":
    add_initial_drivers()