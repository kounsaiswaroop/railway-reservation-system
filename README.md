# Railway Reservation System (Python + MySQL)

A command-line Railway Reservation System built in Python with a MySQL backend.  
It allows users to register, log in, view trains, book tickets, cancel bookings, and view all bookings using a persistent database.

> This project was created as a Class XII CBSE Computer Science (083) practical project.

---

## Features

- User registration and login with credentials stored in MySQL
- View list of trains with route, fare, and available seats
- Book ticket for a selected train
- Cancel an existing booking by phone number
- View all bookings (with booking date and journey details)
- Automatic database and table creation on first run
- Sample train data inserted automatically

---

## Project Structure

This project is intentionally kept simple for Class XII CBSE practicals and uses a **single Python file**:

- **`rrs.py`** – Contains:
  - Database initialisation (creating database and tables)
  - User authentication (register & login)
  - Train management (view trains, sample trains insertion)
  - Booking module (book ticket)
  - Cancellation module (cancel ticket)
  - View bookings module
  - Main menu and user menu (CLI)


---

## Prerequisites

- Python 3.8+ (tested with Python 3.12)
- MySQL Server running on your machine
- Python MySQL connector:
 ```sudo apt install python3-mysql.connector```
On Linux Mint / Ubuntu you should also be able to run:
```python3 -c "import mysql.connector; print('mysql.connector OK')"```


---

## Environment Variables

For safety, database credentials are **not hard-coded**.  
Set these environment variables before running:

- `DB_HOST` – MySQL host (default: `localhost`)
- `DB_USER` – MySQL username (default: `root`)
- `DB_PASS` – MySQL user password (default: `password`)
- `DB_NAME` – Database name (default: `railway`)

Example (Linux / macOS):
```
export DB_HOST=localhost
export DB_USER=root
export DB_PASS='your_mysql_password'
export DB_NAME=railway
```

---

## Installation & Setup

1. **Clone the repository**

```git clone https://github.com/<your-username>/<your-repo-name>.git```
```cd <your-repo-name>```

2. **Ensure MySQL server is running**

```sudo systemctl start mysql```

3. **Install connector (if not already installed)**

```sudo apt update```
```sudo apt install python3-mysql.connector```

4. **Set environment variables**

```export DB_HOST=localhost```
```export DB_USER=root```
```export DB_PASS='your_mysql_password'```
```export DB_NAME=railway```

---

## Running the Application

From the project directory:

```python3 rrs.py```

On first run the application will:

- Create the `railway` database if it does not exist
- Create tables: `user_accounts`, `trains`, `railway`
- Insert sample train records into `trains`


---

## Usage Flow

1. **Register**
   - Choose `Register` from the main menu
   - Enter name, username, password, phone, gender, DOB, age

2. **Login**
   - Choose `Login` from the main menu
   - Enter registered username and password
   - On success, the user menu is shown

3. **User Menu Options**
   - View Available Trains
   - Book Ticket
   - Cancel Ticket
   - View All Bookings
   - Logout

---

## Technologies Used

- **Language:** Python 3
- **Database:** MySQL
- **Connector:** `mysql-connector-python` (via `python3-mysql.connector` package)
- **Interface:** Command-line (terminal)

---

## Notes for Evaluators / Teachers

- The project demonstrates:
  - Database connectivity using Python
  - CRUD operations (INSERT, SELECT, UPDATE, DELETE) on MySQL tables
  - Basic input validation and menu-driven CLI
  - Simple implementation of a reservation system with persistent storage
- The code avoids hard‑coding sensitive credentials by using environment variables.

---

## License

This project is intended for educational purposes (Class XII CBSE Computer Science project).  
You may fork and modify it for learning or practice.





