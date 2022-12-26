import os
from config import DATABASE_URL
import sqlite3


class Inventory:

    def __init__(self):

        self.storageState = ["Waiting Pickup",#0
                             "Robot Going",#1
                             "Robot Going",#2
                             "In Storage",#3
                             "Robot going",#4
                             "Box Picked Up For Outbound",#5
                             "Delivered"#6
                             ]
        # Connect to the database
        self.conn = sqlite3.connect(DATABASE_URL, check_same_thread=False)
        self.cursor = self.conn.cursor()

        # Create the inventory table if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                barcode TEXT,
                sku TEXT,
                item_name TEXT,
                qty INTEGER,
                status TEXT,
                location TEXT,
                state INTEGER 
            )
        """)
        self.conn.commit()
        print("DB ready!")

    def insert(self, barcode, sku, item_name, qty, state):
        self.cursor.execute("""
                INSERT INTO inventory(barcode, sku, item_name, qty, status, state)
                VALUES(?,?,?,?,?,?)
                            """, (barcode, sku, item_name, qty, self.storageState[state], state))
        id = self.cursor.lastrowid
        self.conn.commit()
        return id

    def update_status(self, id, state):
        # Update the status by barcode
        self.cursor.execute("""
            UPDATE inventory
            SET status = ?, state = ?
            WHERE id = ?
        """, (self.storageState[state], state, id))
        self.conn.commit()

    def update_status_barcode(self, barcode, state):
        # Update the status by barcode
        self.cursor.execute("""
            UPDATE inventory
            SET status = ?, state = ?
            WHERE barcode = ?
        """, (self.storageState[state], state, barcode))
        self.conn.commit()

    def update_location(self, location,  barcode, state):
        # Update the inventory location by barcode
        self.cursor.execute("""
            UPDATE inventory
            SET location = ?,
            status = ?, state = ?
            WHERE barcode = ? 
        """, (location, self.storageState[state], state, barcode))
        self.conn.commit()

    def get(self, barcode):
        # Retrieve the inventory by barcode
        self.cursor.execute("""
            SELECT * FROM inventory WHERE barcode = ?
        """, (barcode))
        items = self.cursor.fetchall()
        return items

    def get_by_id(self, id):
        # Retrieve the inventory by id
        self.cursor.execute("""
            SELECT * FROM inventory WHERE id = ?
        """, (id))
        items = self.cursor.fetchall()
        return items

    def get_by_barcode(self, barcode):
            # Retrieve the inventory by id
        self.cursor.execute("""
            SELECT * FROM inventory WHERE barcode = ?
        """, (barcode))
        items = self.cursor.fetchall()
        return items

    def get_barcode(self, id):
        # Retrieve the inventory by id
        self.cursor.execute("""
            SELECT barcode FROM inventory WHERE id = ?
        """, (id))
        items = self.cursor.fetchone()
        return items

    def get_in_storage(self):
        # Retrieve data in the inventory storage
        self.cursor.execute(
            "SELECT * FROM inventory WHERE status = 'In Storage'")
        items = self.cursor.fetchall()
        return items

    def get_all(self):
        # Retrieve the entire inventory
        self.cursor.execute("SELECT * FROM inventory")
        items = self.cursor.fetchall()
        return items

    def row_length(self):
        # Retrieve the length of row in inventory
        self.cursor.execute("SELECT COUNT(*) FROM inventory")
        result = self.cursor.fetchone()
        return result

    def row_length_status(self, state):
        # Retrieve the length of row in inventory
        self.cursor.execute(
            "SELECT COUNT(*) FROM inventory WHERE state = ?", (state))
        result = self.cursor.fetchone()
        return result

    def delete(self, barcode):
        # Retrieve the entire inventory
        self.cursor.execute("""
            DELETE FROM inventory WHERE barcode = ?
        """, (barcode,))
        return barcode + " Delivered!"
