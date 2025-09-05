from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uvicorn

# Import our database functions
from database import store_ride_request, get_all_ride_requests

# Pydantic models for request/response validation
class RideRequest(BaseModel):
    """Model for ride request data"""
    source_location: str
    dest_location: str
    user_id: str
    
class RideRequestResponse(BaseModel):
    """Model for ride request response"""
    id: Optional[int] = None
    source_location: str
    dest_location: str
    user_id: str
    timestamp: Optional[datetime] = None
    status: str = "pending"

# Create FastAPI app
app = FastAPI(title="Ride Request Server", version="1.0.0")

# Enable CORS for client requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Ride Request Server is running!",
        "storage": "Mock Storage (PostgreSQL not configured)",
        "endpoints": {
            "submit_ride": "POST /api/ride/request",
            "get_rides": "GET /api/rides",
            "health": "GET /"
        }
    }

@app.post("/api/ride/request", response_model=RideRequestResponse)
async def submit_ride_request(ride_request: RideRequest):
    """
    Submit a new ride request
    
    Parameters:
    - source_location: Starting location
    - dest_location: Destination location  
    - user_id: ID of the user requesting the ride
    """
    try:
        print(f"\n🚗 New ride request received!")
        print(f"   User ID: {ride_request.user_id}")
        print(f"   From: {ride_request.source_location}")
        print(f"   To: {ride_request.dest_location}")
        
        # Store the ride request
        stored_request = store_ride_request(
            source_location=ride_request.source_location,
            dest_location=ride_request.dest_location,
            user_id=ride_request.user_id
        )
        
        return RideRequestResponse(**stored_request)
        
    except Exception as e:
        print(f"❌ Error processing ride request: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process ride request: {str(e)}")

@app.get("/api/rides")
async def get_all_rides():
    """Get all ride requests"""
    rides = get_all_ride_requests()
    return rides

if __name__ == "__main__":
    print("🚀 Starting Ride Request Server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📖 API documentation at: http://localhost:8000/docs")
    print("💾 Using Mock Storage (PostgreSQL not configured)")
    print("-" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000)