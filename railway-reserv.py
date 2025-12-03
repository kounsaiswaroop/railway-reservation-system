# ================================================================
# RAILWAY RESERVATION SYSTEM – PYTHON + MYSQL (GITHUB VERSION)
# ================================================================

import mysql.connector
import os
from datetime import datetime

# ------------------------------------------------
# DB CONFIG – VALUES COME FROM ENVIRONMENT
# ------------------------------------------------
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')        # change via environment
DB_PASS = os.getenv('DB_PASS', 'password')    # dummy default, DO NOT use in production
DB_NAME = os.getenv('DB_NAME', 'railway')     # can be overridden


# ================================================================
# LOW-LEVEL DB HELPERS
# ================================================================
def get_raw_connection(no_db=False):
    """Return MySQL connection. If no_db=True, do not select database."""
    try:
        kwargs = {
            "host": DB_HOST,
            "user": DB_USER,
            "passwd": DB_PASS,
            "ssl_disabled": True      # important for typical local setups
        }
        if not no_db:
            kwargs["database"] = DB_NAME
        con = mysql.connector.connect(**kwargs)
        con.autocommit = True
        return con
    except mysql.connector.Error as err:
        print(f"[DB ERROR] {err}")
        return None


def init_database_and_tables():
    """Create database + tables + sample trains if needed."""
    # 1. Create database if not exists
    con = get_raw_connection(no_db=True)
    if not con:
        print("Cannot connect to MySQL. Check server & credentials.")
        return False
    cur = con.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cur.close()
    con.close()

    # 2. Connect to railway DB
    con = get_raw_connection()
    if not con:
        print("Cannot connect to DB after creation.")
        return False
    cur = con.cursor()

    # user_accounts table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_accounts (
            fname VARCHAR(100),
            lname VARCHAR(100),
            user_name VARCHAR(100) PRIMARY KEY,
            password VARCHAR(100),
            phno VARCHAR(15),
            gender VARCHAR(50),
            dob VARCHAR(50),
            age VARCHAR(4)
        )
    """)

    # trains table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS trains (
            train_id INT PRIMARY KEY,
            train_name VARCHAR(100),
            route VARCHAR(100),
            total_seats INT,
            available_seats INT,
            fare FLOAT,
            departure_time VARCHAR(20),
            arrival_time VARCHAR(20)
        )
    """)

    # bookings table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS railway (
            booking_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            phno VARCHAR(15),
            age INT,
            gender VARCHAR(50),
            from_f VARCHAR(100),
            to_t VARCHAR(100),
            date_d VARCHAR(20),
            booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 3. Insert sample trains (ignore duplicates)
    sample_trains = [
        (101, 'Express A', 'Delhi to Mumbai', 100, 85, 1500, '08:00 AM', '08:00 PM'),
        (102, 'Express B', 'Mumbai to Bangalore', 80, 45, 1200, '10:00 AM', '08:00 PM'),
        (103, 'Express C', 'Bangalore to Chennai', 120, 60, 900, '06:00 AM', '02:00 PM'),
        (104, 'Express D', 'Chennai to Kolkata', 90, 75, 1800, '02:00 PM', '12:00 AM'),
        (105, 'Express E', 'Kolkata to Delhi', 110, 50, 2000, '04:00 AM', '06:00 PM')
    ]
    cur.executemany("""
        INSERT IGNORE INTO trains
        (train_id, train_name, route, total_seats, available_seats, fare, departure_time, arrival_time)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, sample_trains)

    cur.close()
    con.close()
    return True


# ================================================================
# UTILITY FUNCTIONS
# ================================================================
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def display_header(title):
    print("=" * 70)
    print(title.center(70))
    print("=" * 70)


def display_menu(options):
    for i, opt in enumerate(options, start=1):
        print(f"{i}. {opt}")
    print()


def get_input(prompt, cast=str):
    while True:
        try:
            value = input(prompt)
            if cast is int:
                return int(value)
            if cast is float:
                return float(value)
            return value
        except ValueError:
            print(f"Please enter a valid {cast.__name__}.")


def pause():
    input("\nPress Enter to continue...")


# ================================================================
# AUTHENTICATION: REGISTER + LOGIN
# ================================================================
def register():
    clear_screen()
    display_header("USER REGISTRATION")
    con = get_raw_connection()
    if not con:
        pause()
        return False
    cur = con.cursor()

    fname = input("First name: ").strip()
    lname = input("Last name: ").strip()
    user_name = input("Username: ").strip()
    password = input("Password: ").strip()
    confirm = input("Confirm password: ").strip()

    if password != confirm:
        print("Passwords do not match.")
        cur.close()
        con.close()
        pause()
        return False
    if len(password) < 6:
        print("Password must be at least 6 characters.")
        cur.close()
        con.close()
        pause()
        return False

    phno = input("Phone number: ").strip()
    print("M = MALE\nF = FEMALE\nN = NOT TO MENTION")
    gender_code = input("Gender (M/F/N): ").strip().upper()
    gender_map = {'M': 'MALE', 'F': 'FEMALE', 'N': 'NOT TO MENTION'}
    if gender_code not in gender_map:
        print("Invalid gender.")
        cur.close()
        con.close()
        pause()
        return False

    print("Date of birth:")
    dob = f"{input('Day (DD): ').strip()}/{input('Month (MM): ').strip()}/{input('Year (YYYY): ').strip()}"
    age = input("Age: ").strip()

    try:
        cur.execute("""
            INSERT INTO user_accounts
            (fname, lname, user_name, password, phno, gender, dob, age)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (fname, lname, user_name, password, phno, gender_map[gender_code], dob, age))
        print(f"\nWelcome {fname} {lname}!")
        print("Registration successful. You can now log in.")
        cur.close()
        con.close()
        pause()
        return True
    except mysql.connector.Error as err:
        if err.errno == 1062:
            print("Username already exists. Choose another.")
        else:
            print(f"DB error: {err}")
        cur.close()
        con.close()
        pause()
        return False


