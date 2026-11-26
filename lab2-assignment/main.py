from datetime import date as Date
from typing import Dict, List
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field, root_validator

app = FastAPI()

# Room information
class Room(BaseModel):
    room_id: str
    building: str
    capacity: int = Field(gt=0)


# Booking information
class Booking(BaseModel):
    room_id: str
    date: Date
    start_hour: int = Field(ge=8, le=20)
    end_hour: int = Field(ge=8, le=20)
    purpose: str = Field(min_length=1)

    @root_validator(skip_on_failure=True)
    def check_hours(cls, values):
        if values["end_hour"] <= values["start_hour"]:
            raise ValueError("End hour must be after start hour")
        return values


# Store data
rooms: Dict[str, Room] = {}
bookings: Dict[str, Booking] = {}
# Add a new room
@app.post("/rooms", status_code=201)
def add_room(room: Room):
    if room.room_id in rooms:
        raise HTTPException(409, "Room already exists")

    rooms[room.room_id] = room
    return room


# Get all rooms
@app.get("/rooms")
def get_rooms():
    return list(rooms.values())


# Get one room
@app.get("/rooms/{room_id}")
def get_room(room_id: str):
    if room_id not in rooms:
        raise HTTPException(404, "Room not found")

    return rooms[room_id]


# Get all bookings
@app.get("/bookings")
def get_bookings():
    return bookings


# Get one booking
@app.get("/bookings/{booking_id}")
def get_booking(booking_id: str):
    if booking_id not in bookings:
        raise HTTPException(404, "Booking not found")

    return bookings[booking_id]


# Create or update a booking
@app.put("/bookings/{booking_id}", status_code=201)
def create_booking(
    booking_id: str,
    booking: Booking,
    response: Response
):
    if booking.room_id not in rooms:
        raise HTTPException(404, "Room not found")

    if booking_id in bookings:
        response.status_code = 200

    for old_id, old_booking in bookings.items():
        if old_id == booking_id:
            continue

        if (old_booking.room_id == booking.room_id
                and old_booking.date == booking.date):

            if (booking.start_hour < old_booking.end_hour
                    and old_booking.start_hour < booking.end_hour):
                raise HTTPException(409, "Booking overlaps")

    bookings[booking_id] = booking

    return {
        "booking_id": booking_id,
        "booking": booking
    }


# Delete a booking
@app.delete("/bookings/{booking_id}", status_code=204)
def delete_booking(booking_id: str):
    if booking_id not in bookings:
        raise HTTPException(404, "Booking not found")

    del bookings[booking_id]
    return Response(status_code=204)