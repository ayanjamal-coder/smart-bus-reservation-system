# logic.py - Core Business Logic, Validations, and Operations
import random
from data import routes, CITIES
from storage import bookings, issued_booking_ids

def generate_booking_id():
    """Generate a unique booking ID using sets."""
    while True:
        new_id = f"B{random.randint(1000, 9999)}"
        if new_id not in issued_booking_ids:
            issued_booking_ids.add(new_id)
            return new_id

def search_routes_logic(query):
    """Search routes by ID or city name case-insensitively."""
    query = query.strip().lower()
    matches = []
    for r in routes:
        if (query == r["route_id"].lower() or 
            query in r["departure_city"].lower() or 
            query in r["destination_city"].lower()):
            matches.append(r)
    return matches

def book_ticket_logic(target_route, p_name, p_age, seats_requested):
    """Validate and process ticket booking."""
    if not p_name.strip():
        return False, "Passenger name cannot be empty."
    if p_age <= 0:
        return False, "Age must be a positive integer."
    if seats_requested <= 0:
        return False, "Seat quantity must be greater than zero."
    if seats_requested > target_route["available_seats"]:
        return False, f"Not enough seats available! Only {target_route['available_seats']} left."

    total_fare = target_route["ticket_price"] * seats_requested
    b_id = generate_booking_id()
    
    target_route["available_seats"] -= seats_requested

    new_booking = {
        "booking_id": b_id,
        "passenger_name": p_name.strip(),
        "passenger_age": int(p_age),
        "route_id": target_route["route_id"],
        "journey": f"{target_route['departure_city']} ➔ {target_route['destination_city']}",
        "seats": int(seats_requested),
        "total_fare": total_fare,
        "status": "Confirmed"
    }
    bookings.append(new_booking)
    return True, b_id

def cancel_booking_logic(b_id):
    """Cancel a booking and restore seats once."""
    b_id = b_id.strip().upper()
    target_b = next((b for b in bookings if b["booking_id"] == b_id), None)
    
    if not target_b:
        return False, "Booking ID not found."
    if target_b["status"] == "Cancelled":
        return False, "This booking is already cancelled."

    target_b["status"] = "Cancelled"
    r_obj = next(r for r in routes if r["route_id"] == target_b["route_id"])
    r_obj["available_seats"] += target_b["seats"]
    
    return True, f"Booking {b_id} cancelled successfully! {target_b['seats']} seats restored."

def get_all_bookings():
    """Return all booking records."""
    return bookings

def get_seat_availability():
    """Return seat availability status for all routes."""
    availability_data = []
    for r in routes:
        avail = r["available_seats"]
        total = r["total_seats"]
        status = "🟢 Available" if avail == total else ("🟡 Partially Booked" if avail > 0 else "🔴 Fully Booked")
        availability_data.append({
            "route_id": r["route_id"],
            "journey": f"{r['departure_city']} ➔ {r['destination_city']}",
            "available": avail,
            "total": total,
            "status": status
        })
    return availability_data