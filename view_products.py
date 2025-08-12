import sqlite3

# Connect to your database
conn = sqlite3.connect("db/omni.db")  # Update path if needed
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Query a few products
cursor.execute("SELECT title, image_url FROM products LIMIT 5")
rows = cursor.fetchall()

# Print results
for row in rows:
    print(f"Title: {row['title']}")
    print(f"Image URL: {row['image_url']}")
    print("-" * 40)

conn.close()
