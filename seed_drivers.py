import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app import models

def seed():
    db = SessionLocal()
    print("Clearing existing data...")
    try:
        db.query(models.RideRequest).delete()
        db.query(models.Driver).delete()
        db.commit()
    except Exception as e:
        print(f"Error clearing data: {e}")
        db.rollback()
        return

    print("Seeding new drivers...")
    drivers_data = [
        ("John Doe", "Toyota Prius"),
        ("Jane Smith", "Tesla Model 3"),
        ("Mike Ross", "Honda Civic"),
        ("Sarah Connor", "Ford Mustang"),
        ("Bruce Wayne", "Lamborghini"),
        ("Peter Parker", "Bike"),
        ("Clark Kent", "Flying"),
    ]

    for name, car in drivers_data:
        driver = models.Driver(name=name, car_model=car, status="available", balance=0.0)
        db.add(driver)
    
    db.commit()
    print("Seeded 7 drivers successfully.")
    db.close()

if __name__ == "__main__":
    seed()