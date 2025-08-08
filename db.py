import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="omnimart"
    )
    return conn

def execute_query(query, params=None, fetch=False, dictionary=False):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=dictionary)
    cursor.execute(query, params or ())
    
    result = cursor.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return result
