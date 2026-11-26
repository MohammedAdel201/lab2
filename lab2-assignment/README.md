# Lab Assignment 2
## Campus Room Booking Service

### 1. API Design

The API has the following operations:

| Method | URI | Request Body | Success Code | Error Code |
|---|---|---|---|---|
| POST | /rooms | Room ID, building, capacity | 201 | 409, 422 |
| GET | /rooms | No body | 200 | None |
| GET | /rooms/{room_id} | No body | 200 | 404 |
| GET | /bookings | No body | 200 | None |
| PUT | /bookings/{booking_id} | Room ID, date, start hour, end hour, purpose | 201 / 200 | 404, 409, 422 |
| GET | /bookings/{booking_id} | No body | 200 | 404 |
| DELETE | /bookings/{booking_id} | No body | 204 | 404 |