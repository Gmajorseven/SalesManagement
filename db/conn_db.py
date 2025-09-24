import sqlite3
import os

db = os.getenv("DATABASE")

def get_db_connection():
    try:
        conn = sqlite3.connect(db)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

