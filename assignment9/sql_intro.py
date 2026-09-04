import os
import sqlite3

db_path = "../db/magazines.db"

os.makedirs(os.path.dirname(db_path), exist_ok=True)


CREATE_PUBLISHERS = """
CREATE TABLE IF NOT EXISTS publishers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);
"""

CREATE_MAGAZINES = """
CREATE TABLE IF NOT EXISTS magazines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    publisher_id INTEGER NOT NULL,
    FOREIGN KEY (publisher_id) REFERENCES publishers(id)
);
"""

CREATE_SUBSCRIBERS = """
CREATE TABLE IF NOT EXISTS subscribers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT NOT NULL
);
"""

CREATE_SUBSCRIPTIONS = """
CREATE TABLE IF NOT EXISTS subscriptions (
    subscriber_id INTEGER NOT NULL,
    magazine_id INTEGER NOT NULL,
    expiration_date TEXT NOT NULL,
    PRIMARY KEY (subscriber_id, magazine_id),
    FOREIGN KEY (subscriber_id) REFERENCES subscribers(id),
    FOREIGN KEY (magazine_id) REFERENCES magazines(id)
);
"""
def add_publisher(cursor, name):
    try:
        cursor.execute("INSERT INTO publishers (name) VALUES (?)", (name,))
        print(f"Added publisher: {name}")
    except sqlite3.IntegrityError:
        print(f"Publisher '{name}' already exists.")


def add_magazine(cursor, name, publisher_name):
    try:
        # Find publisher_id by publisher_name
        cursor.execute("SELECT id FROM publishers WHERE name = ?", (publisher_name,))
        row = cursor.fetchone()
        if not row:
            print(f"Error: Publisher '{publisher_name}' not found. Cannot add magazine '{name}'.")
            return
        
        publisher_id = row[0]
        cursor.execute(
            "INSERT INTO magazines (name, publisher_id) VALUES (?, ?)", 
            (name, publisher_id)
        )
        print(f"Added magazine: {name}")
    except sqlite3.IntegrityError:
        print(f"Magazine '{name}' already exists.")


def add_subscriber(cursor, name, address):
    try:
        # Check manually before inserting, or rely on table UNIQUE constraint
        cursor.execute(
            "SELECT id FROM subscribers WHERE name = ? AND address = ?", 
            (name, address)
        )
        if cursor.fetchone():
            print(f"Subscriber '{name}' living at '{address}' already exists.")
            return

        cursor.execute(
            "INSERT INTO subscribers (name, address) VALUES (?, ?)", 
            (name, address)
        )
        print(f"Added subscriber: {name}")
    except sqlite3.IntegrityError:
        print(f"Subscriber '{name}' with address '{address}' already exists.")


def add_subscription(cursor, subscriber_name, subscriber_address, magazine_name, expiration_date):
    try:
        # Look up subscriber_id
        cursor.execute(
            "SELECT id FROM subscribers WHERE name = ? AND address = ?", 
            (subscriber_name, subscriber_address)
        )
        sub_row = cursor.fetchone()
        if not sub_row:
            print(f"Error: Subscriber '{subscriber_name}' at '{subscriber_address}' not found.")
            return
        subscriber_id = sub_row[0]

        # Look up magazine_id
        cursor.execute("SELECT id FROM magazines WHERE name = ?", (magazine_name,))
        mag_row = cursor.fetchone()
        if not mag_row:
            print(f"Error: Magazine '{magazine_name}' not found.")
            return
        magazine_id = mag_row[0]

        cursor.execute(
            "INSERT INTO subscriptions (subscriber_id, magazine_id, expiration_date) VALUES (?, ?, ?)",
            (subscriber_id, magazine_id, expiration_date)
        )
        print(f"Added subscription: {subscriber_name} -> {magazine_name} (Expires: {expiration_date})")
    except sqlite3.IntegrityError:
        print(f"Subscription for '{subscriber_name}' to '{magazine_name}' already exists.")

try:
    # Connect to the SQLite database (creates the file if it does not exist)
    conn = sqlite3.connect(db_path)
    
    conn.execute("PRAGMA foreign_keys = 1")




    cursor = conn.cursor()
    cursor.execute(CREATE_PUBLISHERS)
    cursor.execute(CREATE_MAGAZINES)
    cursor.execute(CREATE_SUBSCRIBERS)
    cursor.execute(CREATE_SUBSCRIPTIONS)


    add_publisher(cursor, "Penguin Random House")
    add_publisher(cursor, "Condé Nast")
    add_publisher(cursor, "Hearst Communications")

    
    add_magazine(cursor, "The New Yorker", "Condé Nast")
    add_magazine(cursor, "Vogue", "Condé Nast")
    add_magazine(cursor, "Cosmopolitan", "Hearst Communications")

    
    add_subscriber(cursor, "Alice Smith", "123 Main St, New York, NY")
    add_subscriber(cursor, "Bob Jones", "456 Oak Ave, Chicago, IL")
    add_subscriber(cursor, "Alice Smith", "789 Pine Rd, Austin, TX")  # Same name, different address

    
    add_subscription(cursor, "Alice Smith", "123 Main St, New York, NY", "The New Yorker", "2026-12-31")
    add_subscription(cursor, "Alice Smith", "123 Main St, New York, NY", "Vogue", "2027-05-15")
    add_subscription(cursor, "Bob Jones", "456 Oak Ave, Chicago, IL", "Cosmopolitan", "2026-10-01")


    conn.commit()
    # --- QUERIES ---

    # Query 1: Retrieve all information from the subscribers table
    print("\n--- QUERY 1: All Subscribers ---")
    try:
        cursor.execute("SELECT * FROM subscribers")
        subscribers = cursor.fetchall()
        for sub in subscribers:
            print(sub)
    except sqlite3.Error as e:
        print(f"Error fetching subscribers: {e}")

    # Query 2: Retrieve all magazines sorted by name
    print("\n--- QUERY 2: All Magazines (Sorted by Name) ---")
    try:
        cursor.execute("SELECT * FROM magazines ORDER BY name ASC")
        magazines = cursor.fetchall()
        for mag in magazines:
            print(mag)
    except sqlite3.Error as e:
        print(f"Error fetching magazines: {e}")

    # Query 3: Retrieve magazines for a particular publisher using JOIN
    target_publisher = "Condé Nast"
    print(f"\n--- QUERY 3: Magazines Published by '{target_publisher}' ---")
    try:
        query = """
        SELECT magazines.id, magazines.name, publishers.name AS publisher_name
        FROM magazines
        JOIN publishers ON magazines.publisher_id = publishers.id
        WHERE publishers.name = ?
        """
        cursor.execute(query, (target_publisher,))
        publisher_magazines = cursor.fetchall()
        for row in publisher_magazines:
            print(row)
    except sqlite3.Error as e:
        print(f"Error fetching magazines for publisher: {e}")

except sqlite3.Error as e:
   print(f"An error occurred : {e}")

conn.close()
