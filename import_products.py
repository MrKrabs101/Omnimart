import os
import csv
from db import get_db_connection

# Path to your CSV file
csv_path = os.path.join("db", "omni-products.csv")
print("📄 Looking for CSV at:", os.path.abspath(csv_path))

# Helper functions to safely convert values
def safe_float(val):
    try:
        val = val.strip('"').strip()
        return float(val) if val.lower() not in ('', 'null') else None
    except:
        return None

def safe_int(val):
    try:
        val = val.strip('"').strip()
        return int(val) if val.lower() not in ('', 'null') else None
    except:
        return None

# Connect to the database
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("BEGIN TRANSACTION")

count = 0
skipped = 0

# Read and insert rows
with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO products (
                    asin, title, brand, description, final_price, currency,
                    availability, reviews_count, categories, images_count,
                    image_url, rating, top_review
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row['asin'],
                row['title'],
                row['brand'],
                row['description'],
                safe_float(row['final_price']),
                row['currency'],
                row['availability'],
                safe_int(row['reviews_count']),
                row['categories'],
                safe_int(row['images_count']),
                row['image_url'],
                safe_float(row['rating']),
                row['top_review']
            ))
            count += 1
            if count % 1000 == 0:
                print(f"✅ {count} rows imported...")
        except Exception as e:
            skipped += 1
            print(f"❌ Skipped row with ASIN {row.get('asin', 'unknown')}: {e}")

# Finalize
conn.commit()
cursor.close()
conn.close()

print(f"\n🎉 Import complete!")
print(f"✅ Total rows imported: {count}")
print(f"⚠️ Rows skipped due to errors: {skipped}")
