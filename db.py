import sqlite3

def get_db_connection():
    conn = sqlite3.connect("db/omni.db")  # Make sure this matches your actual file
    conn.row_factory = sqlite3.Row
    return conn

def execute_query(query, params=(), fetch=False, dictionary=False):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)

    result = None
    if fetch:
        rows = cursor.fetchall()
        result = [dict(row) for row in rows] if dictionary else rows

    conn.commit()
    cursor.close()
    conn.close()
    return result
