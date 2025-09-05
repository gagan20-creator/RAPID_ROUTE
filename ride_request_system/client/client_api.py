import requests
import json
from typing import Dict, Any

class RideRequestClient:
    """Client API for submitting ride requests"""
    
    def __init__(self, server_url: str = "http://localhost:8000"):
        self.server_url = server_url
        self.session = requests.Session()
        
    def submit_ride_request(self, source_location: str, dest_location: str, user_id: str) -> Dict[Any, Any]:
        """
        Submit a ride request to the server
        
        Args:
            source_location (str): Starting location
            dest_location (str): Destination location
            user_id (str): User ID
            
        Returns:
            dict: Response from server
        """
        endpoint = f"{self.server_url}/api/ride/request"
        
        payload = {
            "source_location": source_location,
            "dest_location": dest_location,
            "user_id": user_id
        }
        
        try:
            print(f"📤 Sending ride request to server...")
            print(f"   Endpoint: {endpoint}")
            print(f"   Payload: {json.dumps(payload, indent=2)}")
            
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            
            result = response.json()
            print(f"✅ Success! Server response:")
            print(f"   {json.dumps(result, indent=2, default=str)}")
            
            return result
            
        except requests.exceptions.ConnectionError:
            error_msg = f"❌ Cannot connect to server at {self.server_url}. Make sure server is running!"
            print(error_msg)
            return {"error": error_msg}
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"❌ HTTP Error: {e}"
            print(error_msg)
            return {"error": error_msg}
            
        except Exception as e:
            error_msg = f"❌ Unexpected error: {e}"
            print(error_msg)
            return {"error": error_msg}
    
    def get_all_rides(self) -> Dict[Any, Any]:
        """Get all ride requests from server"""
        endpoint = f"{self.server_url}/api/rides"
        
        try:
            response = self.session.get(endpoint)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def check_server_status(self) -> Dict[Any, Any]:
        """Check if server is running"""
        try:
            response = self.session.get(self.server_url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": f"Server not reachable: {e}"}

# Example usage and testing
if __name__ == "__main__":
    print("🚗 Ride Request Client API")
    print("=" * 50)
    
    # Create client instance
    client = RideRequestClient()
    
    # Check server status
    print("\n1️⃣ Checking server status...")
    status = client.check_server_status()
    print(f"Server status: {status}")
    
    if "error" not in status:
        # Test ride request submission
        print("\n2️⃣ Submitting test ride request...")
        response = client.submit_ride_request(
            source_location="Downtown Mall",
            dest_location="Airport Terminal 1", 
            user_id="user123"
        )
        
        # Get all rides
        print("\n3️⃣ Fetching all ride requests...")
        all_rides = client.get_all_rides()
        print(f"All rides: {json.dumps(all_rides, indent=2, default=str)}")
    else:
        print("❌ Server is not running. Please start the server first!")
        print("💡 Run: python server/main.py")