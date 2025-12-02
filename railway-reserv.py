# ================================================================
# RAILWAY RESERVATION SYSTEM - MAIN APPLICATION
# ================================================================

import os
from datetime import datetime

# Data storage using dictionaries
users = {'admin': 'admin@123', 'user1': 'password123'}
trains = {
    101: {
        'name': 'Express A',
        'route': 'Delhi to Mumbai',
        'total_seats': 100,
        'available_seats': 85,
        'fare': 1500,
        'departure': '08:00 AM',
        'arrival': '08:00 PM'
    },
    102: {
        'name': 'Express B',
        'route': 'Mumbai to Bangalore',
        'total_seats': 80,
        'available_seats': 45,
        'fare': 1200,
        'departure': '10:00 AM',
        'arrival': '08:00 PM'
    },
    103: {
        'name': 'Express C',
        'route': 'Bangalore to Chennai',
        'total_seats': 120,
        'available_seats': 60,
        'fare': 900,
        'departure': '06:00 AM',
        'arrival': '02:00 PM'
    }
}
bookings = {}
current_user = None

# ================================================================
# UTILITY FUNCTIONS
# ================================================================

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header(title):
    """Display a formatted header"""
    print("=" * 60)
    print(title.center(60))
    print("=" * 60)

def display_menu(options):
    """Display menu options"""
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    print()

def get_input(prompt, input_type=str):
    """Get and validate user input"""
    while True:
        try:
            user_input = input(prompt)
            if input_type == int:
                return int(user_input)
            elif input_type == float:
                return float(user_input)
            else:
                return user_input
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")

def pause():
    """Pause and wait for user input"""
    input("\nPress Enter to continue...")

# ================================================================
# AUTHENTICATION MODULE
# ================================================================

def register():
    """Register a new user"""
    clear_screen()
    display_header("USER REGISTRATION")
    
    username = input("Enter username: ").strip()
    
    if username in users:
        print("Username already exists! Please choose a different username.")
        pause()
        return False
    
    password = input("Enter password: ").strip()
    confirm_password = input("Confirm password: ").strip()
    
    if password != confirm_password:
        print("Passwords do not match!")
        pause()
        return False
    
    if len(password) < 6:
        print("Password must be at least 6 characters long!")
        pause()
        return False
    
    users[username] = password
    bookings[username] = []
    print("Registration successful! You can now login.")
    pause()
    return True

def login():
    """Login user"""
    global current_user
    clear_screen()
    display_header("USER LOGIN")
    
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    
    if username in users and users[username] == password:
        current_user = username
        if username not in bookings:
            bookings[username] = []
        print("Login successful!")
        pause()
        return True
    else:
        print("Invalid username or password!")
        pause()
        return False

# ================================================================
# TRAIN MANAGEMENT MODULE
# ================================================================

def view_trains():
    """Display all available trains"""
    clear_screen()
    display_header("AVAILABLE TRAINS")
    
    print(f"{'Train ID':<10} {'Train Name':<15} {'Route':<30} {'Available Seats':<15} {'Fare':<10}")
    print("-" * 80)
    
    for train_id, details in trains.items():
        print(f"{train_id:<10} {details['name']:<15} {details['route']:<30} {details['available_seats']:<15} ₹{details['fare']:<9}")
    
    print()
    pause()

def view_train_details():
    """View detailed information about a train"""
    clear_screen()
    display_header("TRAIN DETAILS")
    
    view_trains()
    train_id = get_input("Enter Train ID to view details: ", int)
    
    if train_id not in trains:
        print("Invalid Train ID!")
        pause()
        return
    
    train = trains[train_id]
    clear_screen()
    display_header(f"DETAILS - {train['name']}")
    
    print(f"Train ID:          {train_id}")
    print(f"Train Name:        {train['name']}")
    print(f"Route:             {train['route']}")
    print(f"Total Seats:       {train['total_seats']}")
    print(f"Available Seats:   {train['available_seats']}")
    print(f"Fare per Ticket:   ₹{train['fare']}")
    print(f"Departure Time:    {train['departure']}")
    print(f"Arrival Time:      {train['arrival']}")
    
    print()
    pause()

# ================================================================
# BOOKING MODULE
# ================================================================

