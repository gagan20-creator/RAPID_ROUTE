from datetime import datetime
from typing import List, Dict, Any

# Mock storage for ride requests
mock_storage: List[Dict[Any, Any]] = []
mock_id_counter = 1

def store_ride_request(source_location: str, dest_location: str, user_id: str) -> Dict[Any, Any]:
    """Store ride request in mock storage"""
    global mock_id_counter
    
    print("📝 We will store this data in Postgres now")
    
    mock_request = {
        "id": mock_id_counter,
        "source_location": source_location,
        "dest_location": dest_location,
        "user_id": user_id,
        "timestamp": datetime.utcnow(),
        "status": "pending"
    }
    
    mock_storage.append(mock_request)
    mock_id_counter += 1
    
    print("🚗 Ride Request Data:")
    print(f"   ID: {mock_request['id']}")
    print(f"   Source: {source_location}")
    print(f"   Destination: {dest_location}")
    print(f"   User ID: {user_id}")
    print(f"   Timestamp: {mock_request['timestamp']}")
    print(f"   Status: {mock_request['status']}")
    print("-" * 50)
    
    return mock_request

def get_all_ride_requests() -> List[Dict[Any, Any]]:
    """Get all stored ride requests"""
    return mock_storage