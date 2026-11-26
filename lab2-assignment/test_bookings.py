import httpx

BASE_URL = "http://127.0.0.1:8000"

with httpx.Client(base_url=BASE_URL) as client:

    # Add a room
    r = client.post("/rooms", json={
        "room_id": "B205",
        "building": "Main Building",
        "capacity": 30
    })
    print("Add room:", r.status_code)

    # Add the same room again
    r = client.post("/rooms", json={
        "room_id": "B205",
        "building": "Main Building",
        "capacity": 30
    })
    print("Duplicate room:", r.status_code)

    # Get all rooms
    r = client.get("/rooms")
    print("Get rooms:", r.status_code)

    # Get one room
    r = client.get("/rooms/B205")
    print("Get room:", r.status_code)

    # Unknown room
    r = client.get("/rooms/B999")
    print("Unknown room:", r.status_code)

    # Create a booking
    booking = {
        "room_id": "B205",
        "date": "2026-12-01",
        "start_hour": 10,
        "end_hour": 12,
        "purpose": "Study group"
    }

    r = client.put("/bookings/booking1", json=booking)
    print("Create booking:", r.status_code)

    # Send the same booking again
    r = client.put("/bookings/booking1", json=booking)
    print("Retry booking:", r.status_code)

    # Overlapping booking
    overlap = {
        "room_id": "B205",
        "date": "2026-12-01",
        "start_hour": 11,
        "end_hour": 13,
        "purpose": "Meeting"
    }

    r = client.put("/bookings/booking2", json=overlap)
    print("Overlapping booking:", r.status_code)

    # Invalid hours
    invalid = {
        "room_id": "B205",
        "date": "2026-12-01",
        "start_hour": 15,
        "end_hour": 14,
        "purpose": "Test"
    }

    r = client.put("/bookings/booking3", json=invalid)
    print("Invalid hours:", r.status_code)

    # Unknown room booking
    unknown = {
        "room_id": "B999",
        "date": "2026-12-01",
        "start_hour": 10,
        "end_hour": 12,
        "purpose": "Test"
    }

    r = client.put("/bookings/booking4", json=unknown)
    print("Unknown room booking:", r.status_code)

    # Get booking
    r = client.get("/bookings/booking1")
    print("Get booking:", r.status_code)

    # Get all bookings
    r = client.get("/bookings")
    print("Get all bookings:", r.status_code)
    
    # Unknown booking
    r = client.get("/bookings/booking999")
    print("Unknown booking:", r.status_code)
    # Delete booking
    r = client.delete("/bookings/booking1")
    print("Delete booking:", r.status_code)

    # Delete missing booking
    r = client.delete("/bookings/booking1")
    print("Delete missing booking:", r.status_code)