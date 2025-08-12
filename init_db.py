from db import execute_query

# Drop tables if they exist
execute_query("DROP TABLE IF EXISTS cart")
execute_query("DROP TABLE IF EXISTS users")
execute_query("DROP TABLE IF EXISTS products")

# Create products table
execute_query("""
CREATE TABLE products (
    asin TEXT PRIMARY KEY,
    title TEXT,
    brand TEXT,
    description TEXT,
    final_price REAL,
    currency TEXT,
    availability TEXT,
    reviews_count INTEGER,
    categories TEXT,
    images_count INTEGER,
    image_url TEXT,
    rating REAL,
    top_review TEXT
)
""")

# Create users table
execute_query("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Create cart table
execute_query("""
CREATE TABLE cart (
    user_id INTEGER,
    product_id TEXT,
    quantity INTEGER DEFAULT 1,
    PRIMARY KEY (user_id, product_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(asin)
)
""")

print("✅ Database initialized successfully.")
