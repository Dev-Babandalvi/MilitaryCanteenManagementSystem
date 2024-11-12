"""
db_setup.py

This script sets up the SQLite database for the Military Canteen Management System.
It creates three tables:
  1. items - for storing inventory information (item name, price, stock).
  2. users - for managing user accounts with roles like 'admin' and 'cashier'.
  3. sales - for recording sales transactions with item details, quantity, total price, and sale date.

Run this script once before starting the application to ensure the database is properly set up.

Created by: Baban Ramdas Dalvi
Institution: Dr. G.Y. Pathrikar College of Computer Science and IT, MGM University
Academic Year: 2024-2025
"""

import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('canteen_db.db')
cursor = conn.cursor()

# Create table for items
cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price REAL,
        stock INTEGER
    )
''')

# Create table for users (canteen staff)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT  -- 'admin' or 'cashier'
    )
''')

# Create table for sales
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER,
        quantity INTEGER,
        total_price REAL,
        sale_date TEXT,
        FOREIGN KEY (item_id) REFERENCES items(id)
    )
''')

# Commit changes and close connection
conn.commit()
conn.close()
