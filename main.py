# main.py - Console / Terminal Application Interface
from data import routes
from storage import bookings
from logic import (
    search_routes_logic, book_ticket_logic, cancel_booking_logic, 
    get_all_bookings, get_seat_availability
)

def main():
    while True:
        print("\n" + "="*45)
        print("SMART BUS TICKET BOOKING & RESERVATION SYSTEM")
        print("="*45)
        print("1. View Available Routes")
        print("2. Search for a Route")
        print("3. Book a Ticket")
        print("4. View My Bookings")
        print("5. Cancel a Booking")
        print("6. View Seat Availability")
        print("7. Exit")
        print("="*45)
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            print("\n--- AVAILABLE ROUTES ---")
            for r in routes:
                print(f"{r['route_id']} | {r['departure_city']} -> {r['destination_city']} | Departs: {r['departure_time']} | Fare: Rs.{r['ticket_price']} | Available: {r['available_seats']}/{r['total_seats']}")
        
        elif choice == "2":
            q = input("\nEnter city name or Route ID: ")
            matches = search_routes_logic(q)
            if matches:
                for m in matches:
                    print(f"Found: {m['route_id']} | {m['departure_city']} -> {m['destination_city']} | Available: {m['available_seats']}")
            else:
                print("No routes found.")
        
        elif choice == "3":
            r_id = input("\nEnter Route ID (e.g., R101): ").upper()
            target = next((r for r in routes if r['route_id'] == r_id), None)
            if target:
                name = input("Enter Passenger Name: ")
                try:
                    age = int(input("Enter Age: "))
                    seats = int(input("Enter Number of Seats: "))
                    ok, msg = book_ticket_logic(target, name, age, seats)
                    if ok:
                        print(f"🎉 Success! Booking ID: {msg}")
                    else:
                        print(f"❌ {msg}")
                except ValueError:
                    print("❌ Invalid numeric input for age or seats.")
            else:
                print("❌ Route not found.")
        
        elif choice == "4":
            print("\n--- MY BOOKINGS ---")
            all_b = get_all_bookings()
            if not all_b:
                print("No bookings found.")
            else:
                for b in all_b:
                    print(f"ID: {b['booking_id']} | Passenger: {b['passenger_name']} | Route: {b['route_id']} | Seats: {b['seats']} | Status: {b['status']}")
        
        elif choice == "5":
            b_id = input("\nEnter Booking ID to cancel: ")
            ok, msg = cancel_booking_logic(b_id)
            if ok:
                print(f"✅ {msg}")
            else:
                print(f"❌ {msg}")
        
        elif choice == "6":
            print("\n--- SEAT AVAILABILITY ---")
            for item in get_seat_availability():
                print(f"Route {item['route_id']} ({item['journey']}): {item['available']}/{item['total']} available [{item['status']}]")
        
        elif choice == "7":
            print("Thank you for using Smart Bus System. Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()