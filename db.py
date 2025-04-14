import sqlite3

conn = sqlite3.connect("car_dealership.db")
cursor = conn.cursor()

# Create Tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS Cars (
    stock_id INTEGER PRIMARY KEY,
    make TEXT NOT NULL,
    model TEXT NOT NULL,
    year INTEGER NOT NULL,
    price REAL NOT NULL,
    availability TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    contact_number TEXT,
    email TEXT,
    address TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Salespersons (
    salesperson_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    hire_date TEXT NOT NULL,
    phone_number TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Sales (
    sale_id INTEGER PRIMARY KEY,
    stock_id INTEGER,
    customer_id INTEGER,
    salesperson_id INTEGER,
    sale_date TEXT NOT NULL,
    sale_price REAL NOT NULL,
    FOREIGN KEY(stock_id) REFERENCES Cars(stock_id),
    FOREIGN KEY(customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY(salesperson_id) REFERENCES Salespersons(salesperson_id)
);
""")

# Add Sample Data
cursor.executemany("INSERT INTO Cars (stock_id, make, model, year, price, availability) VALUES (?, ?, ?, ?, ?, ?)", [
    (1, 'Toyota', 'Land Cruiser', 2015, 33000.00, 'No'),
    (2, 'Toyota', 'Avalon', 2021, 29000.00, 'No'),
    (3, 'Acura', 'MDX', 2008, 8000.00, 'Yes'),
])

cursor.executemany("INSERT INTO Customers (customer_id, first_name, last_name, contact_number, email, address) VALUES  (?, ?, ?, ?, ?, ?)", [
    (1, 'Joe', 'Doe', '123-456-7890', 'john.doe@email.com', '123 Main St'),
    (2, 'Tony', 'Soprano', '987-654-3210', 'tony.soprano@email.com', '456 Oak Ave')
])

cursor.executemany("INSERT INTO Salespersons (salesperson_id, first_name, last_name, hire_date, phone_number) VALUES (?, ?, ?, ?, ?)", [
    (1, 'Jordan', 'Belfort', '2020-05-10', '555-123-4567'),
    (2, 'Joe', 'Pesci', '2021-08-15', '555-987-6543')
])   

cursor.executemany("INSERT INTO Sales (sale_id, stock_id, customer_id, salesperson_id, sale_date, sale_price) VALUES (?, ?, ?, ?, ?, ?)", [
    (1, 1, 2, 1, '2024-03-10', 33000.00),
    (2, 2, 1, 2, '2024-04-05', 29000.00),
])

conn.commit()
conn.close()
print("Database initialized.")
