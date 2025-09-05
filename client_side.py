import requests

BASE_URL = "http://127.0.0.1:5000"

def request_ride(rider_id, ride_type="quick", delay_minutes=0):
    payload = {
        "rider_id": rider_id,
        "ride_type": ride_type,
        "delay_minutes": delay_minutes
    }
    response = requests.post(f"{BASE_URL}/ride", json=payload)
    if response.status_code == 201:
        print("✅ Ride requested:", response.json())
    else:
        print("❌ Failed to request ride:", response.text)

def get_all_rides():
    response = requests.get(f"{BASE_URL}/rides")
    if response.status_code == 200:
        print("🚖 All rides:")
        for ride in response.json():
            print(ride)
    else:
        print("❌ Failed to fetch rides:", response.text)

# Example usage
if _name_ == "_main_":
    # Rider books a quick ride
    request_ride(rider_id=1, ride_type="quick")

    # Rider books a delayed ride (after 30 min)
    request_ride(rider_id=2, ride_type="delayed", delay_minutes=30)

    # View all rides
    get_all_rides()