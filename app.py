# app.py - Streamlit Web Application Interface
import streamlit as st
from data import routes, CITIES
from storage import bookings
from logic import (
    search_routes_logic, book_ticket_logic, cancel_booking_logic, 
    get_all_bookings, get_seat_availability
)

st.set_page_config(page_title="Smart Bus System", page_icon="🚌", layout="wide")

st.title("🚌 Smart Bus Ticket Booking & Reservation System (Web App)")
st.markdown("---")

menu = st.sidebar.radio(
    "Navigation Menu", 
    [
        "View Routes", 
        "Search Route", 
        "Book Ticket", 
        "View My Bookings", 
        "Cancel Booking", 
        "Seat Availability", 
        "Reports"
    ]
)

if menu == "View Routes":
    st.header("📋 Available Bus Routes")
    for r in routes:
        st.write(f"**{r['route_id']}** | {r['departure_city']} ➔ {r['destination_city']} | Departs: {r['departure_time']} | Fare: Rs. {r['ticket_price']} | Available: {r['available_seats']}/{r['total_seats']}")

elif menu == "Search Route":
    st.header("🔍 Search Routes")
    q = st.text_input("Enter city name or Route ID:")
    if q:
        matches = search_routes_logic(q)
        if matches:
            for m in matches:
                st.success(f"Found: {m['route_id']} ({m['departure_city']} ➔ {m['destination_city']}) - Available Seats: {m['available_seats']}")
        else:
            st.error("No matching routes found.")

elif menu == "Book Ticket":
    st.header("🎟️ Book a Ticket")
    route_map = {f"{r['route_id']} ({r['departure_city']} ➔ {r['destination_city']})": r for r in routes}
    selected = st.selectbox("Select Route", list(route_map.keys()))
    target = route_map[selected]
    
    with st.form("web_booking"):
        name = st.text_input("Passenger Name")
        age = st.number_input("Passenger Age", 1, 120, 20)
        seats = st.number_input("Seats", 1, 10, 1)
        sub = st.form_submit_button("Confirm Booking")
        
        if sub:
            ok, msg = book_ticket_logic(target, name, age, seats)
            if ok:
                st.balloons()
                st.success(f"🎉 Success! Booking ID: {msg}")
            else:
                st.error(msg)

elif menu == "View My Bookings":
    st.header("📋 My Bookings History")
    all_bookings = get_all_bookings()
    if not all_bookings:
        st.info("No bookings recorded yet.")
    else:
        booking_list = []
        for idx, b in enumerate(all_bookings, start=1):
            booking_list.append({
                "No.": idx,
                "Booking ID": b["booking_id"],
                "Passenger": b["passenger_name"],
                "Route": b["route_id"],
                "Journey": b["journey"],
                "Seats": b["seats"],
                "Total Fare": f"Rs. {b['total_fare']:,}",
                "Status": b["status"]
            })
        st.dataframe(booking_list, use_container_width=True)

elif menu == "Cancel Booking":
    st.header("❌ Cancel Booking")
    b_id = st.text_input("Enter Booking ID (e.g. B1001):")
    if st.button("Cancel Now"):
        ok, msg = cancel_booking_logic(b_id)
        if ok:
            st.success(msg)
        else:
            st.error(msg)

elif menu == "Seat Availability":
    st.header("🪑 Seat Availability Dashboard")
    availability = get_seat_availability()
    for item in availability:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"Route {item['route_id']}: {item['journey']}")
            st.progress(item['available'] / item['total'])
            st.write(f"**Available Seats:** {item['available']} / {item['total']}")
        with col2:
            st.write("### Status")
            st.write(item['status'])
        st.markdown("---")

elif menu == "Reports":
    st.header("📊 Analytics Report")
    all_bookings = get_all_bookings()
    total = len(all_bookings)
    conf = sum(1 for b in all_bookings if b["status"] == "Confirmed")
    canc = sum(1 for b in all_bookings if b["status"] == "Cancelled")
    res_seats = sum(b["seats"] for b in all_bookings if b["status"] == "Confirmed")
    rev = sum(b["total_fare"] for b in all_bookings if b["status"] == "Confirmed")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Bookings", total)
    c2.metric("Confirmed Bookings", conf)
    c3.metric("Cancelled Bookings", canc)

    c4, c5, _ = st.columns(3)
    c4.metric("Reserved Seats", res_seats)
    c5.metric("Confirmed Revenue", f"Rs. {rev:,}")