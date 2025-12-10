from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import random
from . import models, schemas, database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/drivers", response_model=List[schemas.DriverResponse])
def get_all_drivers(db: Session = Depends(database.get_db)):
    return db.query(models.Driver).all()

@app.post("/driver/mark_available")
def mark_driver_available(action: schemas.RideAction, db: Session = Depends(database.get_db)):
    driver = db.query(models.Driver).filter(models.Driver.id == action.driver_id).first()
    if driver:
        driver.status = "available"
        db.commit()
    return {"message": "Driver is now available"}

@app.post("/ride_request", response_model=schemas.RideResponse)
def create_ride(ride: schemas.RideRequestCreate, db: Session = Depends(database.get_db)):
    dist = round(random.uniform(2.5, 18.0), 1)
    fare = round(40.00 + (12.00 * dist), 0)

    incentive = 0.0
    is_delayed = False
    
    if ride.booking_type == "flexible" and ride.initial_delay > 0:
        is_delayed = True
        base_incentive_factor = 200.0
        sim_dist = random.uniform(2.0, 5.0) 
        incentive = round(base_incentive_factor / sim_dist, 0)
        
        if ride.ad_watched:
            incentive = incentive * 0.80

    db_ride = models.RideRequest(
        **ride.dict(exclude={'initial_delay'}),
        distance_km=dist,
        base_fare=fare,
        final_fare=fare,
        driver_incentive=incentive,
        is_delayed_mode=is_delayed,
        delay_minutes=ride.initial_delay if ride.booking_type == "flexible" else 0,
        rejected_by="" 
    )
    db.add(db_ride)
    db.commit()
    db.refresh(db_ride)
    return db_ride

@app.get("/rides", response_model=List[schemas.RideResponse])
def get_rides(status: str = None, driver_id: int = None, viewer_id: int = None, db: Session = Depends(database.get_db)):
    query = db.query(models.RideRequest)
    
    if status:
        query = query.filter(models.RideRequest.status == status)
    if driver_id:
        query = query.filter(models.RideRequest.driver_id == driver_id)
        
    results = query.all()
    
    # HIDE LOGIC: If the viewer (driver) is in the rejected_by list, don't show the ride
    if viewer_id:
        filtered_results = []
        for r in results:
            rejected_list = (r.rejected_by or "").split(",")
            if str(viewer_id) not in rejected_list:
                filtered_results.append(r)
        return filtered_results
        
    return results

@app.post("/accept_ride")
def accept_ride(action: schemas.RideAction, db: Session = Depends(database.get_db)):
    ride = db.query(models.RideRequest).filter(models.RideRequest.id == action.ride_id).first()
    driver = db.query(models.Driver).filter(models.Driver.id == action.driver_id).first()
    
    if not ride or not driver:
        raise HTTPException(status_code=404, detail="Ride or Driver not found")
        
    ride.driver_id = driver.id
    driver.status = "busy"

    if ride.booking_type == "flexible" and ride.is_delayed_mode:
        ride.status = "waiting_for_start"
        ride.scheduled_time = datetime.utcnow() + timedelta(minutes=ride.delay_minutes)
        ride.final_fare += ride.driver_incentive
    else:
        ride.status = "assigned"

    db.commit()
    return {"message": "Ride accepted"}

@app.post("/propose_delay")
def propose_delay(proposal: schemas.DelayProposal, db: Session = Depends(database.get_db)):
    ride = db.query(models.RideRequest).filter(models.RideRequest.id == proposal.ride_id).first()
    ride.status = "offering_delay"
    ride.is_delayed_mode = True
    ride.delay_minutes = proposal.delay_minutes
    ride.ad_watched = proposal.ad_watched
    db.commit()
    return {"message": "Delay proposed"}

@app.post("/respond_to_delay")
def respond_to_delay(response: schemas.DelayResponse, db: Session = Depends(database.get_db)):
    ride = db.query(models.RideRequest).filter(models.RideRequest.id == response.ride_id).first()
    driver = db.query(models.Driver).filter(models.Driver.id == ride.driver_id).first()
    
    if response.accepted:
        ride.status = "waiting_for_start"
        ride.scheduled_time = datetime.utcnow() + timedelta(minutes=ride.delay_minutes)
        ride.final_fare += ride.driver_incentive 
    else:
        # 1. Block this driver from seeing the ride again
        current_rejected = ride.rejected_by or ""
        if current_rejected:
            ride.rejected_by = f"{current_rejected},{driver.id}"
        else:
            ride.rejected_by = f"{driver.id}"

        # 2. Add Incentive for NEXT driver
        simulated_next_driver_dist = random.uniform(0.5, 10.0)
        base_incentive_factor = 200.0
        calculated_incentive = base_incentive_factor / simulated_next_driver_dist
        
        if ride.ad_watched:
            calculated_incentive = calculated_incentive * 0.80 

        # 3. Reset to Pending
        ride.status = "pending"
        ride.driver_id = None
        ride.is_delayed_mode = False 
        ride.driver_incentive = round(calculated_incentive, 0)
        
        driver.status = "available"
        
    db.commit()
    return {"status": ride.status}

@app.post("/force_ready")
def force_ready(action: schemas.RideAction, db: Session = Depends(database.get_db)):
    ride = db.query(models.RideRequest).filter(models.RideRequest.id == action.ride_id).first()
    if ride:
        ride.status = "assigned" 
        db.commit()
    return {"message": "Driver notified"}

@app.post("/start_ride")
def start_ride(action: schemas.RideAction, db: Session = Depends(database.get_db)):
    ride = db.query(models.RideRequest).filter(models.RideRequest.id == action.ride_id).first()
    ride.status = "in_progress"
    db.commit()
    return {"message": "Ride started"}

@app.post("/complete_ride")
def complete_ride(action: schemas.RideAction, db: Session = Depends(database.get_db)):
    ride = db.query(models.RideRequest).filter(models.RideRequest.id == action.ride_id).first()
    driver = db.query(models.Driver).filter(models.Driver.id == ride.driver_id).first()
    
    ride.status = "completed"
    driver.balance += ride.final_fare
    db.commit()
    return {"message": "Ride completed"}