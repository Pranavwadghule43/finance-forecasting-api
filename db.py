import sqlite3

def get_connection():
    conn = sqlite3.connect("finance.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row  # allows access like row["month"]
    return conn