def book_ticket():
    """Book a railway ticket"""
    clear_screen()
    display_header("BOOK TICKET")
    
    view_trains()
    
    train_id = get_input("Enter Train ID to book: ", int)
    
    if train_id not in trains:
        print("Invalid Train ID!")
        pause()
        return
    
    num_seats = get_input("Enter number of seats to book: ", int)
    
    if num_seats <= 0:
        print("Invalid number of seats!")
        pause()
        return
    
    train = trains[train_id]
    
    if train['available_seats'] < num_seats:
        print(f"Not enough seats available! Only {train['available_seats']} seats available.")
        pause()
        return
    
    # Calculate total fare
    total_fare = train['fare'] * num_seats
    
    # Confirm booking
    print(f"\nBooking Summary:")
    print(f"Train Name:    {train['name']}")
    print(f"Route:         {train['route']}")
    print(f"Seats:         {num_seats}")
    print(f"Fare/Seat:     ₹{train['fare']}")
    print(f"Total Fare:    ₹{total_fare}")
    
    confirm = input("\nConfirm booking? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("Booking cancelled!")
        pause()
        return
    
    # Process booking
    train['available_seats'] -= num_seats
    booking_id = len(bookings[current_user]) + 1
    booking_details = {
        'booking_id': booking_id,
        'train_id': train_id,
        'train_name': train['name'],
        'seats': num_seats,
        'total_fare': total_fare,
        'booking_date': datetime.now().strftime("%d-%m-%Y %H:%M"),
        'status': 'Confirmed'
    }
    bookings[current_user].append(booking_details)
    
    print(f"\n{'*' * 60}")
    print("BOOKING CONFIRMED!".center(60))
    print(f"{'*' * 60}")
    print(f"Booking ID:       {booking_id}")
    print(f"Train:            {train['name']}")
    print(f"Seats Booked:     {num_seats}")
    print(f"Total Amount:     ₹{total_fare}")
    print(f"Booking Date:     {booking_details['booking_date']}")
    print(f"Status:           {booking_details['status']}")
    print(f"{'*' * 60}")
    
    pause()

# ================================================================
# CANCELLATION MODULE
# ================================================================

def cancel_ticket():
    """Cancel a railway ticket"""
    clear_screen()
    display_header("CANCEL TICKET")
    
    if not bookings[current_user]:
        print("You have no bookings to cancel!")
        pause()
        return
    
    # Display user's bookings
    print("Your Bookings:\n")
    for booking in bookings[current_user]:
        if booking['status'] == 'Confirmed':
            print(f"Booking ID: {booking['booking_id']} | Train: {booking['train_name']} | Seats: {booking['seats']} | Fare: ₹{booking['total_fare']}")
    
    print()
    booking_id = get_input("Enter Booking ID to cancel: ", int)
    
    # Find and cancel booking
    booking_found = False
    for booking in bookings[current_user]:
        if booking['booking_id'] == booking_id and booking['status'] == 'Confirmed':
            booking_found = True
            
            # Confirm cancellation
            confirm = input(f"\nCancel booking ID {booking_id}? This will refund ₹{booking['total_fare']}. (yes/no): ").strip().lower()
            
            if confirm == 'yes':
                # Update train seats
                train_id = booking['train_id']
                trains[train_id]['available_seats'] += booking['seats']
                
                # Update booking status
                booking['status'] = 'Cancelled'
                refund = int(booking['total_fare'] * 0.9)  # 10% cancellation charge
                
                print(f"\n{'*' * 60}")
                print("CANCELLATION CONFIRMED!".center(60))
                print(f"{'*' * 60}")
                print(f"Booking ID:       {booking_id}")
                print(f"Train:            {booking['train_name']}")
                print(f"Original Amount:  ₹{booking['total_fare']}")
                print(f"Cancellation Fee: ₹{booking['total_fare'] - refund}")
                print(f"Refund Amount:    ₹{refund}")
                print(f"Status:           Cancelled")
                print(f"{'*' * 60}")
            else:
                print("Cancellation aborted!")
            
            pause()
            return
    
    if not booking_found:
        print("Booking ID not found or already cancelled!")
        pause()

# ================================================================
# VIEW BOOKINGS MODULE
# ================================================================

def view_bookings():
    """View user's bookings"""
    clear_screen()
    display_header("YOUR BOOKINGS")
    
    if not bookings[current_user]:
        print("You have no bookings yet!")
        pause()
        return
    
    print(f"{'ID':<5} {'Train Name':<20} {'Seats':<8} {'Amount':<10} {'Date':<20} {'Status':<15}")
    print("-" * 80)
    
    for booking in bookings[current_user]:
        print(f"{booking['booking_id']:<5} {booking['train_name']:<20} {booking['seats']:<8} ₹{booking['total_fare']:<9} {booking['booking_date']:<20} {booking['status']:<15}")
    
    print()
    pause()

# ================================================================
# MAIN MENU
# ================================================================

def user_menu():
    """Display user menu"""
    while True:
        clear_screen()
        display_header(f"RAILWAY RESERVATION SYSTEM - Welcome {current_user}")
        
        options = [
            "View Available Trains",
            "View Train Details",
            "Book Ticket",
            "Cancel Ticket",
            "View My Bookings",
            "Logout"
        ]
        
        display_menu(options)
        choice = get_input("Enter your choice (1-6): ", int)
        
        if choice == 1:
            view_trains()
        elif choice == 2:
            view_train_details()
        elif choice == 3:
            book_ticket()
        elif choice == 4:
            cancel_ticket()
        elif choice == 5:
            view_bookings()
        elif choice == 6:
            print("Thank you for using Railway Reservation System!")
            break
        else:
            print("Invalid choice! Please try again.")
            pause()

def main():
    """Main application loop"""
    while True:
        clear_screen()
        display_header("RAILWAY RESERVATION SYSTEM")
        
        options = [
            "Login",
            "Register",
            "Exit"
        ]
        
        display_menu(options)
        choice = get_input("Enter your choice (1-3): ", int)
        
        if choice == 1:
            if login():
                user_menu()
        elif choice == 2:
            register()
        elif choice == 3:
            print("Thank you for using Railway Reservation System!")
            break
        else:
            print("Invalid choice! Please try again.")
            pause()

# ================================================================
# PROGRAM ENTRY POINT
# ================================================================

if __name__ == "__main__":
    main()
