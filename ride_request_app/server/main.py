# File: ride_request_app/server/main.py
from pathlib import Path
from fastapi import FastAPI, Depends, Request, Form, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

# This line creates the database tables if they don't exist.
# It uses the models we defined in models.py.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ADD THESE TWO LINES
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# --- Dependency for Database Sessions ---
def get_db():
    """
    This function is a dependency that provides a database session
    for each request and ensures it's closed afterward.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- HTML Serving Endpoints ---

@app.get("/")
def serve_user_homepage(request: Request):
    """Serves the user's ride booking page (index.html)."""
    # The 'request' parameter is required by Jinja2.
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/driver")
def serve_driver_dashboard(request: Request, driver_id: int, db: Session = Depends(get_db)):
    """Serves the driver's dashboard (driver.html)."""
    driver = crud.get_driver(db, driver_id=driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")

    # Fetch data needed for the dashboard
    pending_rides = crud.get_pending_rides(db)
    my_rides = crud.get_driver_rides(db, driver_id=driver_id)

    # Pass the data to the template
    return templates.TemplateResponse("driver.html", {
        "request": request,
        "driver": driver,
        "pending_rides": pending_rides,
        "my_rides": my_rides
    })

# --- API & Form Endpoints ---

@app.post("/ride_request/")
def create_ride_request_from_form(
    source: str = Form(...),
    destination: str = Form(...),
    db: Session = Depends(get_db)
):
    """Endpoint to handle the ride booking form submission from index.html."""
    ride_schema = schemas.RideRequestCreate(source=source, destination=destination)
    crud.create_ride_request(db=db, ride=ride_schema)
    # Redirect back to the homepage after successful booking
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/accept_ride/{ride_id}")
def accept_ride(
    ride_id: int,
    driver_id: int = Form(...),
    db: Session = Depends(get_db)
):
    """Endpoint for a driver to accept a pending ride."""
    crud.update_ride_status(db, ride_id=ride_id, status='accepted', driver_id=driver_id)
    # Redirect back to the driver's dashboard
    return RedirectResponse(url=f"/driver?driver_id={driver_id}", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/complete_ride/{ride_id}")
def complete_ride(
    ride_id: int,
    driver_id: int = Form(...),
    db: Session = Depends(get_db)
):
    """Endpoint for a driver to mark a ride as complete."""
    crud.update_ride_status(db, ride_id=ride_id, status='completed')
    # Redirect back to the driver's dashboard
    return RedirectResponse(url=f"/driver?driver_id={driver_id}", status_code=status.HTTP_303_SEE_OTHER)