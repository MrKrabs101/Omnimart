import sqlite3

conn = sqlite3.connect("db/omni.db")
cursor = conn.cursor()

cursor.execute("SELECT title, image_url FROM products LIMIT 5")
for row in cursor.fetchall():
    print(f"{row[0]} → {row[1]}")