def login():
    clear_screen()
    display_header("USER LOGIN")
    con = get_raw_connection()
    if not con:
        pause()
        return None
    cur = con.cursor()

    user_name = input("Username: ").strip()
    password = input("Password: ").strip()

    cur.execute("""
        SELECT user_name, fname, lname
        FROM user_accounts
        WHERE user_name=%s AND password=%s
    """, (user_name, password))
    row = cur.fetchone()

    if row:
        print(f"Login successful. Welcome {row[1]} {row[2]}!")
        cur.close()
        con.close()
        pause()
        return row[0]
    else:
        print("Invalid username or password.")
        cur.close()
        con.close()
        pause()
        return None


# ================================================================
# TRAINS
# ================================================================
def view_trains():
    clear_screen()
    display_header("AVAILABLE TRAINS")
    con = get_raw_connection()
    if not con:
        pause()
        return
    cur = con.cursor()
    cur.execute("""
        SELECT train_id, train_name, route, available_seats, fare
        FROM trains
    """)
    rows = cur.fetchall()
    if not rows:
        print("No trains available.")
    else:
        print(f"{'Train ID':<10} {'Train Name':<20} {'Route':<30} {'Seats':<10} {'Fare':<10}")
        print("-" * 80)
        for r in rows:
            print(f"{r[0]:<10} {r[1]:<20} {r[2]:<30} {r[3]:<10} ₹{r[4]:<10}")
    cur.close()
    con.close()
    print()
    pause()


# ================================================================
# BOOKING
# ================================================================
def book_ticket(username):
    clear_screen()
    display_header("BOOK TICKET")
    con = get_raw_connection()
    if not con:
        pause()
        return
    cur = con.cursor()

    # Show trains
    cur.execute("""
        SELECT train_id, train_name, route, available_seats, fare
        FROM trains
    """)
    trains = cur.fetchall()
    if not trains:
        print("No trains available.")
        cur.close()
        con.close()
        pause()
        return

    print(f"{'Train ID':<10} {'Train Name':<20} {'Route':<30} {'Seats':<10} {'Fare':<10}")
    print("-" * 80)
    for t in trains:
        print(f"{t[0]:<10} {t[1]:<20} {t[2]:<30} {t[3]:<10} ₹{t[4]:<10}")
    print()

    train_id = get_input("Enter Train ID to book: ", int)
    cur.execute("""
        SELECT train_name, available_seats, fare, route
        FROM trains WHERE train_id=%s
    """, (train_id,))
    train = cur.fetchone()
    if not train:
        print("Invalid Train ID.")
        cur.close()
        con.close()
        pause()
        return

    t_name, available_seats, fare, route = train
    if available_seats <= 0:
        print("No seats available on this train.")
        cur.close()
        con.close()
        pause()
        return

    name = input("Passenger name: ").strip()
    phno = input("Phone number: ").strip()
    age = get_input("Age: ", int)
    print("M = MALE\nF = FEMALE\nN = NOT TO MENTION")
    g_code = input("Gender (M/F/N): ").strip().upper()
    g_map = {'M': 'MALE', 'F': 'FEMALE', 'N': 'NOT TO MENTION'}
    if g_code not in g_map:
        print("Invalid gender.")
        cur.close()
        con.close()
        pause()
        return
    from_f = input("From: ").strip()
    to_t = input("To: ").strip()
    date_d = f"{input('Day (DD): ').strip()}/{input('Month (MM): ').strip()}/{input('Year (YYYY): ').strip()}"

    print("\n" + "*" * 70)
    print("BOOKING SUMMARY".center(70))
    print("*" * 70)
    print(f"Train:           {t_name}")
    print(f"Route:           {route}")
    print(f"Fare/Seat:       ₹{fare}")
    print(f"Available seats: {available_seats}")
    print("*" * 70)

    if input("Confirm booking? (yes/no): ").strip().lower() != "yes":
        print("Booking cancelled.")
        cur.close()
        con.close()
        pause()
        return

    try:
        cur.execute("""
            INSERT INTO railway
            (name, phno, age, gender, from_f, to_t, date_d)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (name, phno, age, g_map[g_code], from_f, to_t, date_d))
        cur.execute("""
            UPDATE trains SET available_seats = available_seats - 1
            WHERE train_id=%s
        """, (train_id,))
        print("\n" + "*" * 70)
        print("BOOKING CONFIRMED".center(70))
        print("*" * 70)
        print(f"Name:         {name}")
        print(f"Phone:        {phno}")
        print(f"Train:        {t_name}")
        print(f"From:         {from_f}")
        print(f"To:           {to_t}")
        print(f"Journey date: {date_d}")
        print(f"Amount:       ₹{fare}")
        print(f"Booked at:    {datetime.now().strftime('%d-%m-%Y %H:%M')}")
        print("*" * 70)
    except mysql.connector.Error as err:
        if err.errno == 1062:
            print("Phone number already used for a booking.")
        else:
            print(f"DB error: {err}")
    cur.close()
    con.close()
    pause()


# ================================================================
# CANCELLATION
# ================================================================
def cancel_ticket():
    clear_screen()
    display_header("CANCEL TICKET")
    con = get_raw_connection()
    if not con:
        pause()
        return
    cur = con.cursor()

    phno = input("Enter phone number used for booking: ").strip()
    cur.execute("""
        SELECT booking_id, name, from_f, to_t, date_d
        FROM railway WHERE phno=%s
        ORDER BY booking_date DESC LIMIT 1
    """, (phno,))
    row = cur.fetchone()
    if not row:
        print("No booking found with this phone number.")
        cur.close()
        con.close()
        pause()
        return

    booking_id, name, from_f, to_t, date_d = row
    print("\nBooking details:")
    print(f"Name:  {name}")
    print(f"From:  {from_f}")
    print(f"To:    {to_t}")
    print(f"Date:  {date_d}")

    if input("Confirm cancellation? (yes/no): ").strip().lower() != "yes":
        print("Cancellation aborted.")
        cur.close()
        con.close()
        pause()
        return

    try:
        cur.execute("DELETE FROM railway WHERE booking_id=%s", (booking_id,))
        # Simple seat restore: add 1 seat to ALL trains (enough for project)
        cur.execute("UPDATE trains SET available_seats = available_seats + 1")
        print("\n" + "*" * 70)
        print("CANCELLATION CONFIRMED".center(70))
        print("*" * 70)
        print(f"Name:   {name}")
        print(f"Phone:  {phno}")
        print(f"Status: Cancelled")
        print(f"Time:   {datetime.now().strftime('%d-%m-%Y %H:%M')}")
        print("*" * 70)
    except mysql.connector.Error as err:
        print(f"DB error: {err}")
    cur.close()
    con.close()
    pause()


# ================================================================
# VIEW BOOKINGS
# ================================================================
def view_bookings_user(username):
    clear_screen()
    display_header("ALL BOOKINGS")
    con = get_raw_connection()
    if not con:
        pause()
        return
    cur = con.cursor()
    cur.execute("""
        SELECT name, phno, from_f, to_t, date_d, booking_date
        FROM railway ORDER BY booking_date DESC
    """)
    rows = cur.fetchall()
    if not rows:
        print("No bookings yet.")
    else:
        print(f"{'Name':<20} {'Phone':<15} {'From':<20} {'To':<20} {'Date':<15}")
        print("-" * 95)
        for r in rows:
            print(f"{r[0]:<20} {r[1]:<15} {r[2]:<20} {r[3]:<20} {r[4]:<15}")
    cur.close()
    con.close()
    print()
    pause()


# ================================================================
# MENUS
# ================================================================
def user_menu(username):
    while True:
        clear_screen()
        display_header(f"RAILWAY RESERVATION SYSTEM – Welcome {username}")
        options = [
            "View Available Trains",
            "Book Ticket",
            "Cancel Ticket",
            "View All Bookings",
            "Logout"
        ]
        display_menu(options)
        choice = get_input("Enter choice (1-5): ", int)
        if choice == 1:
            view_trains()
        elif choice == 2:
            book_ticket(username)
        elif choice == 3:
            cancel_ticket()
        elif choice == 4:
            view_bookings_user(username)
        elif choice == 5:
            break
        else:
            print("Invalid choice.")
            pause()


def main():
    clear_screen()
    print("Initializing Railway Reservation System...")
    if not init_database_and_tables():
        print("Initialization failed.")
        return

    while True:
        clear_screen()
        display_header("RAILWAY RESERVATION SYSTEM")
        options = ["Login", "Register", "Exit"]
        display_menu(options)
        choice = get_input("Enter choice (1-3): ", int)
        if choice == 1:
            u = login()
            if u:
                user_menu(u)
        elif choice == 2:
            register()
        elif choice == 3:
            print("Thank you for using Railway Reservation System.")
            break
        else:
            print("Invalid choice.")
            pause()


# ================================================================
# ENTRY POINT
# ================================================================
if __name__ == "__main__":
    main()
